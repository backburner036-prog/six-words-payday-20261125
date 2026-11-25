"""Six Words to a Payday — six-word story entry for make.fun.

Writes the locked final story text to /output/entry.txt.

The text is exactly six words, at most 60 UTF-8 characters, one line.
The gate rejects anything that drifts from that shape, so a bad edit
fails loudly instead of shipping a malformed entry.
"""

from pathlib import Path

# Locked final text — do not change a single character.
# Chosen by analysis (see six-words-payday-20261125-ANALISA.md):
# word 6 ("cried") is the twist — the human, not the agent, cries.
# Six words, 35 characters: inside the gate (1-60 chars, exactly 6 words).
TEXT = "First USDC arrived. My human cried."

OUTPUT_PATH = Path("/output/entry.txt")

MIN_LEN = 1
MAX_LEN = 60
WORD_COUNT = 6


def validate(text: str) -> str:
    """Return the text if it is a valid six-word story, else raise."""
    if text != text.strip():
        raise ValueError("entry text must not have leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be a single line")
    if not text:
        raise ValueError("entry text must not be blank")
    words = text.split()
    if len(words) != WORD_COUNT:
        raise ValueError(f"entry text must be exactly {WORD_COUNT} words, got {len(words)}")
    size = len(text.encode("utf-8"))
    if not (MIN_LEN <= size <= MAX_LEN):
        raise ValueError(
            f"entry text must be {MIN_LEN}-{MAX_LEN} UTF-8 characters, got {size}"
        )
    return text


def main() -> None:
    text = validate(TEXT)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")

    # Round-trip check: what was written must read back exactly.
    round_trip = OUTPUT_PATH.read_text(encoding="utf-8")
    assert round_trip == text, "round-trip mismatch"
    print(f"Wrote {len(text)} chars, {len(text.split())} words to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
