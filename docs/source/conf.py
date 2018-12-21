# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# sys.path.insert(0, os.path.abspath('.'))
import platform
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
import sys

import supy

print(r'this build is made by:', '\n', sys.version)


# -- Project information -----------------------------------------------------

project = u'SuPy'
doc_name = u'SuPy Documentation'
copyright = u'2018, Dr Ting Sun'
author = u'Dr Ting Sun'

# The short X.Y version
version = supy.__version__
# The full version, including alpha/beta/rc tags
release = supy.__version__


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'nbsphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    # 'rinoh.frontend.sphinx',
    # 'sphinxfortran.fortran_autodoc',
    # 'sphinxfortran.fortran_domain',
    'sphinx.ext.githubpages'

]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'
master_doc_latex = 'index_latex'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .

exclude_patterns = ['_build', '**.ipynb_checkpoints']
# tags.add('html')
# if tags.has('html'):
#     exclude_patterns = ['references.rst']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# default interpretation of `role` markups
default_role = 'any'

# some text replacement defintions
rst_prolog = """
.. |km^-1| replace:: km\ :sup:`-1`
.. |mm^-1| replace:: mm\ :sup:`-1`
.. |m^-1| replace:: m\ :sup:`-1`
.. |m^-2| replace:: m\ :sup:`-2`
.. |m^-3| replace:: m\ :sup:`-3`
.. |m^3| replace:: m\ :sup:`3`
.. |s^-1| replace:: s\ :sup:`-1`
.. |kg^-1| replace:: kg\ :sup:`-1`
.. |K^-1| replace:: K\ :sup:`-1`
.. |W^-1| replace:: W\ :sup:`-1`
.. |h^-1| replace:: h\ :sup:`-1`
.. |ha^-1| replace:: ha\ :sup:`-1`
.. |QF| replace:: Q\ :sub:`F`
.. |Qstar| replace:: Q\ :sup:`*`
.. |d^-1| replace:: d\ :sup:`-1`
.. |d^-2| replace:: d\ :sup:`-2`
.. |)^-1| replace:: )\ :sup:`-1`
.. |Recmd| replace:: **Recommended in this version.**
.. |NotRecmd| replace:: **Not recommended in this version.**
.. |NotAvail| replace:: **Not available in this version.**
.. |NotUsed| replace:: **Not used in this version.**
"""
# -- Options for HTML output -------------------------------------------------
# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_path = ["_themes"]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}
# This is processed by Jinja2 and inserted before each notebook
nbsphinx_prolog = r"""
{% set docname = env.doc2path(env.docname, base='docs') %}

.. only:: html

    .. role:: raw-html(raw)
        :format: html

    .. nbinfo::

        This page was generated from `{{ docname }}`__.
        Interactive online version:
        :raw-html:`<a href="https://mybinder.org/v2/gh/sunt05/SuPy/master?filepath={{ docname }}"><img alt="Binder badge" src="https://mybinder.org/badge.svg" style="vertical-align:text-bottom"></a>`
        Slideshow:
        :raw-html:`<a href="https://nbviewer.jupyter.org/format/slides/github/sunt05/SuPy/tree/master/{{ docname }}"><img alt="Binder badge" src="https://img.shields.io/badge/render-nbviewer-orange.svg" style="vertical-align:text-bottom"></a>`

    __ https://github.com/sunt05/SuPy/blob/master/{{ docname }}

.. raw:: latex

    \vfil\penalty-1\vfilneg
    \vspace{\baselineskip}
    \textcolor{gray}{The following section was generated from
    \texttt{\strut{}{{ docname }}}\\[-0.5\baselineskip]
    \noindent\rule{\textwidth}{0.4pt}}
    \vspace{-2\baselineskip}
"""

# This is processed by Jinja2 and inserted after each notebook
nbsphinx_epilog = r"""
.. raw:: latex

    \textcolor{gray}{\noindent\rule{\textwidth}{0.4pt}\\
    \hbox{}\hfill End of
    \texttt{\strut{}{{ env.doc2path(env.docname, base='doc') }}}}
    \vfil\penalty-1\vfilneg
"""

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#
html_static_path = ['_static']
# html_context = {
#     'css_files': [
#         '_static/theme_overrides.css',  # override wide tables in RTD theme
#         ],
#      }

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}
numfig = True
# html_logo = 'assets/img/SUEWS_LOGO.png'

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'supy_doc'


# -- Options for LaTeX output ------------------------------------------------
# this can be one of ['pdflatex', 'xelatex', 'lualatex', 'platex']
if platform.system() == 'Darwin':
    latex_engine = 'lualatex'
else:
    latex_engine = 'pdflatex'

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    'preamble': r'''
\usepackage[titles]{tocloft}
\usepackage{ragged2e}
\addto\captionsenglish{\renewcommand{\bibname}{References}}
\cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
\setlength{\cftchapnumwidth}{0.75cm}
\setlength{\cftsecindent}{\cftchapnumwidth}
\setlength{\cftsecnumwidth}{1.25cm}
\newcolumntype{T}{L}
\setlength{\tymin}{40pt}
''',


    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_show_pagerefs = False

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc,
     'SuPy.tex',
     doc_name,
     author,
     'manual'),
]
# latex_logo = 'assets/img/SUEWS_LOGO.png'

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'SuPy', u'SuPy Documentation',
     [author], 1),
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'SuPy', u'SuPy Documentation',
     author, 'SuPy', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------
# rinoh_documents = [('index',            # top-level file (index.rst)
#                     'target',           # output (target.pdf)
#                     'Document Title',   # document title
#                     'John A. Uthor')]   # document author

# Fix for scrolling tables in the RTD-theme
# https://rackerlabs.github.io/docs-rackspace/tools/rtd-tables.html
def setup(app):
    app.add_stylesheet('theme_overrides.css')
