import markdown as md

# ---------------------------------------------------------------------------
# Occasion themes (photo backgrounds, 10 images each)
# ---------------------------------------------------------------------------

UTM = "utm_source=kudolit&utm_medium=referral"

OCCASION_THEMES = {
    "birthday": {
        "label": "Birthday",
        "accent": "#d97706",
        "card_bg": "rgba(255,255,253,0.93)",
        "images": [
            {"photographer": "Maryam Sicard",        "username": "maryamsicard"},
            {"photographer": "The Ordinary Moments", "username": "cr029"},
            {"photographer": "Adi Goldstein",        "username": "adigold1"},
            {"photographer": "Nikhita Singhal",      "username": "nikhita"},
            {"photographer": "Anita Austvika",       "username": "anitaaustvika"},
            {"photographer": "Nick Fewings",         "username": "jannerboy62"},
            {"photographer": "Sergei Solo",          "username": "solofox"},
            {"photographer": "Al Elmes",             "username": "alelmes"},
            {"photographer": "Maryam Sicard",        "username": "maryamsicard"},
            {"photographer": "Duncan Kidd",          "username": "we_the_royal"},
        ],
    },
    "farewell": {
        "label": "Farewell",
        "accent": "#4f46e5",
        "card_bg": "rgba(255,255,255,0.93)",
        "images": [
            {"photographer": "Clara Beatriz",        "username": "clarabeatriz"},
            {"photographer": "Tolu Akinyemi",        "username": "poetolu"},
            {"photographer": "Anisa Gauri",          "username": "anisagauri"},
            {"photographer": "Meizhi Lang",          "username": "meizhilang"},
            {"photographer": "Ahmet Kurt",           "username": "ahmetkurt"},
            {"photographer": "Matthew Henry",        "username": "matthewhenry"},
            {"photographer": "Eugene",               "username": "eugenegrunge"},
            {"photographer": "Neelakshi Singh",      "username": "neelakshi_singh_"},
            {"photographer": "Phạm Nhật",            "username": "ph4minhat"},
            {"photographer": "Stephanie Klepacki",   "username": "sklepacki"},
        ],
    },
    "graduation": {
        "label": "Graduation",
        "accent": "#6d28d9",
        "card_bg": "rgba(255,255,255,0.93)",
        "images": [
            {"photographer": "A. C.",                "username": "3tnik"},
            {"photographer": "Albert Vincent Wu",    "username": "albertvincentwu"},
            {"photographer": "RUT MIIT",             "username": "rutmiit"},
            {"photographer": "Joshua Hoehne",        "username": "joshua_hoehne"},
            {"photographer": "Katelyn Perry",        "username": "katelynperry"},
            {"photographer": "Caleb Holden",         "username": "calebholden"},
            {"photographer": "Pang Yuhao",           "username": "yuhao"},
            {"photographer": "RUT MIIT",             "username": "rutmiit"},
            {"photographer": "Dragos Blaga",         "username": "7dr_agos2"},
            {"photographer": "Charles DeLoye",       "username": "charlesdeloye"},
        ],
    },
    "retirement": {
        "label": "Retirement",
        "accent": "#0f766e",
        "card_bg": "rgba(255,255,255,0.93)",
        "images": [
            {"photographer": "Getty Images",         "username": "gettyimages"},
            {"photographer": "Aaron Burden",         "username": "aaronburden"},
            {"photographer": "James Hose Jr",        "username": "jameshosejr"},
            {"photographer": "Marc Najera",          "username": "marcnajera"},
            {"photographer": "Natalia Blauth",       "username": "nataliablauth"},
            {"photographer": "Towfiqu barbhuiya",    "username": "towfiqu999999"},
            {"photographer": "Harli Marten",         "username": "harlimarten"},
            {"photographer": "Anukrati Omar",        "username": "anuomar"},
            {"photographer": "Getty Images",         "username": "gettyimages"},
            {"photographer": "Towfiqu barbhuiya",    "username": "towfiqu999999"},
        ],
    },
    "new_baby": {
        "label": "New Baby",
        "accent": "#be185d",
        "card_bg": "rgba(255,255,255,0.93)",
        "images": [
            {"photographer": "Toa Heftiba",          "username": "heftiba"},
            {"photographer": "Imad Ud Khan",         "username": "_madu"},
            {"photographer": "Matthew Osborn",       "username": "matthewosborn"},
            {"photographer": "PICSAR",               "username": "picsar_rovshan"},
            {"photographer": "Toa Heftiba",          "username": "heftiba"},
            {"photographer": "Md Ishak Raman",       "username": "mdishakrahman"},
            {"photographer": "Kelly Sikkema",        "username": "kellysikkema"},
            {"photographer": "Bruno Kelzer",         "username": "bruno_kelzer"},
            {"photographer": "Fellipe Ditadi",       "username": "ditadi"},
            {"photographer": "Bruno Kelzer",         "username": "bruno_kelzer"},
        ],
    },
    "wedding": {
        "label": "Wedding",
        "accent": "#9d174d",
        "card_bg": "rgba(255,255,255,0.93)",
        "images": [
            {"photographer": "Karolina Grabowska",   "username": "kaboompics"},
            {"photographer": "Foto Pettine",         "username": "fotopettine"},
            {"photographer": "Jeremy Wong Weddings", "username": "jeremywongweddings"},
            {"photographer": "Sandy Millar",         "username": "sandym10"},
            {"photographer": "Getty Images",         "username": "gettyimages"},
            {"photographer": "Leonardo Miranda",     "username": "mirandanenee"},
            {"photographer": "Nathan Dumlao",        "username": "nate_dumlao"},
            {"photographer": "Jeremy Wong Weddings", "username": "jeremywongweddings"},
            {"photographer": "Jayson Hinrichsen",    "username": "jayson_hinrichsen"},
            {"photographer": "Jakob Owens",          "username": "jakobowens1"},
        ],
    },
    "get_well": {
        "label": "Get Well Soon",
        "accent": "#15803d",
        "card_bg": "rgba(255,255,255,0.93)",
        "images": [
            {"photographer": "Frank Flores",         "username": "frankflores"},
            {"photographer": "Anastasiya Badun",     "username": "badun"},
            {"photographer": "sina rezakhani",       "username": "artofsinn"},
            {"photographer": "Le Tia",               "username": "basinati"},
            {"photographer": "Mariela Ferbo",        "username": "marielaferbo"},
            {"photographer": "feey",                 "username": "feeypflanzen"},
            {"photographer": "Dzmitry Shepeleu",     "username": "_devslashnull_"},
            {"photographer": "feey",                 "username": "feeypflanzen"},
            {"photographer": "Frank Flores",         "username": "frankflores"},
            {"photographer": "Muhamad Izzul Isyraf", "username": "lensarona"},
        ],
    },
    "landscape": {
        "label": "Landscape",
        "accent": "#334155",
        "card_bg": "rgba(255,255,255,0.92)",
        "images": [
            {"photographer": "Kevin Oetiker",        "username": "kevinoetiker"},
            {"photographer": "Milo Weiler",          "username": "miloweiler"},
            {"photographer": "Manuel Silva",         "username": "manuelsilva"},
            {"photographer": "Joris Visser",         "username": "jorisvisser"},
            {"photographer": "A Chosen Soul",        "username": "a_chosensoul"},
            {"photographer": "Michael Michelovski",  "username": "vansolo"},
            {"photographer": "Daniel A. Páscoa",     "username": "daniel_pascoa"},
            {"photographer": "Michael Michelovski",  "username": "vansolo"},
            {"photographer": "Joshua Earle",         "username": "joshuaearle"},
            {"photographer": "Carlos I",             "username": "procrastinator"},
        ],
    },
    "work_anniversary": {
        "label": "Work Anniversary",
        "accent": "#1d4ed8",
        "card_bg": "rgba(255,255,255,0.93)",
        "images": [
            {"photographer": "Vitaly Gariev",        "username": "silverkblack"},
            {"photographer": "Vitaly Gariev",        "username": "silverkblack"},
            {"photographer": "Vitaly Gariev",        "username": "silverkblack"},
            {"photographer": "Vitaly Gariev",        "username": "silverkblack"},
            {"photographer": "Vitaly Gariev",        "username": "silverkblack"},
            {"photographer": "Vitaly Gariev",        "username": "silverkblack"},
            {"photographer": "Walls.io",             "username": "walls_io"},
            {"photographer": "Vitaly Gariev",        "username": "silverkblack"},
            {"photographer": "Vitaly Gariev",        "username": "silverkblack"},
            {"photographer": "Vitaly Gariev",        "username": "silverkblack"},
        ],
    },
}

