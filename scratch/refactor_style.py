with open('web/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update Root Tokens
old_root = """/* -------------------------------------------------------------------
   AI Explainable Market Intelligence Dashboard - Pitch Black & Electric Green Theme
   ------------------------------------------------------------------- */

:root {
    --bg-dark: #050505;          /* Pitch Black */
    --bg-surface: #0E0E11;       /* Obsidian Panel */
    --bg-card: #15151A;          /* Graphite Card */
    --bg-card-hover: #1E1E24;
    --border-color: #272730;     /* Dark Slate Border */
    --border-accent: rgba(0, 255, 102, 0.4);
    
    --primary-gradient: linear-gradient(135deg, #00FF66 0%, #00C853 100%);
    --accent-green: #00FF66;     /* Electric Bright Green */
    --accent-emerald: #10B981;   /* Emerald */
    --accent-mint: #00E676;
    --accent-cyan: #00E5FF;
    --accent-purple: #A855F7;
    --accent-rose: #FF2D55;
    --accent-amber: #FFB300;

    --text-main: #FAFAFA;
    --text-muted: #A1A1AA;
    --text-dim: #71717A;

    --radius-sm: 4px;
    --radius-md: 6px;
    --radius-lg: 8px;
    --radius-full: 4px;

    --shadow-main: 0 4px 20px rgba(0, 255, 102, 0.15);
    --shadow-card: 0 2px 10px rgba(0, 0, 0, 0.6);
    --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-heading: 'Space Grotesk', 'Plus Jakarta Sans', sans-serif;
}"""

new_root = """/* -------------------------------------------------------------------
   Omniscope AI - Institutional Finance & Strategy Design Language System
   Palette: Deep Obsidian Canvas, Navy Slate Surfaces, Royal Cobalt Actions,
            and Refined Financial Semantics (Emerald, Crimson, Amber).
   ------------------------------------------------------------------- */

:root {
    /* Base Canvases */
    --bg-base: #0A0D14;
    --bg-dark: #0A0D14;
    --bg-surface: #111622;
    --bg-card: #161D2E;
    --bg-card-hover: #1E273D;
    
    /* Institutional Borders */
    --border-color: rgba(255, 255, 255, 0.08);
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-medium: rgba(255, 255, 255, 0.14);
    --border-accent: rgba(37, 99, 235, 0.35);
    --border-focus: #3B82F6;
    
    /* Primary Brand Action: Royal Cobalt */
    --brand-primary: #2563EB;
    --brand-primary-hover: #1D4ED8;
    --brand-primary-tint: rgba(37, 99, 235, 0.12);
    --primary-gradient: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    
    /* Financial Semantic Palette (Subtle & Understated) */
    --color-growth: #10B981;
    --color-risk: #F43F5E;
    --color-neutral: #F59E0B;
    --color-metric: #6366F1;
    
    /* Backwards compatibility aliases */
    --accent-green: #10B981;
    --accent-emerald: #10B981;
    --accent-mint: #10B981;
    --accent-cyan: #3B82F6;
    --accent-purple: #6366F1;
    --accent-rose: #F43F5E;
    --accent-amber: #F59E0B;
    
    /* High-Contrast Typography */
    --text-main: #F8FAFC;
    --text-primary: #F8FAFC;
    --text-muted: #94A3B8;
    --text-secondary: #94A3B8;
    --text-dim: #64748B;
    --text-tertiary: #64748B;
    
    /* Font Stacks */
    --font-main: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-heading: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace;
    
    /* Standardized Spacing & Radii */
    --radius-sm: 4px;
    --radius-md: 6px;
    --radius-lg: 8px;
    --radius-full: 9999px;
    
    /* Structural Shadows (Zero Radioactive Glow) */
    --shadow-main: 0 4px 16px rgba(0, 0, 0, 0.35);
    --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.24);
    --shadow-modal: 0 20px 40px rgba(0, 0, 0, 0.6);
}"""

if old_root in css:
    css = css.replace(old_root, new_root)
    print("Replaced root tokens successfully!")
else:
    print("Warning: old_root not found exactly, checking substring...")

# Replacements for glowing / fluorescent gradients and colors
replacements = [
    # Gradients
    ("linear-gradient(135deg, #00FF66 0%, #00C853 100%)", "linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)"),
    ("linear-gradient(135deg, #00FF66 0%, #00B050 100%)", "linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)"),
    ("linear-gradient(135deg, #00FF66 0%, #00CC52 100%)", "linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)"),
    ("linear-gradient(135deg, #00FF66 0%, #00E5FF 100%)", "linear-gradient(135deg, #2563EB 0%, #3B82F6 100%)"),
    ("linear-gradient(90deg, #00FF66, #00E5FF, #3B82F6)", "linear-gradient(90deg, #2563EB, #3B82F6, #60A5FA)"),
    ("linear-gradient(135deg, #00E5FF 0%, #0077B6 100%)", "linear-gradient(135deg, #1E40AF 0%, #1D4ED8 100%)"),
    ("linear-gradient(135deg, #00E5FF 0%, #00B0FF 100%)", "linear-gradient(135deg, #2563EB 0%, #3B82F6 100%)"),
    ("var(--primary-gradient, linear-gradient(135deg, #00ff66, #00b344))", "linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)"),
    
    # Neon Glow Box Shadows
    ("box-shadow: 0 0 20px rgba(0, 255, 102, 0.4);", "box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);"),
    ("box-shadow: 0 0 15px rgba(0, 255, 102, 0.3);", "box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);"),
    ("box-shadow: 0 0 25px rgba(0, 255, 102, 0.25);", "box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);"),
    ("box-shadow: 0 0 8px #00FF66;", "box-shadow: none;"),
    ("box-shadow: 0 0 10px #00E5FF;", "box-shadow: none;"),
    ("box-shadow: 0 0 12px rgba(0, 255, 102, 0.4);", "box-shadow: none;"),
    ("box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);", "box-shadow: none;"),
    
    # Glow text shadows
    ("text-shadow: 0 0 10px rgba(0, 255, 102, 0.5);", "text-shadow: none;"),
    ("text-shadow: 0 0 8px rgba(0, 229, 255, 0.4);", "text-shadow: none;"),
    ("text-shadow: 0 0 20px rgba(0, 255, 102, 0.4);", "text-shadow: none;"),
    
    # Canvas / Panel Backgrounds
    ("#050505", "#0A0D14"),
    ("#0E0E11", "#111622"),
    ("#15151A", "#161D2E"),
    ("#1E1E24", "#1E273D"),
    
    # Hex colors in buttons & borders
    ("color: #00FF66;", "color: var(--brand-primary);"),
    ("color: #00E5FF;", "color: var(--text-secondary);"),
    ("border-color: #00FF66;", "border-color: var(--brand-primary);"),
    ("border-color: #00E5FF;", "border-color: var(--border-medium);"),
    ("border-left: 4px solid #00FF66;", "border-left: 3px solid var(--brand-primary);"),
    ("border-left: 4px solid #00E5FF;", "border-left: 3px solid var(--border-medium);"),
    ("background: #00FF66;", "background: var(--brand-primary);"),
    ("background: rgba(0, 255, 102, 0.12);", "background: rgba(37, 99, 235, 0.12);"),
    ("background: rgba(0, 229, 255, 0.12);", "background: rgba(255, 255, 255, 0.06);"),
    ("color: #00FF66 !important;", "color: var(--brand-primary) !important;"),
    ("border-color: #00FF66 !important;", "border-color: var(--brand-primary) !important;")
]

count = 0
for old, new in replacements:
    if old in css:
        c = css.count(old)
        css = css.replace(old, new)
        count += c

print(f"Applied {count} color and style refactor replacements!")

# Add specific institutional finance component rules at end of CSS if needed
extra_styles = """
/* =============================================================== */
/* INSTITUTIONAL FINANCE REFINED COMPONENTS                        */
/* =============================================================== */

/* Tabular figures for financial tables & stats */
.financial-num,
.kpi-num,
.ledger-amount,
.table-val,
.cvp-match-badge,
.history-meta,
.step-metric-value {
    font-family: var(--font-mono);
    font-feature-settings: "tnum" 1, "zero" 1;
    letter-spacing: -0.01em;
}

/* Brand pill styling */
.brand-pill {
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-secondary);
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid var(--border-medium);
    padding: 2px 6px;
    border-radius: var(--radius-sm);
    margin-left: 6px;
    vertical-align: middle;
}

/* Refined Primary Buttons */
.btn-primary-md, .btn-primary-lg, .btn-primary-sm, .btn-cta-lg {
    background: var(--brand-primary) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    font-weight: 500;
    transition: background 0.15s ease, border-color 0.15s ease;
}

.btn-primary-md:hover, .btn-primary-lg:hover, .btn-primary-sm:hover, .btn-cta-lg:hover {
    background: var(--brand-primary-hover) !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
}

/* Refined Outline & Ghost Buttons */
.btn-outline-sm, .btn-outline-md {
    background: rgba(255, 255, 255, 0.03) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-medium) !important;
}

.btn-outline-sm:hover, .btn-outline-md:hover {
    background: rgba(255, 255, 255, 0.07) !important;
    border-color: rgba(255, 255, 255, 0.22) !important;
}

/* Refined Investment Score Radial Gauge */
.investment-score-gauge circle.gauge-bg {
    stroke: rgba(255, 255, 255, 0.07) !important;
}

/* Refined Platform Navbar */
.platform-navbar {
    background: rgba(17, 22, 34, 0.88) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
}

/* Minimalist Card Design */
.dash-card, .glass-panel, .step1-card, .mode-card {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    box-shadow: var(--shadow-card) !important;
}

/* Smooth Progressive Disclosure Details */
details.progressive-disclosure {
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    background: var(--bg-surface);
    margin-top: 16px;
    overflow: hidden;
}

details.progressive-disclosure summary {
    padding: 12px 16px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    user-select: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: background 0.15s ease;
}

details.progressive-disclosure summary:hover {
    background: rgba(255, 255, 255, 0.03);
    color: var(--text-primary);
}

details.progressive-disclosure .disclosure-content {
    padding: 16px;
    border-top: 1px solid var(--border-subtle);
}
"""

css += extra_styles

with open('web/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("web/style.css updated successfully!")
