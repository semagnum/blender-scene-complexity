import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

project = 'Blender Scene Complexity'
copyright = '2023, Spencer Magnusson'
author = 'Spencer Magnusson'

extensions = ['sphinx.ext.autodoc', 'sphinx_autodoc_typehints']

autodoc_mock_imports = ['bpy', 'bmesh']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
