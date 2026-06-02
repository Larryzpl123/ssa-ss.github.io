#!/usr/bin/env python3
"""
SSA Smart Schedule - Personal Schedule Converter
=================================================
Interactively builds a personal-schedule .txt file readable by index.html.

It asks for each class (by period letter A-H) and the 8-day rotation, then
writes <username>.txt in the format the web app expects.

Run:  python3 personal-schedule-converter.py
"""

import re
import sys

COLORS = ["red", "green", "blue", "yellow", "purple", "teal", "orange",
          "pink", "gray", "indigo", "lime", "cyan"]

PERIOD_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]


def ask(prompt, default=None):
    suffix = f" [{default}]" if default is not None else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val if val else (default if default is not None else "")


def norm_time(t):
    """Accept '8:15', '08:15', '1:20pm', '13:20' -> 'HH:MM' 24h."""
    t = t.strip().lower().replace(" ", "")
    pm = t.endswith("pm")
    am = t.endswith("am")
    t = t.replace("am", "").replace("pm", "")
    if ":" not in t:
        t = t + ":00"
    h, m = t.split(":")
    h, m = int(h), int(m)
    if pm and h != 12:
        h += 12
    if am and h == 12:
        h = 0
    # bare hour < 8 assume afternoon (school context)
    if not pm and not am and h < 8:
        h += 12
    return f"{h:02d}:{m:02d}"


def parse_range(r):
    """'8:15-9:05' or '8:15 - 9:05' -> '08:15-09:05'."""
    a, b = re.split(r"\s*-\s*", r, maxsplit=1)
    return f"{norm_time(a)}-{norm_time(b)}"


def main():
    print("=" * 56)
    print("  SSA Smart Schedule - Personal Schedule Converter")
    print("=" * 56)
    print("Tip: copy a friend's choices fast by reusing their answers.\n")

    name = ask("Student full name", "Pei Lin Zhong")
    form = ask("Form line (e.g. 'Junior - Upper Form')", "Junior - Upper Form")
    username = ask("Username for filename (e.g. 27zhongp)", "27zhongp")

    classes = {}
    print("\n--- Classes (enter blank Name to stop) ---")
    for letter in PERIOD_LETTERS:
        print(f"\nPeriod {letter}:")
        nm = ask("  Class name (blank = skip/unscheduled)")
        if not nm:
            # default H to Unscheduled, others skipped
            if letter == "H":
                classes[letter] = ("Unscheduled", "", "", "", "", "gray")
            continue
        num = ask("  Class number (e.g. CH410)")
        sec = ask("  Section (e.g. 1)", "1")
        teacher = ask("  Teacher (e.g. Mr. Grant)")
        room = ask("  Room (e.g. MC 208)")
        color = ask(f"  Color {COLORS}", "blue")
        classes[letter] = (nm, num, sec, teacher, room, color)

    # La/Ea tags
    print("\n--- Late/Early tag per period (La or Ea) ---")
    latearly = {}
    for letter in classes:
        latearly[letter] = ask(f"  {letter} La/Ea", "La") or "La"

    # Fixed daily blocks (e.g. Assembly)
    print("\n--- Fixed daily block (shown every school day; blank to skip) ---")
    fixed = []
    fb_name = ask("  Block name (e.g. Assembly / Community Time)")
    if fb_name:
        fb_time = ask("  Time range (e.g. 10:05-10:30)", "10:05-10:30")
        fb_room = ask("  Room", "Rauh")
        fb_color = ask("  Color", "gray")
        try:
            fixed.append((fb_name, parse_range(fb_time), fb_room, fb_color))
        except Exception:
            print("  (couldn't parse time, skipping fixed block)")

    # Rotation grid
    print("\n--- 8-Day rotation ---")
    print("For each cycle day, enter pairs like: A:8:15-9:05 B:9:10-10:00")
    print("(Use period letters you defined; blank day = no classes)\n")
    days = {}
    for d in range(1, 9):
        raw = ask(f"  Day {d}")
        if not raw:
            days[d] = []
            continue
        pairs = []
        for tok in raw.split():
            if ":" not in tok:
                continue
            p, rng = tok.split(":", 1)
            p = p.upper()
            pairs.append(f"{p}:{parse_range(rng)}")
        days[d] = pairs

    # Preferences
    print("\n--- Preferences (press Enter for defaults) ---")
    bg = ask("  Background color", "#0d0f14")
    hday = ask("  Highlight-day border color", "#ffffff")
    hclass = ask("  Highlight-class border color", "#ffd23f")
    tfmt = ask("  Time format (12h/24h)", "12h")

    # Build file
    out = [name, form, "# Classes: period - name - number - section - teacher - room - color"]
    for letter in PERIOD_LETTERS:
        if letter in classes:
            nm, num, sec, teacher, room, color = classes[letter]
            out.append(f"{letter} - {nm} - {num} - {sec} - {teacher} - {room} - {color}")
    out.append("# La/Ea tag per period:")
    out.append("@latearly " + " ".join(f"{k}={v}" for k, v in latearly.items()))
    for fb in fixed:
        out.append(f"@fixed {fb[0]} - {fb[1].replace('-', '-')} - {fb[2]} - {fb[3]}")
    out.append("# Rotation: each cycle day -> period:HH:MM-HH:MM (24h)")
    for d in range(1, 9):
        out.append(f"@day {d} = " + " ".join(days[d]))
    out.append("# Preferences:")
    out.append(f"@pref background = {bg}")
    out.append(f"@pref highlight_day = {hday}")
    out.append(f"@pref highlight_class = {hclass}")
    out.append(f"@pref time_format = {tfmt}")

    fname = f"{username}.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    print(f"\nWrote {fname}")
    print("Place it in: students/classof<YEAR>/" + fname)
    print("Then open index.html and load this student.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
        sys.exit(1)
