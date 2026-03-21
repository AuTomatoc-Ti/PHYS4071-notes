#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
#  compile.sh — compile main.tex in this directory
#
#  Usage:
#    ./compile.sh            compile once (uses latexmk if found, else 4-pass)
#    ./compile.sh --quick    quick compile (single pdflatex pass, no bibliography)
#    ./compile.sh --lite     compile simplified file (image pages only, much faster)
#    ./compile.sh --clean    remove all auxiliary files
#    ./compile.sh --watch    recompile on every save (requires latexmk)
#    ./compile.sh --open     compile then open the PDF (macOS)
#    ./compile.sh --open-only open existing PDF without compiling
# ══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

TEXLIVE_BIN="/usr/local/texlive/2025/bin/universal-darwin"
[[ -d "$TEXLIVE_BIN" ]] && export PATH="$TEXLIVE_BIN:$PATH"

MAIN="main"
PDF="${MAIN}.pdf"

PDFLATEX="$(command -v pdflatex 2>/dev/null || echo "/usr/local/texlive/2025/bin/universal-darwin/pdflatex")"
BIBER="$(command -v biber 2>/dev/null || echo "/usr/local/texlive/2025/bin/universal-darwin/biber")"
LATEXMK="$(command -v latexmk 2>/dev/null || echo "/usr/local/texlive/2025/bin/universal-darwin/latexmk")"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓  $*${NC}"; }
warn() { echo -e "${YELLOW}⚠  $*${NC}"; }
err()  { echo -e "${RED}✗  $*${NC}"; exit 1; }

[[ -f "${MAIN}.tex" ]] || err "main.tex not found in $(pwd). Are you in the right folder?"

CLEAN=0
WATCH=0
OPEN_AFTER=0
QUICK=0
OPEN_ONLY=0
LITE=0

generate_lite_tex() {
  local source_file="main.tex"
  local lite_file="main_lite.tex"

  [[ -f "$source_file" ]] || err "$source_file not found"

  {
    cat <<'EOF'
\documentclass{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage[a4paper,margin=10mm]{geometry}
\pagestyle{empty}
\begin{document}
EOF

    grep -o 'latexImage_[A-Za-z0-9]*\.png' "$source_file" | awk '!seen[$0]++ {
      print "\\begin{center}";
      print "\\includegraphics[width=\\linewidth,height=0.95\\textheight,keepaspectratio]{" $0 "}";
      print "\\end{center}";
      print "\\newpage";
    }'

    cat <<'EOF'
\end{document}
EOF
  } > "$lite_file"

  ok "Generated $lite_file from image pages in $source_file"
}

open_pdf() {
  if open -a Preview "$PDF" >/dev/null 2>&1; then
    ok "Opened ${PDF}"
    return 0
  fi
  if open "$PDF" >/dev/null 2>&1; then
    ok "Opened ${PDF}"
    return 0
  fi
  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --clean) CLEAN=1 ;;
    --watch) WATCH=1 ;;
    --open) OPEN_AFTER=1 ;;
    --open-only) OPEN_ONLY=1 ;;
    --quick) QUICK=1 ;;
    --lite) LITE=1 ;;
    *)
      echo "Usage: $0 [--clean] [--watch] [--open] [--open-only] [--quick] [--lite]"
      exit 1
      ;;
  esac
  shift
done

if [[ $LITE -eq 1 ]]; then
  generate_lite_tex
  MAIN="main_lite"
  PDF="${MAIN}.pdf"
fi

if [[ $OPEN_ONLY -eq 1 ]]; then
  [[ -f "$PDF" ]] || err "${PDF} not found. Run ./compile.sh first."
  open_pdf || err "Could not open ${PDF}."
  exit 0
fi

if [[ $CLEAN -eq 1 ]]; then
  echo "Cleaning auxiliary files in $(pwd)…"
  rm -f ${MAIN}.{aux,bbl,bcf,blg,fdb_latexmk,fls,log,out,run.xml,synctex.gz,toc}
  rm -f main_lite.{aux,bbl,bcf,blg,fdb_latexmk,fls,log,out,run.xml,synctex.gz,toc,pdf,tex}
  ok "Clean done."
  exit 0
fi

if [[ $WATCH -eq 1 ]]; then
  if [[ -z "$LATEXMK" || ! -x "$LATEXMK" ]]; then
    err "--watch requires latexmk (install via: tlmgr install latexmk)"
  fi
  warn "Watching ${MAIN}.tex for changes — press Ctrl-C to stop."
  exec "$LATEXMK" -pdf -pvc -interaction=nonstopmode -halt-on-error -file-line-error "${MAIN}.tex"
fi

if [[ $OPEN_AFTER -eq 1 && -f "$PDF" ]]; then
  warn "Opening existing ${PDF} now while compilation runs..."
  open_pdf || warn "Could not auto-open existing ${PDF}."
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Compiling  $(pwd)/${MAIN}.tex"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

pdf_run() {
  "$PDFLATEX" -interaction=nonstopmode -halt-on-error -file-line-error "${MAIN}.tex"
  [[ -f "${MAIN}.pdf" ]] || err "pdflatex failed to produce ${MAIN}.pdf — check ${MAIN}.log"
}

if [[ $QUICK -eq 1 ]]; then
  warn "Quick mode enabled: single pdflatex pass (references/bibliography may be incomplete)"
  pdf_run
elif [[ -n "$LATEXMK" && -x "$LATEXMK" ]]; then
  ok "Using latexmk (automatic passes)"
  "$LATEXMK" -pdf -interaction=nonstopmode -halt-on-error -file-line-error -silent "${MAIN}.tex"
  [[ -f "${MAIN}.pdf" ]] || err "latexmk failed to produce ${MAIN}.pdf — check ${MAIN}.log"
else
  warn "latexmk not found; falling back to 4-pass manual compile (pdflatex + biber)"
  pdf_run
  "$BIBER" "${MAIN}" 2>/dev/null || warn "biber had warnings (check ${MAIN}.blg)"
  pdf_run
  pdf_run
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "Done!  Output → $(pwd)/${PDF}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ $OPEN_AFTER -eq 1 ]]; then
  if ! open_pdf; then
    warn "Could not auto-open ${PDF}; please open it manually."
  fi
fi
