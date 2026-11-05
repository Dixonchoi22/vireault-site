# Generates public/images/download-qr.svg.
# SWAP SPOT: when the Play listing is public, set QR_TARGET to
#   https://play.google.com/store/apps/details?id=com.vireault.app
# and re-run: python3 scripts/make-qr.py
import qrcode, qrcode.image.svg
QR_TARGET = "https://dixonchoi22.github.io/vireault-site/"
img = qrcode.make(QR_TARGET, image_factory=qrcode.image.svg.SvgPathImage, border=1)
img.save("public/images/download-qr.svg")
