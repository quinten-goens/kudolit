import string
import random
import streamlit as st
from pocketbase import PocketBase


def generate_code(length: int = 10) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))


@st.cache_resource
def _get_client() -> PocketBase:
    url = st.secrets["POCKETBASE_URL"]
    client = PocketBase(url)
    client.collection("_superusers").auth_with_password(
        st.secrets["POCKETBASE_EMAIL"],
        st.secrets["POCKETBASE_PASSWORD"],
    )
    return client


def get_client() -> PocketBase:
    return _get_client()


def lookup_code(code: str):
    """Returns (role, page_record) or None."""
    client = get_client()
    code_escaped = code.replace('"', '\\"')
    try:
        result = client.collection("kudo_pages").get_list(
            1, 1,
            query_params={
                "filter": f'admin_code="{code_escaped}" || user_code="{code_escaped}" || viewer_code="{code_escaped}"'
            },
        )
    except Exception:
        return None
    if not result.items:
        return None
    page = result.items[0]
    if page.admin_code == code:
        return ("admin", page)
    elif page.user_code == code:
        return ("user", page)
    else:
        return ("viewer", page)


def get_all_pages():
    client = get_client()
    pages = []
    page_num = 1
    while True:
        result = client.collection("kudo_pages").get_list(
            page_num, 50, query_params={"sort": "-created"}
        )
        pages.extend(result.items)
        if page_num >= result.total_pages:
            break
        page_num += 1
    return pages


def create_page(heading: str, theme: dict) -> object:
    client = get_client()
    admin_code = generate_code()
    user_code = generate_code()
    viewer_code = generate_code()
    while user_code == admin_code:
        user_code = generate_code()
    while viewer_code in (admin_code, user_code):
        viewer_code = generate_code()

    record = client.collection("kudo_pages").create(
        {
            "heading": heading,
            "theme": theme,
            "admin_code": admin_code,
            "user_code": user_code,
            "viewer_code": viewer_code,
        }
    )
    return record


def update_page(page_id: str, data: dict) -> object:
    client = get_client()
    return client.collection("kudo_pages").update(page_id, data)


def delete_page(page_id: str):
    client = get_client()
    messages = get_messages(page_id)
    for msg in messages:
        client.collection("kudo_messages").delete(msg.id)
    client.collection("kudo_pages").delete(page_id)


def get_page(page_id: str):
    client = get_client()
    return client.collection("kudo_pages").get_one(page_id)


def get_messages(page_id: str):
    client = get_client()
    messages = []
    page_num = 1
    while True:
        result = client.collection("kudo_messages").get_list(
            page_num, 50,
            query_params={
                "filter": f'page="{page_id}"',
                "sort": "-created",
            },
        )
        messages.extend(result.items)
        if page_num >= result.total_pages:
            break
        page_num += 1
    return messages


def create_message(page_id: str, author_name: str, content: str, image_url: str = "", image_file=None):
    client = get_client()
    body = {
        "page": page_id,
        "author_name": author_name,
        "content": content,
        "image_url": image_url or "",
    }
    if image_file is not None:
        from pocketbase.client import FileUpload
        body["image_file"] = FileUpload(
            (image_file.name, image_file.read(), image_file.type)
        )
    return client.collection("kudo_messages").create(body)


def delete_message(msg_id: str):
    client = get_client()
    client.collection("kudo_messages").delete(msg_id)


def get_file_url(record, field_name: str) -> str:
    """Build the public URL for a file stored on a PocketBase record."""
    client = get_client()
    filename = getattr(record, field_name, "")
    if isinstance(filename, list):
        filename = filename[0] if filename else ""
    if not filename or not isinstance(filename, str):
        return ""
    return client.files.get_url(record, filename)
