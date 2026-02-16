
import sys
import json
import importlib.util

def check_install(package):
    if importlib.util.find_spec(package) is None:
        return False
    return True

def extract_text(pdf_path):
    # Try pypdf first
    if check_install('pypdf'):
        from pypdf import PdfReader
        try:
            reader = PdfReader(pdf_path)
            pages = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                pages.append({"page": i + 1, "text": text})
            return json.dumps({"status": "success", "pages": pages}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False)
    
    # Try PyPDF2
    elif check_install('PyPDF2'):
        import PyPDF2
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages = []
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    pages.append({"page": i + 1, "text": text})
                return json.dumps({"status": "success", "pages": pages}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False)
            
    else:
        return json.dumps({"status": "error", "message": "MISSING_LIB"}, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No file path provided"}))
        sys.exit(1)
        
    pdf_path = sys.argv[1]
    result = extract_text(pdf_path)
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
    else:
        print(result)
