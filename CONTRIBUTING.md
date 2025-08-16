# Contributing

Contributions are very welcome;
please contact us [by email][email] or by filing an issue in [our repository][repo].
All contributors must abide by our [Code of Conduct](./CODE_OF_CONDUCT.md).

## Setup and Operation

-   Install [uv][uv]
-   Create a virtual environment by running `uv venv` in the root directory
-   Activate it by running `source .venv/bin/activate` in your shell
-   Install dependencies by running `uv pip install -r pyproject.toml`
-   This project uses [McCole][mccole] to generate HTML and check the project's structure
-   Run `make` on its own to see a list of common commands

| make task | effect                                   |
| --------- | ---------------------------------------- |
| clean     | clean up                                 |
| commands  | show available commands (default)        |
| lint      | check code and project                   |
| render    | convert to HTML                          |
| serve     | serve generated HTML                     |
| stats     | basic site statistics                    |

-   If you are on MacOS you may want to use [Homebrew][homebrew] to install:
    -   `fswatch`
    -   `pstree`
    -   `tree`
    -   `watch`

## Labels

| Name             | Description                  | Color   |
| ---------------- | ---------------------------- | ------- |
| change           | something different          | #FBCA04 |
| feature          | new feature                  | #B60205 |
| fix              | something broken             | #5319E7 |
| good first issue | newcomers are always welcome | #D4C5F9 |
| talk             | question or discussion       | #0E8A16 |
| task             | one-off task                 | #1D76DB |

Please use [Conventional Commits][conventional] style for pull requests
by using `change:`, `feature:`, `fix:`, or `task:` as the first word
in the title of the commit message.
You may also use `publish:` if the PR just rebuilds the HTML version of the lesson.

## FAQ

Do you need any help?
:   Yes—please see the issues in [our repository][repo].

What sort of feedback would be useful?
:   Everything is welcome,
    from pointing out mistakes in the code to suggestions for better explanations.

Can I add a new section?
:   Absolutely, but please [reach out][email] before doing so.

Why is this material free to read?
:   Because if we all give a little, we all get a lot.

## Colophon

-   The CSS files used to style code were obtained from [highlight-css][highlight_css];
    legibility was checked using [WebAIM WAVE][wave].

-   Diagrams were created with the desktop version of [draw.io][draw_io].

-   The site is hosted on [GitHub Pages][ghp].

-   Thanks to the authors of [BeautifulSoup][bs4],
    [html5validator][html5validator],
    [ruff][ruff],
    and all the other software used in this project.
    If we all give a little,
    we all get a lot.

[bs4]: https://pypi.org/project/beautifulsoup4/
[conventional]: https://www.conventionalcommits.org/
[draw_io]: https://www.drawio.com/
[email]: mailto:gvwilson@third-bit.com
[ghp]: https://pages.github.com/
[highlight_css]: https://numist.github.io/highlight-css/
[homebrew]: https://brew.sh/
[html5validator]: https://pypi.org/project/html5validator/
[mccole]: https://pypi.org/project/mccole/
[repo]: https://github.com/lessonomicon/sudonomicon
[ruff]: https://astral.sh/ruff
[uv]: https://docs.astral.sh/uv/
[wave]: https://wave.webaim.org/
