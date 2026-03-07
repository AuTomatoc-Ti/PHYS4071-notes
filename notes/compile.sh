#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
#  notes/compile.sh — top-level compile dispatcher
#
#  Usage:
#    ./compile.sh phys4071        compile notes/phys4071_notes/main.tex
#    ./compile.sh template        compile notes/template/main.tex
#    ./compile.sh phys4071 --watch     watch mode (requires latexmk)
#    ./compile.sh phys4071 --clean     remove auxiliary files
#    ./compile.sh phys4071 --open      compile and open PDF (macOS)
#
#  You can also run compile.sh directly inside each subfolder:
#    cd phys4071_notes  &&  ./compile.sh [flags]
#    cd template        &&  ./compile.sh [flags]
# ══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
err()  { echo -e "${RED}✗  $*${NC}"; exit 1; }
warn() { echo -e "${YELLOW}⚠  $*${NC}"; }

# ── Target selection ──────────────────────────────────────────────────────────
TARGET="${1:-}"
shift || true   # remaining args are passed through to the inner compile.sh

case "$TARGET" in
  phys4071|notes)
    TARGET_DIR="${SCRIPT_DIR}/phys4071_notes"
    ;;
  template|tmpl)
    TARGET_DIR="${SCRIPT_DIR}/template"
    ;;
  "")
    echo "Which set of notes do you want to compile?"
    echo "  1) phys4071_notes  (your real notes)"
    echo "  2) template        (the placeholder template)"
    read -rp "Enter 1 or 2: " choice
    case "$choice" in
      1) TARGET_DIR="${SCRIPT_DIR}/phys4071_notes" ;;
      2) TARGET_DIR="${SCRIPT_DIR}/template" ;;
      *) err "Invalid choice '$choice'" ;;
    esac
    ;;
  *)
    echo "Unknown target '${TARGET}'."
    echo "Usage: $0 [phys4071|template] [--clean|--watch|--open]"
    exit 1
    ;;
esac

# ── Delegate to the inner script ──────────────────────────────────────────────
[[ -f "${TARGET_DIR}/compile.sh" ]] \
  || err "compile.sh not found in ${TARGET_DIR}"

exec "${TARGET_DIR}/compile.sh" "$@"
