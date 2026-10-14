#!/usr/bin/env python3
"""Static blog generator (Maharashtra regional food).

Usage:  python build.py [image_ext] [site_url]
Example: python build.py jpg https://seo-blog-xyz.vercel.app

- Writes index.html, blog/*.html, style.css, sitemap.xml, robots.txt
- Creates placeholder images/post-N.<ext> ONLY if that file doesn't exist yet,
  so your own photos are never overwritten.
"""
import os
import sys
from datetime import date
from html import escape

EXT = sys.argv[1].lstrip(".") if len(sys.argv) > 1 else "jpg"
SITE = (sys.argv[2] if len(sys.argv) > 2 else "https://YOUR-SITE.vercel.app").rstrip("/")
SITE_NAME = "Thali Trails"
TODAY = date.today().isoformat()

POSTS = [
    {
        "slug": "maharashtra-regional-cuisines-guide",
        "title": "Maharashtra's Regional Cuisines: A Food Map from Konkan to Vidarbha",
        "desc": "Explore Maharashtra's food regions: Konkan, Desh, Khandesh, Marathwada, Kolhapur and Vidarbha, and the signature dishes that define each one.",
        "sections": [
            ("One state, many kitchens", [
                "Maharashtra is often reduced to vada pav and puran poli, but the state has several distinct food cultures shaped by geography, climate and history. The coast cooks with coconut, kokum and fresh fish. The dry interior leans on jowar, groundnuts and fiery chutneys.",
                "Travel a few hours in any direction and the spice level, the staple grain and even the way a simple lentil is cooked will change."]),
            ("The main regions at a glance", [
                "Konkan and Malvan are known for seafood curries, sol kadhi and rice. Western Maharashtra, including Pune and Kolhapur, brings misal, bakarwadi and the famous red and white rassa. Khandesh, around Jalgaon, is loved for bharit, dal batti style dishes and strong black masala.",
                "Marathwada favors jowar bhakri, pithla and thecha. Vidarbha, including Nagpur, is home to Saoji and Varhadi cooking, which are bold, smoky and deeply spiced."]),
            ("How to use this guide", [
                "Each article in this blog zooms into one region or theme, with the dishes to look for and the flavors that make them special. Start with the region closest to your own roots, or the one you plan to visit next, and eat your way across the map."]),
        ],
    },
    {
        "slug": "saoji-food-nagpur",
        "title": "Saoji Food of Nagpur: The Fiery Cuisine Born in Vidarbha",
        "desc": "Discover Nagpur's Saoji cuisine: its spicy mutton and chicken gravies, the signature Saoji masala, and where this bold Vidarbha tradition comes from.",
        "sections": [
            ("What makes Saoji special", [
                "Saoji cuisine comes from the Saoji community of Nagpur and is known for intensely spiced non-vegetarian gravies. The depth comes from a dry masala made with many whole spices, ground and roasted together, rather than from cream or sugar.",
                "The result is a dark, oily, aromatic curry that is hot in the mouth but layered, with smoky and earthy notes."]),
            ("Dishes to try", [
                "Saoji mutton and Saoji chicken are the classic orders, served with roti or rice. Many Saoji eateries also offer a spicy mutton rassa on the side and simple accompaniments like onion and lemon to cut through the heat.",
                "A traditional Saoji plate is about the gravy first. Expect it to be fiery, so ask for the spice level if you are new to it."]),
            ("Eating Saoji in Nagpur", [
                "Nagpur has many small Saoji restaurants, and locals will usually point you to a family favorite. Go hungry, pair the meal with plain roti or steamed rice, and keep water or a cooling side nearby.",
                "If you cook at home, the key is the masala. Dry-roasting whole spices and grinding them fresh makes a big difference to the final flavor."]),
        ],
    },
    {
        "slug": "jalgaon-khandesh-food-varan-batti",
        "title": "Jalgaon and Khandesh Food: Varan Batti, Bharit and Black Masala",
        "desc": "A tour of Khandesh cooking around Jalgaon: varan batti, smoky vangyache bharit, shev bhaji, thecha and the bold kala masala behind them.",
        "sections": [
            ("The flavors of Khandesh", [
                "Khandesh, the region around Jalgaon, is known for rustic, spicy food built on local produce and strong masalas. The cooking is hearty and made to go with bhakri, roti and rice.",
                "Jalgaon is especially famous for its bharit, made from the large local brinjals roasted over fire until smoky, then cooked with onion, green chilli and groundnut oil."]),
            ("Varan batti and other signatures", [
                "Varan batti is a comforting pairing of dal, or varan, with baked wheat balls called batti, served with plenty of ghee. It is a cousin of the dal baati eaten across central and western India, adapted to Khandesh taste.",
                "Other dishes to look for include shev bhaji, a spicy gravy topped with crisp sev, and thecha, a coarse chilli and garlic chutney that wakes up any meal."]),
            ("The role of kala masala", [
                "Khandesh cooks rely on a dark, dry masala that gives gravies their color and heat. Bhakri, bharit, varan and a dab of thecha together make a classic Khandesh meal.",
                "If you visit Jalgaon, try the bharit at a local dhaba during winter, when brinjals are at their best."]),
        ],
    },
    {
        "slug": "kolhapuri-food-tambda-pandhra-rassa",
        "title": "Kolhapuri Food: Tambda Pandhra Rassa, Misal and Fiery Thecha",
        "desc": "Kolhapur is famous for its bold cooking. Learn about tambda and pandhra rassa, Kolhapuri misal, mutton thali and the spice behind them.",
        "sections": [
            ("Kolhapur's reputation for heat", [
                "Kolhapur is known across India for spicy food. The city's cooking uses dried red chillies, a signature Kolhapuri masala and generous amounts of oil to create gravies that are both hot and deeply flavorful.",
                "The spice is balanced by coconut, onion and aromatic whole spices, so the heat comes with depth."]),
            ("Tambda and pandhra rassa", [
                "Tambda rassa is the red, fiery mutton or chicken curry, and pandhra rassa is its white, milder counterpart made with a coconut and spice base. Locals often order both together to enjoy the contrast.",
                "Kolhapuri misal is another favorite, topped with a spicy usal, farsan and a layer of tarri, the hot oily gravy, and served with pav."]),
            ("Eating like a local", [
                "Order a full non-vegetarian thali if you can, and have it with bhakri or rice. Finish with a cooling glass of buttermilk or sol kadhi style drink to calm the heat.",
                "At home, adjust the chilli and add coconut or yogurt gradually to tone things down without losing flavor."]),
        ],
    },
    {
        "slug": "pune-food-misal-pav-bakarwadi",
        "title": "Pune Food Guide: Misal Pav, Bakarwadi, Shrikhand and More",
        "desc": "From Puneri misal pav to crisp bakarwadi and creamy shrikhand, explore the snacks, sweets and old-city eateries that define Pune's food culture.",
        "sections": [
            ("Misal pav, Pune style", [
                "Misal pav is a spicy sprouted-moth-bean curry topped with farsan, onion, lemon and coriander, served with pav and often a bowl of tarri. Pune has its own style, usually a bit more balanced than the extra-hot versions found elsewhere.",
                "Many people eat misal for breakfast, and some of the city's best-known misal shops open early and sell out by midday."]),
            ("Snacks and sweets Pune is known for", [
                "Bakarwadi, a crisp spiral snack with a sweet, spicy and tangy filling, is closely associated with Pune and is a popular gift to carry home. Sabudana khichdi, thalipeeth and batata vada are everyday favorites.",
                "For sweets, shrikhand, a thick strained yogurt dessert flavored with saffron and cardamom, is a classic, often served with puri."]),
            ("Old Pune eating habits", [
                "Pune's old-city eateries are known for strict timings, simple menus and fiercely loyal customers. Many have been serving the same dishes for decades.",
                "Plan your visit around opening hours, and be ready to queue for the most popular spots."]),
        ],
    },
    {
        "slug": "konkan-malvan-seafood-sol-kadhi",
        "title": "Konkan and Malvan Food: Fish Curry, Sol Kadhi and Kombdi Vade",
        "desc": "Discover coastal Maharashtra's cooking: Malvani fish curry, kombdi vade, sol kadhi, and the coconut and kokum flavors of the Konkan coast.",
        "sections": [
            ("Coastal flavors", [
                "The Konkan coast cooks with what the sea and the coconut grove provide: fresh fish, coconut, kokum, tamarind and rice. Malvan, in the south of the coast, is particularly known for its distinctive masala and seafood.",
                "Malvani food is spicy yet fresh, with coconut and a freshly ground masala at the heart of most dishes."]),
            ("Signature dishes", [
                "Malvani fish curry, usually made with a coconut-based masala, is eaten with steamed rice or bhakri. Kombdi vade pairs spicy chicken curry with puffed, deep-fried vade made from rice and other flours.",
                "Sol kadhi, a pink drink of coconut milk and kokum, is both a digestive and a cooling accompaniment to spicy seafood meals."]),
            ("Vegetarian Konkan too", [
                "The Konkan also has a rich vegetarian side, including ukadiche modak, steamed rice dumplings stuffed with coconut and jaggery, which are especially associated with Ganesh Chaturthi.",
                "If you travel there, eat at a small local restaurant where seafood is bought fresh each morning."]),
        ],
    },
    {
        "slug": "mumbai-street-food-vada-pav",
        "title": "Mumbai Street Food: Vada Pav, Pav Bhaji and Beyond",
        "desc": "A guide to Mumbai's street food classics: vada pav, pav bhaji, misal, bhel and kothimbir vadi, and what makes them part of daily city life.",
        "sections": [
            ("The city's everyday food", [
                "Mumbai's street food grew up around busy workers who needed something quick, filling and cheap. Vada pav, a spiced potato fritter in a soft bun with chutneys, became the city's most famous snack.",
                "It is eaten at any time of day and is often paired with fried green chillies."]),
            ("Classics to try", [
                "Pav bhaji, a buttery mashed-vegetable curry with toasted pav, is a staple of late-night stalls. Bhel puri, a mix of puffed rice, sev, chutneys and onion, is a beach and station favorite.",
                "Other local favorites include misal pav, kothimbir vadi and sandwiches grilled with chutney and vegetables."]),
            ("Street food tips", [
                "Choose busy stalls where food is cooked fresh in front of you, and carry water. Go during cooler hours and be adventurous with the chutneys, which carry much of the flavor."]),
        ],
    },
    {
        "slug": "marathwada-food-bhakri-zunka-thecha",
        "title": "Marathwada Food: Jowar Bhakri, Zunka, Pithla and Thecha",
        "desc": "Marathwada's cuisine is rustic and filling: jowar bhakri, zunka, pithla, thecha and Aurangabad's famous naan qalia are the dishes to know.",
        "sections": [
            ("A cuisine of the dry plains", [
                "Marathwada, in central Maharashtra, has a drier climate, so its cooking relies on hardy grains like jowar and bajra, pulses and groundnuts. The food is simple, filling and full of flavor.",
                "Meals traditionally center on bhakri, a flat unleavened bread, eaten with a vegetable, a chutney and sometimes curd or onion."]),
            ("Signature dishes", [
                "Zunka is a dry, spiced besan preparation, and pithla is its softer, gravy-like cousin. Both are classic partners for bhakri, and zunka bhakar has become a symbol of rural Maharashtrian food.",
                "Thecha, a coarse chutney of green chilli, garlic and groundnuts, adds heat to any meal."]),
            ("Aurangabad's Mughlai influence", [
                "The city of Aurangabad, also known as Chhatrapati Sambhajinagar, is known for naan qalia, a rich mutton curry served with soft naan. It reflects the region's historic Mughal and Deccan connections and shows that Marathwada's food is not only rustic but also royal."]),
        ],
    },
    {
        "slug": "varhadi-food-vidarbha-patodi",
        "title": "Varhadi Food of Vidarbha: Patodi Rassa, Kadhi and Wedding Feasts",
        "desc": "Varhadi cuisine from Vidarbha features patodi rassa, kadhi, spicy mutton and hearty thalis. Learn what makes this region's food so distinctive.",
        "sections": [
            ("What is Varhadi cooking", [
                "Varhadi, or Varhad, is the traditional name for much of Vidarbha, and the food of the region is known for its spice, its use of groundnut and sesame, and its generous use of dried coconut.",
                "It is closely related to Saoji cooking but also has a strong vegetarian tradition."]),
            ("Dishes that define the region", [
                "Patodi rassa is made from steamed gram flour cakes cooked in a spicy gravy, a satisfying vegetarian dish with plenty of flavor. Varhadi kadhi, vada, and spicy vegetable preparations like bharleli vangi round out the table.",
                "Non-vegetarian options such as Varhadi mutton are also popular, especially on festive occasions."]),
            ("A full Varhadi thali", [
                "A traditional meal includes rice or roti, dal, a vegetable, kadhi, chutney and something fried. Lunch is often followed by a sweet like shrikhand or puran poli.",
                "Visit Nagpur or Amravati to try authentic Varhadi dishes in family-run restaurants."]),
        ],
    },
    {
        "slug": "maharashtrian-sweets-festival-food",
        "title": "Maharashtrian Sweets and Festival Food: Puran Poli, Modak and Shrikhand",
        "desc": "From puran poli at Gudi Padwa to modak at Ganesh Chaturthi, discover the sweets and festival dishes that mark the Maharashtrian calendar.",
        "sections": [
            ("Food tied to festivals", [
                "In Maharashtra, many dishes are linked to particular festivals. Ukadiche modak are the offering of Ganesh Chaturthi. Puran poli, a flatbread stuffed with sweet chana dal and jaggery, is prepared for Holi and many other celebrations.",
                "Til gul, made from sesame and jaggery, marks Makar Sankranti with the saying to speak sweet words."]),
            ("Everyday sweets", [
                "Shrikhand, basundi, shankarpali and anarsa show up at weddings and family gatherings. Each has its own technique, from slowly reducing milk for basundi to fermenting rice flour for anarsa.",
                "Many of these recipes are passed down through families and still made at home."]),
            ("Bringing them home", [
                "If you want to try making them, start with simple recipes like shankarpali or shrikhand. Use good ghee and fresh ingredients, and give the dough or yogurt the time it needs.",
                "Sweet dishes are also a good way to introduce friends to Maharashtrian food."]),
        ],
    },
]

