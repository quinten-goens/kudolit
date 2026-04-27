import streamlit as st
import pb_client
from styles import (
    inject_global_css,
    inject_page_theme_css,
    render_message_card_html,
    render_page_header_html,
    PRESET_THEMES,
)

st.set_page_config(page_title="KudoLit", page_icon="✨", layout="centered")
inject_global_css()


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def main():
    if "role" not in st.session_state:
        code = st.query_params.get("code", "")
        if code:
            result = pb_client.lookup_code(code)
            if result is None:
                st.query_params.clear()
                st.session_state.pop("role", None)
                code_entry_screen(error="Invalid code. Please try again.")
                return
            role, page = result
            st.session_state["role"] = role
            st.session_state["page_id"] = page.id
            st.session_state["code"] = code
        else:
            code_entry_screen()
            return

    role = st.session_state["role"]
    page_id = st.session_state["page_id"]

    try:
        page = pb_client.get_page(page_id)
    except Exception:
        st.session_state.clear()
        st.query_params.clear()
        code_entry_screen(error="Page not found. It may have been deleted.")
        return

    if role == "admin":
        render_admin_view(page)
    elif role == "user":
        render_user_view(page)
    else:
        render_viewer_view(page)


# ---------------------------------------------------------------------------
# Code entry
# ---------------------------------------------------------------------------

