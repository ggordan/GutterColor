from sublime_plugin import EventListener, WindowCommand
import sublime

# True if Sublime Text 3
ST3 = (int(sublime.version()) >= 3000)

if ST3: from .file import File
else: from file import File


def clear_cache(force = False):
  """
  If the folder exists, and has more than 5MB of icons in the cache, delete
  it to clear all the icons then recreate it.
  """
  from os.path import getsize, join, isfile, exists
  from os import makedirs, listdir
  from shutil import rmtree

  # The directory where the icons are stored. Silly conditional for ST2/3
  if ST3:
    cache_dir = join(sublime.cache_path(), 'GutterColor')
  else:
    cache_dir = join(sublime.packages_path(), 'Theme - Default', 'GutterColor')

  # The maximum amount of space to take up
  limit = 5242880 # 5 MB

  if exists(cache_dir):
    size = sum(getsize(join(cache_dir, f)) for f in listdir(cache_dir) if isfile(join(cache_dir, f)))
    if force or (size > limit): rmtree(cache_dir)

  if not exists(cache_dir): makedirs(cache_dir)


def plugin_loaded():
  clear_cache()

if not ST3:
	clear_cache()


class GutterColorClearCacheCommand(WindowCommand):
  def run(self):
    clear_cache(True)


class GutterColorEventListener(EventListener):
  """Scan the view when it gains focus, and when it is saved."""

  # Synchronous 

  def on_activated(self, view):
    """Scan file synchronously when it gets focus"""
    if not ST3 and syntax(view) in settings().get('supported_syntax'):
      File(view).start()

  def on_modified(self, view):
    """Scan file when it is modified"""
    if syntax(view) in settings().get('supported_syntax'):
      File(view, 'update')

  def on_pre_save(self, view):
    """Scan file before it is saved"""
    if not ST3 and syntax(view) in settings().get('supported_syntax'):
      File(view, 'update')

  # Asynchronous 

  def on_activated_async(self, view):
    """Scan file asynchronously when it gets focus"""
    if syntax(view) in settings().get('supported_syntax'):
      File(view)

  def on_pre_save_async(self, view):
    """Scan file before it is saved"""
    if syntax(view) in settings().get('supported_syntax'):
      File(view, 'update')     


def settings():
  """Shortcut to the settings"""
  return sublime.load_settings("GutterColor.sublime-settings")

def syntax(view):
  """Return the view syntax"""
  try:
    return view.settings().get('syntax').split('/')[-1].split('.')[0].lower()
  except:
    return None