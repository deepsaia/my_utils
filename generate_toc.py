import re
import argparse
from pathlib import Path

TOC_START = "<!-- toc -->"
TOC_END = "<!-- tocstop -->"


class TOCGenerator:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.original_lines = []
        self.updated_lines = []
        self.headings = []

    def slugify(self, text):
        text = text.strip().lower()
        text = re.sub(r'[^\w\s-]', '', text)
        return re.sub(r'\s+', '-', text)

    def read_file(self):
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {self.filepath}")
        with self.filepath.open("r", encoding="utf-8") as f:
            self.original_lines = f.readlines()

    def extract_headings(self):
        in_code_block = False
        self.headings = []

        for line in self.original_lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block or not stripped.startswith("#"):
                continue

            match = re.match(r'^(#{2,6})\s+(.*)', stripped)
            if match:
                level = len(match.group(1)) - 2
                title = match.group(2).strip()
                anchor = self.slugify(title)
                self.headings.append((level, title, anchor))

    def build_toc_block(self):
        lines = [TOC_START + "\n"]
        for level, title, anchor in self.headings:
            indent = "  " * level
            lines.append(f"{indent}- [{title}](#{anchor})\n")
        lines.append(TOC_END + "\n")
        return lines

    def update_lines(self):
        toc_block = self.build_toc_block()
        start_idx = next((i for i, l in enumerate(self.original_lines) if TOC_START in l), None)
        end_idx = next((i for i, l in enumerate(self.original_lines) if TOC_END in l), None)

        if start_idx is not None and end_idx is not None:
            self.updated_lines = (
                self.original_lines[:start_idx] + toc_block + self.original_lines[end_idx + 1:]
            )
        else:
            for i, line in enumerate(self.original_lines):
                if line.startswith("# "):
                    self.updated_lines = (
                        self.original_lines[:i+1] + ["\n"] + toc_block + ["\n"] + self.original_lines[i+1:]
                    )
                    return
            self.updated_lines = toc_block + ["\n"] + self.original_lines

    def write_file(self):
        with self.filepath.open("w", encoding="utf-8") as f:
            f.writelines(self.updated_lines)

    def preview_toc(self):
        print("📝 Preview of TOC:\n")
        print("".join(self.build_toc_block()))

    def generate(self, dry_run=False):
        self.read_file()
        self.extract_headings()
        if not self.headings:
            print("[!] No valid markdown headings (## to ######) found.")
            return

        self.update_lines()
        if dry_run:
            self.preview_toc()
        else:
            self.write_file()
            print(f"[Success] TOC updated in {self.filepath}")


def main():
    parser = argparse.ArgumentParser(description="Generate or update Table of Contents in a Markdown file.")
    parser.add_argument("file", help="Path to the markdown file (e.g., README.md)")
    parser.add_argument("--dry-run", action="store_true", help="Preview TOC without writing to file")
    args = parser.parse_args()

    try:
        toc = TOCGenerator(args.file)
        toc.generate(dry_run=args.dry_run)
    except Exception as e:
        print(f"[x] Error: {e}")


if __name__ == "__main__":
    main()
