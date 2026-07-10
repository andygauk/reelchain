from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
img = Image.new("RGB", (W, H), (13, 15, 23))
d = ImageDraw.Draw(img)

try:
    f_black = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 96)
    f_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 34)
    f_tag = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
except Exception as e:
    f_black = f_sub = f_tag = ImageFont.load_default()

# Title: ReelChain
d.text((80, 150), "ReelChain", font=f_black, fill=(255, 77, 109))
# Subtitle
d.text((84, 280), "Connect two films through the actors they share.", font=f_sub, fill=(232, 234, 242))
# Tag
d.text((84, 540), "reelchain-dhk.pages.dev", font=f_tag, fill=(138, 144, 166))

# Decorative node chips (film -> actor -> film)
def chip(x, y, text, color, txt_fill):
    d.rounded_rectangle([x, y, x + 300, y + 70], radius=20, outline=color, width=3, fill=(27, 35, 51))
    d.text((x + 18, y + 20), text, font=f_sub, fill=txt_fill)

chip(480, 380, "\U0001F3AC Hugo", (91, 140, 255), (157, 184, 255))
chip(560, 470, "\U0001F464 DiCaprio", (255, 184, 77), (255, 206, 138))

img.save("deploy/og-image.png")
print("wrote deploy/og-image.png", img.size)
