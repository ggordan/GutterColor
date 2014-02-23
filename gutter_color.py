from .file import File
from sublime_plugin import EventListener, WindowCommand
from sublime import load_settings

def clear_cache(force = False):
  """
  If the folder exists, and has more than 5MB of icons in the cache, delete
  it to clear all the icons then recreate it.
  """
  from os.path import getsize, join, isfile, exists
  from os import makedirs, listdir
  from sublime import cache_path
  from shutil import rmtree
  
  # The icon cache path
  icon_path = join(cache_path(), "GutterColor")

  # The maximum amount of space to take up
  limit = 5242880 # 5 MB

  if exists(icon_path):
    size = sum(getsize(join(icon_path, f)) for f in listdir(icon_path) if isfile(join(icon_path, f)))
    if force or (size > limit): rmtree(icon_path)

  if not exists(icon_path): makedirs(icon_path)

def plugin_loaded():
  clear_cache()

class GutterColorClearCacheCommand(WindowCommand):
  def run(self):
    clear_cache(True)

class GutterColorEventListener(EventListener):
  """Scan the view when it gains focus, and when it is saved."""

  def on_activated_async(self, view):
    """Scan file when it gets focus"""
    if syntax(view) in settings().get('supported_syntax'):
      File(view)

  def on_modified(self, view):
    """Scan file when it is modified"""
    if syntax(view) in settings().get('supported_syntax'):
      File(view, 'update')

  def on_pre_save_async(self, view):
    """Scan file before it is saved"""
    if syntax(view) in settings().get('supported_syntax'):
      File(view, 'update')

def settings():
  """Shortcut to the settings"""
  return load_settings("GutterColor.sublime-settings")

def syntax(view):
  """Return the view syntax"""
  return view.settings().get('syntax').split('/')[-1].split('.')[0].lower()
