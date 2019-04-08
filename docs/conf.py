import problemdetails

project = 'Tornado Problem Details'
copyright = '2019, Dave Shawley'
author = 'Dave Shawley'
release = problemdetails.version

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

html_theme = 'python_docs_theme'
master_doc = 'index'
html_theme_options = {
    'root_name': 'tornado-problem-details',
    'root_url': 'index.html',
    'root_icon': 'Warning.svg',
    'root_include_title': False,
}
html_sidebars = {
    '**': ['globaltoc.html'],
}
html_static_path = ['static']   # default.css overrides & svg image
templates_path = ['templates']  # layout overrides

intersphinx_mapping = {
    'https://docs.python.org/': None,
    'https://python-jsonschema.readthedocs.io/en/stable': None,
    'https://www.tornadoweb.org/en/stable/': None,
}
