from PIL import Image, ImageDraw
import sys

SRC = "C:/Users/andyg/AppData/Local/hermes/cache/images/img_0ecbd61dc936.jpg"
im = Image.open(SRC).convert("RGBA")
w, h = im.size

# 1) Flood-fill the dark background from all four corners -> transparent.
#    Tolerance covers the near-black charcoal (#030409-ish) without eating
#    the dark parts of the artwork (reels/silhouettes are lighter/coloured).
def bg_to_alpha(img, tol=42):
    img = img.copy()
    px = img.load()
    W, H = img.size
    for corner in [(1,1),(W-2,1),(1,H-2),(W-2,H-2)]:
        ImageDraw.floodfill(img, corner, (0,0,0,0), thresh=tol)
    return img

flooded = bg_to_alpha(im)

# 2) Autocrop to the non-transparent bounding box (tight logo lockup)
alpha = flooded.split()[3]
bbox = alpha.getbbox()
trim = flooded.crop(bbox) if bbox else flooded
# small transparent padding
pad = 12
canvas = Image.new("RGBA", (trim.width+pad*2, trim.height+pad*2), (0,0,0,0))
canvas.paste(trim, (pad,pad), trim)
canvas.save("deploy/logo.png")
print("logo.png", canvas.size)

# 3) Favicon: square, transparent bg, from the trimmed lockup (top graphic-heavy);
#    just scale the full lockup into a padded square.
side = max(canvas.width, canvas.height)
sq = Image.new("RGBA", (side, side), (0,0,0,0))
sq.paste(canvas, ((side-canvas.width)//2, (side-canvas.height)//2), canvas)
sq.resize((256,256), Image.LANCZOS).save("deploy/favicon.png")
# also a .ico for classic favicon support
sq.resize((64,64), Image.LANCZOS).save("deploy/favicon.ico")
print("favicon.png / favicon.ico written")

# 4) OG image 1200x630 on game bg, logo centered
OGW, OGH = 1200, 630
og = Image.new("RGBA", (OGW, OGH), (13,15,23,255))  # #0d0f17
# scale trimmed lockup to fit ~86% height
scale = (OGH*0.86)/canvas.height
nw, nh = int(canvas.width*scale), int(canvas.height*scale)
logo_big = canvas.resize((nw,nh), Image.LANCZOS)
og.alpha_composite(logo_big, ((OGW-nw)//2, (OGH-nh)//2))
og.convert("RGB").save("deploy/og-image.png", quality=92)
print("og-image.png", (OGW,OGH))
