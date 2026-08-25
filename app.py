import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from marketintel.analysis import score_submission  # noqa: E402
from marketintel.config import (  # noqa: E402
    INTERACTION_MATRIX_PATH,
    NEWS_EMBEDDINGS_PATH,
    NEWS_PATH,
    PESTLE_DIMS,
    PESTLE_LABELS,
    PORTERS_DIMS,
    PORTERS_LABELS,
)
from marketintel.data_loader import load_interaction_matrix, load_news  # noqa: E402
from marketintel.embeddings import embed_text  # noqa: E402

POSITIVE_COLOR = "#2ca02c"
NEGATIVE_COLOR = "#d62728"
NEUTRAL_COLOR = "#9e9e9e"

st.set_page_config(page_title="Explainable Market Intelligence", layout="centered")


@st.cache_resource
def get_model_warm():
    from marketintel.embeddings import get_model

    return get_model()


@st.cache_data
def get_news():
    return load_news()


@st.cache_data
def get_interaction_matrix():
    return load_interaction_matrix()


def data_ready() -> bool:
    return NEWS_PATH.exists() and NEWS_EMBEDDINGS_PATH.exists() and INTERACTION_MATRIX_PATH.exists()


AXIS_LABEL_OVERRIDES = {
    "threat_new_entrants": "New Entrants",
    "threat_substitutes": "Substitutes",
}


def make_radar(dims: list[str], labels: dict, values: dict, near_zero: set, title: str) -> go.Figure:
    axis_labels = {d: AXIS_LABEL_OVERRIDES.get(d, labels[d]) for d in dims}
    categories = [axis_labels[d] for d in dims] + [axis_labels[dims[0]]]
    radii = [abs(values[d]) for d in dims] + [abs(values[dims[0]])]
    signed = [values[d] for d in dims] + [values[dims[0]]]

    def color_for(d, v):
        if d in near_zero:
            return NEUTRAL_COLOR
        return POSITIVE_COLOR if v >= 0 else NEGATIVE_COLOR

    colors = [color_for(d, v) for d, v in zip(dims + [dims[0]], signed)]

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
        f"<span style='color:{NEUTRAL_COLOR}'>&#9679;</span> negligible&nbsp;&nbsp;&nbsp;"
        f"radius = sensitivity magnitude (0-100)",
        unsafe_allow_html=True,
    )


st.title("Explainable Market Intelligence")
st.caption("Paste your CVP / business description. Location is fixed to LPU, Punjab.")

if not data_ready():
    st.error(
        "Fabricated data or trained interaction matrix not found. Generate/train it first:\n\n"
        "```\npython scripts/generate_news.py\n"
        "python scripts/generate_startups.py\n"
        "python scripts/train_interaction_matrix.py\n```"
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
        W = get_interaction_matrix()

        cvp_embedding = embed_text(cvp_text)
        result = score_submission(news, news_embeddings, cvp_embedding, W)

    st.subheader("Sensitivity profile")

    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.plotly_chart(
            make_radar(PESTLE_DIMS, PESTLE_LABELS, result["pestle_display"], result["near_zero"], "PESTLE"),
            use_container_width=True,
        )
        legend_note()
    with chart_cols[1]:
        st.plotly_chart(
            make_radar(
                PORTERS_DIMS, PORTERS_LABELS, result["porters_display"], result["near_zero"], "Porter's Five Forces"
            ),
            use_container_width=True,
        )
        legend_note()

    st.divider()
    st.subheader("Top contributing events")

    tab_pestle, tab_porters = st.tabs(["PESTLE", "Porter's Five Forces"])

    def render_events(ranked, labels):
        if not ranked:
            st.info("No contributing articles found.")
            return
        for item in ranked:
            article = item["article"]
            dim_label = labels[item["dim"]]
            direction_color = POSITIVE_COLOR if item["contribution"] >= 0 else NEGATIVE_COLOR
            direction_word = "helping" if item["contribution"] >= 0 else "hurting"
            st.markdown(
                f"**{article['title']}** &nbsp;"
                f"<span style='color:{direction_color}; font-size:0.85em'>&#9679; {direction_word}</span>",
                unsafe_allow_html=True,
            )
            st.caption(
                f"{article['date']} · {article['scope']} · affects **{dim_label}** · "
                f"contribution {item['contribution']:+.2f}"
            )

    with tab_pestle:
        render_events(result["pestle_articles"], PESTLE_LABELS)
    with tab_porters:
        render_events(result["porters_articles"], PORTERS_LABELS)