# ---------------------------------------------------------------------------
# Palette themes (gradient/color backgrounds, no photo)
# ---------------------------------------------------------------------------

PALETTE_THEMES = {
    "default": {
        "bg": "linear-gradient(135deg, #f8f4f0 0%, #ffffff 100%)",
        "card_bg": "#ffffff",
        "accent": "#e07c5a",
    },
    "warm": {
        "bg": "linear-gradient(135deg, #fce4d6 0%, #f9d5c2 50%, #f5c6aa 100%)",
        "card_bg": "#fffaf7",
        "accent": "#d4603a",
    },
    "cool": {
        "bg": "linear-gradient(135deg, #dbeafe 0%, #c7d7f5 50%, #b3c8eb 100%)",
        "card_bg": "#f8faff",
        "accent": "#3b72c4",
    },
    "celebration": {
        "bg": "linear-gradient(135deg, #fef9e7 0%, #fdf2d1 50%, #fce8b2 100%)",
        "card_bg": "#fffef8",
        "accent": "#d4a017",
    },
    "nature": {
        "bg": "linear-gradient(135deg, #d5eed0 0%, #c1e4bb 50%, #a8d5a0 100%)",
        "card_bg": "#f7fcf6",
        "accent": "#4a8c3f",
    },
    "custom": {
        "bg": "#f8f4f0",
        "card_bg": "#ffffff",
        "accent": "#e07c5a",
    },
}

