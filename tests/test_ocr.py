import unittest
from unittest.mock import patch, MagicMock
from ocr import extract_text

class TestOcrExtractText(unittest.TestCase):

    @patch('ocr.convert_from_bytes')
    @patch('ocr.pytesseract.image_to_string')
    @patch('ocr.pix3texModel')  # Mock the callable instance
    def test_successful_extraction_text_and_math(
        self, mock_pix3tex_model, mock_image_to_string, mock_convert_from_bytes
    ):
        # Configure mocks
        mock_image1 = MagicMock()
        mock_image2 = MagicMock()
        mock_convert_from_bytes.return_value = [mock_image1, mock_image2]
        
        mock_image_to_string.side_effect = ['Page 1 text', 'Page 2 text']
        mock_pix3tex_model.side_effect = ['math_expr_1', 'math_expr_2']

        # Call the function
        result = extract_text(b'dummy_pdf_data')

        # Assertions
        mock_convert_from_bytes.assert_called_once_with(
            b'dummy_pdf_data', dpi=500, fmt="jpeg", thread_count=4, grayscale=True
        )
        
        self.assertEqual(mock_image_to_string.call_count, 2)
        mock_image_to_string.assert_any_call(mock_image1, lang="eng+hin+deva")
        mock_image_to_string.assert_any_call(mock_image2, lang="eng+hin+deva")

        self.assertEqual(mock_pix3tex_model.call_count, 2)
        mock_pix3tex_model.assert_any_call(mock_image1)
        mock_pix3tex_model.assert_any_call(mock_image2)

        expected_text = "\n\nPage 1 text\n\nMaths expressions:math_expr_1\n\nPage 2 text\n\nMaths expressions:math_expr_2"
        self.assertEqual(result.strip(), expected_text.strip())

    @patch('ocr.convert_from_bytes')
    @patch('ocr.pytesseract.image_to_string')
    @patch('ocr.pix3texModel')
    @patch('builtins.print') # Mock print to check error messages
    def test_math_extraction_fails_gracefully(
        self, mock_print, mock_pix3tex_model, mock_image_to_string, mock_convert_from_bytes
    ):
        # Configure mocks
        mock_image1 = MagicMock()
        mock_image2 = MagicMock()
        mock_convert_from_bytes.return_value = [mock_image1, mock_image2]
        
        mock_image_to_string.side_effect = ['Page 1 text', 'Page 2 text']
        mock_pix3tex_model.side_effect = Exception("Pix2Tex Error")

        # Call the function
        result = extract_text(b'dummy_pdf_data')

        # Assertions
        mock_convert_from_bytes.assert_called_once_with(
            b'dummy_pdf_data', dpi=500, fmt="jpeg", thread_count=4, grayscale=True
        )
        
        self.assertEqual(mock_image_to_string.call_count, 2)
        mock_image_to_string.assert_any_call(mock_image1, lang="eng+hin+deva")
        mock_image_to_string.assert_any_call(mock_image2, lang="eng+hin+deva")

        self.assertEqual(mock_pix3tex_model.call_count, 2) # It's called for each image
        mock_pix3tex_model.assert_any_call(mock_image1)
        mock_pix3tex_model.assert_any_call(mock_image2)
        
        # Check if the error was printed
        mock_print.assert_any_call("Error during math extraction with pix2tex: Pix2Tex Error")

        expected_text = "\n\nPage 1 text\n\nPage 2 text" # No math expressions
        self.assertEqual(result.strip(), expected_text.strip())

    @patch('ocr.convert_from_bytes')
    @patch('ocr.pytesseract.image_to_string')
    @patch('ocr.pix3texModel')
    def test_no_images_from_pdf(
        self, mock_pix3tex_model, mock_image_to_string, mock_convert_from_bytes
    ):
        # Configure mocks
        mock_convert_from_bytes.return_value = [] # No images

        # Call the function
        result = extract_text(b'dummy_pdf_data')

        # Assertions
        mock_convert_from_bytes.assert_called_once_with(
            b'dummy_pdf_data', dpi=500, fmt="jpeg", thread_count=4, grayscale=True
        )
        
        mock_image_to_string.assert_not_called()
        mock_pix3tex_model.assert_not_called()

        self.assertEqual(result.strip(), "") # Expect empty string if no images

if __name__ == '__main__':
    unittest.main()
