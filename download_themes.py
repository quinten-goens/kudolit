"""
One-time script: downloads all theme background images from Unsplash
and saves them to static/themes/{theme}/{idx}.jpg.

Run once before launching the app:
    python download_themes.py
"""
import time
from pathlib import Path
import requests

# Each entry: cdn_id is the CDN path fragment (photo-XXX or premium_photo-XXX).
# Build download URL: images.unsplash.com/{cdn_id}  or  plus.unsplash.com/{cdn_id}
THEMES = {
    "birthday": [
        {"cdn_id": "premium_photo-1663839412026-51a44cfadfb8", "photographer": "Maryam Sicard",       "username": "maryamsicard"},
        {"cdn_id": "photo-1729870526122-0de9a7113dc6",          "photographer": "The Ordinary Moments","username": "cr029"},
        {"cdn_id": "photo-1530103862676-de8c9debad1d",          "photographer": "Adi Goldstein",       "username": "adigold1"},
        {"cdn_id": "photo-1502035618526-6b2f1f5bca1b",          "photographer": "Nikhita Singhal",     "username": "nikhita"},
        {"cdn_id": "premium_photo-1677221924410-0d27f4940396",  "photographer": "Anita Austvika",      "username": "anitaaustvika"},
        {"cdn_id": "photo-1558636508-e0db3814bd1d",             "photographer": "Nick Fewings",        "username": "jannerboy62"},
        {"cdn_id": "photo-1482731910308-31e96e5d1d28",          "photographer": "Sergei Solo",         "username": "solofox"},
        {"cdn_id": "photo-1527529482837-4698179dc6ce",          "photographer": "Al Elmes",            "username": "alelmes"},
        {"cdn_id": "premium_photo-1663839412165-0d60a57e7a91",  "photographer": "Maryam Sicard",       "username": "maryamsicard"},
        {"cdn_id": "photo-1610670444950-0b29430891b4",          "photographer": "Duncan Kidd",         "username": "we_the_royal"},
    ],
    "farewell": [
        {"cdn_id": "premium_photo-1756162033396-9d83be3fd4dd",  "photographer": "Clara Beatriz",       "username": "clarabeatriz"},
        {"cdn_id": "photo-1687773868626-6d6fc49dee4b",          "photographer": "Tolu Akinyemi",       "username": "poetolu"},
        {"cdn_id": "photo-1713934586938-e17292c35cee",          "photographer": "Anisa Gauri",         "username": "anisagauri"},
        {"cdn_id": "photo-1762117862909-34b0d164fb54",          "photographer": "Meizhi Lang",         "username": "meizhilang"},
        {"cdn_id": "premium_photo-1714393004905-a05fdc2a8102",  "photographer": "Ahmet Kurt",          "username": "ahmetkurt"},
        {"cdn_id": "photo-1497281559858-4ae63e694d04",          "photographer": "Matthew Henry",       "username": "matthewhenry"},
        {"cdn_id": "photo-1665949950478-2b5c8f9aed8d",          "photographer": "Eugene",              "username": "eugenegrunge"},
        {"cdn_id": "photo-1712997569565-1eaa7315dd89",          "photographer": "Neelakshi Singh",     "username": "neelakshi_singh_"},
        {"cdn_id": "premium_photo-1685693685482-c319b7868cb7",  "photographer": "Phạm Nhật",           "username": "ph4minhat"},
        {"cdn_id": "photo-1666999515309-6268df3e0d8a",          "photographer": "Stephanie Klepacki",  "username": "sklepacki"},
    ],
    "graduation": [
        {"cdn_id": "premium_photo-1713296255442-e9338f42aad8",  "photographer": "A. C.",               "username": "3tnik"},
        {"cdn_id": "photo-1623461487986-9400110de28e",          "photographer": "Albert Vincent Wu",   "username": "albertvincentwu"},
        {"cdn_id": "photo-1627556704302-624286467c65",          "photographer": "RUT MIIT",            "username": "rutmiit"},
        {"cdn_id": "photo-1590012314607-cda9d9b699ae",          "photographer": "Joshua Hoehne",       "username": "joshua_hoehne"},
        {"cdn_id": "premium_photo-1683749808307-e5597ac69f1e",  "photographer": "Katelyn Perry",       "username": "katelynperry"},
        {"cdn_id": "photo-1639765766830-d829d2fe4219",          "photographer": "Caleb Holden",        "username": "calebholden"},
        {"cdn_id": "photo-1541339907198-e08756dedf3f",          "photographer": "Pang Yuhao",          "username": "yuhao"},
        {"cdn_id": "photo-1627556704290-2b1f5853ff78",          "photographer": "RUT MIIT",            "username": "rutmiit"},
        {"cdn_id": "photo-1636231945376-3d40fdcbc462",          "photographer": "Dragos Blaga",        "username": "7dr_agos2"},
        {"cdn_id": "photo-1525921429624-479b6a26d84d",          "photographer": "Charles DeLoye",      "username": "charlesdeloye"},
    ],
    "retirement": [
        {"cdn_id": "premium_photo-1667511062439-71e8515fab38",  "photographer": "Getty Images",        "username": "gettyimages"},
        {"cdn_id": "photo-1473186578172-c141e6798cf4",          "photographer": "Aaron Burden",        "username": "aaronburden"},
        {"cdn_id": "photo-1533444273691-ebf51af8fd9c",          "photographer": "James Hose Jr",       "username": "jameshosejr"},
        {"cdn_id": "photo-1616964913831-5d22886c3392",          "photographer": "Marc Najera",         "username": "marcnajera"},
        {"cdn_id": "premium_photo-1675368994978-0c7c12d7d4bd",  "photographer": "Natalia Blauth",      "username": "nataliablauth"},
        {"cdn_id": "photo-1633158829875-e5316a358c6f",          "photographer": "Towfiqu barbhuiya",   "username": "towfiqu999999"},
        {"cdn_id": "photo-1473679408190-0693dd22fe6a",          "photographer": "Harli Marten",        "username": "harlimarten"},
        {"cdn_id": "photo-1576477987917-9d056d379228",          "photographer": "Anukrati Omar",       "username": "anuomar"},
        {"cdn_id": "premium_photo-1681881045620-2d64f37ca396",  "photographer": "Getty Images",        "username": "gettyimages"},
        {"cdn_id": "photo-1634474588707-de99f09285c0",          "photographer": "Towfiqu barbhuiya",   "username": "towfiqu999999"},
    ],
    "new_baby": [
        {"cdn_id": "premium_photo-1668613456796-44c07d99d10e",  "photographer": "Toa Heftiba",         "username": "heftiba"},
        {"cdn_id": "photo-1656707133318-03c23b0f85f5",          "photographer": "Imad Ud Khan",        "username": "_madu"},
        {"cdn_id": "photo-1618847472790-0ca60378235e",          "photographer": "Matthew Osborn",      "username": "matthewosborn"},
        {"cdn_id": "photo-1608043661120-421ed8794e1c",          "photographer": "PICSAR",              "username": "picsar_rovshan"},
        {"cdn_id": "premium_photo-1668613456805-6fd7db279ff0",  "photographer": "Toa Heftiba",         "username": "heftiba"},
        {"cdn_id": "photo-1761568879596-8c90ce63e668",          "photographer": "Md Ishak Raman",      "username": "mdishakrahman"},
        {"cdn_id": "photo-1517588487680-fc59cb1a55cf",          "photographer": "Kelly Sikkema",       "username": "kellysikkema"},
        {"cdn_id": "photo-1621937479002-d79b1dbf7ccf",          "photographer": "Bruno Kelzer",        "username": "bruno_kelzer"},
        {"cdn_id": "premium_photo-1675035675328-137d88c6c62c",  "photographer": "Fellipe Ditadi",      "username": "ditadi"},
        {"cdn_id": "photo-1621937479066-a7929e407438",          "photographer": "Bruno Kelzer",        "username": "bruno_kelzer"},
    ],
    "wedding": [
        {"cdn_id": "premium_photo-1675003662150-2569448d2b3b",  "photographer": "Karolina Grabowska",  "username": "kaboompics"},
        {"cdn_id": "photo-1532712938310-34cb3982ef74",          "photographer": "Foto Pettine",        "username": "fotopettine"},
        {"cdn_id": "photo-1520854221256-17451cc331bf",          "photographer": "Jeremy Wong Weddings","username": "jeremywongweddings"},
        {"cdn_id": "photo-1606800052052-a08af7148866",          "photographer": "Sandy Millar",        "username": "sandym10"},
        {"cdn_id": "premium_photo-1663076211121-36754a46de8d",  "photographer": "Getty Images",        "username": "gettyimages"},
        {"cdn_id": "photo-1583939003579-730e3918a45a",          "photographer": "Leonardo Miranda",    "username": "mirandanenee"},
        {"cdn_id": "photo-1519741497674-611481863552",          "photographer": "Nathan Dumlao",       "username": "nate_dumlao"},
        {"cdn_id": "photo-1523438885200-e635ba2c371e",          "photographer": "Jeremy Wong Weddings","username": "jeremywongweddings"},
        {"cdn_id": "premium_photo-1664530452596-e1c17e342876",  "photographer": "Jayson Hinrichsen",   "username": "jayson_hinrichsen"},
        {"cdn_id": "photo-1606216794074-735e91aa2c92",          "photographer": "Jakob Owens",         "username": "jakobowens1"},
    ],
    "get_well": [
        {"cdn_id": "premium_photo-1676068244542-8d4e24053b7a",  "photographer": "Frank Flores",        "username": "frankflores"},
        {"cdn_id": "photo-1769372742183-9495f9d1b303",          "photographer": "Anastasiya Badun",    "username": "badun"},
        {"cdn_id": "photo-1761156255022-baa3f8601895",          "photographer": "sina rezakhani",      "username": "artofsinn"},
        {"cdn_id": "photo-1773045446183-e0aa29488126",          "photographer": "Le Tia",              "username": "basinati"},
        {"cdn_id": "premium_photo-1753159114046-cb07dbc5ecc8",  "photographer": "Mariela Ferbo",       "username": "marielaferbo"},
        {"cdn_id": "photo-1759420319818-1a2c8684a584",          "photographer": "feey",                "username": "feeypflanzen"},
        {"cdn_id": "photo-1764323288536-e1c7c7318896",          "photographer": "Dzmitry Shepeleu",    "username": "_devslashnull_"},
        {"cdn_id": "photo-1759420303135-0224b8d9b798",          "photographer": "feey",                "username": "feeypflanzen"},
        {"cdn_id": "premium_photo-1676068244571-ae64144575c9",  "photographer": "Frank Flores",        "username": "frankflores"},
        {"cdn_id": "photo-1769738135759-027dd68f1e45",          "photographer": "Muhamad Izzul Isyraf","username": "lensarona"},
    ],
    "landscape": [
        {"cdn_id": "premium_photo-1668354804669-287b9d538ca1",  "photographer": "Kevin Oetiker",          "username": "kevinoetiker"},
        {"cdn_id": "photo-1626948688703-0136bc0a90da",          "photographer": "Milo Weiler",            "username": "miloweiler"},
        {"cdn_id": "photo-1560380104-fe43b50ffcbc",             "photographer": "Manuel Silva",           "username": "manuelsilva"},
        {"cdn_id": "photo-1594028355881-9942abbaa2af",          "photographer": "Joris Visser",           "username": "jorisvisser"},
        {"cdn_id": "premium_photo-1710267324565-a29302fc8b9f",  "photographer": "A Chosen Soul",          "username": "a_chosensoul"},
        {"cdn_id": "photo-1600257729950-13a634d32697",          "photographer": "Michael Michelovski",    "username": "vansolo"},
        {"cdn_id": "photo-1712330138676-60e86456c218",          "photographer": "Daniel A. Páscoa",       "username": "daniel_pascoa"},
        {"cdn_id": "photo-1598439473183-42c9301db5dc",          "photographer": "Michael Michelovski",    "username": "vansolo"},
        {"cdn_id": "premium_photo-1690917227107-54b8a7d77afa",  "photographer": "Joshua Earle",           "username": "joshuaearle"},
        {"cdn_id": "photo-1636893580433-5ac59809bb13",          "photographer": "Carlos I",               "username": "procrastinator"},
    ],
    "work_anniversary": [
        {"cdn_id": "photo-1758520144658-c87be518b87e",          "photographer": "Vitaly Gariev",       "username": "silverkblack"},
        {"cdn_id": "photo-1758520144661-73849bde0da1",          "photographer": "Vitaly Gariev",       "username": "silverkblack"},
        {"cdn_id": "photo-1758520144623-65998e96a7d8",          "photographer": "Vitaly Gariev",       "username": "silverkblack"},
        {"cdn_id": "photo-1758691737538-220c1902b1ca",          "photographer": "Vitaly Gariev",       "username": "silverkblack"},
        {"cdn_id": "photo-1758691737492-48e8fdd336f7",          "photographer": "Vitaly Gariev",       "username": "silverkblack"},
        {"cdn_id": "photo-1758691737584-a8f17fb34475",          "photographer": "Vitaly Gariev",       "username": "silverkblack"},
        {"cdn_id": "photo-1676277757297-bef06498ebb0",          "photographer": "Walls.io",            "username": "walls_io"},
        {"cdn_id": "photo-1758691737433-2269d5cdd910",          "photographer": "Vitaly Gariev",       "username": "silverkblack"},
        {"cdn_id": "photo-1758691737535-57edd2a11d73",          "photographer": "Vitaly Gariev",       "username": "silverkblack"},
        {"cdn_id": "photo-1758873268933-e0765262e58d",          "photographer": "Vitaly Gariev",       "username": "silverkblack"},
    ],
}

