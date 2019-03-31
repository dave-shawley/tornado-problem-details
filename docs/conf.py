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

html_theme = 'haiku'
intersphinx_mapping = {
    'https://docs.python.org/': None,
    'https://www.tornadoweb.org/en/stable/': None,
}
