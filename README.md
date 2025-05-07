# my_utils
my utils to speed things a little

<!-- toc -->
[**TOC Generator Utility**](#toc-generator-utility)
<!-- toc -->

# 🧰 TOC Generator Utility

The **TOC Generator** is a Python utility that automatically inserts or updates a Table of Contents in Markdown files (like `README.md`) by scanning headings and generating anchor-compatible links. It is designed to work seamlessly with GitHub-flavored Markdown.

> ⚙️ This script is part of [my_utils](https://github.com/deepsaia/my_utils) repository.

---

## 🚀 Features

- Supports multi-level headings (`##` to `######`)
- Compatible with GitHub-flavored anchor links
- Automatically replaces TOC between `<!-- toc -->` and `<!-- tocstop -->`
- Skips headings inside code blocks
- CLI-friendly, with dry-run preview mode

---

## 📦 Installation

Clone or download this repo:

```bash
git clone https://github.com/deepsaia/my_utils.git
cd utils
```

(Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

---

## 🧪 Usage

```bash
python toc_generator.py path/to/README.md
```

### 🧾 Examples

**Update TOC in-place:**
```bash
python toc_generator.py README.md
```

**Preview TOC without modifying the file:**
```bash
python toc_generator.py README.md --dry-run
```

---

## ✍️ Markdown TOC Format

This script uses the following comment markers to identify the TOC block:

```md
<!-- toc -->
... (auto-generated links here) ...
<!-- tocstop -->
```

If no markers exist, the TOC will be inserted below the main title (`# Heading`), or at the top of the file.

---

## 🔧 Integration Tips

You can add this script to your `Makefile` or CI pipelines to enforce consistent and up-to-date documentation TOCs.

---

## 🛠 Development

If you'd like to make changes, modify `toc_generator.py`. The main class is `TOCGenerator`.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
```
