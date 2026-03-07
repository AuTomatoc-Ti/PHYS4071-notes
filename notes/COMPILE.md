# Compiling the Notes

There are two note sets:

| Target keyword | Folder |
|---|---|
| `phys4071` | `notes/phys4071_notes/` |
| `template` | `notes/template/` |

---

## Running from `notes/` (top-level dispatcher)

```bash
cd notes/

# Compile once
./compile.sh phys4071
./compile.sh template

# Compile and immediately open the PDF (macOS)
./compile.sh phys4071 --open
./compile.sh template --open

# Watch mode — recompiles on every file save (requires latexmk)
./compile.sh phys4071 --watch
./compile.sh template --watch

# Remove all auxiliary files (.aux, .bbl, .log, etc.)
./compile.sh phys4071 --clean
./compile.sh template --clean
```

If called with no arguments, the script prompts you to choose a target interactively.

---

## Running from inside a note folder

Each subfolder has its own `compile.sh` that accepts the same flags:

```bash
cd notes/template/
./compile.sh            # compile once
./compile.sh --open     # compile + open PDF
./compile.sh --watch    # watch mode
./compile.sh --clean    # clean aux files
```

```bash
cd notes/phys4071_notes/
./compile.sh
./compile.sh --open
./compile.sh --watch
./compile.sh --clean
```

---

## How compilation works

The script automatically detects `latexmk` from the TeXLive installation and runs a full `pdflatex → biber → pdflatex → pdflatex` cycle so that bibliography citations (`\citep`, `\cite`) resolve correctly.

If `latexmk` is unavailable, it falls back to calling `pdflatex` and `biber` manually in the correct order.

Output PDF is written to the same folder as `main.tex`.

---

## Requirements

- **MacTeX 2025** (or any TeX Live 2025 installation) at `/usr/local/texlive/2025/`
- Packages used: `tcolorbox`, `titlesec`, `biblatex` (with `biber` backend), `tikz`, `fancyhdr`, `hyperref`, `booktabs`

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `pdflatex: command not found` | TeXLive bin not in `PATH` | The script adds it automatically; re-run `./compile.sh` |
| Citations show `[?]` or `(Author Year)` | biber not run | Run `./compile.sh --clean` then recompile |
| Missing image warnings | `images/` folder empty | Add figure files or comment out `\includegraphics` lines |
| `latexmk: command not found` | Not in `PATH` | The script locates it inside TeXLive automatically |

├── COMPILE.md                    ← this file
│
├── template/                     ← read-only reference with placeholder lipsum content
│   ├── compile.sh                ← folder-level compile script
│   ├── main.tex                  ← document root (\documentclass + \input chapters)
│   ├── preamble.tex              ← all packages, colours, environments, macros
│   ├── references.bib            ← BibTeX entries
│   ├── images/                   ← figures
│   └── chapters/
│       ├── intro.tex
│       ├── ch01_expanding_universe.tex
│       ├── ch02_friedmann_equations.tex
│       ├── ch03_energy_budget.tex
│       └── appendix.tex
│
└── phys4071_notes/      # Compiling the Cosmology Notes

## File Structure

```
notes/
├── compile.sh   ??
## File Structure

```
notes/le.
```
notes/
├?rnoer├?b├── COMPILE.md                    ← this file
│
├── template/    │
├── template/                     ← read??????   ├iedmann_equations.tex
        ├── ch03_energy_budget.tex
        └── append│   ├── main.tex                  ← document root (\documentcl t│   ├── preamble.tex              ← all packages, colours, environments, macros
│Us│   ├── references.bib            ← BibTeX entries
│   ├── images/    le│   ├── images/                   ← figures
│   t│   └── chapters/
│       ├── intro.`b│       ├── intr .│       ├── ch01_exppi│  ript Flags

| Flag | Description |
|------|│       ├── ch03_energy_budget.tex
│ it│       └── appendix.tex
│
└?r│
└── phys4071_notes/  ` ?e
## File Structure

```
notes/
├── compile.sh   ??
## F PD
```
notes/
├?Exnopl├?`## File Structure