CSS = """\
:root{--bg:#0d1117;--card:#161b22;--border:#262c36;--text:#e6edf3;--muted:#9aa4b2;--accent:#ffb454;--accent2:#ff7a59}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font:17px/1.7 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%;height:auto;display:block}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
header.site{border-bottom:1px solid var(--border);background:#0d1117ee;position:sticky;top:0;backdrop-filter:blur(8px);z-index:10}
header.site .wrap{display:flex;align-items:center;justify-content:space-between;height:60px}
.brand{font-weight:800;font-size:1.15rem;color:var(--text)}
.brand span{color:var(--accent)}
nav a{margin-left:18px;color:var(--muted);font-size:.95rem}
.hero{padding:64px 0 32px}
.hero h1{font-size:clamp(2rem,5vw,3.2rem);line-height:1.15;margin:0 0 12px}
.hero p{color:var(--muted);max-width:640px;margin:0;font-size:1.1rem}
.grid{display:grid;gap:22px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));padding:24px 0 64px}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden;transition:transform .15s,border-color .15s}
.card:hover{transform:translateY(-3px);border-color:var(--accent)}
.card a{color:inherit;text-decoration:none;display:block;height:100%}
.card img{aspect-ratio:1200/630;object-fit:cover;width:100%}
.card .body{padding:16px 18px 20px}
.card h2{font-size:1.1rem;line-height:1.35;margin:0 0 8px}
.card p{margin:0;color:var(--muted);font-size:.93rem;line-height:1.55}
article{max-width:760px;margin:0 auto;padding:40px 20px 64px}
article .crumbs{font-size:.9rem;color:var(--muted)}
article h1{font-size:clamp(1.8rem,4.5vw,2.6rem);line-height:1.2;margin:10px 0 8px}
article .meta{color:var(--muted);font-size:.9rem;margin-bottom:24px}
article .featured{border-radius:12px;margin-bottom:28px;border:1px solid var(--border);width:100%}
article h2{margin-top:36px;font-size:1.45rem;color:var(--accent2)}
article p{color:#d0d7de}
.related{border-top:1px solid var(--border);margin-top:48px;padding-top:24px}
.related h3{margin:0 0 10px}
.related ul{padding-left:20px;margin:0}
footer.site{border-top:1px solid var(--border);padding:28px 0;color:var(--muted);text-align:center;font-size:.9rem}
@media(max-width:600px){body{font-size:16px}nav a{margin-left:12px}.hero{padding:40px 0 16px}}
"""


