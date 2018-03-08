#!/usr/bin/python
# File: toplevelminimal.py


import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import BOTH, YES
import pygubu

try:
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
except:
    CURRENT_DIR = '/home/yuanchueh/Documents/git/measureFromImage'

#CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class MyApplication(pygubu.TkApplication):

    def _create_ui(self):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file(os.path.join(CURRENT_DIR, 'measureFromImage_ui_v2.ui'))

        #3: Create the widget using self.master as parent
        self.mainwindow = builder.get_object('root', self.master)

        # Set root window resizable
        #   self.set_resizable
    def on_quit_button_click(self):
        self.master.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = MyApplication(root)
    app.run()
