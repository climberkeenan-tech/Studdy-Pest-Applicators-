#!/bin/bash
# Browser tests of the reader and of saved progress: the recorded voice, the live Claude voice (a stand-in for
# it), bad connections, progress saved across devices and tabs, and the day streak over a moved calendar. Run them after any change to the reader or the storage code in app/template.html:
#
#     python3 tools/build.py && tools/browser/run.sh
#
# Needs Playwright (require('playwright') must work in node) and the Chapter 1 recordings in dist/audio.
# In a new container, get the recordings first: tools/narrate.py --chapters ch01,practice (see CLAUDE.md).
# One test alone:  node tools/browser/rec.js <site dir> [scenario]   (run.sh prints the site dir it made)
set -u
cd "$(dirname "$0")/../.."
site=$(mktemp -d)
python3 tools/narrate.py --chapters ch01,practice --stage "$site" || exit 1
if [ "$(find "$site/audio" -name '*.mp3' | wc -l)" -lt 26 ]; then
  echo "Chapter 1 is not fully recorded in dist/audio: record it first (tools/narrate.py --chapters ch01,practice)"
  exit 1
fi
cp dist/pest-study.html "$site/pest-study.html"
echo "site: $site"
fail=0
run() {
  echo "== $1"
  shift
  out=$(node "$@" 2>&1)
  code=$?
  echo "$out" | grep -E '^FAIL|checks passed' | cut -c1-400
  if [ $code -ne 0 ]; then fail=1; fi
}
run "recorded voice"                    tools/browser/rec.js "$site"
run "Claude voice (stand-in)"           tools/browser/claude.js "$site"
run "stalled and dead connections"      tools/browser/cold.js "$site"
run "saved progress, taps before load"  tools/browser/sync.js "$site/pest-study.html"
run "saved progress, failed first read" tools/browser/sync2.js "$site/pest-study.html"
run "progress across devices, day streak" tools/browser/progress.js "$site"
if [ $fail -eq 0 ]; then echo "all browser tests passed"; rm -rf "$site"; else echo "FAILED (site kept: $site)"; fi
exit $fail
