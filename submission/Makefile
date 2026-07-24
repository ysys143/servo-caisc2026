# SERVO v5 single build path (post-submission revision).
#
# This Makefile builds the v5 POST-SUBMISSION REVISION (main_post-submit) and its
# supplementary-material bundle in one deterministic path.
#
# It deliberately does NOT rebuild the archival version of record: main.tex /
# servo_caiscfp2026.pdf is the submitted/archived paper and is left untouched by the
# v5 reconstruction. The version of record is the OpenReview camera-ready; this
# revision is a dated correction that ships alongside it.

PY          := .venv/bin/python
TEX_BIN     := /usr/local/texlive/2026basic/bin/universal-darwin
XELATEX     := $(TEX_BIN)/xelatex
BIBTEX      := $(TEX_BIN)/bibtex
REVISION    := main_post-submit
DIST        := servo_caiscfp2026_post-submit
# Frozen source corpus (the six case PDFs). Override on the command line if needed:
#   make verify SOURCE_ROOT=/path/to/ai_scientist
SOURCE_ROOT ?= /Users/jaesolshin/Documents/GitHub/ai_scientist

.PHONY: revision tables provenance verify pdf supplement release-verify clean help

## revision: full deterministic v5 build (tables -> pdf -> provenance -> supplement -> verify)
revision: tables pdf provenance supplement verify
	@echo "OK: v5 revision built ($(REVISION).pdf + caisc2026-servo-supplement.zip)"

## tables: regenerate the v5 evidence tables (policy A, boundary B1, relations B2) + manifest
tables:
	$(PY) analysis/build_servo_v5_tables.py

## provenance: emit the M8 root manifest binding source->...->tables->PDF->supplement
## (run after tables and pdf so the bound table/tex/PDF hashes are fresh)
provenance:
	$(PY) -m analysis.servo_v5_provenance --submission-root . --emit

## verify: source-freeze gate + provenance internal chain + v5 test suite (fail-closed)
verify:
	$(PY) -m analysis.servo_v5_freeze --root . --source-root $(SOURCE_ROOT)
	$(PY) -m analysis.servo_v5_provenance --submission-root . --verify
	$(PY) -m pytest analysis/tests/servo_v5 -q

## pdf: compile the revised manuscript (xelatex + bibtex + 2x resolve)
pdf:
	$(XELATEX) -interaction=nonstopmode $(REVISION).tex
	-$(BIBTEX) $(REVISION)
	$(XELATEX) -interaction=nonstopmode $(REVISION).tex
	$(XELATEX) -interaction=nonstopmode $(REVISION).tex
	@grep -q "Output written on $(REVISION).pdf" $(REVISION).log \
	  && ! grep -q "^!" $(REVISION).log \
	  && echo "OK: $(REVISION).pdf compiled with no errors" \
	  || (echo "FAIL: compile error or no output in $(REVISION).log" && exit 1)
	rm -f $(DIST).pdf && cp $(REVISION).pdf $(DIST).pdf
	@echo "OK: distribution copy $(DIST).pdf"

## supplement: deterministic supplementary-material zip (byte-reproducible leaf hash)
supplement:
	$(PY) -m analysis.servo_v5_supplement_zip --submission-root .

## release-verify: internal chain PLUS released-asset binding (release-cut gate;
## fails while the local tree is ahead of the published EXTERNAL_PUBLICATION assets)
release-verify:
	$(PY) -m analysis.servo_v5_provenance --submission-root . --verify-release

## clean: remove LaTeX aux files for the revision
clean:
	rm -f $(REVISION).aux $(REVISION).log $(REVISION).out $(REVISION).bbl $(REVISION).blg $(REVISION).toc

## help: list targets
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/^## //'