def header():
    return (f'<header class="site"><div class="wrap"><a class="brand" href="/">Thali <span>Trails</span></a>'
            f'<nav><a href="/">Home</a><a href="/#posts">Articles</a></nav></div></header>')


def footer():
    return f'<footer class="site"><div class="wrap">&copy; {date.today().year} {SITE_NAME}. Maharashtra food guides.</div></footer>'


def head(title, desc, canonical, image, og_type="website"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc, quote=True)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(desc, quote=True)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/style.css">
</head>
<body>
"""


def write(path, text):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def make_placeholder(n, title, path):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed; skipping placeholder", path)
        return
    w, h = 1200, 630
    palettes = [("#3b0d0d", "#b23a1e"), ("#2a0f0f", "#8a2a1a"), ("#3a1f0a", "#c77d1a"),
                ("#2d1b0e", "#a0522d"), ("#3b0a1f", "#c2410c"), ("#1f2a0f", "#b7791f"),
                ("#0f2a2e", "#2a8a7a"), ("#3a150a", "#d9622b"), ("#2a1a0a", "#9c6b1e"),
                ("#3b1212", "#c9532d")]
    c1, c2 = palettes[(n - 1) % len(palettes)]
    img = Image.new("RGB", (w, h), c1)
    top = tuple(int(c1[i:i + 2], 16) for i in (1, 3, 5))
    bot = tuple(int(c2[i:i + 2], 16) for i in (1, 3, 5))
    px = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        px.line([(0, y), (w, y)], fill=tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3)))

    def font(size):
        for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                  "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans-Bold.ttf"):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
        return ImageFont.load_default()

    px.text((70, 40), f"{n:02d}", font=font(150), fill=(255, 255, 255, 60))
    words, lines, cur = title.split(), [], ""
    f = font(58)
    for wd in words:
        test = (cur + " " + wd).strip()
        if px.textlength(test, font=f) > w - 140:
            lines.append(cur)
            cur = wd
        else:
            cur = test
    lines.append(cur)
    y = h - 70 - 70 * len(lines)
    for ln in lines:
        px.text((70, y), ln, font=f, fill="white")
        y += 70
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fmt = "PNG" if path.lower().endswith("png") else "JPEG"
    img.save(path, fmt, quality=82, optimize=True)


def main():
    write("style.css", CSS)

    # Images (placeholders only when missing)
    for i, p in enumerate(POSTS, 1):
        img_path = f"images/post-{i}.{EXT}"
        if not os.path.exists(img_path):
            make_placeholder(i, p["title"], img_path)

    # Post pages
    for i, p in enumerate(POSTS, 1):
        url = f"{SITE}/blog/{p['slug']}.html"
        img_url = f"{SITE}/images/post-{i}.{EXT}"
        body = []
        for h2, paras in p["sections"]:
            body.append(f"<h2>{escape(h2)}</h2>")
            body.extend(f"<p>{escape(t)}</p>" for t in paras)
        others = [q for j, q in enumerate(POSTS, 1) if j != i]
        rel = [others[(i + k) % len(others)] for k in range(3)]
        rel_html = "".join(f'<li><a href="/blog/{q["slug"]}.html">{escape(q["title"])}</a></li>' for q in rel)
        html = head(f"{p['title']} | {SITE_NAME}", p["desc"], url, img_url, "article")
        html += header()
        html += f"""<article>
