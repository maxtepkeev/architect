import os
import sys
import alabaster
import sphinx.ext.autodoc

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('..'))

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['alabaster', 'sphinx.ext.autodoc']

# How to sort documented members
autodoc_member_order = 'bysource'

# What content will be inserted into the main body of an autoclass directive
autoclass_content = 'both'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Architect'
copyright = u'2015, Max Tepkeev'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'logo': 'img/logo.gif',
    'github_user': 'maxtepkeev',
    'github_repo': 'architect',
    'github_type': 'star',
    'github_banner': 'true',
    'gratipay_user': 'maxtepkeev',
    'show_powered_by': 'false',
    'code_font_size': '14px',
}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [alabaster.get_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    '**': ['about.html', 'navigation.html', 'searchbox.html', 'donate.html']
}

# If false, no index is generated.
html_use_index = True

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'Architectdoc'


# Returns object name without class name or module name prepended
class NameOnlyMixin(object):
    def format_name(self):
        return self.objpath[1]

    def add_directive_header(self, sig):
        super(NameOnlyMixin, self).add_directive_header(sig)
        for index, line in enumerate(self.directive.result):
            if ':module:' in line:
                del self.directive.result[index]


class AttributeNameOnlyDocumenter(NameOnlyMixin, sphinx.ext.autodoc.AttributeDocumenter):
    objtype = 'attribute-name-only'
    directivetype = 'attribute'


class MethodNameOnlyDocumenter(NameOnlyMixin, sphinx.ext.autodoc.MethodDocumenter):
    objtype = 'method-name-only'


# Documentation setup
def setup(app):
    app.add_stylesheet('css/architect.css')
    app.add_autodocumenter(AttributeNameOnlyDocumenter)
    app.add_autodocumenter(MethodNameOnlyDocumenter)
