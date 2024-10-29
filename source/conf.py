import os
import sys
sys.path.insert(0, os.path.abspath('../'))  


# Configuration file for the Sphinx documentation builder.

project = 'RPG Game'
copyright = '2024, vitalinc & gerrickl (galbats)'
author = 'vitalinc & gerrickl (galbats)'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
]


templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']