<div class="crumbs"><a href="/">Home</a> / Articles</div>
<h1>{escape(p['title'])}</h1>
<div class="meta">Published {TODAY} &middot; {SITE_NAME}</div>
<img class="featured" src="/images/post-{i}.{EXT}" alt="{escape(p['title'], quote=True)}" width="1200" height="630">
{''.join(body)}
<div class="related"><h3>Keep reading</h3><ul>{rel_html}</ul></div>
</article>
"""
        html += footer() + "\n</body>\n</html>\n"
        write(f"blog/{p['slug']}.html", html)

    # Homepage
    cards = []
    for i, p in enumerate(POSTS, 1):
        cards.append(f"""<div class="card"><a href="/blog/{p['slug']}.html">
<img src="/images/post-{i}.{EXT}" alt="{escape(p['title'], quote=True)}" width="1200" height="630" {'loading="lazy"' if i > 3 else ''}>
<div class="body"><h2>{escape(p['title'])}</h2><p>{escape(p['desc'])}</p></div></a></div>""")
    home_title = f"{SITE_NAME} | Maharashtra Regional Food Guides"
    home_desc = "Explore Maharashtra's regional cuisines: Saoji from Nagpur, varan batti from Jalgaon, Kolhapuri rassa, Malvani seafood, misal pav and more."
    html = head(home_title, home_desc, f"{SITE}/", f"{SITE}/images/post-1.{EXT}")
    html += header()
    html += f"""<main class="wrap">
<section class="hero"><h1>Maharashtra on a plate, region by region.</h1>
<p>Ten guides to the dishes, flavors and food traditions of Nagpur, Jalgaon, Kolhapur, Pune, Konkan and beyond.</p></section>
<section id="posts" class="grid">
{chr(10).join(cards)}
</section>
</main>
"""
    html += footer() + "\n</body>\n</html>\n"
    write("index.html", html)

    # Sitemap + robots
    urls = [f"{SITE}/"] + [f"{SITE}/blog/{p['slug']}.html" for p in POSTS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

    print(f"Built {len(POSTS)} posts for {SITE} (images: .{EXT})")


if __name__ == "__main__":
    main()
