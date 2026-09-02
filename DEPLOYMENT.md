# Deployment walkthrough

Written for someone deploying this for the first time, assuming no prior
familiarity with Supabase, Render, or Vercel. Follow the steps **in order** —
each one produces a value the next one needs.

**What this gets you:** a live URL where you can click "Run GDELT ingestion
now" or upload an LPU JSON file, review and approve what it produces, and have
the approved facts land directly in a hosted Postgres database (Supabase) -
never on your laptop, and never needing a later migration, because production
*is* where the data lives from the first run onward.

This is a **private deployment**: nothing here asks you to share a public
link, and the last step in Vercel locks the site to your own account.

**Time required:** roughly 30–40 minutes, mostly waiting for builds.

All platforms are used on their **free tiers**. Read
[Operational risks](README.md#operational-risks) in the README before relying
on this unattended — Supabase can pause after 7 days of no activity, and
there's currently no automatic keep-alive (see that section for why, and the
two ways to handle it).

---

## Environment variables you'll need

Collect these as you go. **Do not commit any of them.**

| Variable | What it's for | Where to get it | Needed by |
|---|---|---|---|
| `DATABASE_URL` | Postgres connection string; where facts, announcements, embeddings, and the review queue live | Supabase → Connect → **Session pooler** (Step 1.5) | Render |
| `GROQ_API_KEY` | Authenticates LLM calls for fact decomposition, classification, and summaries | console.groq.com → API Keys (Step 2) | Render |
| `LLM_PROVIDER` | Selects the LLM transport | Not a secret; literal value `groq` | Render |
| `PYTHON_VERSION` | Pins Render's Python runtime | Not a secret; literal value `3.11` | Render |

Only Render needs secrets for this deployment. (GitHub Actions secrets are
**optional** - only relevant if you later re-enable the dormant bulk-ingestion
workflow; see the appendix at the end.)

---

## Step 1 — Supabase (the database). Do this first.

The backend needs the connection string, so this must exist before Render.

1. Go to **https://supabase.com** and click **Start your project**. Sign in
   with GitHub (simplest, since you may use GitHub later anyway).
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

5. **Get the connection string — use the pooler, not the direct connection.**
   Click **Connect** in the top bar. You'll see two options:
   - ❌ **Direct connection** (`db.<ref>.supabase.co`) — do NOT use this one.
     It's IPv6-only, which fails to resolve (`getaddrinfo failed`) on many
     home networks and on some hosts. This exact mistake happened during
     development of this project.
   - ✅ **Session pooler** — use this. It looks like:
     ```
     postgresql://postgres.abcdefgh:[YOUR-PASSWORD]@aws-0-<region>.pooler.supabase.com:5432/postgres
     ```
   Replace `[YOUR-PASSWORD]` with the password from step 3.

   Save this whole string. This is your **`DATABASE_URL`**.

   ⚠️ Before moving on, sanity-check the string itself: the host must contain
   `pooler.supabase.com` (not `db.<ref>.supabase.co`), and the port must match
   what Supabase's Connect panel showed you for that mode.

6. **Create the tables.** In the left sidebar click **SQL Editor** → **New
   query**. Open `db/schema.sql` from this repo, copy its entire contents,
   paste into the editor, and click **Run**. (This runs inside Supabase's own
   browser environment, so it works even if your local machine can't reach the
   database directly.)

   ✅ **Working state:** a green *Success. No rows returned* message. Click
   **Table Editor** in the sidebar — you should now see six tables:
   `announcements`, `facts`, `ingestion_runs`, `ingestion_exclusions`,
   `review_batches`, `review_items`.

   ⚠️ If you get `ERROR: extension "vector" is not available`, your project is
   still provisioning — wait a minute and re-run.

---

## Step 2 — Groq (the LLM API key)

1. Go to **https://console.groq.com** and sign in (Google or GitHub).
2. In the left sidebar click **API Keys**.
3. Click **Create API Key**, give it a name like `market-intelligence`, and
   click **Submit**.
4. **Copy the key immediately** — it starts with `gsk_` and is shown only
   once.

   Save it. This is your **`GROQ_API_KEY`**.

---

## Step 3 — Render (the backend API)

This deploys `server.py` — the API the frontend talks to, and the only thing
that ever writes to Supabase.

1. Go to **https://render.com** and click **Get Started** / sign in **with
   GitHub**.
2. Push this repository to GitHub if it isn't already (it can be **private**).
3. On the Render dashboard click **New +** (top right) → **Web Service**.
4. Under *Connect a repository*, find this repo and click **Connect**. If it
   isn't listed, click **Configure account** and grant Render access to it.
5. Render reads `render.yaml` and pre-fills most fields. Confirm:
   - **Name**: `market-intelligence-api`
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -e .` (single command - `psycopg[binary]`
     is a normal dependency in `pyproject.toml`, not a second, separately
     appended install; that second command is exactly what produced a
     `Invalid requirement: 'psycopg[binary]poetry'` failure during this
     project's own deploy, most likely Render's dashboard mangling a
     manually-quoted second `pip install`. If your Build Command field shows
     anything longer than `pip install -e .`, replace it with just that.)
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: **Free**
6. Scroll to **Environment Variables** and add each row:

   | Key | Value |
   |---|---|
   | `DATABASE_URL` | the **pooler** connection string from Step 1.5 |
   | `GROQ_API_KEY` | the key from Step 2 |
   | `LLM_PROVIDER` | `groq` |
   | `PYTHON_VERSION` | `3.11` |

7. Click **Create Web Service**. The first build takes ~5–10 minutes (it
   downloads the embedding model, ~90 MB, via `fastembed`).

   ℹ️ **On the memory question**: this app was measured, not assumed, to fit
   the free tier's 512 MB limit - a real embedding call sits at ~252 MB RSS
   (~51% headroom), using `fastembed`/ONNX Runtime rather than
   `sentence-transformers`/PyTorch, which alone would have used ~500 MB
   (~2% headroom - too tight to trust). See CLAUDE.md's "Known gaps" for the
   full measurement. If you ever add a heavier dependency later, re-check
   this rather than assuming it still fits.

   ✅ **Working state:** the log ends with `Uvicorn running on http://0.0.0.0:...`
   and the status badge at the top turns green and reads **Live**. Your URL
   appears just under the service name, like
   `https://market-intelligence-api.onrender.com`.

