"""
Assignment 3 - Queue
CSSE1001/7030
Semester 2, 2018
"""

import tkinter as tk

__author__ = "Blake Rowden s4427634"


class TopHeader(tk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master)
        self._master = master
        self._frame = tk.Frame(self._master, bg=kwargs['bg'])
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


class RequestPanel(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self._master = master
        self._frame = tk.Frame(self._master, bg="#fff")
        self._frame.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=20, anchor=tk.N)

        self._mainheader = tk.Frame(self._frame,
                                    bg=kwargs["titlebg"],
                                    highlightbackground=kwargs["titleborder"],
                                    highlightcolor=kwargs["titleborder"],
                                    highlightthickness=1,
                                    bd=0)
        self._mainheader.pack(pady=20, fill=tk.X, expand=1)
        self._title = tk.Label(self._mainheader,
                               text=kwargs["title"],
                               font=("Helvetica Neue", 18, "bold"),
                               bg=kwargs["titlebg"],
                               fg=kwargs["titlefg"])
        self._title.pack(pady=5)
        self._tuttime = tk.Label(self._mainheader,
                                 text=kwargs["tuttime"],
                                 font=("Helvetica Neue", 10, "bold"),
                                 bg=kwargs["titlebg"],
                                 fg="#666")
        self._tuttime.pack(pady=(20, 5))

        self._examples = (tk.Text(self._frame,
                                  font=("Arial", 10),
                                  spacing1=6,
                                  relief=tk.FLAT,
                                  width=60,
                                  height=5,))
        self._examples.insert(tk.INSERT, kwargs["exampletext"])
        self._examples.pack(anchor=tk.W)
        self._examples.config(state=tk.DISABLED)

        self._reqbutborder = tk.Frame(self._frame,
                                      highlightbackground=kwargs["reqbuttonborder"],
                                      highlightcolor=kwargs["reqbuttonborder"],
                                      highlightthickness=3,
                                      bd=0)
        self._reqbutborder.pack(pady=30, anchor=tk.CENTER,)
        self._requestbutton = tk.Button(self._reqbutborder,
                                        text=kwargs["reqbuttontxt"],
                                        font=("Arial", 10),
                                        bg=kwargs["reqbuttonbg"], fg="#fff",
                                        relief=tk.FLAT)
        self._requestbutton.pack()


class MainApplication(object):

    def __init__(self, master):
        self._master = master
        self._master.title("CSSE 1001 Queue")
        self._master.minsize()
        self._topheader = TopHeader(self._master,
                                    bg="#FEFBED",
                                    fg="#C09853",
                                    title="Important",
                                    fontsize=10,
                                    text="Individual assessment items must be solely your own work. "
                                         "While students are encouraged to have high-level "
                                         "conversations about the problems they are "
                                         "trying to solve, you must not look at another student’s "
                                         "code or copy from it. The university uses sophisticated "
                                         "anti-collusion measures to automatically "
                                         "detect similarity between assignment submissions.")
        self._topheader.pack()

        self._mainscreen = tk.Frame(self._master, bg="#fff")
        self._mainscreen.pack(expand=0, fill=tk.BOTH)
        self._quickquestions = RequestPanel(self._mainscreen,
                                            title="Quick Questions",
                                            titlebg="#dff0d8",
                                            titleborder="#d6e9c6",
                                            titlefg="#3c763d",
                                            tuttime="> 2 mins with a tutor",
                                            exampletext="Some examples of quick questions:\n"
                                                        "  \u2022 Syntax errors\n"
                                                        "  \u2022 Interpreting error output\n"
                                                        "  \u2022 Assignment/MyPyTutor interpretation\n"
                                                        "  \u2022 MyPyTutor submission issues",
                                            reqbuttonborder="#4cae4c",
                                            reqbuttontxt="Request Quick Help",
                                            reqbuttonbg="#5cb85c"
                                            )
        self._quickquestions.pack()
        self._longquestions = RequestPanel(self._mainscreen,
                                           title="Long Questions",
                                           titlebg="#d9edf7",
                                           titleborder="#bce8f1",
                                           titlefg="#31708f",
                                           tuttime="< 2 mins with a tutor",
                                           exampletext="Some examples of long questions:\n"
                                                       "  \u2022 Open ended questions\n"
                                                       "  \u2022 How to start a problem\n"
                                                       "  \u2022 How to improve code\n"
                                                       "  \u2022 Assignment Help",
                                           reqbuttonborder="#46b8da",
                                           reqbuttontxt="Request Long Help",
                                           reqbuttonbg="#5bc0de"
                                           )
        self._longquestions.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(background="#fff")
    app = MainApplication(root)
    root.mainloop()
