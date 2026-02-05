# AI Karyashala - Certificate Generator

Generates PDF certificates, social media preview thumbnails, and static HTML pages for AI Karyashala Bootcamp participants. The web pages are deployed via GitHub Pages from the `docs/` folder.

## Project Structure

```
├── generate.py                  # Certificate generation script
├── template.html                # HTML template for per-student pages
├── students.csv                 # Student data (CName, CRollNumber)
├── requirements.txt             # Python dependencies
├── pdfs/                        # Generated PDFs (not served by Pages)
│   ├── {rollno}.pdf             # Individual certificate PDFs
│   ├── batch-{n}.pdf            # Combined batch PDFs
│   └── all-certificates.pdf     # Combined PDF of all certificates
└── docs/                        # GitHub Pages root
    └── bootcamp/
        └── kiet/
            ├── index.html       # Student login portal
            ├── render.html      # Playwright rendering page (used by generate.py)
            ├── students.csv     # Student data for browser-side lookup
            ├── assets/
            │   ├── css/style.css
            │   ├── js/
            │   │   ├── certificate-renderer.js
            │   │   └── main.js
            │   ├── signature.png
            │   └── student_images/{rollno}.jpg
            └── {rollno}/        # Generated per-student pages
                ├── index.html
                └── preview.jpg
```

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage

### Generate everything for all students

```bash
python generate.py --all
```

### Generate only PDFs

```bash
python generate.py --pdfs
```

### Generate only web pages and thumbnails

```bash
python generate.py --pages
```

### Generate for a single student

```bash
python generate.py --student AIK24B21A42C7
```

### Batch generation

Generate in batches for printing. Each batch produces individual PDFs plus a single combined PDF.

```bash
# First 20 students → pdfs/batch-1.pdf
python generate.py --pdfs --batch-size 20 --batch 1

# Next 20 students → pdfs/batch-2.pdf
python generate.py --pdfs --batch-size 20 --batch 2

# Batch of 50 → pdfs/batch-1.pdf
python generate.py --pdfs --batch-size 50 --batch 1

# All students without batching → pdfs/all-certificates.pdf
python generate.py --pdfs
```

### All options

| Flag | Description |
|------|-------------|
| `--all` | Generate PDFs, thumbnails, and HTML pages |
| `--pdfs` | Generate only PDFs |
| `--pages` | Generate only HTML pages and thumbnails |
| `--student ROLLNO` | Generate for a single student |
| `--batch-size N` | Number of students per batch |
| `--batch N` | Batch number to process (1-indexed, default: 1) |
| `--base-url URL` | Base URL for OG tags (default: aikaryashala.com) |
| `--csv PATH` | Path to students CSV (default: students.csv) |
| `--output DIR` | Output directory for web pages |
| `--keep-png` | Keep temporary PNG files |

## GitHub Pages Deployment

The site is served from the `docs/` folder. Configure GitHub Pages:

1. Go to repo Settings > Pages
2. Set Source to "Deploy from a branch"
3. Set Branch to `main` and folder to `/docs`

Live URLs:
- Portal: `https://aikaryashala.com/certificates/bootcamp/kiet/`
- Student certificate: `https://aikaryashala.com/certificates/bootcamp/kiet/{rollno}/`

## How It Works

1. **generate.py** reads `students.csv` and launches a headless Chromium browser via Playwright
2. It loads `render.html` which includes `certificate-renderer.js` — the canvas-based certificate renderer
3. For each student, it renders the certificate on an HTML canvas, takes a screenshot, and produces:
   - A PDF from the rendered image (at `pdfs/`)
   - A thumbnail for social media previews (`preview.jpg`)
   - A static HTML page with Open Graph tags for link sharing
4. When using `--batch-size`, a combined PDF with all certificates in the batch is also generated

## Student Data

`students.csv` format:

```csv
CName,CRollNumber
Student Name,AIK24B21A42C7
```

Student photos should be placed at `docs/bootcamp/kiet/assets/student_images/{CRollNumber}.jpg`.