def code_entry_screen(error: str = ""):
    st.markdown(
        '<div class="code-entry-container">'
        "<h1>KudoLit</h1>"
        "<p>Enter your access code to continue</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if error:
            st.error(error)
        with st.form("code_form"):
            code = st.text_input("Access code", placeholder="e.g. ab12cd34ef", label_visibility="collapsed")
            submitted = st.form_submit_button("Enter", use_container_width=True)
        if submitted and code.strip():
            st.query_params["code"] = code.strip()
            st.rerun()


def logout_button():
    if st.button("↩ Switch code", key="logout"):
        st.session_state.clear()
        st.query_params.clear()
        st.rerun()


# ---------------------------------------------------------------------------
# Viewer view
# ---------------------------------------------------------------------------

def render_viewer_view(page):
    theme = page.theme if isinstance(page.theme, dict) else {}
    inject_page_theme_css(theme)

    st.markdown(render_page_header_html(page.heading), unsafe_allow_html=True)
    logout_button()

    messages = pb_client.get_messages(page.id)
    if not messages:
        st.info("No kudos yet — share the user code so people can start adding messages!")
    else:
        _render_messages_grid(messages)


# ---------------------------------------------------------------------------
# User view
# ---------------------------------------------------------------------------

def render_user_view(page):
    theme = page.theme if isinstance(page.theme, dict) else {}
    inject_page_theme_css(theme)

    st.markdown(render_page_header_html(page.heading), unsafe_allow_html=True)
    logout_button()

    with st.expander("Add a kudo", expanded=False):
        with st.form("new_message", clear_on_submit=True):
            author = st.text_input("Your name", max_chars=100)
            content = st.text_area(
                "Your message (markdown supported)",
                max_chars=5000,
                height=150,
                help="You can use **bold**, *italic*, lists, links, and more.",
            )
            image_url = st.text_input("Image / GIF URL (optional)")
            image_file = st.file_uploader(
                "Or upload an image",
                type=["png", "jpg", "jpeg", "gif", "webp"],
            )
            submitted = st.form_submit_button("Send kudo ✨", use_container_width=True)

        if submitted:
            if not author.strip():
                st.error("Please enter your name.")
            elif not content.strip():
                st.error("Please write a message.")
            else:
                pb_client.create_message(
                    page.id,
                    author.strip(),
                    content.strip(),
                    image_url.strip(),
                    image_file,
                )
                st.toast("Kudo sent!")
                st.rerun()

    st.divider()
    messages = pb_client.get_messages(page.id)
    if not messages:
        st.info("No kudos yet — be the first!")
    else:
        _render_messages_grid(messages)


# ---------------------------------------------------------------------------
# Admin view
# ---------------------------------------------------------------------------

def render_admin_view(page):
    inject_page_theme_css({"preset": "default"})

    st.markdown(
        '<div class="page-header"><h1>KudoLit Admin</h1></div>',
        unsafe_allow_html=True,
    )
    logout_button()

    tab_dashboard, tab_create, tab_manage = st.tabs(["Dashboard", "Create page", "Manage page"])

    # --- Dashboard ---
    with tab_dashboard:
        pages = pb_client.get_all_pages()
        if not pages:
            st.info("No kudo pages yet. Create one in the 'Create page' tab.")
        for p in pages:
            with st.container(border=True):
                st.subheader(p.heading)
                col_codes, col_actions = st.columns([3, 1])
                with col_codes:
                    st.markdown(
                        f'<div class="admin-code-box"><span class="label">Admin</span><span class="code">{p.admin_code}</span></div>'
                        f'<div class="admin-code-box"><span class="label">User</span><span class="code">{p.user_code}</span></div>'
                        f'<div class="admin-code-box"><span class="label">Viewer</span><span class="code">{p.viewer_code}</span></div>',
                        unsafe_allow_html=True,
                    )
                with col_actions:
                    msg_count = len(pb_client.get_messages(p.id))
                    st.metric("Messages", msg_count)
                    if st.button("Delete page", key=f"del_{p.id}", type="secondary"):
                        st.session_state[f"confirm_del_{p.id}"] = True
                    if st.session_state.get(f"confirm_del_{p.id}"):
                        st.warning("Are you sure?")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("Yes, delete", key=f"yes_del_{p.id}", type="primary"):
                                pb_client.delete_page(p.id)
                                st.session_state.pop(f"confirm_del_{p.id}", None)
                                if p.id == page.id:
                                    st.session_state.clear()
                                    st.query_params.clear()
                                st.toast("Page deleted.")
                                st.rerun()
                        with c2:
                            if st.button("Cancel", key=f"cancel_del_{p.id}"):
                                st.session_state.pop(f"confirm_del_{p.id}", None)
                                st.rerun()

    # --- Create page ---
    with tab_create:
        with st.form("create_page"):
            heading = st.text_input("Page heading", placeholder="Happy Birthday, Jane!")
            preset = st.selectbox("Theme", list(PRESET_THEMES.keys()), index=0)
            custom_color = None
            if preset == "custom":
                custom_color = st.color_picker("Background color", "#f8f4f0")
            submitted = st.form_submit_button("Create page", use_container_width=True)

        if submitted:
            if not heading.strip():
                st.error("Please enter a heading.")
            else:
                theme = {"preset": preset}
                if custom_color:
                    theme["bg_color"] = custom_color
                new_page = pb_client.create_page(heading.strip(), theme)
                st.toast("Page created!")
                st.success("New page created! Here are the access codes:")
                st.markdown(
                    f'<div class="admin-code-box"><span class="label">Admin</span><span class="code">{new_page.admin_code}</span></div>'
                    f'<div class="admin-code-box"><span class="label">User</span><span class="code">{new_page.user_code}</span></div>'
                    f'<div class="admin-code-box"><span class="label">Viewer</span><span class="code">{new_page.viewer_code}</span></div>',
                    unsafe_allow_html=True,
                )

    # --- Manage current page ---
    with tab_manage:
        st.subheader(page.heading)

        with st.expander("Edit page settings"):
            with st.form("edit_page"):
                new_heading = st.text_input("Heading", value=page.heading)
                current_theme = page.theme if isinstance(page.theme, dict) else {}
                current_preset = current_theme.get("preset", "default")
                presets = list(PRESET_THEMES.keys())
                idx = presets.index(current_preset) if current_preset in presets else 0
                new_preset = st.selectbox("Theme", presets, index=idx)
                new_custom_color = None
                if new_preset == "custom":
                    new_custom_color = st.color_picker(
                        "Background color",
                        current_theme.get("bg_color", "#f8f4f0"),
                    )
                save = st.form_submit_button("Save changes", use_container_width=True)
            if save:
                theme = {"preset": new_preset}
                if new_custom_color:
                    theme["bg_color"] = new_custom_color
                pb_client.update_page(page.id, {"heading": new_heading.strip(), "theme": theme})
                st.toast("Page updated!")
                st.rerun()

        st.divider()
        st.caption("Messages — click delete to remove a message")
        messages = pb_client.get_messages(page.id)
        if not messages:
            st.info("No messages on this page yet.")
        for msg in messages:
            col_card, col_del = st.columns([5, 1])
            with col_card:
                _render_message(msg)
            with col_del:
                if st.button("🗑", key=f"delmsg_{msg.id}", help="Delete this message"):
                    pb_client.delete_message(msg.id)
                    st.toast("Message deleted.")
                    st.rerun()


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _message_card_html(msg) -> str:
    image_url = getattr(msg, "image_url", "") or ""
    file_url = pb_client.get_file_url(msg, "image_file")
    display_image = image_url or file_url

    created = getattr(msg, "created", "")
    if created:
        if hasattr(created, "strftime"):
            created = created.strftime("%Y-%m-%d %H:%M")
        else:
            created = str(created)[:16].replace("T", " ")

    return render_message_card_html(
        author=msg.author_name,
        content_markdown=msg.content,
        timestamp=created,
        image_url=display_image,
    )


def _render_message(msg):
    st.markdown(_message_card_html(msg), unsafe_allow_html=True)


def _render_messages_grid(messages):
    cols = st.columns(3)
    for i, msg in enumerate(messages):
        with cols[i % 3]:
            st.markdown(_message_card_html(msg), unsafe_allow_html=True)


# ---------------------------------------------------------------------------

main()
