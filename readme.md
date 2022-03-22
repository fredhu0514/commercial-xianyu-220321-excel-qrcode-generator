## I. Explanation of codes

### 1. Import Module

```python
# pyzbar is a decoding module
from pyzbar.pyzbar import decode
# input and output module
from io import StringIO
# python image processing module
from PIL import Image
# python data frame processing
import pandas as pd
# python QRcode generator code 
import qrcode
```
### 2. Comparing Dataframe Module

```python
# `df1` is the original (self) dataframe and `df2` is the target (other) dataframe.
# `filename` is the generation of the difference file
def _compare(df1, df2, filename):
  	# first assert if the shape of two files are the same, if not raise error
    assert(df1.shape == df2.shape)
    # pandas inside funtion of comparing two dataframes
    dif = df1.compare(df2)
    # dataframe that contains the difference export to an excel
    dif.to_excel(filename)
```

### 3. Excel to Image

```python
# `path` is the input path of the excel file.
# `fill_color` and `back_color` are the style of the QR code, default to black an white
def xlsx2img(path, fill_color="black", back_color="white"):
  	# read in the excel to dataframe
    df = pd.read_excel(path)
    # dataframe to string
    str_df = df.to_string()
    # parameters for QR code, no need to moify
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=0,
    )
    # add the data into the buffer of the qrcode
    qr.add_data(str_df)
    # See if the data exceeds the limit of a QR code
    try:
      	# make the qr code
        qr.make(fit=True)
        # turn the qr code into an image
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        # save the qr code
        img.save(path + ".png")
        # standard out the file path
        print("Successful! QRcode saved at " + path + ".png")
    # if file oversize 
    except qrcode.exceptions.DataOverflowError as e:
      	# warn the error
        print("Your file exceed the limit.")
```

### 4. Image to Excel

```python
# 'path' is the path of the image file
def img2xlsx(path):
  	# use the decode funtion in the `pyzbar` module
    data = decode(Image.open(path))
    # turn the decode information into utf-8 form
    str_df = data[0].data.decode("utf-8")
    # use standard io module to add comma separtion to the string dataframe and read it into the buffer
    df = pd.read_csv(StringIO(str_df), sep='\s+')
    # finally write the data into the excel
    df.to_excel(path + ".xlsx")
    # output the data frame
    return df
```

### 5. Compare the Image

```python
# 'img1' & 'img2' are two paths of the images of the excels
def compare_img(img1, img2):
  	# read the images respectively
    df1 = img2xlsx(img1)
    df2 = img2xlsx(img2)
    # generate the new file name
    filename = (img1 + img2 +".xlsx")
    # call the `_compare` and generate the excel given the filename
    _compare(df1, df2, filename)
    # return the file name
    return filename
```

## II. Usage of the code

### 1. How to start the code

* If `python` does not work, then try `python3`. Below is just an example:

```bash
$ python -i app.py
>>> xlsx2img("input_form.xlsx")
Successful! QRcode saved at input_form.xlsx.png
>>> img2xlsx("input_form.xlsx.png")
>>> compare_img("img1.png", "img2.png")
```

- `python -i app.py`, starts the shell of the script.
- `xlsx2img("input_form.xlsx")`, excel file to qrcode.
- `img2xlsx("input_form.xlsx.png")`, qrcode to excel file.
- `compare_img("img1.png", "img2.png")`, compare the two images and generate the difference excel file.

## III. Install Dependencies

```bash
$ pip3 install -r requirements.txt
```



