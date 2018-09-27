"""
Assignment 3 - Queue
CSSE1001/7030
Semester 2, 2018
"""

import tkinter as tk

__author__ = "Blake Rowden s4427634"


class Header(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._master = master

        # Notice
        self._noticeframe = tk.Frame(self._master, bg="#fefcec")
        self._noticeframe.pack(fill=tk.X)
        self._nflabel1 = tk.Label(self._noticeframe, text="Important",
                                  font=("Helvetica Neue", 18, "bold"),
                                  fg="#C09853", bg="#FEFBED")
        self._nflabel1.pack(anchor=tk.W, padx=13, pady=(14, 0))
        self._nflabel2 = tk.Label(self._noticeframe, text=("Individual assessment items must be solely your own work. "
                                                           "While students are encouraged to have high-level "
                                                           "conversations about the problems they are "
                                                           "trying to solve, you must not look at another student’s "
                                                           "code or copy from it. The university uses sophisticated "
                                                           "anti-collusion measures to automatically "
                                                           "detect similarity between assignment submissions."),
                                  font=("sans-serif", 14,),
                                  bg="#FEFBED",
                                  justify=tk.LEFT,
                                  wraplength=1300)
        self._nflabel2.pack(anchor=tk.W, padx=13, pady=(0, 15))

        # Question Container
        self._questioncontainer = tk.Frame(self._master)
        self._questioncontainer.pack(expand=1, fill=tk.BOTH)

        # Quick Question Frame
        self._quickquestionframe = tk.Frame(self._questioncontainer)
        self._quickquestionframe.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

        # Quick Question Title Frame
        self._qqframe1 = tk.Frame(self._quickquestionframe, bg="#dff0d8", highlightbackground="#d6e9c6",
                                  highlightcolor="#d6e9c6",
                                  highlightthickness=1,
                                  bd=0)
        self._qqframe1.pack(ipadx=150, pady=20)
        self._qqlabel1 = tk.Label(self._qqframe1, text="Quick Questions", font=("Helvetica Neue", 25, "bold"),
                                  bg="#dff0d8",
                                  fg="#3c763d")
        self._qqlabel1.pack(pady=5)
        self._qqlabel2 = tk.Label(self._qqframe1, text="< 2 mins with a tutor", font=("Helvetica Neue", 10, "bold"),
                                  bg="#dff0d8",
                                  fg="#666")
        self._qqlabel2.pack(pady=(30, 5))

        # Description
        self._qqlabel3 = (tk.Label(self._quickquestionframe, text="Some examples of quick questions:\n"
                                                                  "  \u2022 Syntax errors\n"
                                                                  "  \u2022 Interpreting error output\n"
                                                                  "  \u2022 Assignment/MyPyTutor interpretation\n"
                                                                  "  \u2022 MyPyTutor submission issues",
                                   font=("Arial", 10),
                                   justify=tk.LEFT))
        self._qqlabel3.pack(anchor=tk.W, padx=(50, 0))

        # Button Border
        self._qqbuttonborder = tk.Frame(self._quickquestionframe,
                                        highlightbackground="#4cae4c",
                                        highlightcolor="#4cae4c",
                                        highlightthickness=3,
                                        bd=0)
        self._qqbuttonborder.pack(pady=50)
        # Button
        self._qqbutton = tk.Button(self._qqbuttonborder,
                                   text="Request Quick Help",
                                   font=("Arial", 11),
                                   bg="#5cb85c", fg="#fff",
                                   relief=tk.FLAT)
        self._qqbutton.pack()

        # Long Question Frame
        self._longquestionframe = tk.Frame(self._questioncontainer)
        self._longquestionframe.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH)

        # Long Question Title Frame
        self._lqframe1 = tk.Frame(self._longquestionframe, bg="#d9edf7", highlightbackground="#bce8f1",
                                  highlightcolor="#bce8f1",
                                  highlightthickness=1,
                                  bd=0)
        self._lqframe1.pack(ipadx=150, pady=20)
        self._lqlabel1 = tk.Label(self._lqframe1, text="Long Questions", font=("Helvetica Neue", 25, "bold"),
                                  bg="#d9edf7",
                                  fg="#31708f")
        self._lqlabel1.pack(pady=5)
        self._lqlabel2 = tk.Label(self._lqframe1, text="> 2 mins with a tutor", font=("Helvetica Neue", 10, "bold"),
                                  bg="#d9edf7",
                                  fg="#666")
        self._lqlabel2.pack(pady=(30, 5))

        # Description
        self._lqlabel3 = (tk.Label(self._longquestionframe, text="Some examples of long questions:\n"
                                                                 "  \u2022 Open ended questions\n"
                                                                 "  \u2022 to start a problem\n"
                                                                 "  \u2022 How to improve code\n"
                                                                 "  \u2022 Debugging\n"
                                                                 "  \u2022 Assignment help",
                                   font=("Arial", 10),
                                   justify=tk.LEFT))
        self._lqlabel3.pack(anchor=tk.W, padx=(50, 0))

        #Button Border
        self._lqbuttonborder = tk.Frame(self._longquestionframe,
                                        highlightbackground="#46b8da",
                                        highlightcolor="#46b8da",
                                        highlightthickness=3,
                                        bd=0)
        self._lqbuttonborder.pack(pady=50)
        #Button
        self._lqbutton = tk.Button(self._lqbuttonborder,
                                   text="Request Long Help",
                                   font=("Arial", 11),
                                   bg="#5bc0de", fg="#fff",
                                   relief=tk.FLAT)
        self._lqbutton.pack()


class QuickQuestionQueue(tk.Frame):
    def __init__(self, master):
        super().__init__(master)


class LongQuestionQueue(tk.Frame):
    def __init__(self, master):
        super().__init__(master)


class MainApplication(object):

    def __init__(self, master):
        self._master = master
        self._master.title("CSSE 1001 Queue")
        self._master.minsize(1322, 579)

        self._header = Header(self._master)
        self._header.pack(fill=tk.X)

        self._mainwindow = tk.Frame(self._master)
        self._mainwindow.pack(fill=tk.BOTH, expand=1, pady=15)
        self._quickquestions = QuickQuestionQueue(self._mainwindow)
        self._quickquestions.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5)
        self._longquestions = LongQuestionQueue(self._mainwindow)
        self._longquestions.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
