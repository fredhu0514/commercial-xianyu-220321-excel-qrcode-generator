from pyzbar.pyzbar import decode
from io import StringIO
from PIL import Image
import pandas as pd
import qrcode


def _compare(df1, df2, filename):
    assert(df1.shape == df2.shape)
    dif = df1.compare(df2)
    dif.to_excel(filename)

def xlsx2img(path, fill_color="black", back_color="white"):
    df = pd.read_excel(path)
    str_df = df.to_string()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=0,
    )
    qr.add_data(str_df)
    try:
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(path + ".png")
        print("Successful! QRcode saved at " + path + ".png")
    except qrcode.exceptions.DataOverflowError as e:
        print("Your file exceed the limit.")

def img2xlsx(path):
    data = decode(Image.open(path))
    str_df = data[0].data.decode("utf-8")
    df = pd.read_csv(StringIO(str_df), sep='\s+')
    df.to_excel(path + ".xlsx")
    return df

def compare_img(img1, img2):
    df1 = img2xlsx(img1)
    df2 = img2xlsx(img2)
    filename = (img1 + img2 +".xlsx")
    _compare(df1, df2, filename)
    return filename
