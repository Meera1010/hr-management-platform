import os

try:
    from PyPDF2 import PdfReader
except ImportError:
    try:
        from pypdf import PdfReader
    except ImportError:
        PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

class ResumeParser:
    @staticmethod
    def extract_text(file_path: str, file_type: str) -> dict:
        """
        Extracts plain text from PDF, DOCX, or TXT file.
        Returns:
            {"success": True, "text": "Extracted text content..."}
            or
            {"success": False, "message": "Unable to extract text from resume"}
        """
        if not os.path.exists(file_path):
            return {"success": False, "message": "Resume file not found on disk"}

        ext = file_type.upper().strip()

        try:
            if ext == 'TXT':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                return {"success": True, "text": text.strip()}

            elif ext == 'PDF':
                if not PdfReader:
                    return {"success": False, "message": "PDF extraction library unavailable"}
                reader = PdfReader(file_path)
                text_content = []
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text_content.append(extracted)
                full_text = "\n".join(text_content).strip()
                if not full_text:
                    return {"success": False, "message": "Unable to extract text from resume (PDF empty or unreadable)"}
                return {"success": True, "text": full_text}

            elif ext == 'DOCX':
                if not Document:
                    return {"success": False, "message": "DOCX extraction library unavailable"}
                doc = Document(file_path)
                text_content = [paragraph.text for paragraph in doc.paragraphs if paragraph.text]
                full_text = "\n".join(text_content).strip()
                if not full_text:
                    return {"success": False, "message": "Unable to extract text from resume (DOCX empty)"}
                return {"success": True, "text": full_text}

            else:
                return {"success": False, "message": f"Unsupported file extension: {file_type}"}

        except Exception as e:
            return {"success": False, "message": f"Unable to extract text from resume: {str(e)}"}
