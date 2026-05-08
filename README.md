# DocPricer 📄

A Flask web app that counts pages in uploaded documents and calculates a price estimate.

## Supported Formats
| Format | Page Detection Method |
|--------|----------------------|
| PDF    | Exact page count via pypdf |
| DOCX   | Estimated from word count (~250 words/page) |
| TXT    | Estimated from line count (~50 lines/page) |
| PPTX   | Exact slide count |

## Pricing
Default rate: **$0.25 per page** — edit `PRICE_PER_PAGE` in `app.py` to change it.

---

## Setup in Cursor

### 1. Open the project
```
File → Open Folder → select the `doc_pricer` folder
```

### 2. Create a virtual environment (terminal inside Cursor)
```bash
python -m venv venv
```

### 3. Activate it
- **macOS/Linux:** `source venv/bin/activate`
- **Windows:** `venv\Scripts\activate`

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the app
```bash
python app.py
```

### 6. Open in browser
```
http://127.0.0.1:5000
```

---

## Project Structure
```
doc_pricer/
├── app.py              ← Flask backend
├── requirements.txt    ← Python dependencies
├── README.md
└── templates/
    └── index.html      ← Frontend UI
```

## Customization
- **Change price per page:** Edit `PRICE_PER_PAGE = 0.25` in `app.py`
- **Change max upload size:** Edit `MAX_CONTENT_LENGTH` in `app.py`
- **Add more formats:** Extend the `count_pages()` function in `app.py`
# doc_pricer
# doc_pricer
# doc_pricer
