import streamlit as st
from utils.styles import GLOBAL_CSS
from utils.api import login, register

st.set_page_config(
    page_title="GameLog",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# Session defaults
for key, default in [
    ("token", None),
    ("username", None),
    ("page", "games"),
    ("edit_game_id", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# Auth guard
def show_auth():
    st.markdown("""
    <div class="auth-wrap">
        <div class="auth-brand">
            <div class="auth-dot"></div>
            GameLog
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        st.markdown("#### Welcome back")
        with st.form("login_form"):
            uname = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
        if submitted:
            if not uname or not pwd:
                st.error("Please fill all fields.")
            else:
                data, code = login(uname, pwd)
                if code == 200:
                    st.session_state.token = data["access_token"]
                    st.session_state.username = uname
                    st.rerun()
                else:
                    st.error(data.get("detail", "Login failed"))

    with tab_register:
        st.markdown("#### Create account")
        with st.form("register_form"):
            r_uname = st.text_input("Username", key="ru")
            r_pwd = st.text_input("Password", type="password", key="rp")
            r_submitted = st.form_submit_button("Register", use_container_width=True)
        if r_submitted:
            if not r_uname or not r_pwd:
                st.error("Please fill all fields.")
            else:
                data, code = register(r_uname, r_pwd)
                if code == 201:
                    st.success("Account created! Please log in.")
                else:
                    st.error(data.get("detail", "Registration failed"))


# Sidebar navigation
def show_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div class="auth-brand" style="margin-bottom:1.5rem;">
            <div class="auth-dot"></div>
            GameLog
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"Logged in as **{st.session_state.username}**")
        st.divider()

        pages = {"My Games": "games", "Add Game": "add", "Statistics": "stats"}
        for label, key in pages.items():
            if st.button(label, use_container_width=True, key=f"nav_{key}"):
                st.session_state.page = key
                st.session_state.edit_game_id = None
                st.rerun()

        st.divider()
        if st.button("Logout", use_container_width=True):
            for k in ["token", "username", "edit_game_id"]:
                st.session_state[k] = None
            st.session_state.page = "games"
            st.rerun()


# Router
if not st.session_state.token:
    show_auth()
else:
    show_sidebar()

    page = st.session_state.page

    if page == "games":
        from views.game_list import render
        render()
    elif page == "add":
        from views.game_form import render_add
        render_add()
    elif page == "edit":
        from views.game_form import render_edit
        render_edit()
    elif page == "stats":
        from views.statistics import render
        render()
