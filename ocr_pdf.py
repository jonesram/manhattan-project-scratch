from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import sys


def pdf2text(pdf_filename):

    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[1]

    req_image = []
    final_text = []

    image_pdf = Image(filename=pdf_filename, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')

    for img in image_jpeg.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))

    for img in req_image:

      txt = tool.image_to_string(
          PI.open(io.BytesIO(img)),
          lang=lang,
          builder=pyocr.builders.TextBuilder()
      )

      final_text.append(txt)

    return final_text


if __name__ == "__main__":

    text = pdf2text(sys.argv[1])

    if len(sys.argv)==3:
        ofilename = sys.argv[2]
    else:
        ofilename = "ocrpdf_output.txt"

    with open(ofilename,'wb') as ofile:
        for chunk in text:
            ofile.write(chunk.encode('ascii', 'ignore'))
