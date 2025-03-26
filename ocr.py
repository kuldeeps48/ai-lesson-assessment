from munch import Munch
from pdf2image import convert_from_bytes
from pix2tex.cli import LatexOCR
import pytesseract

pix3texModel = LatexOCR(
    Munch(
        {
            "config": "settings/config.yaml",
            "checkpoint": "checkpoints/weights.pth",
            "no_cuda": True,
            "no_resize": True,
        }
    )
)


def extract_text(data: bytes) -> str:
    try:
        print("Starting OCR")
        ocr_data = ""
        images = convert_from_bytes(
            data, dpi=500, fmt="jpeg", thread_count=4, grayscale=True
        )
        for i, image in enumerate(images):
            if not image:
                continue
            text = pytesseract.image_to_string(image, lang="eng+hin+deva")
            # maths = pix3texModel(image)
            # if maths and len(maths) > 0:
            #     text += "\n\nMaths expressions:" + maths

            ocr_data = ocr_data + "\n\n" + text
        print("OCR completed")
        return ocr_data
    except Exception as e:
        print(e)
        raise e
