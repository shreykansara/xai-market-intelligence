import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from marketintel.analysis import (  # noqa: E402
    blend_pestle,
    blend_porters,
    rank_pestle_articles,
    rank_porters_articles,
    top_k_similar_startups,
)
from marketintel.config import (  # noqa: E402
    NEWS_EMBEDDINGS_PATH,
    NEWS_PATH,
    PESTLE_DIMS,
    PESTLE_LABELS,
    PORTERS_DIMS,
    PORTERS_LABELS,
    STARTUP_EMBEDDINGS_PATH,
    STARTUPS_PATH,
)
from marketintel.data_loader import load_news, load_startups, news_by_id  # noqa: E402
from marketintel.embeddings import embed_text  # noqa: E402

POSITIVE_COLOR = "#2ca02c"
NEGATIVE_COLOR = "#d62728"

st.set_page_config(page_title="Explainable Market Intelligence", layout="centered")


@st.cache_resource
def get_model_warm():
    from marketintel.embeddings import get_model

    return get_model()


@st.cache_data
def get_news():
    return load_news()


@st.cache_data
def get_startups():
    return load_startups()


def data_ready() -> bool:
    return NEWS_PATH.exists() and NEWS_EMBEDDINGS_PATH.exists() and STARTUPS_PATH.exists() and STARTUP_EMBEDDINGS_PATH.exists()


AXIS_LABEL_OVERRIDES = {
    "threat_new_entrants": "New Entrants",
    "threat_substitutes": "Substitutes",
}


def make_radar(dims: list[str], labels: dict, values: dict, title: str) -> go.Figure:
    axis_labels = {d: AXIS_LABEL_OVERRIDES.get(d, labels[d]) for d in dims}
    categories = [axis_labels[d] for d in dims] + [axis_labels[dims[0]]]
    radii = [abs(values[d]) for d in dims] + [abs(values[dims[0]])]
    signed = [values[d] for d in dims] + [values[dims[0]]]
    colors = [POSITIVE_COLOR if v >= 0 else NEGATIVE_COLOR for v in signed]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=radii,
        theta=categories,
        fill="toself",
        fillcolor="rgba(130,130,130,0.15)",
        line=dict(color="rgba(120,120,120,0.7)", width=2),
        marker=dict(size=11, color=colors, line=dict(width=1, color="white")),
        customdata=signed,
        hovertemplate="%{theta}: %{customdata:+.1f}<extra></extra>",
        name=title,
    ))
    fig.update_layout(
        polar=dict(
            domain=dict(x=[0.12, 0.88], y=[0.08, 0.92]),
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9)),
            angularaxis=dict(tickfont=dict(size=12)),
        ),
        showlegend=False,
        title=dict(text=title, x=0.5),
        margin=dict(t=60, b=30, l=60, r=60),
        height=440,
    )
    return fig


def legend_note():
    st.markdown(
        f"<span style='color:{POSITIVE_COLOR}'>&#9679;</span> helping&nbsp;&nbsp;&nbsp;"
        f"<span style='color:{NEGATIVE_COLOR}'>&#9679;</span> hurting&nbsp;&nbsp;&nbsp;"
        f"radius = sensitivity magnitude (0-100)",
        unsafe_allow_html=True,
    )


st.title("Explainable Market Intelligence")
st.caption("Paste your CVP / business description. Location is fixed to LPU, Punjab.")

if not data_ready():
    st.error(
        "Fabricated data not found. Generate it first:\n\n"
        "```\npython scripts/generate_news.py\npython scripts/generate_startups.py\n```"
    )
    st.stop()

cvp_text = st.text_area(
    "Your CVP",
    height=180,
    placeholder=(
        "e.g. We build a mobile app that gives small farmers in Punjab real-time soil moisture "
        "readings and irrigation advice in their own language..."
    ),
)
submitted = st.button("Analyze", type="primary")

if submitted:
    if not cvp_text.strip():
        st.warning("Paste a CVP first.")
        st.stop()

    with st.spinner("Embedding and analyzing..."):
        get_model_warm()
        news, news_embeddings = get_news()
        startups, startup_embeddings = get_startups()
        lookup = news_by_id(news)

        cvp_embedding = embed_text(cvp_text)
        top_idx, sims = top_k_similar_startups(cvp_embedding, startup_embeddings)

        pestle_values, pestle_weights = blend_pestle(startups, top_idx, sims)
        porters_values, porters_weights = blend_porters(startups, top_idx, sims)

        pestle_articles = rank_pestle_articles(startups, lookup, top_idx, pestle_weights)
        porters_articles = rank_porters_articles(startups, lookup, top_idx, porters_weights)

    st.subheader("Most similar startups")
    cols = st.columns(len(top_idx))
    for col, idx, sim in zip(cols, top_idx, sims):
        s = startups[idx]
        with col:
            st.markdown(f"**{s['name']}**")
            st.caption(s["domain"])
            st.progress(min(max(float(sim), 0.0), 1.0), text=f"similarity {sim:.2f}")

    st.divider()
    st.subheader("Sensitivity profile")

    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.plotly_chart(make_radar(PESTLE_DIMS, PESTLE_LABELS, pestle_values, "PESTLE"), use_container_width=True)
        legend_note()
    with chart_cols[1]:
        st.plotly_chart(make_radar(PORTERS_DIMS, PORTERS_LABELS, porters_values, "Porter's Five Forces"), use_container_width=True)
        legend_note()

    st.divider()
    st.subheader("Top contributing events")

    tab_pestle, tab_porters = st.tabs(["PESTLE", "Porter's Five Forces"])

    def render_events(ranked, labels):
        if not ranked:
            st.info("No linked articles found.")
            return
        for item in ranked[:10]:
            article = item["article"]
            dim_label = labels[item["dim"]]
            polarity_color = POSITIVE_COLOR if article["polarity"] == "positive" else NEGATIVE_COLOR
            st.markdown(
                f"**{article['title']}** &nbsp;"
                f"<span style='color:{polarity_color}; font-size:0.85em'>&#9679; {article['polarity']}</span>",
                unsafe_allow_html=True,
            )
            st.caption(
                f"{article['date']} · {article['scope']} · affects **{dim_label}** · "
                f"via {item['source_startup']}"
            )

    with tab_pestle:
        render_events(pestle_articles, PESTLE_LABELS)
    with tab_porters:
        render_events(porters_articles, PORTERS_LABELS)