8. **Test the database connection specifically.** Open
   `https://<your-render-url>/api/review/batches` in a browser.

   ✅ **Working state:** `{"batches": []}` — an empty list, not an error. This
   confirms Render can actually reach Supabase (the part most likely to be
   wrong on a first attempt).

   ⚠️ If you see `"Database unavailable: ..."`, your `DATABASE_URL` env var on
   Render is wrong — check it's the pooler string, not the direct one (see
   Step 1.5), then edit the env var in Render's dashboard and it will
   redeploy automatically.

9. Also check `https://<your-render-url>/api/news?page_size=1` — should
   return JSON with a `summary` block. (`/api/analyze` will return a 503 with
   an explanatory message — expected, unrelated to this deployment: the
   scored file-based corpus isn't wired up yet.)

   ℹ️ On the free tier the service sleeps after ~15 minutes idle. The next
   request takes ~50 seconds to wake it. Normal, not a fault.

10. **Copy your Render URL** — Vercel needs it next.

---

## Step 4 — Vercel (the frontend)

1. Go to **https://vercel.com** and **Sign Up** / log in **with GitHub**.
2. Click **Add New...** → **Project**.
3. Find this repo and click **Import**.
4. **Before deploying**, point the frontend at your Render backend: open
   `vercel.json` in this repo, replace
   `https://REPLACE-WITH-YOUR-RENDER-URL.onrender.com` with the URL from Step
   3.10, and commit + push that change. (The frontend calls same-origin
   `/api/*` paths; this rewrite forwards them to Render.)
5. Back on Vercel's import screen, leave **Framework Preset** as *Other*. The
   `vercel.json` already sets the output directory to `web`.
6. Click **Deploy**. This takes under a minute — there's no build step.

   ✅ **Working state:** a *Congratulations* screen. Click **Continue to
   Dashboard**, then **Visit** to open the site.

7. **Keep it private:** Vercel Project → **Settings** → **Deployment
   Protection** → enable **Vercel Authentication**. Only your logged-in
   account can then open it.

---

## Step 5 — Verify the whole thing, live in production

This is the part that actually matters: confirming a real run, from the
deployed UI, lands in the hosted database — not a local file.

1. On your Vercel URL, open the **"..." menu → Ingest & review**.
2. Either click **Run GDELT ingestion now**, or upload a small LPU JSON file
   (a file with just a handful of records is a good first test).
3. Wait for a batch to appear under **Batches** with status **Awaiting chunk
   review**, then click it open.

   ⚠️ If GDELT itself fails (a `GDELT fetch failed` message, not a database
   error), that's GDELT's own live API being flaky, not a deployment problem —
   try again, or test with the LPU upload path instead, which doesn't depend
   on it.

4. Review a few of the atomic facts, select some, click **Approve selected**.
   The batch should move to **Awaiting final review** shortly after
   (embeddings + a summary are generated in the background).
5. Review the summaries, select some, click **Approve selected** again.
6. **Confirm it's actually in the database, not just the UI.** In Supabase →
   **Table Editor** → `facts`, you should see the rows you just approved.

   ✅ **This is the real success condition for this deployment**: data you
   approved through the live URL is sitting in Supabase, with nothing having
   touched your laptop except the browser.

---

## Final checklist

- [ ] **Supabase** project shows *Project is healthy*
- [ ] **Supabase** Table Editor lists all six tables (see Step 1.6)
- [ ] **Render** service status badge reads **Live**
- [ ] **Render** all four environment variables are set, using the **pooler** connection string
- [ ] **Render** `/api/review/batches` returns `{"batches": []}`, not a database error
- [ ] **Vercel** deployment succeeded and the landing page loads
- [ ] **Vercel** `vercel.json` contains your real Render URL, committed and pushed
- [ ] **Vercel** Deployment Protection is enabled (keeps it private)
- [ ] **End to end**: a batch run through the live "Ingest & review" page, approved twice, and confirmed present in Supabase's `facts` table

---

## Appendix: the bulk ingestion workflow (optional, currently dormant)

`.github/workflows/ingest.yml` exists for a different, earlier approach: an
unattended job that decomposes and classifies LPU announcements straight into
`facts`/`announcements` with **no approval step**. It's deliberately dormant
(its `schedule` trigger is commented out) because running it alongside the
review-gated flow above would mean two different trust models writing to the
same tables, and it would compete with manual runs for the same daily Groq
quota.

Nothing here requires it. If you want it later - e.g. to also process the
large existing LPU backlog unattended, bypassing manual review - add
`DATABASE_URL` and `GROQ_API_KEY` as **GitHub repository secrets** (Settings →
Secrets and variables → Actions) and uncomment the `schedule:` block in that
workflow file.
