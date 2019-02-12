"""
Assignment 3 - Support
.py file 3/3
CSSE1001/7030
Semester 2, 2018
"""

__author__ = "Blake Rowden s4427634"

import tkinter as tk


class TopHeader(tk.Frame):
    """
    A visual header used at the top of an application.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master)
        """
        Create an instance of the header.
        
        Parameters:
            master (tk.Frame): Container for the header.
            kwargs (keyword arguments):
                bg (string): Background colour.
                fg (string): Title text colour.
                title (String): Title text.
                fontsize (int): Size of font.
                text (string): Text to go into the description box.   
        Preconditions:
            All colours parsed as strings must be compatible with tkinter library
        """

        self._frame = tk.Frame(self, bg=kwargs['bg'])
        self._frame.pack(fill=tk.X)
        self._title = tk.Label(self._frame, text=kwargs['title'],
                               font=("Helvetica Neue", int(kwargs['fontsize']*1.3), "bold"),
                               fg=kwargs['fg'], bg=kwargs['bg'])
        self._title.pack(anchor=tk.W, padx=13, pady=(20, 5))

        self._body = (tk.Text(self._frame,
                              font=("sans-serif", kwargs['fontsize']),
                              spacing1=1,
                              relief=tk.FLAT,
                              height=4,
                              wrap=tk.WORD,
                              bg=kwargs["bg"]
                              ))
        self._body.insert(tk.INSERT, kwargs["text"])
        self._body.pack(anchor=tk.W, padx=13, expand=1, fill=tk.X)
        self._body.config(state=tk.DISABLED)