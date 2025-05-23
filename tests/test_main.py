import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, UploadFile
from fastapi.testclient import TestClient
from io import BytesIO
import pytest # For pytest.raises, if preferred for ValueError testing, or use self.assertRaises

# Import what's needed from main.py
from main import app, _validate_file_size

class TestMainValidationUtils(unittest.TestCase):

    def test_validate_file_size_valid(self):
        """Test _validate_file_size with a file size within the limit."""
        try:
            _validate_file_size(b'a' * 500_000)  # 0.5 MB
        except ValueError:
            self.fail("_validate_file_size raised ValueError unexpectedly for valid size.")

    def test_validate_file_size_exceeds_limit(self):
        """Test _validate_file_size with a file size exceeding the limit."""
        with self.assertRaises(ValueError) as context:
            _validate_file_size(b'a' * 1_000_001)  # Just over 1 MB
        self.assertEqual(str(context.exception), "File size exceeds 1MB limit.")


class TestMainAPIFileValidation(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_generate_assessment_non_pdf_file(self):
        """Test /generate-assessment with a non-PDF file type."""
        response = self.client.post(
            "/generate-assessment",
            files={'file': ('test.png', BytesIO(b'fake png data'), 'image/png')}
        )
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.json()['detail'], "Unsupported file type. Only PDF files are allowed.")

    def test_check_answer_non_pdf_file(self):
        """Test /check-answer with a non-PDF file type."""
        response = self.client.post(
            "/check-answer",
            data={'question_with_choices': 'Q1?', 'correct_answer': 'A1'},
            files={'file': ('test.txt', BytesIO(b'fake text data'), 'text/plain')}
        )
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.json()['detail'], "Unsupported file type. Only PDF files are allowed.")

    @patch('main.extract_text')
    @patch('main.get_assessment_response')
    def test_generate_assessment_pdf_file_mocks_services(
        self, mock_get_assessment_response, mock_extract_text
    ):
        """Test /generate-assessment with a PDF file, mocking underlying services."""
        mock_extract_text.return_value = "dummy extracted text"
        
        # Mock for StreamingResponse, needs to be an iterable/generator
        async def mock_stream_response_gen(*args, **kwargs):
            yield "dummy "
            yield "response"
        mock_get_assessment_response.return_value = mock_stream_response_gen()

        response = self.client.post(
            "/generate-assessment",
            files={'file': ('lesson.pdf', BytesIO(b'fake pdf data' * 100), 'application/pdf')} # Ensure some data
        )
        
        self.assertEqual(response.status_code, 200)
        # For streaming response, you might want to check content or parts of it
        # For simplicity, we'll just check if the mocks were called
        # response_content = b"".join([chunk for chunk in response.iter_bytes()]) # consume the stream
        # self.assertEqual(response_content, b"dummy response")
        
        mock_extract_text.assert_called_once()
        # Ensure the argument to extract_text was the file data
        self.assertEqual(mock_extract_text.call_args[0][0], b'fake pdf data' * 100)
        
        mock_get_assessment_response.assert_called_once_with(lesson_text="dummy extracted text")


    @patch('main.extract_text')
    @patch('main.check_question_answer')
    def test_check_answer_pdf_file_mocks_services(
        self, mock_check_question_answer, mock_extract_text
    ):
        """Test /check-answer with a PDF file, mocking underlying services."""
        mock_extract_text.return_value = "dummy extracted text from lesson"
        
        async def mock_stream_response_gen(*args, **kwargs):
            yield "dummy "
            yield "check answer response"
        mock_check_question_answer.return_value = mock_stream_response_gen()

        question_data = "Q: What is 1+1? A) 1 B) 2 C) 3 D) 4"
        correct_answer_data = "B) 2"

        response = self.client.post(
            "/check-answer",
            data={'question_with_choices': question_data, 'correct_answer': correct_answer_data},
            files={'file': ('lesson_for_answer.pdf', BytesIO(b'pdf data for answer check' * 50), 'application/pdf')}
        )

        self.assertEqual(response.status_code, 200)
        
        mock_extract_text.assert_called_once()
        self.assertEqual(mock_extract_text.call_args[0][0], b'pdf data for answer check' * 50)
        
        mock_check_question_answer.assert_called_once_with(
            lesson_text="dummy extracted text from lesson",
            question_with_choices=question_data,
            correct_answer=correct_answer_data
        )

if __name__ == '__main__':
    unittest.main()
