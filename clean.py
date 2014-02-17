import GutterColor.settings as settings
from os import walk, remove, path, listdir
from shutil import rmtree
from threading import Thread

class Clean(Thread):
  """Clean up the cache and generated icons"""

  def __init__(self, files):
    Thread.__init__(self)
    self.files = files

  def run(self):
    self.remove_folders()
    self.remove_files()


  def folder_ids(self, name):
    """Return all the open folder ids"""
    name = name.split('/')[-1]
    return int(name) if not name == 'icons' else None


  def file_ids(self, name):
    """Return all file ids"""
    name = name.split('/')[-1]
    return int(name) if not name == 'icons' else None


  def remove_folders(self):
    """Remove all the icon folders which are not currently open"""
    # Get all the folder ids
    folders = list(filter(None, map(self.folder_ids, [x[0] for x in walk(settings.ICON_PATH)])))
    # Delete the folders
    for folder in folders:
      if folder not in self.files:
        rmtree(path.join(settings.ICON_PATH, str(folder)))


  def remove_files(self):
    """Remove all the cached files which are not currently open"""
    files = [ f for f in listdir(settings.CACHE_PATH) if path.isfile(path.join(settings.CACHE_PATH,f)) ]
    for f in files:
      if f == '.keep': pass
      if int(f) not in self.files:
        remove(path.join(settings.CACHE_PATH, f))
