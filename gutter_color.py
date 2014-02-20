from GutterColor.file import File
from sublime_plugin import EventListener
from sublime import load_settings


def plugin_loaded():
    """
    If the folder exists, delete it to clear all the icons then recreate it.
    """
    from os import makedirs, path
    from sublime import cache_path
    from shutil import rmtree
    icon_path = path.join(cache_path(), "GutterColor")

    if path.exists(icon_path):
      rmtree(icon_path)

    makedirs(icon_path)


class GutterColorEventListener(EventListener):
  """Scan the view when it gains focus, and when it is saved."""

  def on_activated_async(self, view):
    """Scan file when it gets focus"""
    if syntax(view) in settings().get('supported_syntax'):
      File(view)

  def on_modified(self, view):
    """Scan file when it gets focus"""
    if syntax(view) in settings().get('supported_syntax'):
      File(view, 'update')

  def on_pre_save_async(self, view):
    """Scan file when it gets focus"""
    if syntax(view) in settings().get('supported_syntax'):
      File(view, 'update')

def settings():
  """Shortcut to the settings"""
  return load_settings("GutterColor.sublime-settings")

def syntax(view):
  """Return the view syntax"""
  return view.settings().get('syntax').split('/')[-1].split('.')[0].lower()
