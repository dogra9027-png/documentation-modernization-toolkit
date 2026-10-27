
"""Search Markdown knowledge articles and return relevant passages."""

from pathlib import Path
import argparse
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCS = ROOT / "docs"


def tokenize(text):
    """Return normalized words, excluding common stop words."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    stop_words = {
        "a", "an", "and", "are", "as", "at", "be", "by",
        "for", "from", "how", "in", "is", "it", "of", "on",
        "or", "the", "to", "what", "when", "where", "which",
        "who", "with", "your"
    }
    return [word for word in words if word not in stop_words]


def load_articles(docs_dir):
    """Load Markdown files and separate metadata from article content."""
    articles = []

    for path in sorted(docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        title = path.stem.replace("-", " ").title()

        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) == 3:
                metadata = parts[1]
                match = re.search(
                    r"(?m)^title:\s*[\"']?(.+?)[\"']?\s*$",
                    metadata,
                )
                if match:
                    title = match.group(1).strip()

                content = parts[2].strip()
            else:
                content = text
        else:
            content = text

        articles.append({
            "path": path,
            "title": title,
            "content": content,
            "tokens": set(tokenize(title + " " + content)),
        })

    return articles


def search_articles(question, articles, limit=3):
    """Rank articles by simple keyword overlap with the question."""
    query_tokens = set(tokenize(question))

    if not query_tokens:
        return []

    results = []

    for article in articles:
        overlap = query_tokens.intersection(article["tokens"])
        if overlap:
            score = len(overlap) / len(query_tokens)
            results.append((score, article, overlap))

    results.sort(key=lambda item: (-item[0], item[1]["title"].lower()))
    return results[:limit]


def main():
    parser = argparse.ArgumentParser(
        description="Search Markdown knowledge articles."
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="Question or keywords to search for.",
    )
    parser.add_argument(
        "--docs",
        type=Path,
        default=DEFAULT_DOCS,
        help="Directory containing Markdown articles.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Maximum number of results.",
    )
    args = parser.parse_args()

    if args.limit < 1:
        parser.error("--limit must be at least 1")

    if not args.docs.is_dir():
        print(f"Error: documentation directory not found: {args.docs}")
        return 1

    articles = load_articles(args.docs)
    if not articles:
        print(f"No Markdown articles found in {args.docs}")
        return 1

    question = args.question or input("Ask a documentation question: ")
    results = search_articles(question, articles, args.limit)

    if not results:
        print("I couldn't find relevant information in the documentation.")
        print("Try different keywords or check whether an article covers this topic.")
        return 0

    print("\nRelevant documentation passages\n")

    for rank, (score, article, overlap) in enumerate(results, start=1):
        print(f"{rank}. {article['title']} (match: {score:.0%})")
        print(f"   Source: {article['path'].relative_to(ROOT)}")
        print(f"   Matched terms: {', '.join(sorted(overlap))}")

        # Show a concise excerpt from the article body.
        excerpt = re.sub(r"(?m)^---\s*$", "", article["content"])
        excerpt = re.sub(r"(?m)^#+\s*", "", excerpt)
        excerpt = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", excerpt)
        excerpt = re.sub(r"[*_`]", "", excerpt)
        excerpt = re.sub(r"\s+", " ", excerpt).strip()

        print(f"   Excerpt: {excerpt[:350]}")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
