# Configuration file for the Sphinx documentation builder.
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', '..')))

project = 'MaskMaker'
copyright = '2024, Kollar Lab'
author = 'Kollar Lab'
release = '2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.viewcode',
              ]

master_doc = 'index'
toc_object_entries_show_parents = 'hide'
add_module_names = False
templates_path = ['_templates']
exclude_patterns = []
autodoc_mock_imports = ['ezdxf']
suppress_warnings = ['docutils']
autosummary_generate = True



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['css/custom_style.css']
html_theme_options = {
    "show_nav_level": 1,
    "primary_sidebar_end": ["indices.html"],
    "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
    "navbar_align": "right",
    "navigation_depth": 2,
    "icon_links":[
        {
            "name": "Github",
            "url" : "https://github.com/KollarLab/MaskMaker",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        }
    ]
}

html_sidebars = {
    '**': [
        'globaltoc.html',
        'sourcelink.html',
        'searchbox.html',
    ], 
}