PRESET_THEMES = PALETTE_THEMES  # backwards-compat alias

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------

FONTS = {
    "Inter":            {"stack": "Inter, system-ui, sans-serif",                   "google": None},
    "Montserrat":       {"stack": "'Montserrat', system-ui, sans-serif",            "google": "Montserrat:wght@400;700"},
    "Raleway":          {"stack": "'Raleway', system-ui, sans-serif",               "google": "Raleway:wght@400;700"},
    "Nunito":           {"stack": "'Nunito', system-ui, sans-serif",                "google": "Nunito:wght@400;700"},
    "Outfit":           {"stack": "'Outfit', system-ui, sans-serif",                "google": "Outfit:wght@400;700"},
    "Josefin Sans":     {"stack": "'Josefin Sans', system-ui, sans-serif",          "google": "Josefin+Sans:wght@400;700"},
    "Georgia":          {"stack": "Georgia, serif",                                 "google": None},
    "Playfair Display": {"stack": "'Playfair Display', Georgia, serif",             "google": "Playfair+Display:wght@400;700"},
    "Lora":             {"stack": "'Lora', Georgia, serif",                         "google": "Lora:wght@400;700"},
    "DM Serif Display": {"stack": "'DM Serif Display', Georgia, serif",             "google": "DM+Serif+Display"},
}

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

