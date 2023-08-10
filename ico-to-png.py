from PIL import Image

img = Image.open(r'C:/Users/yungng07/Documents/qr-code-reader/icons/icon.ico')
img.save('icon.png', format='PNG', sizes=[(64,64)])
