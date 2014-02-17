from sublime_plugin import EventListener
from GutterColor.clean import Clean
from GutterColor.file import File
import sublime

class GutterColorEventListener(EventListener):

  def on_load_async(self, view):
    '''Initialize the file by creating the regions'''
    File(view).start()

  def on_pre_save_async(self, view):
    '''Update the regions in the view'''
    File(view, 'update').start()

  def on_pre_close(self, view):
    """Ensure that all the assets are deleted, including for files which are
    somehow hanging around.
    N.B. This needs to be a on_pre_close() since view.window() isn't accessible
    on on_close().
    """
    views = map(lambda x: x.views(), sublime.windows())
    open_files = list(map((lambda x: x.buffer_id()), [x for y in views for x in y]))
    Clean(open_files).start()
