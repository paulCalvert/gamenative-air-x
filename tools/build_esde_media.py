"""Stage missing ES-DE media for GameNative games from Steam's public store data.

Fills covers (library_600x900), screenshots, fanart (library_hero), marquees (logo.png),
videos (the store trailer's legacy movie480.mp4) and composes a miximage
(screenshot + cover + logo) for any game that lacks one.

Setup in <workdir>:
  device_media.txt  one line per media file already on the device, as
                    <system>/<type>/<rom basename>.<ext>   e.g. steam/covers/Mago.png
                    (from: adb shell "cd <ES-DE>/downloaded_media && find . -type f" with ./ stripped)
  devcopy/          optional: existing device covers/screenshots/marquees, same layout,
                    so miximages can reuse them
Edit GAMES below: (ES-DE system, ROM file basename, Steam app id).
Output: <workdir>/stage/downloaded_media/... -> push into ES-DE/downloaded_media/ with ES-DE closed.
Also writes meta.json (description, developer, publisher, genre, release date) for gamelist.xml.

Usage: python -I build_esde_media.py <workdir>
Media downloaded this way is for personal use on your own device; don't redistribute it.
"""
import json, os, sys, time, html, io, urllib.request, urllib.error
from PIL import Image, ImageDraw, ImageFilter

W = sys.argv[1]
STAGE = os.path.join(W, 'stage', 'downloaded_media')
API = os.path.join(W, 'api')
os.makedirs(API, exist_ok=True)

GAMES = [  # (system, rom basename, steam appid)
    ('steam', 'Bad North_ Jotunn Edition', 688420),
    ('steam', 'Bot Vice', 491040),
    ('steam', 'CARRION', 953490),
    ('steam', 'Cast n Chill', 3483740),
    ('steam', 'Gravity Circuit', 858710),
    ('steam', 'Hollow Knight', 367520),
    ('steam', 'Kingdom New Lands', 496300),
    ('steam', 'Mago', 1098280),
    ('steam', 'Megabonk', 3405340),
    ('steam', 'Retro City Rampage™ DX', 204630),
    ('steam', 'STAR WARS™ Jedi Knight_ Dark Forces II', 32380),
    ('steam', 'Shovel Knight_ Treasure Trove', 250760),
    ('steam', 'Sine Mora EX', 606730),
    ('steam', 'Spidersaurs', 1191620),
    ('steam', 'SteamWorld Dig', 252410),
    ('steam', 'Swords & Bones', 1534700),
    ('steam', 'Wizordum', 1715590),
    ('epic', 'Cave Story+', 200900),
]
UA = {'User-Agent': 'Mozilla/5.0'}

existing = set()
for line in open(os.path.join(W, 'device_media.txt'), encoding='utf-8-sig'):
    line = line.strip()
    if line:
        p = line.split('/')
        existing.add((p[0], p[1], os.path.splitext('/'.join(p[2:]))[0]))

def have(sysname, typ, name):
    return (sysname, typ, name) in existing or os.path.exists(target(sysname, typ, name, '.png')) or os.path.exists(target(sysname, typ, name, '.jpg')) or os.path.exists(target(sysname, typ, name, '.mp4'))

def target(sysname, typ, name, ext):
    return os.path.join(STAGE, sysname, typ, name + ext)

def get(url, tries=2):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404, 403):
                return None
            time.sleep(2)
        except Exception:
            time.sleep(2)
    return None

def appdetails(appid):
    f = os.path.join(API, f'{appid}.json')
    if not os.path.exists(f):
        b = get(f'https://store.steampowered.com/api/appdetails?appids={appid}&l=english&cc=US')
        open(f, 'wb').write(b or b'{}')
        time.sleep(1.5)
    j = json.load(open(f, encoding='utf-8'))
    d = j.get(str(appid), {})
    return d.get('data') if d.get('success') else None

def asset(appid, d, fname):
    bases = []
    hi = (d or {}).get('header_image', '')
    if hi:
        bases.append(hi.split('header.jpg')[0])
    bases += [f'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/',
              f'https://cdn.akamai.steamstatic.com/steam/apps/{appid}/']
    for b in bases:
        data = get(b + fname)
        if data and len(data) > 2000:
            try:
                Image.open(io.BytesIO(data)).verify()
                return data
            except Exception:
                pass
    return None

def save(sysname, typ, name, ext, data):
    p = target(sysname, typ, name, ext)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'wb').write(data)
    return p

