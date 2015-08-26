from .file import File
from sublime_plugin import EventListener, WindowCommand, TextCommand
from sublime import load_settings, save_settings, load_resource, packages_path

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
  fix_schemes_in_windows()

class GutterColorClearCacheCommand(WindowCommand):
  def run(self):
    clear_cache(True)

class GutterColorEventListener(EventListener):
  """Scan the view when it gains focus, and when it is saved."""

  def on_activated_async(self, view):
    """Scan file when it gets focus"""
    if syntax(view) in settings().get('supported_syntax'):
      fix_scheme_in_view(view)
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
  syntax = view.settings().get('syntax')
  return syntax.split('/')[-1].split('.')[0].lower() if syntax is not None else "plain text"

def current_directory(full=False):
  """Return the name of the directory containing this plugin"""
  from os.path import dirname, realpath, split
  if full:
    return dirname(realpath(__file__))
  else:
    return split(dirname(realpath(__file__)))[1]

def fix_schemes_in_windows():
  """Change color schemes for all current views in the supported syntax list"""
  from sublime import windows
  for window in windows():
    for view in window.views():
      if syntax(view) in settings().get('supported_syntax'):
        fix_scheme_in_view(view)

def fix_scheme_in_view(view, regenerate=False, ignore_flags=False):
  """Change color scheme in settings relevant to current view"""
  fix_flag = settings().get("fix_color_schemes", False)
  (fix_syntax, fix_global, fix_custom) = (False, False, False)
  custom_files = []
  if fix_flag == True:
    (fix_syntax, fix_global) = (True, True)
  elif isinstance(fix_flag, list):
    for label in fix_flag:
      if label in ("syntax", "syntax-specific"):
        fix_syntax = True
      if label in ("user", "global", "preferences"):
        fix_global = True
      if ".sublime-settings" in label:
        fix_custom = True
        custom_files.append(label)
  elif ignore_flags:
    pass # otherwise we might quit when we want to force a check contrary to user prefs
  else:
    return # setting is false, nonexistant, or malformed, so exit

  current_scheme = view.settings().get("color_scheme")
  modified_marker = ".gcfix."
  if modified_marker in current_scheme:
    if regenerate:
      new_scheme = current_scheme
    else:
      return # this view already has a fixed scheme and we aren't regenerating, so exit
  else:
    new_scheme =  "Packages/"+current_directory()+"/"+current_scheme.split("/")[-1].split(".")[0]+\
                  modified_marker + current_scheme.split(".")[-1]

  if fix_custom:
    for custom_filename in custom_files:
      if fix_scheme_in_settings(custom_filename, current_scheme, new_scheme):
        return
  if fix_syntax or ignore_flags:
    syntax_filename = view.settings().get('syntax').split('/')[-1].split('.')[0] + ".sublime-settings"
    if fix_scheme_in_settings(syntax_filename, current_scheme, new_scheme):
      return
  if fix_global or ignore_flags:
    if fix_scheme_in_settings("Preferences.sublime-settings", current_scheme, new_scheme):
      return
  print("Could not find or access the settings file where current color_scheme ("+current_scheme+") is set.")

def fix_scheme_in_settings(settings_file,current_scheme, new_scheme, regenerate=False):
  """Change the color scheme in the given Settings to a background-corrected one"""
  from os.path import join, normpath, isfile

  settings = load_settings(settings_file)
  settings_scheme = settings.get("color_scheme")
  if current_scheme == settings_scheme:
    new_scheme_path =  join(packages_path(), normpath(new_scheme[len("Packages/"):]))
    if isfile(new_scheme_path) and not regenerate:
      settings.set("color_scheme", new_scheme)
    else:
      generate_scheme_fix(current_scheme, new_scheme_path)
      settings.set("color_scheme", new_scheme)
    save_settings(settings_file)
    return True
  return False

def generate_scheme_fix(old_scheme, new_scheme_path):
  """Appends background-correction XML to a color scheme file"""
  from os.path import join
  from re import sub
  UUID_REGEX = '[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}'

  with open(join(packages_path(),current_directory(),'background_fix.xml')) as f:
    xml = f.read()
  scheme_data = load_resource(old_scheme) # only valid for ST3 API!

  insertion_point = scheme_data.rfind("</array>")
  new_scheme_data = scheme_data[:insertion_point] + xml + scheme_data[insertion_point:]

  def uuid_gen(args):
    from uuid import uuid4
    return str(uuid4())
  new_scheme_data = sub(UUID_REGEX, uuid_gen, new_scheme_data)

  with open(new_scheme_path, "wb") as f:
    f.write(new_scheme_data.encode("utf-8"))

class GutterColorFixCurrentScheme(TextCommand):
  def run(self, args):
    fix_scheme_in_view(self.view, True, True)
