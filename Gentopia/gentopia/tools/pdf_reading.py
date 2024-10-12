from typing import Any, Type
from pydantic import BaseModel, Field
from io import BytesIO
import requests
import PyPDF2  # Ensure you're using version 3.0.0 or newer
from gentopia.tools.basetool import BaseTool


class PDFReaderArgs(BaseModel):
    # URL argument for the PDF document
    url: str = Field(..., description="Link to the PDF document to be downloaded and parsed")


class PDFReader(BaseTool):
    """A tool for fetching and reading the contents of a PDF from a URL."""

    name = "pdf_reader"
    description = "Downloads a PDF from a given URL, extracts the text, and returns it."

    # Defining the argument schema for the tool
    args_schema: Type[BaseModel] = PDFReaderArgs

    def _run(self, url: str) -> str:
        try:
            # Download the PDF from the provided URL
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors
            
            # Load the response content as a binary stream
            pdf_stream = BytesIO(response.content)
            
            # Use PyPDF2's PdfReader to extract text from the PDF
            reader = PyPDF2.PdfReader(pdf_stream)
            extracted_text = ""
            
            # Iterate through each page to extract its text content
            for page in reader.pages:
                extracted_text += page.extract_text() or ""  # Avoid adding 'None'

            return extracted_text if extracted_text else "No text could be extracted from the PDF."
        
        except Exception as error:
            return f"An error occurred while reading the PDF: {str(error)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        # This method is not implemented for asynchronous operation
        raise NotImplementedError


if __name__ == "__main__":
    # Example usage
    pdf_url = "https://example.com/sample.pdf"
    result = PDFReader()._run(pdf_url)
    print(result)
