"""Regenerate the Open Graph share card (deploy/og-image.png, 1200x630).

This is the image every link scraper (Telegram, WhatsApp, iMessage, Slack,
Discord, Twitter) pulls from <meta property="og:image">. It MUST be on-brand:
the real ReelChain logo lockup + the canonical domain, no placeholder boxes.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG_TOP = (13, 15, 23)      # #0d0f17  (matches site)
BG_BOT = (20, 24, 38)      # subtle lift for depth
BRAND_TEAL = (88, 196, 220)
BRAND_PINK = (255, 77, 109)
BRAND_GOLD = (255, 196, 92)

# --- background: vertical gradient ---
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
for y in range(H):
    t = y / (H - 1)
    r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
    g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
    b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# --- brand logo lockup (reels + chain + REEL CHAIN + tagline), centered ---
logo = Image.open("deploy/logo.png").convert("RGBA")
maxw = 940
scale = maxw / logo.width
nw, nh = int(logo.width * scale), int(logo.height * scale)
logo = logo.resize((nw, nh), Image.LANCZOS)
lx = (W - nw) // 2
ly = (H - nh) // 2 - 30   # nudge up to leave room for the domain footer
img.paste(logo, (lx, ly), logo)

# --- footer: canonical domain (no placeholder boxes) ---
try:
    f_domain = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34)
except Exception:
    f_domain = ImageFont.load_default()

dom = "reelchain.app"
dw = d.textlength(dom, font=f_domain)
d.text(((W - int(dw)) // 2, H - 70), dom, font=f_domain, fill=BRAND_TEAL)

img.save("deploy/og-image.png", "PNG")
print("wrote deploy/og-image.png", img.size)
