from os.path import dirname, realpath, join

# The path where the color cache is stored
CACHE_PATH = join(dirname(realpath(__file__)), '.cache')

# The path where the icons are stored
ICON_PATH = join(dirname(realpath(__file__)), 'icons')

# Only run for the following syntax
SUPPORTED_SYNTAX = ['sass', 'css', 'scss', 'less']
