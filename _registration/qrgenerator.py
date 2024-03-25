import qrcode
import gspread
import sys
import os
from PIL import Image

link = "https://docs.google.com/spreadsheets/d/1YkTPcmD_jJMCJ6FtgV7owGlv2Hc9sw4ucKnkhXugG_k/edit?usp=share_link"

if __name__ == "__main__":
    data = sys.argv[1]
    def create_qr_code(data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="#FF77FF", back_color="white")
        img = img.convert("RGBA")

        # Make the white background transparent
        pixdata = img.load()
        width, height = img.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (255, 255, 255, 0)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        qr_code_file = os.path.join(script_dir, "qrcode.png")
        img.save(qr_code_file)

    # Example usage
    create_qr_code(data)

    # Load background image
    # background = Image.open("fuchsia2.jpg")

    # # Paste the QR code image on top of the background image
    # img = Image.open("qr_code.png")
    # img = img.convert("RGBA")
    # background.paste(img, (175, 100), img)

    # # # Save the final image
    # background.save("/home/fouzanasif/mysite/qr_code2.png")
