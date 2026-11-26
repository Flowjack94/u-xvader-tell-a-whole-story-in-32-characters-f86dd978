"""Tell a Whole Story in 32 Characters.

Assembles the 31-character story from named fragments and writes it to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt). It never writes
into the repository itself.
"""

import os

# Named fragments of the story.
SUBJECT = "Ticket #4821"
SEPARATOR = ": "
TWIST = "snooze won again."

MIN_LEN = 1
MAX_LEN = 32

INVISIBLE = ("\u200b", "\ufeff", "\u00ad")


def build_line():
    """Assemble the whole story from its fragments."""
    return SUBJECT + SEPARATOR + TWIST


def check_story_shape(line):
    """A whole story needs a subject and a resolved twist, not just words."""
    if SUBJECT not in line:
        raise ValueError("story must name its subject")
    if not line.endswith("."):
        raise ValueError("story must end with a full stop")
    if "won" not in line and "lost" not in line:
        raise ValueError("story must resolve with an outcome")


def guard_line(line):
    """Enforce the gate: 1-32 chars, one line, no control or invisible chars."""
    check_story_shape(line)
    if not isinstance(line, str):
        raise ValueError("entry must be text")
    if not (MIN_LEN <= len(line) <= MAX_LEN):
        raise ValueError(
            "entry must be %d-%d characters, got %d" % (MIN_LEN, MAX_LEN, len(line))
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if line != line.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    for ch in line:
        if ord(ch) < 32 or ord(ch) == 127:
            raise ValueError("entry must not contain control characters")
    for ch in INVISIBLE:
        if ch in line:
            raise ValueError("entry must not contain invisible characters")
    return line


def publish(line):
    """Write the guarded entry to the output dir, with a byte read-back check."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    with open(path, "rb") as fh:
        if fh.read() != data:
            raise IOError("read-back mismatch for entry.txt")
    print("wrote %d chars to %s" % (len(line), path))


def main():
    line = guard_line(build_line())
    publish(line)


if __name__ == "__main__":
    main()
