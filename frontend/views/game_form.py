import streamlit as st
from utils.api import create_game, update_game, get_game


PLATFORM_OPTIONS = ["pc", "mobile", "console"]
STATUS_OPTIONS = ["wishlist", "playing", "completed"]


def _form(title: str, subtitle: str, defaults: dict, on_submit, submit_label: str):
    st.markdown(f'<h1 class="gl-heading">{title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="gl-sub">{subtitle}</p>', unsafe_allow_html=True)

    with st.form("game_form"):
        col1, col2 = st.columns(2)
        with col1:
            f_title = st.text_input("Title *", value=defaults.get("title", ""))
            f_genre = st.text_input("Genre *", value=defaults.get("genre", ""))
            f_platform = st.selectbox(
                "Platform *",
                PLATFORM_OPTIONS,
                index=PLATFORM_OPTIONS.index(defaults["platform"]) if defaults.get("platform") in PLATFORM_OPTIONS else 0,
            )
        with col2:
            f_status = st.selectbox(
                "Status *",
                STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(defaults["status"]) if defaults.get("status") in STATUS_OPTIONS else 0,
            )
            f_hours = st.number_input("Hours Played", min_value=0, value=int(defaults.get("hours_played", 0)))
            f_rating = st.slider("Rating (0–10)", 0, 10, int(defaults.get("rating", 0)))
        f_review = st.text_area("Review / Notes", value=defaults.get("review", ""), height=80)

        submitted = st.form_submit_button(submit_label, use_container_width=True)

    if submitted:
        if not f_title or not f_genre:
            st.error("Title and Genre are required.")
            return
        payload = {
            "title": f_title,
            "genre": f_genre,
            "platform": f_platform,
            "status": f_status,
            "hours_played": int(f_hours),
            "rating": int(f_rating),
            "review": f_review,
        }
        on_submit(payload)

    if st.button("← Back to list"):
        st.session_state.page = "games"
        st.session_state.edit_game_id = None
        st.rerun()


def render_add():
    def submit(payload):
        data, code = create_game(payload)
        if code == 201:
            st.success(f"**{payload['title']}** added!")
            st.session_state.page = "games"
            st.rerun()
        else:
            st.error(data.get("detail", "Failed to add game."))

    _form("Add Game", "Log a new game to your collection", {}, submit, "Save Game")


def render_edit():
    game_id = st.session_state.get("edit_game_id")
    if not game_id:
        st.session_state.page = "games"
        st.rerun()

    game = get_game(game_id)
    if not game:
        st.error("Game not found.")
        return

    def submit(payload):
        data, code = update_game(game_id, payload)
        if code == 200:
            st.success("Changes saved!")
            st.session_state.page = "games"
            st.session_state.edit_game_id = None
            st.rerun()
        else:
            st.error(data.get("detail", "Failed to update game."))

    _form("Edit Game", "Update your game entry", game, submit, "Save Changes")
