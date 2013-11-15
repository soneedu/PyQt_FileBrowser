Pyqt filebrowser

A standard file browser that lets you browse your computer and select files or directories.

Summary

This is a file browser designed to be included in projects and very simplistic to use. Built using PyQt all users have to do is create a FileBrowser object specify some settings (can directories be selected? What file extensions are allowed) and then call the show method inherited from QDialog

Planned Features

The ability to select multiple files through shift-click or ctrl-click (and other OS specifics)
Improvements to the User interface - back button as well as up, aesthetic changes, ability to see directory tree
Drop down menu allowing users to filter files similar to windows
Possibly icons (although this is a trickier area)
Keyboard control

Basic Usage

In another Qt window:

def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    '''setup code'''
    QtCore.QObject.connect(self.ui.browseButton, QtCore.SIGNAL('clicked()'), self.openFileBrowser)

def openFileBrowser(self):
    self.fileBrowser=Browser()
    self.fileBrowser.setAllowedExtensions(('py', 'txt', 'xml'))
    self.fileBrowser.exec_()
    '''To access the selected path:'''
    self.fileBrowser.path
Pyqt filebrowser maintained by xd009642
