"""Offline validation tests; do not need network or copyrighted fixtures."""
import io
import sys
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from download_originals import validate_file, sha256_hex


class SourceValidationTests(unittest.TestCase):
    def test_pdf_signature_is_accepted(self):
        self.assertEqual(validate_file("report.pdf", b"%PDF-1.7\n1 0 obj\n%%EOF"), "application/pdf")

    def test_html_error_is_not_pdf(self):
        with self.assertRaises(ValueError):
            validate_file("report.pdf", b"<html>Forbidden</html>")

    def test_docx_requires_ooxml_parts(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as zip_file:
            zip_file.writestr("[Content_Types].xml", "<Types/>")
            zip_file.writestr("word/document.xml", "<document/>")
        self.assertEqual(
            validate_file("supplement.docx", buffer.getvalue()),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    def test_corrupt_docx_rejected(self):
        with self.assertRaises(ValueError):
            validate_file("supplement.docx", b"PK-invalid")

    def test_sha256(self):
        self.assertEqual(
            sha256_hex(b"hello"),
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )


if __name__ == "__main__":
    unittest.main()
