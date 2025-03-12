from pdf2image import convert_from_bytes
import pytesseract


def extract_text(data: bytes) -> str:
    try:
        print("Starting OCR")
        ocr_data = ""
        images = convert_from_bytes(
            data, dpi=500, fmt="jpeg", thread_count=4, grayscale=True
        )
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            ocr_data = ocr_data + "\n\n" + text
        print("OCR completed")
        return ocr_data
    except Exception as e:
        print(e)
        raise e
