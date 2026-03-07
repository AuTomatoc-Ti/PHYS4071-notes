# Compiling the Cosmology Notes

## Prerequisites

Install a TeX distribution that includes the packages listed below.

| Platform | Recommended distribution |
|----------|--------------------------|
| macOS    | [MacTeX](https://www.tug.org/mactex/) — full install preferred |
| Linux    | TeX Live (`sudo apt install texlive-full`) |
| Windows  | [MiKTeX](https://miktex.org/) or TeX Live |

### Required LaTeX packages

All packages below are included in the **full MacTeX / TeX Live** install.
If you use a minimal install, add them individually via `tlmgr`.

| Package | Purpose |
|---------|---------|
| `mathpazo` | Palatino font for text + math |
| `microtype` | Microtypography |
| `geometry` | Page margins |
| `amsmath`, `amssymb`, `bm` | Mathematics |
| `xcolor` | Custom colors |
| `tikz` | Title page graphics |
| `tcolorbox` + `most`, `breakable` skins | Styled block boxes |
| `titlesec` | Section heading style |
| `fancyhdr` | Header / footer |
| `hyperref` | Clickable TOC links |
| `enumitem` | Bullet list style |
| `booktabs` | Professional tables |
| `lipsum` | Placeholder text (remove when done) |

---

## Compiling

Navigate to the `notes/` folder first:

```bash
cd /Users/automatocti/Documents/ust/course/PHYS4071/notes
```

> **macOS note:** MacTeX installs to `/usr/local/texlive/2025/bin/universal-darwin/`.
> If `pdflatex` is not on your `PATH`, either add that directory to `~/.zshrc`:
> ```bash
> export PATH="/usr/local/texlive/2025/bin/universal-darwin:$PATH"
> ```
> or call it with the full path (replace `pdflatex` with
> `/usr/local/texlive/2025/bin/universal-darwin/pdflatex` in the commands below).

### Option A — pdflatex (standard, recommended)

Run `pdflatex` **twice** so the table of contents and cross-references resolve:

```bash
pdflatex cosmology_notes.tex
pdflatex cosmology_notes.tex
```

Output: `cosmology_notes.pdf` in the same directory.

### Option B — latexmk (automatic, easiest)

`latexmk` handles the number of passes automatically:

```bash
latexmk -pdf cosmology_notes.tex
```

To continuously recompile on save (useful while writing):

```bash
latexmk -pdf -pvc cosmology_notes.tex
```

To clean up auxiliary files afterwards:

```bash
latexmk -c
```

### Option C — VS Code with LaTeX Workshop

1. Install the **LaTeX Workshop** extension (`James-Yu.latex-workshop`).
2. Open `cosmology_notes.tex` in VS Code.
3. Press **⌘⇧P** → `LaTeX Workshop: Build LaTeX project`.
4. The PDF preview opens automatically in the side panel.

Recommended `settings.json` snippet for the project:
```json
{
  "latex-workshop.latex.tools": [
    {
      "name": "pdflatex",
      "command": "pdflatex",
      "args": ["-interaction=nonstopmode", "-synctex=1", "%DOC%"]
    }
  ],
  "latex-workshop.latex.recipes": [
    {
      "name": "pdflatex × 2",
      "tools": ["pdflatex", "pdflatex"]
    }
  ]
}
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `tcolorbox` errors | Missing `tcolorbox` skins | Run `tlmgr install tcolorbox` |
| `mathpazo` not found | Missing `psnfss` bundle | `tlmgr install psnfss` |
| Starfield very slow | TikZ random loop | Normal on first run; subsequent runs use cache |
| `! Undefined control sequence` on `\lipsum` | `lipsum` not installed | `tlmgr install lipsum`, or delete placeholder lines |

---

## Workflow for Adding Content

Each section is structured with four **block environments**. Replace the
`\lipsum[...]` lines with real content:

```latex
\begin{intuition}
  Your plain-text motivation / history here.
\end{intuition}

\begin{theory}
  Detailed derivation, equations, assumptions.
\end{theory}

\begin{example}{Title of the question}{}
  Question statement.
  \medskip\textbf{Solution.}\quad Solution here.
\end{example}

\begin{extra}
  Side notes, fun facts, deeper references.
\end{extra}
```

> **Tip:** Remove `\usepackage{lipsum}` and all `\lipsum[...]` calls once
> sections are filled with real content.

---

## Adding a New Section

Copy-paste this template at the appropriate place in `cosmology_notes.tex`:

```latex
% ══════════════════════════════════════════════════════════════════════════════
%  §N  SECTION TITLE
% ══════════════════════════════════════════════════════════════════════════════
\section{Section Title}

\begin{intuition}
% ...
\end{intuition}
\bigskip

\begin{theory}
% ...
\end{theory}
\bigskip

\begin{example}{Question title}{}
% Question ...
\medskip\textbf{Solution.}\quad
% Solution ...
\end{example}
\bigskip

\begin{extra}
% ...
\end{extra}

\clearpage
```
