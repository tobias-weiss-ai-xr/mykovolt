# MykoVolt Paper Makefile
# Requires: xelatex, biber (or bibtex)

PAPER = mykovolt_paper1
BUILD_DIR = build

all: $(BUILD_DIR)/$(PAPER).pdf

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/$(PAPER).pdf: $(PAPER).tex | $(BUILD_DIR)
	cd $(BUILD_DIR) && xelatex -interaction=nonstopmode ../$(PAPER).tex
	cd $(BUILD_DIR) && bibtex $(PAPER) || true
	cd $(BUILD_DIR) && xelatex -interaction=nonstopmode ../$(PAPER).tex
	cd $(BUILD_DIR) && xelatex -interaction=nonstopmode ../$(PAPER).tex
	@echo "✅ Paper built: $(BUILD_DIR)/$(PAPER).pdf"

clean:
	rm -rf $(BUILD_DIR)

open: $(BUILD_DIR)/$(PAPER).pdf
	xdg-open $(BUILD_DIR)/$(PAPER).pdf 2>/dev/null || open $(BUILD_DIR)/$(PAPER).pdf

watch:
	@echo "Watching $(PAPER).tex for changes..."
	@while inotifywait -q -e modify $(PAPER).tex; do \
		make; \
	done

.PHONY: all clean open watch
