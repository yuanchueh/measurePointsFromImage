#!/usr/bin/python
# File: toplevelminimal.py
#Status: Works as simple interface loader.

import os
import tkinter as tk
import pygubu

try:
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
except:
    CURRENT_DIR = '/home/yuanchueh/Documents/git/measureFromImage'

#CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class MyApplication:
    def __init__(self):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file(os.path.join(CURRENT_DIR, 'measureFromImage_ui_v1.ui'))

        #3: Create the toplevel widget.
        self.mainwindow = builder.get_object('root')

        #Connect callbacks
        builder.connect_callbacks(self)

    def quit(self, event=None):
        self.mainwindow.quit()

    def on_quit_button_click(self):
        quit()

    def btnQuit(self):
        quit()

    def run(self):
        self.mainwindow.mainloop()

print(CURRENT_DIR)

if __name__ == '__main__':
    app = MyApplication()
    app.run()
