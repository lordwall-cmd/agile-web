# agile-web

Generate product web pages from YAML briefs, following the Kura Biotech / Blikka Genomics design template.

## Quick start

```bash
pip install -r requirements.txt
python generate.py briefs/example.yaml
# → output/example.html
```

Open `output/example.html` in your browser to preview.

## Usage

```
python generate.py <brief.yaml> [options]

Options:
  -o, --output PATH     Output HTML file (default: output/<brief-name>.html)
  -t, --template NAME   Template file in templates/ (default: page.html.j2)
  -w, --watch           Rebuild automatically when the brief changes
```

## Brief structure

A brief is a YAML file with these top-level sections (all optional except `meta`, `brand`, `nav`, `hero`, `content`):

| Section | Required | Description |
|---|---|---|
| `meta` | ✓ | Page title, description, language |
| `brand` | ✓ | Company name, logo, color overrides |
| `nav` | ✓ | Navigation links + optional CTA button |
| `hero` | ✓ | Category label + H1 (2 lines) + optional bg image |
| `content` | ✓ | Image + body paragraphs (HTML allowed) + CTA button |
| `data_section` | — | Performance data cards (image + title + caption) |
| `resources` | — | Downloadable files (PDF links with type + label) |
| `cta_banner` | — | Full-width call-to-action with highlighted word |
| `footer` | — | Copyright, legal links, column links |

See [`briefs/example.yaml`](briefs/example.yaml) for a fully annotated example.

## Design tokens

Override the default colors in the `brand` block:

```yaml
brand:
  primary_color: "#3d1152"   # nav, content section, CTA banner background
  purple_dark:   "#15002a"   # footer background
  accent_teal:   "#2ed9c3"   # highlight word, hover states
  accent_blue:   "#00b5e2"   # buttons, download icons
```

## Project layout

```
agile-web/
├── generate.py          # CLI generator
├── requirements.txt
├── templates/
│   └── page.html.j2     # Jinja2 template
├── briefs/
│   └── example.yaml     # Annotated example brief
└── output/              # Generated HTML files (git-ignored)
```