def local_or_device_img(sysname, typ, name):
    for ext in ('.png', '.jpg'):
        p = target(sysname, typ, name, ext)
        if os.path.exists(p):
            return Image.open(p).convert('RGBA')
    p = os.path.join(W, 'devcopy', sysname, typ, name)
    for ext in ('.png', '.jpg'):
        if os.path.exists(p + ext):
            return Image.open(p + ext).convert('RGBA')
    return None

def fit(img, bw, bh):
    r = min(bw / img.width, bh / img.height)
    return img.resize((max(1, int(img.width * r)), max(1, int(img.height * r))), Image.LANCZOS)

def miximage(shot, cover, logo):
    canvas = Image.new('RGBA', (1280, 960), (0, 0, 0, 0))
    # screenshot frame (approximating ES-DE's default miximage)
    fx, fy, fw, fh = 140, 70, 1085, 820
    shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((fx + 6, fy + 8, fx + fw + 6, fy + fh + 8), 14, fill=(0, 0, 0, 170))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(canvas).rounded_rectangle((fx, fy, fx + fw, fy + fh), 14, fill=(40, 120, 160, 255))
    sw, sh = fw - 20, fh - 20
    s = shot.copy()
    tr = sw / sh
    if s.width / s.height > tr:  # crop sides to fill
        nw = int(s.height * tr); s = s.crop(((s.width - nw) // 2, 0, (s.width - nw) // 2 + nw, s.height))
    else:
        nh = int(s.width / tr); s = s.crop((0, (s.height - nh) // 2, s.width, (s.height - nh) // 2 + nh))
    canvas.alpha_composite(s.resize((sw, sh), Image.LANCZOS), (fx + 10, fy + 10))
    if cover is not None:
        c = fit(cover, 400, 610)
        canvas.alpha_composite(c, (0, 960 - c.height - 30))
    if logo is not None:
        l = fit(logo, 700, 150)
        canvas.alpha_composite(l, (1280 - l.width - 20, 0))
    return canvas

meta = {}
report = []
for sysname, name, appid in GAMES:
    d = appdetails(appid)
    got = []
    if not d:
        report.append(f'{name}: NO STEAM DATA'); continue
    meta[(sysname, name)] = {
        'desc': html.unescape(d.get('short_description', '')).strip(),
        'developer': ', '.join(d.get('developers', []) or []),
        'publisher': ', '.join(d.get('publishers', []) or []),
        'genre': ', '.join(g['description'] for g in d.get('genres', []) or []),
        'date': (d.get('release_date') or {}).get('date', ''),
    }
    shots = [s['path_full'] for s in d.get('screenshots', []) or []]
    if not have(sysname, 'covers', name):
        b = asset(appid, d, 'library_600x900_2x.jpg') or asset(appid, d, 'library_600x900.jpg')
        if b: save(sysname, 'covers', name, '.jpg', b); got.append('cover')
    if not have(sysname, 'screenshots', name) and shots:
        b = get(shots[0])
        if b: save(sysname, 'screenshots', name, '.jpg', b); got.append('screenshot')
    if not have(sysname, 'fanart', name):
        b = asset(appid, d, 'library_hero.jpg') or (get(shots[1]) if len(shots) > 1 else None)
        if b: save(sysname, 'fanart', name, '.jpg', b); got.append('fanart')
    if not have(sysname, 'marquees', name):
        b = asset(appid, d, 'logo.png')
        if b: save(sysname, 'marquees', name, '.png', b); got.append('marquee')
    if not have(sysname, 'videos', name):
        movies = d.get('movies', []) or []
        movies.sort(key=lambda m: not m.get('highlight'))
        for m in movies:
            b = get(f"https://cdn.akamai.steamstatic.com/steam/apps/{m['id']}/movie480.mp4")
            if b and b[4:8] == b'ftyp':
                save(sysname, 'videos', name, '.mp4', b); got.append(f"video({m.get('name')}, {len(b)//1048576} MB)"); break
    if not have(sysname, 'miximages', name):
        shot = local_or_device_img(sysname, 'screenshots', name)
        if shot is not None:
            mi = miximage(shot, local_or_device_img(sysname, 'covers', name), local_or_device_img(sysname, 'marquees', name))
            p = target(sysname, 'miximages', name, '.png'); os.makedirs(os.path.dirname(p), exist_ok=True)
            mi.save(p, optimize=True); got.append('miximage')
    report.append(f"{name}: {', '.join(got) if got else 'nothing missing'}")

json.dump({f'{k[0]}|{k[1]}': v for k, v in meta.items()}, open(os.path.join(W, 'meta.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n'.join(report))
