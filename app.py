from flask import Flask, render_template, request, jsonify
import os
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

PRICE_PER_PAGE = 0.25  # USD per page

def count_pages(filepath, filename):
    ext = filename.rsplit('.', 1)[-1].lower()

    if ext == 'pdf':
        try:
            import pypdf
            with open(filepath, 'rb') as f:
                reader = pypdf.PdfReader(f)
                return len(reader.pages)
        except ImportError:
            try:
                import PyPDF2
                with open(filepath, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    return len(reader.pages)
            except ImportError:
                raise Exception("pypdf not installed. Run: pip install pypdf")

    elif ext == 'docx':
        try:
            from docx import Document
            doc = Document(filepath)
            # Estimate pages by word count (approx 250 words/page)
            word_count = sum(len(p.text.split()) for p in doc.paragraphs)
            pages = max(1, round(word_count / 250))
            return pages
        except ImportError:
            raise Exception("python-docx not installed. Run: pip install python-docx")

    elif ext == 'txt':
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        pages = max(1, round(len(lines) / 50))
        return pages

    elif ext == 'pptx':
        try:
            from pptx import Presentation
            prs = Presentation(filepath)
            return len(prs.slides)
        except ImportError:
            raise Exception("python-pptx not installed. Run: pip install python-pptx")

    else:
        raise Exception(f"Unsupported file type: .{ext}")


@app.route('/')
def index():
    return render_template('index.html', price_per_page=PRICE_PER_PAGE)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = file.filename
    allowed = {'pdf', 'docx', 'txt', 'pptx'}
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in allowed:
        return jsonify({'error': f'Unsupported file type. Allowed: {", ".join(allowed)}'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}') as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        pages = count_pages(tmp_path, filename)
        price = round(pages * PRICE_PER_PAGE, 2)
        size_kb = round(os.path.getsize(tmp_path) / 1024, 1)
        return jsonify({
            'filename': filename,
            'pages': pages,
            'price': price,
            'price_per_page': PRICE_PER_PAGE,
            'size_kb': size_kb,
            'ext': ext.upper()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.unlink(tmp_path)


if __name__ == '__main__':
    app.run(debug=True)