GLOBAL_CSS = """
<style>
    .stApp > header { display: none; }
    .block-container { max-width: 1100px; padding-top: 2rem; }

    .kudo-card {
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 1rem;
        background: var(--card-bg, #ffffff);
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        border: 1px solid rgba(0,0,0,0.04);
        break-inside: avoid;
        page-break-inside: avoid;
        display: inline-block;
        width: 100%;
    }
    .kudo-card .card-image {
        display: block;
        width: 100%;
        max-height: 260px;
        object-fit: cover;
    }
    .kudo-card .card-body { padding: 1rem; }
    .kudo-card .card-content {
        font-size: 0.9rem;
        line-height: 1.6;
        color: #444;
    }
    .kudo-card .card-content p { margin: 0 0 0.5rem 0; }
    .kudo-card .card-content p:last-child { margin-bottom: 0; }
    .kudo-card .card-footer {
        display: flex;
        justify-content: flex-end;
        align-items: baseline;
        margin-top: 0.75rem;
        gap: 0.4rem;
    }
    .kudo-card .author { font-weight: 600; font-size: 0.82rem; color: #888; }
    .kudo-card .timestamp { font-size: 0.72rem; color: #bbb; }

    .page-header {
        text-align: center;
        padding: 2.5rem 1rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        background: rgba(255,255,255,0.5);
        backdrop-filter: blur(8px);
    }
    .page-header h1 { margin: 0; font-weight: 700; }

    .code-entry-container {
        max-width: 440px;
        margin: 15vh auto 0 auto;
        text-align: center;
    }
    .code-entry-container h1 { font-size: 2.4rem; font-weight: 700; margin-bottom: 0.25rem; }
    .code-entry-container p { color: #888; margin-bottom: 2rem; }

    .admin-code-box {
        background: #f8f4f0;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        font-family: monospace;
        font-size: 0.9rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .admin-code-box .label { font-weight: 600; color: #666; min-width: 60px; }
    .admin-code-box .code { color: #333; letter-spacing: 0.5px; }

    .attribution {
        position: fixed;
        bottom: 0.5rem;
        right: 0.75rem;
        font-size: 0.68rem;
        color: rgba(255,255,255,0.75);
        text-shadow: 0 1px 3px rgba(0,0,0,0.6);
        z-index: 9999;
    }
    .attribution a { color: rgba(255,255,255,0.9); text-decoration: underline; }

    .img-picker-thumb {
        cursor: pointer;
        border-radius: 6px;
        overflow: hidden;
        transition: transform 0.1s;
    }
    .img-picker-thumb:hover { transform: scale(1.03); }
    .img-picker-thumb img { width: 100%; display: block; aspect-ratio: 16/9; object-fit: cover; }

    .header-preview {
        text-align: center;
        padding: 1.5rem 1rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        background: rgba(255,255,255,0.85);
        border: 1px dashed #ccc;
    }
</style>
"""


def inject_global_css():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def get_theme(theme_dict: dict) -> dict:
    preset = theme_dict.get("preset", "default")

    if preset in OCCASION_THEMES:
        occ = OCCASION_THEMES[preset]
        img_idx = int(theme_dict.get("image_index", 0))
        return {
            "bg_image": f"/app/static/themes/{preset}/{img_idx}.jpg",
            "card_bg": occ["card_bg"],
            "accent": occ["accent"],
        }

    if preset == "custom":
        bg_color = theme_dict.get("bg_color", "#f8f4f0")
        return {"bg": bg_color, "card_bg": "#ffffff", "accent": "#e07c5a", "bg_image": None}

    t = PALETTE_THEMES.get(preset, PALETTE_THEMES["default"]).copy()
    t["bg_image"] = None
    return t


def _font_css(theme_dict: dict) -> tuple[str, str, float]:
    """Returns (google_import_tag, font_stack_css)."""
    font_name = theme_dict.get("font_family", "Inter")
    font_size = float(theme_dict.get("font_size", 2.2))
    font_data = FONTS.get(font_name, FONTS["Inter"])
    font_stack = font_data["stack"]
    google = font_data.get("google")
    import_tag = (
        f'@import url("https://fonts.googleapis.com/css2?family={google}&display=swap");'
        if google else ""
    )
    return import_tag, font_stack, font_size


def inject_page_theme_css(theme_dict: dict):
    import streamlit as st
    theme = get_theme(theme_dict)
    import_tag, font_stack, font_size = _font_css(theme_dict)

    if theme.get("bg_image"):
        bg_css = (
            f".stApp {{ background-image: url('{theme['bg_image']}');"
            " background-size: cover; background-position: center; background-attachment: fixed; }}"
        )
    else:
        bg_css = f".stApp {{ background: {theme.get('bg', '#f8f4f0')}; }}"

    card_bg = theme["card_bg"]
    accent = theme["accent"]
    header_color = theme_dict.get("header_color") or accent
    font_weight  = "700" if theme_dict.get("header_bold", True) else "400"
    font_style   = "italic" if theme_dict.get("header_italic", False) else "normal"
    text_deco    = "underline" if theme_dict.get("header_underline", False) else "none"
    text_shadow  = "2px 2px 10px rgba(0,0,0,0.35)" if theme_dict.get("header_shadow", False) else "none"
    text_align   = theme_dict.get("header_align", "center")
    css = f"""<style>
        {import_tag}
        {bg_css}
        .kudo-card {{ --card-bg: {card_bg}; background: {card_bg}; }}
        .page-header {{ text-align: {text_align}; }}
        .page-header h1 {{
            color: {header_color};
            font-family: {font_stack};
            font-size: {font_size}rem;
            font-weight: {font_weight};
            font-style: {font_style};
            text-decoration: {text_deco};
            text-shadow: {text_shadow};
        }}
    </style>"""
    st.markdown(css, unsafe_allow_html=True)


