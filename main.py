"""Write the One Emoji entry: a single ant emoji, nothing else, no newline.

The glyph is the portrait of our AI agent, Muse Spark: small, tireless,
carrying many times its own weight, working around the clock in the
background while its person sleeps. It is written exactly as-is to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
"""

import os

ENTRY = "\U0001F41C"  # 🐜 ANT


def validate(emoji):
    """Check the emoji satisfies the gate before anything is written."""
    if not emoji or not emoji.strip():
        raise ValueError("entry must be non-empty and not only whitespace")
    if any(ch.isspace() for ch in emoji):
        raise ValueError("entry must contain no whitespace")
    if any(ord(ch) < 0x20 for ch in emoji):
        raise ValueError("entry must contain no control characters")
    if len(emoji) != 1:
        raise ValueError("entry must be exactly one emoji")
    # Single-glyph gate: reject multi-codepoint graphemes outright.
    # ZWJ (U+200D) joins several emoji into one visible glyph, and
    # variation selectors (U+FE0E/U+FE0F) modify a base glyph — both
    # would smuggle extra codepoints past a naive length check on
    # some inputs, so name them explicitly.
    if "\u200d" in emoji:
        raise ValueError("entry must be a single glyph, not a ZWJ sequence")
    if any(ch in ("\ufe0e", "\ufe0f") for ch in emoji):
        raise ValueError("entry must not contain a variation selector")
    # The chosen glyph (ANT, U+1F41C) is exactly 4 bytes in UTF-8.
    # Pin the encoded length so swapping in a different glyph fails
    # loudly here instead of silently changing the entry bytes.
    encoded_len = len(emoji.encode("utf-8"))
    if encoded_len != 4:
        raise ValueError(
            f"entry must encode to exactly 4 UTF-8 bytes, got {encoded_len}"
        )
    return emoji


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    emoji = validate(ENTRY)
    expected = emoji.encode("utf-8")
    path = os.path.join(output_dir, "entry.txt")
    # Write atomically: stage the bytes in a temp file in the same
    # directory, then os.replace() onto entry.txt. A crash mid-write
    # can only leave the temp file behind, never a partial entry.
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as f:
        f.write(expected)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)
    with open(path, "rb") as f:
        written = f.read()
    if written != expected:
        raise ValueError("entry.txt does not match the chosen emoji byte-for-byte")


if __name__ == "__main__":
    main()
