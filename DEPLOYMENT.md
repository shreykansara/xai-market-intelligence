# Deployment walkthrough

Written for someone deploying this for the first time, assuming no prior
familiarity with Supabase, Render, Vercel, or GitHub Actions secrets. Follow
the steps **in order** — each one produces a value the next one needs.

This is a **private deployment**: nothing here asks you to share a public link.
The goal is that ingestion keeps running remotely so your own machine doesn't
have to stay on.

**Time required:** roughly 45–60 minutes, mostly waiting for builds.

All four platforms are used on their **free tiers**. Read
[Operational risks](README.md#operational-risks) in the README before relying on
this unattended — there are two real failure modes (Supabase pausing, GitHub
disabling the schedule) that you should understand rather than be surprised by.

---

## Environment variables you'll need

Collect these as you go. **Do not commit any of them.**

| Variable | What it's for | Where to get it | Needed by |
|---|---|---|---|
| `DATABASE_URL` | Postgres connection string; where facts, announcements, embeddings and run history are stored | Supabase → Project Settings → Database → Connection string → URI (Step 1.5) | Render, GitHub Actions |
| `GROQ_API_KEY` | Authenticates LLM calls for fact decomposition and classification | console.groq.com → API Keys → Create API Key (Step 2) | Render, GitHub Actions |
| `LLM_PROVIDER` | Selects the LLM transport. Must be `groq` on any hosted runner — there is no local Ollama there | Not a secret; type the literal value `groq` | Render, GitHub Actions |
| `PYTHON_VERSION` | Pins Render's Python runtime | Not a secret; literal value `3.11` | Render |

There is no value in this repo for any of these. Every one comes from an
account you create below.

---

## Step 1 — Supabase (the database). Do this first.

The backend and the scheduled job both need the connection string, so this must
exist before either.

1. Go to **https://supabase.com** and click **Start your project**. Sign in with
   GitHub (simplest, since you'll need GitHub later anyway).
2. On the dashboard click **New project**.
3. Fill in:
   - **Name**: `market-intelligence` (any name is fine)
   - **Database Password**: click **Generate a password** and **save it
     somewhere safe now** — it's part of your connection string and Supabase
     will not show it again.
   - **Region**: pick the one geographically closest to you.
   - **Plan**: Free
4. Click **Create new project**. Provisioning takes ~2 minutes. Wait until the
   green **Project is healthy** indicator appears.
5. **Get the connection string.** Click the **Connect** button in the top bar
   (or Project Settings → Database → Connection string). Choose the **URI** tab.
   You'll see something like:
   ```
   postgresql://postgres.abcdefgh:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
   Replace `[YOUR-PASSWORD]` with the password from step 3. **Use the pooler
   (port 6543)** — short-lived connections from GitHub Actions and a
   cold-starting Render service work better through the pooler than through the
   direct port 5432.

   Save this whole string. This is your **`DATABASE_URL`**.

6. **Create the tables.** In the left sidebar click **SQL Editor** → **New
   query**. Open `db/schema.sql` from this repo, copy its entire contents, paste
   into the editor, and click **Run**.

   ✅ **Working state:** a green *Success. No rows returned* message. Click
   **Table Editor** in the sidebar — you should now see four tables:
   `announcements`, `facts`, `ingestion_runs`, `ingestion_exclusions`.

   ⚠️ If you get `ERROR: extension "vector" is not available`, your project is
   still provisioning — wait a minute and re-run.

---

## Step 2 — Groq (the LLM API key)

1. Go to **https://console.groq.com** and sign in (Google or GitHub).
2. In the left sidebar click **API Keys**.
3. Click **Create API Key**, give it a name like `market-intelligence`, and
   click **Submit**.
4. **Copy the key immediately** — it starts with `gsk_` and is shown only once.

   Save it. This is your **`GROQ_API_KEY`**.

---

## Step 3 — GitHub Actions (the ingestion schedule)

This is what makes ingestion run without your machine.

1. Push this repository to GitHub if it isn't already. It can be **private**.
2. On the repo page click **Settings** (top row, far right).
3. In the left sidebar: **Secrets and variables** → **Actions**.
4. Click **New repository secret**, then add each of these — one at a time:

   | Name | Secret value |
   |---|---|
   | `DATABASE_URL` | the connection string from Step 1.5 |
   | `GROQ_API_KEY` | the key from Step 2 |

   Type the name **exactly** as shown (case-sensitive), paste the value into the
   *Secret* box, and click **Add secret**.

5. Click the **Actions** tab at the top of the repo. If you see a banner saying
   *Workflows aren't being run on this forked repository* or asking you to
   enable workflows, click the green **I understand my workflows, go ahead and
   enable them** button.
6. In the left sidebar click **LPU ingestion (scheduled)**, then the **Run
   workflow** dropdown on the right → **Run workflow**. This triggers it
   manually so you don't have to wait up to 30 minutes to know whether it works.

   ✅ **Working state:** after ~3–5 minutes the run shows a **green check**.
   Click into it and confirm the steps *Apply database schema*, *Process a
   bounded chunk*, *Sync newly processed facts* and *Record run status* all
   passed.

   ⚠️ If *Apply database schema* fails with a connection error, your
   `DATABASE_URL` secret is wrong — most often the `[YOUR-PASSWORD]` placeholder
   was left unreplaced.

7. **Confirm data actually landed.** Back in Supabase → **Table Editor** →
   `ingestion_runs`. You should see at least one row with `ok = true`. Check the
   `facts` table too — it should have rows.

---

## Step 4 — Render (the backend API)

1. Go to **https://render.com** and click **Get Started** / sign in **with
   GitHub**.
2. On the dashboard click **New +** (top right) → **Web Service**.
3. Under *Connect a repository*, find this repo and click **Connect**. If it
   isn't listed, click **Configure account** and grant Render access to it.
4. Render reads `render.yaml` and pre-fills most fields. Confirm:
   - **Name**: `market-intelligence-api`
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -e . && pip install 'psycopg[binary]'`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: **Free**
5. Scroll to **Environment Variables** and click **Add Environment Variable**
   for each row:

   | Key | Value |
   |---|---|
   | `DATABASE_URL` | connection string from Step 1.5 |
   | `GROQ_API_KEY` | key from Step 2 |
   | `LLM_PROVIDER` | `groq` |
   | `PYTHON_VERSION` | `3.11` |

6. Click **Create Web Service**. The first build takes ~5–10 minutes (it
   downloads the sentence-transformer model).

   ✅ **Working state:** the log ends with `Uvicorn running on http://0.0.0.0:...`
   and the status badge at the top turns green and reads **Live**. Your URL
   appears just under the service name, like
   `https://market-intelligence-api.onrender.com`.

7. **Test it.** Open `https://<your-render-url>/api/news?page_size=1` in a
   browser.

   ✅ You should get JSON with a `summary` block and a `total` count.

   ℹ️ Note: `/api/analyze` currently returns **503 with an explanatory
   message**. That is expected right now — the scored corpus isn't wired up yet
   (deferred deliberately). Browsing works; analysis doesn't.

   ℹ️ On the free tier the service sleeps after ~15 minutes idle. The next
   request takes ~50 seconds to wake it. This is normal, not a fault.

8. **Copy your Render URL** — Vercel needs it next.

---

## Step 5 — Vercel (the frontend)

1. Go to **https://vercel.com** and **Sign Up** / log in **with GitHub**.
2. Click **Add New...** → **Project**.
3. Find this repo and click **Import**.
4. **Before deploying**, you must point the frontend at your Render backend:
   open `vercel.json` in this repo, replace
   `https://REPLACE-WITH-YOUR-RENDER-URL.onrender.com` with the URL from Step
   4.8, and commit + push that change. (The frontend calls same-origin `/api/*`
   paths; this rewrite forwards them to Render.)
5. Back on Vercel's import screen, leave **Framework Preset** as *Other*. The
   `vercel.json` already sets the output directory to `web`.
6. Click **Deploy**. This takes under a minute — there's no build step.

   ✅ **Working state:** a *Congratulations* screen with a screenshot preview.
   Click **Continue to Dashboard**, then **Visit** to open the site. The landing
   page should render, and the **"..." menu → Browse news data** page should
   load rows from your Render backend.

   ⚠️ If the news page shows an error, the first request is probably waking the
   sleeping Render service — wait ~50 seconds and reload. If it still fails, the
   rewrite URL in `vercel.json` is wrong.

7. **Keep it private:** Vercel Project → **Settings** → **Deployment
   Protection** → enable **Vercel Authentication**. Only your logged-in account
   can then open it.

---

## Final checklist

Confirm every line before considering deployment complete:

- [ ] **Supabase** project shows *Project is healthy*
- [ ] **Supabase** Table Editor lists all four tables: `announcements`, `facts`, `ingestion_runs`, `ingestion_exclusions`
- [ ] **Supabase** `facts` table contains rows
- [ ] **Supabase** `ingestion_runs` contains at least one row with `ok = true`
- [ ] **GitHub** repo has both secrets saved: `DATABASE_URL`, `GROQ_API_KEY`
- [ ] **GitHub** Actions tab shows a green check for *LPU ingestion (scheduled)*
- [ ] **GitHub** the schedule is enabled (workflow is not greyed out / disabled)
- [ ] **Render** service status badge reads **Live**
- [ ] **Render** all four environment variables are set
- [ ] **Render** `/api/news?page_size=1` returns JSON in a browser
- [ ] **Vercel** deployment succeeded and the landing page loads
- [ ] **Vercel** `vercel.json` contains your real Render URL, committed and pushed
- [ ] **Vercel** the Browse news data page shows rows fetched from Render
- [ ] **Vercel** Deployment Protection is enabled (keeps it private)

### After the checklist passes

Tell me, and I'll do the final verification: wait for a **scheduled** run (not a
manual one) to fire on its own, then report whether it succeeded, how many facts
it processed, and whether a fresh query against Supabase shows the new data.

Don't skip the wait — a manually-triggered run proves the job works, but only an
unattended scheduled run proves the *schedule* works, which is the whole point
of this deployment.
