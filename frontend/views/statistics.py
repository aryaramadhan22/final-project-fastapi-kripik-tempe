import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.api import get_stats


COLORS = {
    "accent":  "#7c6aff",
    "success": "#22c997",
    "warn":    "#e8a020",
    "danger":  "#e03535",
    "muted":   "#6b7094",
    "surface": "#1c1e2a",
    "border":  "#2a2d3e",
    "text":    "#e8eaf0",
}

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color=COLORS["text"],
    font_family="-apple-system, BlinkMacSystemFont, Helvetica Neue, Arial, sans-serif",
    margin=dict(l=20, r=20, t=30, b=20),
)


def render():
    st.markdown('<h1 class="gl-heading">Statistics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="gl-sub">Your gaming collection at a glance</p>', unsafe_allow_html=True)

    stats = get_stats()
    if not stats or stats.get("total", 0) == 0:
        st.markdown('<div class="gl-empty"><p>No games in your collection yet.</p></div>', unsafe_allow_html=True)
        return

    # KPI row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Games", stats["total"])
    with k2:
        st.metric("Total Hours", f"{stats['total_hours']}h")
    with k3:
        completed = stats["status_distribution"].get("completed", 0)
        st.metric("Completed", completed)
    with k4:
        playing = stats["status_distribution"].get("playing", 0)
        st.metric("Playing Now", playing)

    st.divider()

    # Charts row
    c1, c2 = st.columns(2)

    # Platform donut
    with c1:
        plat = stats.get("platform_distribution", {})
        if plat:
            fig = go.Figure(go.Pie(
                labels=[k.upper() for k in plat.keys()],
                values=list(plat.values()),
                hole=0.55,
                marker_colors=[COLORS["accent"], COLORS["success"], COLORS["warn"]],
                textinfo="label+percent",
                textfont_color=COLORS["text"],
            ))
            fig.update_layout(
                title="Platform Distribution",
                title_font_color=COLORS["text"],
                showlegend=False,
                **PLOTLY_THEME,
            )
            st.plotly_chart(fig, use_container_width=True)

    # Status bar
    with c2:
        sts = stats.get("status_distribution", {})
        if sts:
            status_colors = {
                "playing": COLORS["accent"],
                "completed": COLORS["success"],
                "wishlist": COLORS["warn"],
            }
            fig = go.Figure(go.Bar(
                x=[k.capitalize() for k in sts.keys()],
                y=list(sts.values()),
                marker_color=[status_colors.get(k, COLORS["muted"]) for k in sts.keys()],
            ))
            fig.update_layout(
                title="Status Breakdown",
                title_font_color=COLORS["text"],
                xaxis=dict(showgrid=False, color=COLORS["muted"]),
                yaxis=dict(showgrid=True, gridcolor=COLORS["border"], color=COLORS["muted"]),
                **PLOTLY_THEME,
            )
            st.plotly_chart(fig, use_container_width=True)

    # Avg rating by genre
    genre_ratings = stats.get("avg_rating_by_genre", {})
    if genre_ratings:
        sorted_genres = sorted(genre_ratings.items(), key=lambda x: x[1], reverse=True)
        genres, ratings = zip(*sorted_genres)

        fig = go.Figure(go.Bar(
            x=list(genres),
            y=list(ratings),
            marker_color=COLORS["warn"],
            text=[f"{r:.1f}" for r in ratings],
            textposition="outside",
            textfont_color=COLORS["text"],
        ))
        fig.update_layout(
            title="Average Rating by Genre",
            title_font_color=COLORS["text"],
            yaxis=dict(range=[0, 11], showgrid=True, gridcolor=COLORS["border"], color=COLORS["muted"]),
            xaxis=dict(showgrid=False, color=COLORS["muted"]),
            **PLOTLY_THEME,
        )
        st.plotly_chart(fig, use_container_width=True)
