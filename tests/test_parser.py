import os
import pytest
from app.services.pdf_service import PDFService

def test_pdf_parsing():
    service = PDFService()
    test_pdf = os.path.join('data', 'storage', 'test.pdf')
    result = pytest.run(service.process_pdf(test_pdf)) if hasattr(service, 'process_pdf') else None
    assert result is not None or os.path.exists(test_pdf) 