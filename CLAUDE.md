# Claude

## Project Overview

-   A tutorial on systems programming, networking, and related topics for data scientists who have been wrangling data with Python for years but have little or no formal training in computer science.
-   Learners are comfortable reading and writing classes and unit tests in Python,
    but have limited understanding of lower-level programming (e.g., C or Rust),
    and limited understanding of threading, networking, containers, and other systems-level issues.
-   Learners use an LLM as a coding assistant but write and debug code themselves.

## Structure

-   Lessons are written in Markdown and compiled to HTML using the `mccole` static site generator.
-   Boilerplate Markdown files:
    -   `CODE_OF_CONDUCT.md`
    -   `CONTRIBUTING.md`
    -   `LICENSE.md`
-   Lesson files:
    -   `README.md`: lesson home page (including table of contents used by `mccole`).
    -   `*/index.md`: lessons (see `README.md` for order).
    -   `docs`: generated HTML.
    -   `_extras/links.md`: Markdown link definitions included in all other Markdown files.
    -   `_static/`: web site assets.
    -   `_templates/`: `jinja2` page template.
-   Custom scripts are put in `bin/*.py`.
    -   This project has a `uv` virtual environment, so use `python` rather than `python3` to run commands.

## Build and Test Commands

-   Repeatable actions are saved in `Makefile`.
    -   Run `make` with no arguments to get an up-to-date list of targets.
-   `make site` rebuilds the website from the Markdown files.
-   `make html` checks the generated HTML (but is slow, so should only be used before `git commit`).

## Style Rules

-   `*/index.md` starts with a single H1-level heading (the lesson title).
-   The next line of `*/index.md` may be a subtitle paragraph.
-   Figures, code inclusions, citations, and glossary references are formatted using `mccole` shortcodes.
-   Lessons are written as point-form notes.
-   Do *not* use **bold** or *italics*.
-   Do *not* attempt to be funny or offer generic positive feedback to readers.
-   Use `[text][key]` format for external links, and define `key` in `_extras/links.md`.

## Interaction

-   Save a summary of prompts given and actions taken in files in `./log`
    with the date and time of the interaction in UTC.
-   Run shell commands that do not modify files without asking for permission.
