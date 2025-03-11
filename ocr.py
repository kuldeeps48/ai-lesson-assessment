import os
from pdf2image import convert_from_bytes
import pytesseract
import cv2


def extract_text(data: bytes) -> str:
    try:
        print("Starting OCR")
        ocr_data = ""
        images = convert_from_bytes(data, dpi=500)
        for i, image in enumerate(images):
            fname = "image" + str(i) + ".jpeg"
            image.save(fname, format="jpeg")
            text = pytesseract.image_to_string(cv2.imread(fname))
            os.remove(fname)
            ocr_data = ocr_data + "\n\n" + text
        print("OCR completed")
        return ocr_data
    except Exception as e:
        print(e)
        raise e
