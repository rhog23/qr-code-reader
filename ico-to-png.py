from PIL import Image

img = Image.open(r"./icons/icon.ico")
img.save("icon.png", format="PNG", sizes=[(64, 64)])
