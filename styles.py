import markdown as md


PRESET_THEMES = {
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
}

GLOBAL_CSS = """
<style>
    .stApp > header { display: none; }
    .block-container { max-width: 900px; padding-top: 2rem; }

    .kudo-card {
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background: var(--card-bg, #ffffff);
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        border: 1px solid rgba(0,0,0,0.04);
    }
    .kudo-card .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    .kudo-card .author {
        font-weight: 600;
        font-size: 1rem;
        color: #333;
    }
    .kudo-card .timestamp {
        font-size: 0.8rem;
        color: #999;
    }
    .kudo-card .card-content {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #444;
    }
    .kudo-card .card-content p { margin: 0 0 0.5rem 0; }
    .kudo-card .card-content p:last-child { margin-bottom: 0; }
    .kudo-card .card-image {
        margin-top: 0.75rem;
        border-radius: 8px;
        max-width: 100%;
        max-height: 400px;
        object-fit: contain;
    }

    .page-header {
        text-align: center;
        padding: 2.5rem 1rem;
        border-radius: 16px;
        margin-bottom: 2rem;
    }
    .page-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }

    .code-entry-container {
        max-width: 440px;
        margin: 15vh auto 0 auto;
        text-align: center;
    }
    .code-entry-container h1 {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .code-entry-container p {
        color: #888;
        margin-bottom: 2rem;
    }

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
    .admin-code-box .label {
        font-weight: 600;
        color: #666;
        min-width: 60px;
    }
    .admin-code-box .code {
        color: #333;
        letter-spacing: 0.5px;
    }
</style>
"""


def inject_global_css():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def get_theme(theme_dict: dict) -> dict:
    preset = theme_dict.get("preset", "default")
    if preset == "custom":
        bg_color = theme_dict.get("bg_color", "#f8f4f0")
        return {
            "bg": bg_color,
            "card_bg": "#ffffff",
            "accent": "#e07c5a",
        }
    return PRESET_THEMES.get(preset, PRESET_THEMES["default"])


def inject_page_theme_css(theme_dict: dict):
    import streamlit as st
    theme = get_theme(theme_dict)
    bg = theme["bg"]
    card_bg = theme["card_bg"]
    accent = theme["accent"]
    css = f"""
    <style>
        .stApp {{ background: {bg}; }}
        .kudo-card {{ --card-bg: {card_bg}; background: {card_bg}; }}
        .page-header {{ background: rgba(255,255,255,0.5); backdrop-filter: blur(8px); }}
        .page-header h1 {{ color: {accent}; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_message_card_html(author: str, content_markdown: str, timestamp: str, image_url: str = "") -> str:
    content_html = md.markdown(content_markdown, extensions=["extra"])
    image_html = ""
    if image_url:
        image_html = f'<img class="card-image" src="{image_url}" alt="attached image" />'

    return f"""
    <div class="kudo-card">
        <div class="card-header">
            <span class="author">{_escape(author)}</span>
            <span class="timestamp">{_escape(timestamp)}</span>
        </div>
        <div class="card-content">{content_html}</div>
        {image_html}
    </div>
    """


def render_page_header_html(heading: str) -> str:
    return f"""
    <div class="page-header">
        <h1>{_escape(heading)}</h1>
    </div>
    """


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
