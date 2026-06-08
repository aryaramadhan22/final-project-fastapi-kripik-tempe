GLOBAL_CSS = """
<style>
/* ── Design tokens ── */
:root {
    --c-bg:      #0e0f14;
    --c-surface: #161820;
    --c-card:    #1c1e2a;
    --c-border:  #2a2d3e;
    --c-accent:  #7c6aff;
    --c-success: #22c997;
    --c-warn:    #e8a020;
    --c-danger:  #e03535;
    --c-text:    #e8eaf0;
    --c-muted:   #6b7094;
    --radius:    14px;
    --pill:      999px;
}

/* ── Global resets ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--c-bg) !important;
    color: var(--c-text) !important;
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif !important;
}
[data-testid="stSidebar"] {
    background: var(--c-surface) !important;
    border-right: 1px solid var(--c-border) !important;
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Inputs ── */
input, textarea, [data-baseweb="select"] > div {
    background: var(--c-surface) !important;
    border-color: var(--c-border) !important;
    color: var(--c-text) !important;
    border-radius: 8px !important;
}
input:focus, textarea:focus { border-color: var(--c-accent) !important; }

/* ── Buttons ── */
.stButton > button {
    background: var(--c-accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--pill) !important;
    font-weight: 500 !important;
    transition: filter .15s, transform .1s !important;
}
.stButton > button:hover  { filter: brightness(1.12) !important; }
.stButton > button:active { transform: scale(.97) !important; }

/* ── Game card ── */
.gl-card {
    background: var(--c-card);
    border: 1px solid var(--c-border);
    border-radius: var(--radius);
    padding: 1.1rem 1.2rem;
    margin-bottom: .75rem;
    transition: border-color .18s, transform .18s;
}
.gl-card:hover { border-color: rgba(124,106,255,.35); transform: translateY(-2px); }
.gl-card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: .5rem; }
.gl-title { font-weight: 600; font-size: 1rem; letter-spacing: -.01em; }
.gl-meta  { display: flex; flex-wrap: wrap; gap: .3rem; margin-top: .35rem; }
.gl-stats { color: var(--c-muted); font-size: .82rem; margin-top: .35rem; }
.gl-review{ color: var(--c-muted); font-size: .82rem; margin-top: .45rem; font-style: italic; 
            display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

/* ── Badges ── */
.badge {
    display: inline-flex; align-items: center;
    padding: 2px 10px; border-radius: var(--pill);
    font-size: .67rem; font-weight: 600; letter-spacing: .05em; text-transform: uppercase;
}
.badge-playing   { background: rgba(124,106,255,.15); color: #a89bff; border: 1px solid rgba(124,106,255,.28); }
.badge-completed { background: rgba(34,201,151,.12);  color: #22c997; border: 1px solid rgba(34,201,151,.25); }
.badge-wishlist  { background: rgba(232,160,32,.12);  color: #e8a020; border: 1px solid rgba(232,160,32,.25); }

/* ── Chips ── */
.chip {
    display: inline-flex; align-items: center;
    padding: 2px 9px; border-radius: var(--pill);
    font-size: .72rem; font-weight: 500;
    background: rgba(255,255,255,.05); border: 1px solid var(--c-border); color: var(--c-muted);
}

/* ── Headings ── */
.gl-heading { font-weight: 700; font-size: 1.55rem; letter-spacing: -.025em; margin-bottom: .25rem; }
.gl-sub     { color: var(--c-muted); font-size: .88rem; margin-bottom: 1.25rem; }

/* ── Auth card ── */
.auth-wrap {
    max-width: 400px; margin: 3rem auto;
    background: var(--c-card); border: 1px solid var(--c-border);
    border-radius: var(--radius); padding: 2rem;
}
.auth-brand {
    display: flex; align-items: center; gap: 8px;
    font-weight: 700; font-size: 1.2rem; margin-bottom: 1.5rem;
}
.auth-dot {
    width: 9px; height: 9px; border-radius: 50%; background: var(--c-accent); flex-shrink: 0;
}

/* ── Nav ── */
.gl-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: .6rem 0; margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--c-border);
}
.gl-nav-brand {
    display: flex; align-items: center; gap: 8px;
    font-weight: 700; font-size: 1.05rem;
}
.gl-nav-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--c-accent); flex-shrink: 0; }

/* ── Empty state ── */
.gl-empty {
    text-align: center; color: var(--c-muted);
    padding: 3rem 1rem;
}

/* Hide default Streamlit chrome bits */
[data-testid="stDecoration"] { display: none; }
footer { display: none !important; }
</style>
"""


def badge(status: str) -> str:
    cls = f"badge-{status}"
    labels = {"playing": "Playing", "completed": "Completed", "wishlist": "Wishlist"}
    return f'<span class="badge {cls}">{labels.get(status, status)}</span>'


def chip(text: str) -> str:
    return f'<span class="chip">{text}</span>'


def star_rating(rating: int) -> str:
    filled = "★" * rating
    empty = "☆" * (10 - rating)
    return f'<span style="color:#e8a020;font-size:.85rem;">{filled}</span><span style="color:#2a2d3e;font-size:.85rem;">{empty}</span>'
