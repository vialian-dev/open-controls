import re
import unicodedata
from functools import cache
from html import unescape
from html.parser import HTMLParser
from pathlib import Path, PureWindowsPath
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

root = Path.cwd().resolve()
profile = root / "specs/baseline-evidence-record"
readme = root / "README.md"
template = root / "templates/AI_WORK_CONTRACT_TEMPLATE.md"
required_root_targets = {template, profile / "README.md"}
parser = MarkdownIt("gfm-like")
parser.validateLink = lambda url: True

class HtmlTargets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.anchors.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.anchors.add(attrs["name"])
        if tag == "a" and attrs.get("href") is not None:
            self.links.append((attrs["href"], False))
        if tag == "img" and attrs.get("src") is not None:
            self.links.append((attrs["src"], True))

def inline_text(tokens):
    for token in tokens:
        if token.type in {"text", "text_special", "code_inline"}:
            yield token.content
        elif token.type in {"softbreak", "hardbreak"}:
            yield " "
        elif token.children:
            yield from inline_text(token.children)

@cache
def parse_document(source):
    if not source.resolve().is_relative_to(root):
        raise ValueError("document escapes the repository")
    tokens = parser.parse(source.read_text(encoding="utf-8"))
    html = HtmlTargets()
    links = []
    slugs = set()
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            heading = "".join(inline_text(tokens[index + 1].children))
            name = unescape(heading).strip().lower()
            base = "".join(
                "-" if char == " " else char
                for char in name
                if char in " _-" or unicodedata.category(char)[0] in "LMN"
            )
            slug, suffix = base, 0
            while slug in slugs:
                suffix += 1
                slug = f"{base}-{suffix}"
            slugs.add(slug)
        elif token.type == "html_block":
            html.feed(token.content)
        elif token.type == "inline":
            for child in token.children:
                if child.type == "link_open":
                    links.append((child.attrGet("href"), False))
                elif child.type == "image":
                    links.append((child.attrGet("src"), True))
                elif child.type == "html_inline":
                    html.feed(child.content)
    html.close()
    return links + html.links, slugs | html.anchors

def local_target(directory, path):
    target = directory.resolve()
    for part in path.split("/"):
        if part in {"", "."}:
            continue
        if part == "..":
            target = target.parent
        else:
            if not target.is_dir():
                raise ValueError("target does not exist")
            entries = {entry.name: entry for entry in target.iterdir()}
            if part not in entries:
                raise ValueError(f"target does not exist with exact case at {part!r}")
            target = entries[part].resolve()
        if not target.is_relative_to(root):
            raise ValueError("target escapes the repository")
    if not (target.is_file() or target.is_dir()):
        raise ValueError("target does not exist")
    return target

def check_fragment(target, fragment):
    anchor_file = local_target(target, "README.md") if target.is_dir() else target
    line_range = re.fullmatch(r"L([1-9][0-9]*)(?:-L([1-9][0-9]*))?", fragment)
    if line_range and target.is_file():
        start, end = line_range.groups()
        first, last = int(start), int(end or start)
        with target.open(encoding="utf-8") as lines:
            line_count = sum(1 for line in lines)
        if not first <= last <= line_count:
            raise ValueError(f"line range {fragment!r} is outside the file or reversed")
    elif fragment not in parse_document(anchor_file)[1]:
        raise ValueError(f"unknown anchor {fragment!r}")

def check_document(source):
    try:
        links, _ = parse_document(source)
    except (OSError, ValueError) as error:
        raise SystemExit(f"{source.relative_to(root)}: {error}") from None

    targets = set()
    for destination, image in links:
        try:
            parts = urlsplit(destination)
            if parts.scheme == "file" or len(parts.scheme) == 1:
                raise ValueError("expected a repository-relative path")
            if parts.scheme or parts.netloc:
                continue
            path = unquote(parts.path, errors="strict")
            if path.startswith("/") or "\\" in path or PureWindowsPath(path).drive:
                raise ValueError("expected a repository-relative path")
            target = local_target(source.parent, path) if path else source.resolve()
            if parts.fragment:
                check_fragment(target, unquote(parts.fragment, errors="strict"))
            if not image:
                targets.add(target)
        except (OSError, ValueError) as error:
            raise SystemExit(f"{source.relative_to(root)}: {destination!r}: {error}") from None
    return targets

missing = required_root_targets - check_document(readme)
if missing:
    names = ", ".join(path.relative_to(root).as_posix() for path in sorted(missing))
    raise SystemExit(f"README.md: missing required links to {names}")

documents = set(root.glob("*.md")) | set(profile.rglob("*.md")) | {template}
for source in sorted(documents - {readme}):
    check_document(source)
print(f"Local Markdown links checked in {len(documents)} documents")
