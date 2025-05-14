
import os
import requests
import argparse
import pandas as pd
from pathlib import Path
from urllib.parse import urlparse


class TheConverter:
    """
    A class that converts anything to anything
    """
    def __init__(self, file_path: str, transpose: bool = False, output_path: str = None):
        self.file_path = file_path
        self.transpose = transpose
        self.output_path = output_path or str(Path(file_path).parent)
        self.local_file = self._fetch_file_if_needed()

    def _fetch_file_if_needed(self) -> str:
        """Download file if it's a URL."""
        parsed = urlparse(self.file_path)
        if parsed.scheme in ('http', 'https'):
            filename = os.path.basename(parsed.path)
            local_path = os.path.join(self.output_path, filename)
            response = requests.get(self.file_path)
            response.raise_for_status()
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return local_path
        return self.file_path

    def _read_markdown_table(self, file: str) -> pd.DataFrame:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Extract only table lines
        table_lines = [line for line in lines if '|' in line and not line.strip().startswith('#')]
        clean_lines = [line.strip() for line in table_lines if line.strip()]

        if not clean_lines:
            raise ValueError("No markdown table found.")

        # Split and clean header/data
        headers = [cell.strip() for cell in clean_lines[0].strip('|').split('|')]
        data = []
        for line in clean_lines[2:]:  # Skip header and separator
            row = [cell.strip() for cell in line.strip('|').split('|')]
            data.append(row)

        df = pd.DataFrame(data, columns=headers)
        return df

    def _write_markdown_table(self, df: pd.DataFrame, output_file: str):
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('# Transposed Table\n\n')
            f.write('| ' + ' | '.join(df.columns) + ' |\n')
            f.write('| ' + ' | '.join(['---'] * len(df.columns)) + ' |\n')
            for _, row in df.iterrows():
                f.write('| ' + ' | '.join(str(x) for x in row) + ' |\n')

    def convert(self):
        if self.transpose:
            df = self._read_markdown_table(self.local_file)
            df = df.set_index(df.columns[0]).T.reset_index()
            df.columns = ['Framework / Tool'] + list(df.columns[1:])
            out_file = os.path.join(self.output_path, f'transposed_{Path(self.local_file).name}')
            self._write_markdown_table(df, out_file)
            print(f"✅ Transposed markdown table written to: {out_file}")
        else:
            print("ℹ️ No transformation selected. Use --transpose to enable transposing.")


def main():
    parser = argparse.ArgumentParser(description="Convert markdown tables and other formats.")
    parser.add_argument("file_path", help="Path or URL to the markdown file")
    parser.add_argument("--transpose", action="store_true", help="Transpose the markdown table")
    parser.add_argument("--output_path", default=None, help="Output directory path (optional)")

    args = parser.parse_args()

    converter = TheConverter(
        file_path=args.file_path,
        transpose=args.transpose,
        output_path=args.output_path
    )
    converter.convert()


if __name__ == "__main__":
    main()
