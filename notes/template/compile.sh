#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
#  compile.sh — compile main.tex in this directory
#
#  Usage:
#    ./compile.sh            compile once (uses latexmk if found, else 4-pass)
#    ./compile.sh --clean    remove all auxiliary files
#    ./compile.sh --watch    recompile on every save (requires latexmk)
#    ./compile.sh --open     compile then open the PDF (macOS)
#
#  Run from INSIDE the folder that contains main.tex, e.g.:
#    cd notes/template  &&  ./compile.sh
#    cd notes/phys4071_notes  &&  ./compile.sh
# ══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── Resolve script directory (works whether called via ./compile.sh or a path)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Ensure TeXLive binaries are on PATH ───────────────────────────────────────
TEXLIVE_BIN="/usr/local/texlive/2025/bin/universal-darwin"
[[ -d "$TEXLIVE_BIN" ]] && export PATH="$TEXLIVE_BIN:$PATH"

MAIN="main"
PDF="${MAIN}.pdf"

# ── Locate pdflatex (MacTeX default path as fallback) ─────────────────────────
PDFLATEX="$(command -v pdflatex 2>/dev/null \
            || echo "/usr/local/texlive/2025/bin/universal-darwin/pdflatex")"
BIBER="$(command -v biber 2>/dev/null \
         || echo "/usr/local/texlive/2025/bin/universal-darwin/biber")"
LATEXMK="$(command -v latexmk 2>/dev/null \
           || echo "/usr/local/texlive/2025/bin/universal-darwin/latexmk")"

# ── Colour helpers ─────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓  $*${NC}"; }
warn() { echo -e "${YELLOW}⚠  $*${NC}"; }
err()  { echo -e "${RED}✗  $*${NC}"; exit 1; }

# ── Validate main.tex exists ──────────────────────────────────────────────────
[[ -f "${MAIN}.tex" ]] || err "main.tex not found in $(pwd). Are you in the right folder?"

# ── Argument dispatch ─────────────────────────────────────────────────────────
case "${1:-}" in

  --clean)
    echo "Cleaning auxiliary files in $(pwd)…"
    rm -f ${MAIN}.{aux,bbl,bcf,blg,fdb_latexmk,fls,log,out,run.xml,synctex.gz,toc}
    ok "Clean done."
    exit 0
    ;;

  --watch)
    if [[ -z "$LATEXMK" || ! -x "$LATEXMK" ]]; then
      err "--watch requires latexmk (install via: tlmgr install latexmk)"
    fi
    warn "Watching ${MAIN}.tex for changes — press Ctrl-C to stop."
    exec "$LATEXMK" -pdf -pvc -interaction=nonstopmode "${MAIN}.tex"
    ;;

  --open)
    # Compile then open PDF (macOS only)
    "$0"                       # recursive call without flag = compile
    [[ -f "$PDF" ]] && open "$PDF"
    exit 0
    ;;

  "")
    # Default: compile once
    ;;

  *)
    echo "Usage: $0 [--clean | --watch | --open]"
    exit 1
    ;;
esac

# ── Compile ───────────────────────────────────────────────────────────────────
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Compiling  $(pwd)/${MAIN}.tex"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run pdflatex but treat the result as success if the PDF was produced
# (package-level errors like titlesec/biblatex warnings cause non-zero exits
#  while still generating a valid PDF)
pdf_run() {
  "$PDFLATEX" -interaction=nonstopmode "${MAIN}.tex" || true
  [[ -f "${MAIN}.pdf" ]] || err "pdflatex failed to produce ${MAIN}.pdf — check ${MAIN}.log"
}

if [[ -n "$LATEXMK" && -x "$LATEXMK" ]]; then
  ok "Using latexmk (automatic passes)"
  "$LATEXMK" -pdf -interaction=nonstopmode "${MAIN}.tex" || true
  [[ -f "${MAIN}.pdf" ]] || err "latexmk failed to produce ${MAIN}.pdf — check ${MAIN}.log"
else
  warn "latexmk not found; falling back to 4-pass manual compile (pdflatex + biber)"
  pdf_run   # pass 1
  "$BIBER" "${MAIN}" 2>/dev/null || warn "biber had warnings (check ${MAIN}.blg)"
  pdf_run   # pass 2
  pdf_run   # pass 3 (resolves cross-references)
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "Done!  Output → $(pwd)/${PDF}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
