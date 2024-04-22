# Tutorial data.
title = "The Sudonomicon"
subtitle = "Unix Systems for Weary Data Scientists"
repo = "https://github.com/gvwilson/sys-tutorial"
site = f"https://gvwilson.github.io/sys-tutorial/"
release = "https://github.com/gvwilson/sys-tutorial/raw/main/sys-tutorial.zip"
plausible = "gvwilson.github.io/sys-tutorial"
author = {
    "name": "Greg Wilson",
    "email": "gvwilson@third-bit.com",
    "site": "https://third-bit.com/",
}
lang = "en"
highlight = "tango.css"
slug = "systut"

chapters = [
    "intro",
    "fs",
    "proc",
    "jobs",
    "http",
    "auth",
    "virt",
    "finale",
]

appendices = [
    "license",
    "conduct",
    "contrib",
    "bib",
    "glossary",
    "author",
    "colophon",
]

# What to copy.
copy = [
    "*.svg",
]

# Files and directories to skip.
exclude = {
    "virt/python3_interpreter",
    "virt/ubuntu_python3",
}

# Theme information.
theme = "mccole"
src_dir = "src"
out_dir = "docs"
extension = "/"

# Enable various Markdown extensions.
markdown_settings = {
    "extensions": [
        "markdown.extensions.extra",
        "markdown.extensions.smarty",
        "pymdownx.superfences",
    ]
}

# Show theme.
if __name__ == "__main__":
    print(theme)
