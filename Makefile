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

## profile: render with profiling
profile:
	mccole profile ${CSS}
	@touch docs/.nojekyll

## refresh: refresh all file inclusions
refresh:
	mccole refresh --files *_*/index.md

## serve: serve generated HTML
serve:
	@python -m http.server -d docs $(PORT)

## stats: basic site statistics
stats:
	@mccole stats
