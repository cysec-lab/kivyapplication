import hashlib
import qrcode

f = open('C:/Users/yuncong/Desktop/1234.txt','rb')

thehash = hashlib.sha256(f.read())

img = qrcode.make(thehash.hexdigest())
img.get_image().show()
print(thehash.hexdigest())