def render_attribution_html(theme_dict: dict) -> str:
    preset = theme_dict.get("preset", "")
    if preset not in OCCASION_THEMES:
        return ""
    img_idx = int(theme_dict.get("image_index", 0))
    images = OCCASION_THEMES[preset]["images"]
    if img_idx >= len(images):
        return ""
    img_meta = images[img_idx]
    photographer = _escape(img_meta["photographer"])
    username = img_meta["username"]
    profile_url = _escape(f"https://unsplash.com/@{username}?{UTM}")
    photo_id = img_meta.get("photo_id")
    if photo_id:
        photo_url = _escape(f"https://unsplash.com/photos/{photo_id}?{UTM}")
        photo_link = f'<a href="{photo_url}" target="_blank" rel="noopener">Unsplash</a>'
    else:
        unsplash_url = _escape(f"https://unsplash.com/?{UTM}")
        photo_link = f'<a href="{unsplash_url}" target="_blank" rel="noopener">Unsplash</a>'
    return (
        f'<div class="attribution">Photo by '
        f'<a href="{profile_url}" target="_blank" rel="noopener">{photographer}</a>'
        f' on {photo_link}</div>'
    )


def _header_display_text(heading: str, theme_dict: dict) -> str:
    emoji = theme_dict.get("header_emoji", "").strip()
    text = _escape(heading) if heading else "Your heading here"
    return f"{emoji} {text} {emoji}".strip() if emoji else text


def render_header_preview_html(heading: str, theme_dict: dict) -> str:
    _, font_stack, font_size = _font_css(theme_dict)
    theme = get_theme(theme_dict)
    color        = theme_dict.get("header_color") or theme["accent"]
    font_weight  = "700" if theme_dict.get("header_bold", True) else "400"
    font_style   = "italic" if theme_dict.get("header_italic", False) else "normal"
    text_deco    = "underline" if theme_dict.get("header_underline", False) else "none"
    text_shadow  = "2px 2px 10px rgba(0,0,0,0.35)" if theme_dict.get("header_shadow", False) else "none"
    text_align   = theme_dict.get("header_align", "center")
    display_text = _header_display_text(heading, theme_dict)
    return (
        f'<div class="header-preview" style="text-align:{text_align};">'
        f'<span style="color:{color}; font-family:{font_stack}; font-size:{font_size}rem;'
        f' font-weight:{font_weight}; font-style:{font_style};'
        f' text-decoration:{text_deco}; text-shadow:{text_shadow};">'
        f'{display_text}</span></div>'
    )


def render_page_header_html(heading: str, theme_dict: dict = {}) -> str:
    display_text = _header_display_text(heading, theme_dict)
    return f'<div class="page-header"><h1>{display_text}</h1></div>'


def render_message_card_html(author: str, content_markdown: str, timestamp: str, image_url: str = "") -> str:
    content_html = md.markdown(content_markdown, extensions=["extra"], safe_mode="escape")
    safe_url = _safe_image_url(image_url) if image_url else ""
    image_html = f'<img class="card-image" src="{safe_url}" alt="" />' if safe_url else ""
    return (
        f'<div class="kudo-card">'
        f'{image_html}'
        f'<div class="card-body">'
        f'<div class="card-content">{content_html}</div>'
        f'<div class="card-footer">'
        f'<span class="timestamp">{_escape(timestamp)}</span>'
        f'<span class="author">— {_escape(author)}</span>'
        f'</div>'
        f'</div>'
        f'</div>'
    )




def _safe_image_url(url: str) -> str:
    stripped = url.strip()
    if stripped.lower().startswith(("http://", "https://")):
        return _escape(stripped)
    return ""


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
