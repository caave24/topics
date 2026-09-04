from pathlib import Path


def is_heading(line):
    stripped = line.lstrip()
    return stripped.startswith("# ") or stripped == "#"


def is_list_item(line):
    stripped = line.lstrip()

    return (
        stripped.startswith("- ")
        or stripped.startswith("* ")
        or stripped.startswith("+ ")
        or stripped.startswith("> ")
        or (
            len(stripped) > 2
            and stripped[0].isdigit()
            and stripped[1] in ".)"
            and stripped[2] == " "
        )
    )


def format_markdown(text):
    lines = text.splitlines()
    output = []

    in_code_block = False
    inside_heading_section = False

    for line in lines:
        stripped = line.strip()

        # Toggle fenced code blocks.
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_block = not in_code_block
            output.append(line)
            continue

        # Never modify code blocks.
        if in_code_block:
            output.append(line)
            continue

        # Headings start a new section.
        if is_heading(line):
            inside_heading_section = True
            output.append(line)
            continue

        # Blank lines are left alone.
        if not stripped:
            output.append(line)
            continue

        # Existing lists / blockquotes / etc. stay untouched.
        if is_list_item(line):
            output.append(line)
            continue

        # If we're inside a heading section, turn plain lines into bullets.
        if inside_heading_section:
            indent = line[: len(line) - len(line.lstrip())]
            output.append(f"{indent}- {stripped}")
            continue

        output.append(line)

    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def main():
    for path in Path(".").rglob("*.md"):
        # Don't touch GitHub's own workflow files or hidden dependency dirs.
        if any(part in {".git", "node_modules"} for part in path.parts):
            continue

        original = path.read_text(encoding="utf-8")
        formatted = format_markdown(original)

        if formatted != original:
            print(f"Formatting: {path}")
            path.write_text(formatted, encoding="utf-8")


if __name__ == "__main__":
    main()
