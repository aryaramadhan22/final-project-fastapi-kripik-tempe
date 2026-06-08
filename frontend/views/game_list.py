import streamlit as st
from utils.api import get_games, delete_game
from utils.styles import badge, chip, star_rating


def render():
    st.markdown('<h1 class="gl-heading">My Games</h1>', unsafe_allow_html=True)

    # Filter bar
    col1, col2, col3 = st.columns([3, 1.5, 1.5])
    with col1:
        q = st.text_input("", placeholder="Search games…", label_visibility="collapsed")
    with col2:
        platform = st.selectbox(
            "", ["", "pc", "mobile", "console"],
            format_func=lambda x: "All Platforms" if x == "" else x.upper(),
            label_visibility="collapsed",
        )
    with col3:
        status = st.selectbox(
            "", ["", "playing", "completed", "wishlist"],
            format_func=lambda x: "All Status" if x == "" else x.capitalize(),
            label_visibility="collapsed",
        )

    games = get_games(q=q or None, platform=platform or None, status=status or None)

    st.markdown(
        f'<p class="gl-sub">{len(games)} game{"s" if len(games) != 1 else ""} tracked</p>',
        unsafe_allow_html=True,
    )

    if not games:
        st.markdown(
            '<div class="gl-empty"><p style="font-weight:600;">No games found.</p>'
            '<p style="font-size:.84rem;margin-top:.3rem;">Clear your filters or add a new game.</p></div>',
            unsafe_allow_html=True,
        )
        return

    # Grid
    cols = st.columns(3)
    for i, game in enumerate(games):
        with cols[i % 3]:
            review_html = (
                f'<p class="gl-review">{game["review"]}</p>'
                if game.get("review") else ""
            )
            st.markdown(f"""
            <div class="gl-card">
                <div class="gl-card-top">
                    <span class="gl-title">{game["title"]}</span>
                    {badge(game["status"])}
                </div>
                <div class="gl-meta">
                    {chip(game["genre"]) if game.get("genre") else ""}
                    {chip(game["platform"].upper()) if game.get("platform") else ""}
                </div>
                <div class="gl-stats">
                    {star_rating(game["rating"])}
                    &nbsp;&nbsp;{game["hours_played"]}h played
                </div>
                {review_html}
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Edit", key=f"edit_{game['id']}", use_container_width=True):
                    st.session_state.edit_game_id = game["id"]
                    st.session_state.page = "edit"
                    st.rerun()
            with c2:
                if st.button("Delete", key=f"del_{game['id']}", use_container_width=True):
                    st.session_state[f"confirm_del_{game['id']}"] = True

            # Confirm delete
            if st.session_state.get(f"confirm_del_{game['id']}"):
                st.warning(f"Delete **{game['title']}**?")
                y, n = st.columns(2)
                with y:
                    if st.button("Yes, delete", key=f"yes_{game['id']}", use_container_width=True):
                        delete_game(game["id"])
                        del st.session_state[f"confirm_del_{game['id']}"]
                        st.rerun()
                with n:
                    if st.button("Cancel", key=f"no_{game['id']}", use_container_width=True):
                        del st.session_state[f"confirm_del_{game['id']}"]
                        st.rerun()