HEADERS = {"User-Agent": "KudoLit/1.0 (personal project; unsplash attribution included)"}


def cdn_url(cdn_id: str) -> str:
    if cdn_id.startswith("premium_photo-"):
        return f"https://plus.unsplash.com/{cdn_id}?w=1600&auto=format&fit=crop&q=80"
    return f"https://images.unsplash.com/{cdn_id}?w=1600&auto=format&fit=crop&q=80"


def download_all():
    Path("static/themes").mkdir(parents=True, exist_ok=True)
    total = sum(len(v) for v in THEMES.values())
    done = 0

    for theme_key, images in THEMES.items():
        theme_dir = Path(f"static/themes/{theme_key}")
        theme_dir.mkdir(exist_ok=True)

        for idx, img in enumerate(images):
            dest = theme_dir / f"{idx}.jpg"
            done += 1
            if dest.exists():
                print(f"[{done}/{total}] skip  {theme_key}/{idx}.jpg")
                continue

            url = cdn_url(img["cdn_id"])
            print(f"[{done}/{total}] fetch {theme_key}/{idx}.jpg  ({img['photographer']})")
            try:
                r = requests.get(url, stream=True, timeout=30, headers=HEADERS)
                r.raise_for_status()
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(8192):
                        f.write(chunk)
                print(f"         {dest.stat().st_size // 1024}KB")
                time.sleep(0.15)
            except Exception as e:
                print(f"         ERROR: {e}")

    print(f"\nDone. {sum(1 for _ in Path('static/themes').rglob('*.jpg'))} images in static/themes/")


if __name__ == "__main__":
    download_all()