```
n71
```
notes/le.
`mpino a```
notePDno./├?e│
├── template/    │
├── template/                    cl? ├── template/      to        ├── ch03_energy_budget.tex
        └── append│   ├── mah         └── append│   ├──ks│Us│   ├── references.bib            ← BibTeX entries
│   ├── images/    le│   ├── images/                   ← figures
│   t│   └── chapters/
│ ???  tex → pdflatex → pdflatex`

If `pdflatex`/`latexmk` are not on `PATH`, the script falls back to
the MacTeX default path `/usr/local/texlive/│       ├── intro.`b│ a
| Flag | Description |
|------|│       ├── ch03_energy_budget.tex
│ it│       └─? >|------|│       ├zs│ it│       └── appendix.tex
│
└?rte│
└?r│
└── phys4071_note e.g. └─?a## File Structure

```
notes/
?h
```
notes/
├?tsnoit├? ## F PD
```
notes/
?ck st```
noe belo├? R
```
n71
```
notes/le.
`mpino a```comn7le``h noys`mpino aatnotePDno./ve├── template/r-├── template/      

        └── append│   ├── mah         └── append│   ├──ks│Us│   ├── referon│   ├── images/    le│   ├── images/                   ← figures
│   t│   └── chapters/
│ ???  tex → pdflatex → pon│   t│   └── chapters/
│ ???  tex → pdflde notes, deeper references│ ???  tex → pdflatex → New Chapter

1. Create `chapters/ch04_your_tthe MacTeX default path `/usr/local/texlive/│       ├── in b| Flag | Description |
|------|│       ├── ch03_energy_budget.tex
?7|------|│       ?en │ it│       └─? >|------|│       ├zser│
└?rte│
└?r│
└── phys4071_note e.g. └─?a## File Structure

``\l?l└?label}}└─?u
```
notes/
?h
```
notes/
├?tsnoit├? ## F PD
`1. nost?h
*L```X nork├?* ```
notes/
?ck st```
nop`no
2?ck n noe belin.t```
n71
```
no??n7* ``? noaT`mpino aho
        └── append│   ├── mah         └── append│   ├──ks│Us?pes": [
    {
      "name": "pdflatex → bibtex → pdflatex × 2",
      "tools": ["pdflatex", "bibtex", "pdflatex", "pdflatex"]
    }
  ],
  "latex-workshop.latex.tools": [
    { "name": "pdflate│ ???  tex → pdflatex →  │ ???  tex → pdflde notes, deeper references│ ???  tex ?{
1. Create `chapters/ch04_your_tthe MacTeX default path `/usr/local/texlive/│       ├─isi|------|│       ├── ch03_energy_budget.tex
?7|------|│       ?en │ it│       └─? >|------|│     la?7|------|│       ?en │ it│       └─ge└?rte│
└?r│
└── phys4071_note e.g. └─?a## File Structure

 |└?r│

|└─? 
``\e page |
| `tcolorbox` + `most`, `breakable` | Block b```
notes/
?h
```
notes/
?hnodi?h

|```annohd├?He`1. nost?h
*L```X norkre*L```X norkblnotes/
?ck st```
no +?ck eXnop`no
2?c2?ck| n71
```
no??n7* ``? s`,``danoti        └── append?Placeholder (template only — remove when done) |

---

## Troubleshooting

| Symptom | Likely cause     x       "tools": ["pdflatex", "bibtex", "pdflatex", "pds     }
  ],
  "latex-workshop.latex.tools": [
    { "name": "ot  ],nd  "Mi    { "name": "pdflate│ ??? ps1. Create `chapters/ch04_your_tthe MacTeX default path `/usr/local/texlive/│       ├─isi|------|│       ├──  W?7|------|│       ?en │ it│       └─? >|------|│     la?7|------|│       ?en │ it│       └─ge└?rte│
└?r│ps└?r│
└── phys4071_note e.g. └─?a## File Structure

 |└?r│

|└─? 
``\e page |
| `tcolorbox` + `most`, `brno└?nd` | PATH not set | Add MacTeX bin to `~/.zshrc` (see above) |
