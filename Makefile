# Runnable tasks.

include common.mk

all: commands

HTML_IGNORES = 

## build: convert to HTML
build:
	mccole build ${CSS}
	@touch docs/.nojekyll

## lint: check code and project
lint:
	@ruff check --exclude docs .
	@mccole lint --html

## refresh: refresh all file inclusions
refresh:
	mccole refresh --files *_*/index.md

## serve: serve generated HTML
serve:
	@python -m http.server -d docs $(PORT)

## spelling: check for unknown words
spelling:
	@cat *.md */*.md | aspell list | sort | uniq | diff - extras/words.txt
