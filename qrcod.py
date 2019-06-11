import qrcode
img = qrcode.make("0x6622274e7c2c76ecba5f0c516b7d0dbac365b411")
img.get_image().show()