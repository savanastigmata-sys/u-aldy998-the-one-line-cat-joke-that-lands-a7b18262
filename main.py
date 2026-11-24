"""The One-Line Cat Joke That Lands.

Writes a single original one-line cat joke (under 200 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt and nothing else. Deterministic: the same
joke every run, no randomness, no network, no model calls.
"""

import os
import sys

JOKE = "My cat stares at the same blank wall every night for an hour, and honestly, I'm starting to check it too."

MAX_CHARS = 200


def validate(text):
    """Enforce the competition's entry rules: one line, under 200 chars."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("joke must be a non-empty string")
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be a single line")
    if len(text) >= MAX_CHARS:
        raise ValueError("joke must be under 200 characters, got %d" % len(text))
    if text != text.strip():
        raise ValueError("joke must not have leading or trailing whitespace")
    return text


def resolve_output_dir():
    """Return the output directory, honouring MAKEFUN_OUTPUT_DIR."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def main():
    joke = validate(JOKE)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(joke + "\n")
    # Round-trip check: what was written must validate as the same one line.
    with open(path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != joke + "\n":
        raise RuntimeError("entry.txt round-trip mismatch")
    print("wrote %s (%d chars)" % (path, len(joke)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
