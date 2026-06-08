"""Sphinx configuration."""

project = "dFizza"
author = "dfox3"
copyright = "2026, dfox3"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "shibuya"
