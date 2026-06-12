#!/usr/bin/env python3
"""
SSA Smart Schedule - Personal Schedule Converter
=================================================
Builds a personal-schedule .txt in the term-based format read by index.html.

The 8-day rotation, La/Ea tags, Assembly/community time, Wednesday bell times,
immersive blocks, dismissal, and finals all live in the shared schedule.txt now.
A personal file only contains: name, grade line, and one or more @term sections
(each with classes A-H plus optional @immersive / @sport), then @pref lines.

Run:  python3 personal-schedule-converter.py
"""

import re
import sys

COLORS = ["red", "green", "blue", "yellow", "purple", "teal", "orange",
          "pink", "gray", "indigo", "lime", "cyan"]
PERIOD_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]
GRADES = {"9": "Freshman", "10": "Sophomore", "11": "Junior", "12": "Senior"}


def ask(prompt, default=None):
    suffix = f" [{default}]" if default is not None else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val if val else (default if default is not None else "")


def norm_md(s):
    s = s.strip().replace("/", ".").replace("-", ".")
    m = re.match(r"(\d{1,2})\.(\d{1,2})", s)
    if not m:
        return s
    return f"{int(m.group(1)):02d}.{int(m.group(2)):02d}"


def ask_term(label_default, range_default):
    label = ask("  Term label (e.g. 'Fall 2025', blank to finish)", label_default)
    if not label:
        return None
    rng = ask("  Date range MM.DD-MM.DD", range_default)
    a, b = re.split(r"\s*-\s*", rng, maxsplit=1)
    classes = {}
    print("  Classes for this term (blank name = skip; H blank = Unscheduled):")
    for letter in PERIOD_LETTERS:
        nm = ask(f"    {letter} name")
        if not nm:
            if letter == "H":
                classes[letter] = ("Unscheduled", "", "", "", "", "gray")
            continue
        num = ask(f"    {letter} number", "")
        sec = ask(f"    {letter} section", "1")
        teacher = ask(f"    {letter} teacher", "")
        room = ask(f"    {letter} room", "")
        color = ask(f"    {letter} color {COLORS}", "blue")
        classes[letter] = (nm, num, sec, teacher, room, color)

    imm = None
    iname = ask("  Immersive course name (blank = none)")
    if iname:
        inum = ask("    number", "IM327")
        iteach = ask("    teacher(s)", "")
        iroom = ask("    room", "")
        icolor = ask("    color", "indigo")
        imm = (iname, inum, iteach, iroom, icolor)

    sports = []
    while True:
        sname = ask("  Sport name (blank = done)")
        if not sname:
            break
        sdays = ask("    days (e.g. Mon,Thu)", "Mon,Thu")
        stime = ask("    time HH:MM-HH:MM", "15:45-17:15")
        srange = ask("    season MM.DD-MM.DD", "09.01-11.30")
        scolor = ask("    color", "cyan")
        sports.append((sname, sdays, stime, srange, scolor))

    return {"label": label, "from": norm_md(a), "to": norm_md(b),
            "classes": classes, "imm": imm, "sports": sports}


def main():
    print("=" * 56)
    print("  SSA Smart Schedule - Personal Schedule Converter")
    print("=" * 56)
    print("Tip: reuse a friend's answers; often only one class differs.\n")

    name = ask("Student full name", "Pei Lin Zhong")
    grade = ask("Grade (9/10/11/12)", "11")
    grade_word = GRADES.get(grade, "Junior")
    classyr = ask("Class year for filename folder (e.g. 27)", "27")
    last = ask("Last name for filename (e.g. zhongp = zhong + p)", "zhongp")

    print("\n--- Terms (add as many as needed) ---")
    terms = []
    defaults = [("Fall 2025", "08.26-01.16"), ("Spring 2026", "01.20-06.30")]
    i = 0
    while True:
        ld, rd = defaults[i] if i < len(defaults) else ("", "")
        print(f"\nTerm {i + 1}:")
        t = ask_term(ld, rd)
        if not t:
            break
        terms.append(t)
        i += 1
        if ask("Add another term? (y/n)", "n").lower() != "y":
            break

    print("\n--- Preferences ---")
    bg = ask("  Background color", "#0d0f14")
    hday = ask("  Highlight-day border color", "#ffffff")
    hclass = ask("  Highlight-class border color", "#ffd23f")
    tfmt = ask("  Time format (12h/24h)", "12h")

    out = [name, f"{classyr} - {grade_word}", ""]
    for t in terms:
        out.append(f"@term {t['label']} = {t['from']}-{t['to']}")
        for letter in PERIOD_LETTERS:
            if letter in t["classes"]:
                nm, num, sec, teacher, room, color = t["classes"][letter]
                out.append(f"{letter} - {nm} - {num} - {sec} - {teacher} - {room} - {color}")
        if t["imm"]:
            nm, num, teach, room, color = t["imm"]
            out.append(f"@immersive {nm} - {num} - {teach} - {room} - {color}")
        for s in t["sports"]:
            out.append(f"@sport {s[0]} - {s[1]} - {s[2]} - {s[3]} - {s[4]}")
        out.append("")
    out.append("@pref background = " + bg)
    out.append("@pref highlight_day = " + hday)
    out.append("@pref highlight_class = " + hclass)
    out.append("@pref time_format = " + tfmt)

    fname = f"{last}.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    print(f"\nWrote {fname}")
    print(f"Place it in: students/{classyr}/{fname}")
    print(f"Add to students/index.txt:  {classyr} | <Last> | <First> | students/{classyr}/{fname}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
        sys.exit(1)
