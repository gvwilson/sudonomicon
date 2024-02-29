DOCS := docs
OUT := out
PAGES := pages
SITE := site
SRC := src
TEMPLATE := lib/tut

## --- : ---

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## build: rebuild website
.PHONY: build
build:
	@ark build
	@rm -rf ${DOCS}/${SRC} ${DOCS}/${OUT} ${DOCS}/${SITE} && cp -r ${SRC} ${OUT} ${SITE} ${DOCS}

## serve: rebuild and serve website
.PHONY: serve
serve:
	@ark serve

## lint: check project state
.PHONY: lint
lint:
	@python ${TEMPLATE}/bin/lint.py \
	--glossary info/glossary.yml \
	--lang $$(python config.py lang) \
	--makefile Makefile \
	--output ${OUT} \
	--page ${PAGES}/index.md \
	--source ${SRC} \
	--unused ${UNUSED}

## ordered: get all inclusions in order
.PHONY: ordered
ordered:
	@python ${TEMPLATE}/bin/ordered.py < ${PAGES}/index.md

## count: count items
.PHONY: count
count:
	@python ${TEMPLATE}/bin/count.py < ${PAGES}/index.md

## style: check Python code style
.PHONY: style
style:
	@ruff check .

## reformat: reformat unstylish Python code
.PHONY: reformat
reformat:
	@ruff format .

## clean: clean up stray files
.PHONY: clean
clean:
	@find . -name '*~' -exec rm {} \;
	@find . -name '*.bkp' -exec rm {} \;
	@find . -name '.*.dtmp' -exec rm {} \;
	@find . -type d -name __pycache__ | xargs rm -r
