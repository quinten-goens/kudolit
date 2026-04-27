import streamlit as st
import pb_client
from styles import (
    inject_global_css,
    inject_page_theme_css,
    get_theme,
    render_message_card_html,
    render_page_header_html,
    render_attribution_html,
    render_header_preview_html,
    _img_to_data_url,
    PALETTE_THEMES,
    OCCASION_THEMES,
    FONTS,
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
    st.markdown(render_page_header_html(page.heading, theme), unsafe_allow_html=True)
    logout_button()

    messages = pb_client.get_messages(page.id)
    if not messages:
        st.info("No kudos yet — share the user code so people can start adding messages!")
    else:
        _render_messages_grid(messages)

    attribution = render_attribution_html(theme)
    if attribution:
        st.markdown(attribution, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# User view
# ---------------------------------------------------------------------------

def render_user_view(page):
    theme = page.theme if isinstance(page.theme, dict) else {}
    inject_page_theme_css(theme)
    st.markdown(render_page_header_html(page.heading, theme), unsafe_allow_html=True)
    logout_button()

    with st.form("new_message", clear_on_submit=True):
        st.markdown("**Add a kudo**")
        author = st.text_input("Your name", max_chars=100)
        content = st.text_area(
            "Your message (markdown supported)",
            max_chars=5000,
            height=150,
            help="You can use **bold**, *italic*, lists, links, and more.",
        )
        image_url = st.text_input(
            "Image / GIF URL (optional)",
            help="Paste a direct image or GIF URL. On [Giphy](https://giphy.com), find a GIF, right-click it and choose **Copy Image Link**, then paste it here.",
        )
        st.caption("Find a GIF on [Giphy](https://giphy.com) → right-click the GIF → Copy Image Link → paste above.")
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

    attribution = render_attribution_html(theme)
    if attribution:
        st.markdown(attribution, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Admin view
# ---------------------------------------------------------------------------

def render_admin_view(page):
    inject_page_theme_css({"preset": "default"})
    st.markdown('<div class="page-header"><h1>KudoLit Admin</h1></div>', unsafe_allow_html=True)
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
        heading = st.text_input("Page heading", placeholder="Happy Birthday, Jane!", key="create_heading")
        st.divider()
        new_theme = _render_theme_picker("create", {})
        st.divider()
        if heading.strip():
            st.markdown(render_header_preview_html(heading.strip(), new_theme), unsafe_allow_html=True)

        if st.button("Create page ✨", use_container_width=True, type="primary", key="create_submit"):
            if not heading.strip():
                st.error("Please enter a heading.")
            else:
                new_page = pb_client.create_page(heading.strip(), new_theme)
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

        with st.expander("Edit page settings", expanded=False):
            new_heading = st.text_input("Heading", value=page.heading, key="edit_heading")
            st.divider()
            current_theme = page.theme if isinstance(page.theme, dict) else {}
            new_theme = _render_theme_picker("edit", current_theme)
            st.divider()
            st.markdown(render_header_preview_html(new_heading or page.heading, new_theme), unsafe_allow_html=True)

            if st.button("Save changes", use_container_width=True, type="primary", key="save_edit"):
                pb_client.update_page(page.id, {"heading": new_heading.strip(), "theme": new_theme})
                st.toast("Page updated!")
                st.rerun()

        st.divider()
        st.caption("Messages — click 🗑 to delete")
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
# Theme picker helper
# ---------------------------------------------------------------------------

def _render_theme_picker(key_prefix: str, current_theme: dict) -> dict:
    """
    Renders the background + font picker. Returns the complete theme dict to store.
    Must be called outside any st.form so image selection buttons trigger reruns.
    """
    preset = current_theme.get("preset", "default")
    is_occasion = preset in OCCASION_THEMES

    bg_type = st.radio(
        "Background",
        ["Color palette", "Occasion photo"],
        index=1 if is_occasion else 0,
        horizontal=True,
        key=f"{key_prefix}_bg_type",
    )

    new_theme: dict = {}

    if bg_type == "Color palette":
        palette_keys = list(PALETTE_THEMES.keys())
        current_palette = preset if preset in PALETTE_THEMES else "default"
        chosen = st.selectbox(
            "Palette",
            palette_keys,
            index=palette_keys.index(current_palette),
            key=f"{key_prefix}_palette",
        )
        new_theme["preset"] = chosen
        if chosen == "custom":
            new_theme["bg_color"] = st.color_picker(
                "Background color",
                current_theme.get("bg_color", "#f8f4f0"),
                key=f"{key_prefix}_custom_color",
            )

    else:  # Occasion photo
        occasion_keys = list(OCCASION_THEMES.keys())
        current_occasion = preset if preset in OCCASION_THEMES else "birthday"
        chosen_occasion = st.selectbox(
            "Occasion",
            occasion_keys,
            index=occasion_keys.index(current_occasion),
            format_func=lambda k: OCCASION_THEMES[k]["label"],
            key=f"{key_prefix}_occasion",
        )
        new_theme["preset"] = chosen_occasion

        # Reset selected image when occasion changes
        occ_track_key = f"{key_prefix}_last_occasion"
        idx_key = f"{key_prefix}_img_idx"
        if st.session_state.get(occ_track_key) != chosen_occasion:
            st.session_state[idx_key] = (
                current_theme.get("image_index", 0)
                if current_occasion == chosen_occasion else 0
            )
            st.session_state[occ_track_key] = chosen_occasion

        selected_idx = st.session_state.get(idx_key, 0)

        # 2-row × 5-col thumbnail grid
        st.markdown("**Select background photo:**")
        images = OCCASION_THEMES[chosen_occasion]["images"]
        for row in range(2):
            cols = st.columns(5)
            for col_i in range(5):
                idx = row * 5 + col_i
                if idx >= len(images):
                    break
                with cols[col_i]:
                    is_selected = idx == selected_idx
                    border = "#e07c5a" if is_selected else "transparent"
                    st.markdown(
                        f'<div style="border:3px solid {border}; border-radius:6px; overflow:hidden; margin-bottom:4px;">'
                        f'<img src="{_img_to_data_url(chosen_occasion, idx)}"'
                        f' style="width:100%;display:block;aspect-ratio:16/9;object-fit:cover;" /></div>',
                        unsafe_allow_html=True,
                    )
                    label = "✓" if is_selected else "Select"
                    if st.button(label, key=f"{key_prefix}_img_{idx}", use_container_width=True):
                        st.session_state[idx_key] = idx
                        st.rerun()

        new_theme["image_index"] = st.session_state.get(idx_key, 0)

        # Attribution preview
        photographer = images[new_theme["image_index"]]["photographer"]
        username = images[new_theme["image_index"]]["username"]
        st.caption(f"Photo by [{photographer}](https://unsplash.com/@{username}?utm_source=kudolit&utm_medium=referral) on Unsplash")

    # Font + color picker
    st.markdown("**Heading font:**")
    font_names = list(FONTS.keys())
    current_font = current_theme.get("font_family", "Inter")
    font_idx = font_names.index(current_font) if current_font in font_names else 0
    col_font, col_size, col_color = st.columns([2, 1, 1])
    with col_font:
        new_theme["font_family"] = st.selectbox(
            "Font",
            font_names,
            index=font_idx,
            key=f"{key_prefix}_font",
        )
    with col_size:
        new_theme["font_size"] = st.slider(
            "Size (rem)",
            min_value=1.2,
            max_value=3.5,
            value=float(current_theme.get("font_size", 2.2)),
            step=0.1,
            key=f"{key_prefix}_font_size",
        )
    with col_color:
        default_color = current_theme.get("header_color") or get_theme(new_theme).get("accent", "#e07c5a")
        new_theme["header_color"] = st.color_picker(
            "Color",
            value=default_color,
            key=f"{key_prefix}_header_color",
        )

    # Style toggles + alignment + emoji
    st.markdown("**Heading style:**")
    col_b, col_i, col_u, col_s, col_align, col_emoji = st.columns([1, 1, 1, 1, 2, 2])
    with col_b:
        new_theme["header_bold"] = st.checkbox(
            "**B**", value=current_theme.get("header_bold", True), key=f"{key_prefix}_bold"
        )
    with col_i:
        new_theme["header_italic"] = st.checkbox(
            "_I_", value=current_theme.get("header_italic", False), key=f"{key_prefix}_italic"
        )
    with col_u:
        new_theme["header_underline"] = st.checkbox(
            "U̲", value=current_theme.get("header_underline", False), key=f"{key_prefix}_underline"
        )
    with col_s:
        new_theme["header_shadow"] = st.checkbox(
            "Shadow", value=current_theme.get("header_shadow", False), key=f"{key_prefix}_shadow"
        )
    with col_align:
        align_opts = ["left", "center", "right"]
        new_theme["header_align"] = st.radio(
            "Align",
            align_opts,
            index=align_opts.index(current_theme.get("header_align", "center")),
            horizontal=True,
            key=f"{key_prefix}_align",
        )
    with col_emoji:
        new_theme["header_emoji"] = st.text_input(
            "Emoji (flanks heading)",
            value=current_theme.get("header_emoji", ""),
            max_chars=4,
            placeholder="🎉",
            key=f"{key_prefix}_emoji",
        )

    return new_theme


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
