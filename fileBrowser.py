# -*- coding: utf-8 -*-
"""
Created on Tue Nov 05 22:00:43 2013

@author: Daniel
"""
from browsingWindow import Ui_Dialog
from browsingWindow import *
import ctypes
import win32api
import time
import os
class Browser(QtGui.QDialog):
    
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui=Ui_Dialog()
        self.path='C:\Users'
        self.displayedPath=self.path
        self.ui.setupUi(self)
        self.allowedExtensions=()
        self.refreshlist()
        self.acceptDir=True
        self.time=time.time()
        self.prevTime=time.time()
        self.ui.fileWindow.clicked.connect(self.selectItem)
        self.ui.upButton.clicked.connect(self.upLevel)
        
   
        
    def accept(self):
        if os.path.isdir(self.path) and not self.firstClick:
            os.path.join(self.path, str(self.ui.fileWindow.currentItem().text()))
        if os.path.isfile(self.path) or self.acceptDir:
            QtGui.QDialog.accept(self)
        else:
            ctypes.windll.user32.MessageBoxW(0, u"Invalid selection "+self.path, u"Select a file", 0)

    def __getAllowedFilesInDir(self):
        Dirlist= os.listdir(self.path)
        shownList=()
        for entry in Dirlist:
                if os.path.isdir(os.path.join(self.path, entry)):
                    shownList+=(entry,)
                elif '.' in entry:
                    split=entry.split('.')
                    if any(ext==split[len(split)-1] for ext in self.allowedExtensions):
                        shownList+=(entry,)
        return shownList
    def refreshlist(self):
        try:
            Dirlist= os.listdir(self.path)
            shownList=()
            if len(self.allowedExtensions)==0:
                shownList=Dirlist
            else:
                shownList=self.__getAllowedFilesInDir()
                    
            self.displayedPath= self.path
            self.ui.fileWindow.clear()
            self.ui.fileWindow.addItems(shownList)
            self.firstClick=True
        except OSError:
            ctypes.windll.user32.MessageBoxW(0, u"Cannot Access "+self.path, u"Location is not available", 0)
            self.path=os.path.split(self.path)[0]  
        
    def selectFolder(self):
        temp= str(self.ui.fileWindow.currentItem().text())
        if os.path.isdir(os.path.join(self.path, temp)):
            self.path=os.path.join(self.path, temp)
            self.refreshlist()
            
    def selectItem(self):
        self.time=time.time()
        clickTime=self.time-self.prevTime
        if self.firstClick:
            self.firstClick=False
            temp= str(self.ui.fileWindow.currentItem().text())
            self.path=os.path.join(self.path, temp)
        else:
            tempPath= os.path.split(self.path)[0]
            temp= str(self.ui.fileWindow.currentItem().text())
            self.path=os.path.join(tempPath, temp)
            
        if clickTime<0.5:
            if os.path.isdir(self.path):
                self.refreshlist()
            elif os.path.isfile(self.path):
                self.accept()
        self.prevTime=self.time
        
    def upLevel(self):
        self.displayedPath= os.path.split(self.displayedPath)[0]
        previous=self.path
        self.path=self.displayedPath
        if self.path !=previous:
            self.refreshlist()
        else:
            self.driveList()
            
    def driveList(self):
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        self.ui.fileWindow.clear()
        self.ui.fileWindow.addItems(drives)
        
    def setAllowedExtensions(self, extensionList):
        print extensionList
        self.allowedExtensions=extensionList
        self.refreshlist()
        
    def canAcceptDirectories(self, acceptDir):
        self.acceptDir=acceptDir
        
    def getPathContents(self):
        if os.path.isfile(self.path):
            return None
        else:
            return self.__getAllowedFilesInDir()
            