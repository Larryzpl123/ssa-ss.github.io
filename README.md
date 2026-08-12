# SSA Smart Schedule
Live demo at: [smartschedule.pythonanywhere.com](https://smartschedule.pythonanywhere.com/app).
A single‑page, offline‑capable web application for viewing the Shady Side Academy Senior School daily schedule. Built with vanilla HTML, CSS, and JavaScript.  
It handles the school’s **8‑day rotating cycle**, **immersive terms**, **community time**, **Wednesday late‑start**, **athletics**, and **school holidays** — all driven by plain‑text configuration files.

## Features

- 📅 **Week view** – Shows Monday through Friday, with cycle day number and day type (Normal, Wednesday, Immersive, No Class).
- 🔄 **Anchor‑based rotation** – Define fixed cycle‑day references (e.g., *September 5 is Day 7*) and the app calculates the entire year automatically.
- 🎨 **Student‑specific colors** – Each class block uses the color assigned in the student’s file.
- ⏱️ **Current‑time indicator** – A yellow line and highlighted “now” block.
- 👤 **Student search** – Search by first name, last name, class year, or username; loads that student’s schedule instantly.
- 🕒 **12h / 24h toggle** – Switch between AM/PM and 24‑hour time display.
- 📆 **Jump to any date** – Pick a specific day; the view jumps to that week.
- 📅 **Multi‑year support** – Drop‑down to choose school years (2025–26, 2026–27, …).
- 🏷️ **Legend** – Shows class‑color mapping for the selected student.
- 📦 **Fully offline** – Embedded fallback data for the school’s shared definitions, a sample student, and two sample years. No server required to explore the interface.
- 🔌 **Live data** – The repository already includes real text files for the schedule, calendar, and student data, so you can serve it locally and see live schedules.

--- 

## Quick start

1. **Serve the directory** with any static HTTP server (the app fetches configuration files):
   ```bash
   python -m http.server 8000
   # or
   npx serve .
   ```
2. Open `http://localhost:8000` in a modern browser.
   All required data files (`schedule.txt`, `calendar/*.txt`, `students/index.txt`, student files) are **already included** in the repository.
3. Navigate with the **arrow buttons**, **Today**, **Pick date**, or **keyboard** (`←`/`A` = previous week, `→`/`D` = next week).
4. Search for a student by typing in the **search box** — the student index is populated from `students/index.txt`.

> You can also open `index.html` directly (`file://`), but it will fall back to embedded sample data because `fetch()` is blocked on local files. For real data, always use a server.

---

## Repository file structure

```
.
├── calendar
│   ├── 2025-2026.txt
│   └── 2026-2027.txt
├── days
│   ├── final_exam_day.txt
│   ├── holiday.txt
│   ├── normal.txt
│   ├── review_day.txt
│   ├── standard-test-day.txt
│   └── wednesday.txt
├── students
│   ├── 27
│   │   └── zhongp.txt
│   └── index.txt
├── index.html
├── LICENSE
├── personal-schedule-converter.py
├── README.md
└── schedule.txt
```

- **`index.html`** – The entire application.
- **`schedule.txt`** – School‑wide definitions (cycle, community time, dismissals, etc.).
- **`calendar/`** – One text file per school year, defining date ranges and cycle anchors.
- **`days/`** – Template definitions for different day types (normal, Wednesday, final exams, etc.) — used as reference and by the converter script.
- **`students/`** – Individual student schedule files, organized by class year.
- **`personal-schedule-converter.py`** – Python script to convert exported personal schedules into the required `.txt` format.
- **`LICENSE`** – MIT license.

---

## Data format

### `schedule.txt` – school‑wide definitions
Shared across all students. Defines:
- **Community time** block (normal days, Mon–Fri labels)
- **Immersive community time** and immersive daily blocks
- **8‑day cycle** (`@day 1 = A:08:15-09:05 …`)
- **Wednesday late‑start remap** (`@wed 08:15 => 09:35-10:25`)
- **Dismissal times** (`@dismiss normal = 15:00`)
- **Late/Early** indication (`@latearly A=La B=Ea …`)
- Any **`@fixed`** blocks that appear on all school days

Example snippet:
```
@community time = 10:05-10:30
@community Mon = Assembly
@community Tue = Advisory
@community Wed =
@community Thu = Club Time
@community Fri = Assembly

@day 1 = A:08:15-09:05 B:09:10-10:00 C:10:35-11:45 …
```

### `calendar/<year>.txt` – yearly calendar
Uses date ranges and optional anchors.
- **Anchors**: `@anchor YYYY-MM-DD = <cycle-day>` fixes a specific date’s cycle day.
- **Date ranges**: `MM.DD-MM.DD` optionally followed by `"description" type`  
  Types: `noclass`, `immersive`, or omitted for a normal school day.
- The app automatically computes cycle days for all normal school days based on the nearest anchor (if any) or starts counting from Day 1 on the first school day.

Example:
```
@anchor 2025-09-05 = 7

08.26-08.29                     # Normal days, days counted from anchor
09.01-09.01 "Labor Day" noclass
09.02-09.05                     # continues rotation
05.13-05.15 "Immersive" immersive
```

### `students/index.txt` – student manifest
One student per line, pipe‑separated:
```
<graduation-year> | <Last Name> | <First Name> | <path-to-student-file>
```
Example:
```
27 | Zhong | Pei Lin | students/27/zhongp.txt
```

### Student file (e.g., `zhongp.txt`)
Two header lines (name, form), then class assignments, sports, immersive project, and preferences.
- **Class block**: `A - AP Calculus BC - MA560 - 1 - Mrs. Yam - R 202 - blue`
- **`@immersive`**: immersive course name, number, teachers, room, color.
- **`@sport`**: sport name, days, time range, date range (MM.DD-MM.DD), color.
- **`@latearly`**, **`@day 1‑8`**: can override school definitions; usually inherited from `schedule.txt`.
- **`@pref`**: personal preferences (`background`, `highlight_class`, `highlight_day`, `time_format`). If omitted, school‑wide defaults apply.

Example snippet:
```
Pei Lin Zhong
Junior - Upper Form
A - AP Calculus BC - MA560 - 1 - Mrs. Yam - R 202 - blue
B - French 2 - FR200 - 1 - Ms. Lembrechts - C 3 - green
…
@sport Swimming - Mon,Thu - 15:45-17:15 - 09.01-11.30 - cyan
@immersive Your Move - IM327 - Mr. Solomon, Ms. Wang, M. Roland - MC 110 - indigo
@pref time_format = 12h
```

---

## Customization

- **Add a new year**: create `calendar/2027-2028.txt` and add an entry to the `YEARS` array in `index.html` (or modify the embedded `EMBED` object).
- **Change school‑wide definitions**: edit `schedule.txt` (or the embedded `EMBED.school` string).
- **Add student files**: place the `.txt` files in `students/` and update `students/index.txt`.
- **Modify colors**: define custom color names in the `COLOR_MAP` dictionary inside the `<script>` tag.
- **Convert personal schedules**: Use `personal-schedule-converter.py` to transform exported personal schedule data into the expected student file format. The `days/` folder contains templates that the converter may reference.

---

## Technical notes

- The schedule is recalculated entirely in the browser; no backend is needed.
- The time axis spans **08:00–18:00** and uses a fixed pixel‑per‑minute ratio.
- The app uses `dialog.showModal()` for the date picker and `fetch` with `cache: "no-store"` to always load fresh files when served locally.
- Keyboard shortcuts (`←` / `A` and `→` / `D`) work only when no input is focused.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
