
from html.parser import HTMLParser
from pathlib import Path
from datetime import date
import argparse
import re


class HTMLToMarkdown(HTMLParser):
    """Convert a simple HTML knowledge article into Markdown."""

    BLOCK_TAGS = {
        "p", "div", "section", "article",
        "ul", "ol", "li", "blockquote",
        "h1", "h2", "h3", "h4", "h5", "h6",
        "table", "tr"
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip_depth = 0
        self.list_stack = []
        self.link_stack = []

    def add(self, text):
        if text:
            self.out.append(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag in ("head", "script", "style", "title"):
            self.skip_depth += 1
            return

        if self.skip_depth:
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            self.add("\n\n" + "#" * level + " ")

        elif tag in ("p", "div", "section", "article"):
            self.add("\n\n")

        elif tag == "br":
            self.add("\n")

        elif tag in ("strong", "b"):
            self.add("**")

        elif tag in ("em", "i"):
            self.add("*")

        elif tag == "a":
            self.link_stack.append(attrs.get("href", ""))
            self.add("[")

        elif tag in ("ul", "ol"):
            self.list_stack.append(tag)
            self.add("\n")

        elif tag == "li":
            if self.list_stack and self.list_stack[-1] == "ol":
                self.add("\n1. ")
            else:
                self.add("\n- ")

    def handle_endtag(self, tag):
        if tag in ("head", "script", "style", "title"):
            if self.skip_depth:
                self.skip_depth -= 1
            return

        if self.skip_depth:
            return

        if tag in ("strong", "b"):
            self.add("**")

        elif tag in ("em", "i"):
            self.add("*")

        elif tag == "a":
            href = self.link_stack.pop() if self.link_stack else ""
            self.add(f"]({href})" if href else "]")

        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
            self.add("\n")

        elif tag in self.BLOCK_TAGS:
            self.add("\n")

    def handle_data(self, data):
        if not self.skip_depth:
            self.add(data)


def clean_markdown(text):
    """Normalize whitespace and remove formatting errors."""

    # Remove bold markers surrounding Markdown headings.
    text = re.sub(
        r"(?m)^\s*\*\*(#{1,6}\s.+?)\*\*\s*$",
        r"\1",
        text,
    )

    # Remove unnecessary backslashes before Markdown punctuation.
    text = re.sub(r"\\([\\`*_{}\[\]()#+.!|>-])", r"\1", text)

    # Normalize line endings and excessive blank lines.
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip() + "\n"


def convert_file(source_file, output_file, all_source_names):
    """Convert one HTML file and add basic article metadata."""

    parser = HTMLToMarkdown()
    parser.feed(source_file.read_text(encoding="utf-8"))
    body = clean_markdown("".join(parser.out))

    slug = source_file.stem
    title = slug.replace("-", " ").title()

    # Prefer the first H1 heading as the article title.
    match = re.search(r"(?m)^#\s+(.+)$", body)
    if match:
        title = match.group(1).strip()

           # Keep the H1 heading in the Markdown body.
    body = re.sub(
        r"(?m)^#\s+" + re.escape(title) + r"\s*\n*",
        "",
        body,
        count=1,
    ).lstrip()

    body = f"# {title}\n\n{body}"

    # Update links to other HTML files when the destination exists.
    for source_name in all_source_names:
        old_link = source_name.name
        new_link = source_name.stem + ".md"
        body = body.replace(f"]({old_link})", f"]({new_link})")

    metadata = (
        "---\n"
        f'title: "{title}"\n'
        f'slug: "{slug}"\n'
        'content_type: "knowledge-article"\n'
        'audience: "service-desk"\n'
        'tags: [support, troubleshooting]\n'
        f'review_date: "{date.today().isoformat()}"\n'
        "---\n\n"
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(metadata + body.rstrip() + "\n", encoding="utf-8")


def main():
    argument_parser = argparse.ArgumentParser(
        description="Convert sample HTML documentation into Markdown."
    )
    argument_parser.add_argument(
        "--input",
        default="sample_source",
        help="Folder containing source HTML files.",
    )
    argument_parser.add_argument(
        "--output",
        default="docs",
        help="Folder where Markdown files will be written.",
    )
    args = argument_parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        raise SystemExit(f"Input folder not found: {input_dir}")

    source_files = sorted(input_dir.glob("*.html"))

    if not source_files:
        raise SystemExit(f"No HTML files found in: {input_dir}")

    for source_file in source_files:
        output_file = output_dir / f"{source_file.stem}.md"
        convert_file(source_file, output_file, source_files)
        print(f"Converted {source_file.name} -> {output_file}")


if __name__ == "__main__":
    main()
