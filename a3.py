"""
Assignment 3 - Queue
.py file 1/3
CSSE1001/7030
Semester 2, 2018
"""

__author__ = "Blake Rowden s4427634"

import tkinter.messagebox
import tkinter as tk
import time
from hangman import GameScreen
from support import TopHeader

students = []  # List of all students who have used or are using the queue


class RequestPanel(tk.Frame):
    """
    An interactive panel for asking questions and showing all students who are waiting in the queue.

    The request panel allows for a student to ask a question and will place that student in the GUI.
    This interactive queue allows for questions to be canceled or answered and will show stats
    on how many questions the student has asked and how long they have been waiting in the queue.
    """
    def __init__(self, master, **kwargs):
        """
        Construct a new panel used for students to ask questions.

        Parameters:
            master: Frame/Application for the Request Panel to be inserted.
            kwargs (Keyword Arguments):
                title (str): Request panel title.
                titlebg (str): Background for title box.
                titleborder (str): Highlight colour for title box.
                titlefg (str): Text colour of title.
                tuttime (str): Amount of time with tutor.
                exampletext (str): Example questions.
                reqbuttontxt (str): Text placed inside the request button.
                reqbuttonbg (str): Colour of the request button.
                reqbuttonborder (str): Border colour of the request button.
                command2 (arg): argument to execute when request button is pressed
        Preconditions:
            All colours parsed as strings must be compatible with tkinter library
        """
        super().__init__(master)
        self._master = master

        self._frame = tk.Frame(self._master, bg="#fff")
        self._frame.pack(side=tk.LEFT, expand=1, fill=tk.BOTH, padx=20, anchor=tk.N)

        self._mainheader = tk.Frame(self._frame,
                                    bg=kwargs["titlebg"],
                                    highlightbackground=kwargs["titleborder"],
                                    highlightcolor=kwargs["titleborder"],
                                    highlightthickness=1)
        self._mainheader.pack(pady=20, fill=tk.X)

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
                                        relief=tk.FLAT,
                                        activebackground=kwargs["reqbuttonbg"],
                                        activeforeground="#fff",
                                        command=kwargs["command2"])
        self._requestbutton.pack()

        self.sub_frame = tk.Frame(self._frame)
        self.sub_frame.pack(fill=tk.BOTH, expand=1)

        self._avg_wait_time = tk.Label(self.sub_frame, text="No students in queue.", bg="#fff", anchor=tk.W)
        self._avg_wait_time.pack(fill=tk.X, pady=2, ipady=15)

        self._header = tk.Frame(self.sub_frame, bg="#fff")
        self._header.pack(side=tk.TOP, pady=(0, 2), anchor=tk.N, fill=tk.X)

        self._hash = tk.Label(self._header, text="#", bg="#fff",
                              font=("Arial", 10, "bold"))
        self._hash.pack(side=tk.LEFT)

        self._name_label = tk.Label(self._header, text=" Name", bg="#fff", width=15, anchor=tk.W,
                                    font=("Arial", 10, "bold"))
        self._name_label.pack(side=tk.LEFT)

        self._qa_label = tk.Label(self._header, text="Questions Asked", bg="#fff", width=15,
                                  font=("Arial", 10, "bold"))
        self._qa_label.pack(side=tk.LEFT)

        self._time_label = tk.Label(self._header, text="Time", bg="#fff",
                                    font=("Arial", 10, "bold"),
                                    anchor=tk.N)
        self._time_label.pack(side=tk.LEFT, expand=1, anchor=tk.W, padx=(12, 0))

        self._dynamic_queue_frame = tk.Frame(self.sub_frame, bg="#fff")
        self._dynamic_queue_frame.pack(side=tk.TOP, expand=1, anchor=tk.N, fill=tk.BOTH)

    def create_dynamic_queue(self, student_list):
        """
        Refreshes the queue with an ordered list of students currently waiting in the queue.

        Parameters:
            student_list (list<Student>): A list of student objects to add to queue.
        Returns:
            None
        Preconditions:
            All students in the list must be assigned to this queue.
        """

        self._dynamic_queue_frame.destroy()  # Clear old queue to make changes

        self._dynamic_queue_frame = tk.Frame(self.sub_frame, bg="#fff")
        self._dynamic_queue_frame.pack(side=tk.TOP, expand=1, anchor=tk.N, fill=tk.BOTH)

        for queue_no, student in enumerate(sorted(student_list), 1):  # Add each student to the queue in order
            VisualStudent(self._dynamic_queue_frame, student, queue_no).pack(side=tk.TOP,
                                                                             anchor=tk.N,
                                                                             fill=tk.X)

    def average_update(self, student_list):
        """
        Refreshes the average wait time label using data from students currently in the queue.

        Parameters:
            student_list (list<Student>): Students whom time is to be averaged.
        Returns:
            None
        Preconditions:
            All students in the list must be assigned to this queue.
        """

        tot_time = 0
        tot_students = len(student_list)

        for student in student_list:
            tot_time += student.get_numeric_wait_time()

        if tot_students == 0:
            self._avg_wait_time.configure(text="No students in queue.")
        else:  # Pick the appropriate english to use depending on unit of time.
            avg_time = int((tot_time / tot_students))
            if avg_time == 1:
                time_units = "second"
            elif avg_time < 60:
                time_units = "seconds"
            elif avg_time < 120:
                time_units = "minute"
                avg_time = int(avg_time/60)
            else:
                time_units = "minutes"
                avg_time = int(avg_time/60)

            if tot_students == 1:
                student_units = "student"
            else:
                student_units = "students"

            #  Update the average wait time.
            self._avg_wait_time.configure(text="An average wait time of about {0} {1} " 
                                               "for {2} {3}.".format(avg_time,
                                                                     time_units,
                                                                     tot_students,
                                                                     student_units))


class Student(object):
    """
    A class to represent a Student.
    """

    def __init__(self, name):
        """
        Construct a new student object.

        Parameters:
             name (str): The name of the student.
        Preconditions:
            Student name must be unique as it acts as the unique identifier for the queue.
        """
        self._name = name
        self.quick_questions_asked = -1
        self.long_questions_asked = -1
        self._wait_time = 0
        self._active_queue = "None"
        self._epoch = time.clock()  # The epoch is the time stamp for when the student joins a queue.

    def get_name(self):
        """
        Returns the students name

        Returns:
            str: Students name
        """
        return self._name

    def change_queue_status(self, new_queue):
        """
        Changes the students current active queue.

        Parameters:
            new_queue (str): A string containing a description of the new queue
        Returns:
            None
        """
        self._active_queue = new_queue

    def check_queue(self):
        """
        Returns the students current queue.

        Returns:
             str: The students current active queue.
        """
        return self._active_queue

    def ask_question(self, qtype, number=1):
        """
        Adds a question to the students respective question total.

        Parameters:
            qtype (str): Type of question (quick or long).
            number (int): How many questions to add to total. Defaults to 1.
        Return:
            None
        """
        if qtype == "Long":
            self.long_questions_asked += number
        else:
            self.quick_questions_asked += number

    def get_quick_questions_asked(self):
        """
        Returns the numbers of quick questions the student has asked.

        Returns:
            int: Number of quick questions asked in total.
        """
        return self.quick_questions_asked

    def get_long_questions_asked(self):
        """
        Returns the numbers of long questions the student has asked.

        Returns:
            int: Number of long questions asked in total.
        """
        return self.long_questions_asked

    def update_wait_time(self, wait_amount):
        """
        Updates the students wait time to a new wait time.

        Parameters:
            wait_amount (int): Amount of time student has been in queue.
        Returns:
             None
        """
        self._wait_time = wait_amount

    def clear_wait_time(self):
        """
        Sets the wait time back to zero.

        Returns:
             None
        """
        self._wait_time = 0

    def get_epoch(self):
        """
        Returns the time stamp for when a student joined a queue.

        Returns:
             float: time in which the student joined the queue.
        """
        return self._epoch

    def set_epoch(self, current_time):
        """
        Sets the students queue joining time.

        Parameters:
            current_time (float): Time on clock when student joined queue.
        Returns:
            None
        """
        self._epoch = current_time

    def get_wait_time(self):
        """
        Returns the readable english form of the students wait time.

        Returns:
            str: Text version of wait time.
        """
        if self._wait_time < 60:
            return "a few seconds ago"
        elif self._wait_time < 120:
            return "a minute ago"
        elif self._wait_time < 3600:
            return "{0} minutes ago".format(int(self._wait_time/60))
        elif self._wait_time < 7200:
            return "1 hour ago"
        else:
            return "{} hours ago".format(int(self._wait_time/3600))

    def get_numeric_wait_time(self):
        """
        Returns the numerical form of the students wait time.

        Returns:
            float: numerical version of wait time.
        """
        return self._wait_time

    def __lt__(self, other):
        """
        Sorts the student relative to another student.

        The sorting in done first by questions asked and then by time waited in the queue.
        Parameters:
            other (Student): Student to be compared to.
        Return:
            bool: True if student is considered lower in the list
                  compared to the other student.
        """
        if self.check_queue() == "Quick":
            return self.get_quick_questions_asked() < other.get_quick_questions_asked() or \
                   (self.get_quick_questions_asked() == other.get_quick_questions_asked() and
                    self.get_numeric_wait_time() > other.get_numeric_wait_time())
        elif self.check_queue() == "Long":
            return self.get_long_questions_asked() < other.get_long_questions_asked() or \
                   (self.get_long_questions_asked() == other.get_long_questions_asked() and
                    self.get_numeric_wait_time() > other.get_numeric_wait_time())

    def __repr__(self):
        """
        String representation of the student using unique ID.

        Returns:
             str: Student name.
        """
        return self.get_name()


class VisualStudent(tk.Frame):
    """
    A class to represent the interactive GUI version of a Student in a queue.
    """
    def __init__(self, master, student, queue_no):
        """
        Construct a new interactive GUI student object.

        Parameters:
             master (tk.Frame): The frame to insert the visual student object.
             student (Student): Student object to convert to GUI.
             queue_no (int): Order of student in the queue.
        """
        super().__init__(master)

        self._id = student
        self.configure(bg="#fff")

        if student.check_queue() == "Quick":  # Set questions asked relative to the active queue.
            total_questions_asked = student.get_quick_questions_asked()
        else:
            total_questions_asked = student.get_long_questions_asked()

        self._frame = tk.Frame(self, bg="#fff")
        self._frame.pack(side=tk.LEFT, expand=1, fill=tk.X, anchor=tk.N, pady=1)

        self._number = tk.Label(self._frame, text=queue_no, bg="#fff")
        self._number.pack(side=tk.LEFT)

        self._name = tk.Label(self._frame, text=student.get_name(), bg="#fff", width=17, anchor=tk.W)
        self._name.pack(side=tk.LEFT)

        self._questions_asked = tk.Label(self._frame, text=total_questions_asked, bg="#fff", width=17, anchor=tk.W)
        self._questions_asked.pack(side=tk.LEFT, padx=10)

        self._time = tk.Label(self._frame, text=student.get_wait_time(), bg="#fff")
        self._time.pack(side=tk.LEFT, expand=1, anchor=tk.W)

        self._cancel_border = tk.Frame(self._frame,
                                       highlightbackground="red",
                                       highlightcolor="red",
                                       highlightthickness=1,
                                       width=10,
                                       height=10)
        self._cancel_border.pack(anchor=tk.E, side=tk.LEFT, padx=(10, 0))
        self._cancel_button = tk.Button(self._cancel_border, command=self.cancel, bg="coral",
                                        width=2, relief=tk.FLAT)
        self._cancel_button.pack(side=tk.LEFT, anchor=tk.E)

        self._accept_border = tk.Frame(self._frame,
                                       highlightbackground="green",
                                       highlightcolor="green",
                                       highlightthickness=1,
                                       width=10,
                                       height=10)
        self._accept_border.pack(anchor=tk.E, side=tk.LEFT)
        self._accept_button = tk.Button(self._accept_border, command=self.accept, bg="palegreen",
                                        width=2, relief=tk.FLAT)
        self._accept_button.pack(side=tk.LEFT, anchor=tk.E)

    def accept(self):
        """
        Accepts student question and removes student from queue.

        Returns:
             None
        """
        for student in students:  # Using students name as ID, sets active queue to None.
            if self._id == student:
                student.change_queue_status("None")
                student.clear_wait_time()
        app.redraw_queue()  # Visually remove student from queue.

    def cancel(self):
        """
        Declines student question and removes student from queue.

        Returns:
             None
        """
        for student in students:
            # Using students name as ID, sets active queue to None. Ensures total questions asked is unchanged.
            if self._id == student:
                if student.check_queue() == "Quick" and student.get_quick_questions_asked() != 0:
                    student.ask_question("Quick", -1)
                elif student.check_queue() == "Long" and student.get_long_questions_asked() != 0:
                    student.ask_question("Long", -1)
                student.change_queue_status("None")
                student.clear_wait_time()
        app.redraw_queue()  # Visually remove student from queue.


# noinspection PyMissingConstructor
class InputWindow(tk.Toplevel):
    """
    Pop-up window prompting the user to input his/her name.
    """

    def __init__(self, master):
        """
        Create a popup window.

        Parameters:
             master: Main application to have pop-up overlay
        """

        self._top = tk.Toplevel(master)
        tk.Label(self._top, text="Please enter your name:", bg="#FEFBED",
                 font=("Arial", 10, "bold")).pack(fill=tk.X)

        self._frame = tk.Frame(self._top, bg="#FEFBED")
        self._frame.pack(expand=1, fill=tk.BOTH)

        self._top.minsize(280, 20)
        self._top.title("What is your name?")

        self.e = tk.Entry(self._frame)
        self.e.pack(padx=10, pady=10, fill=tk.X)
        self.e.focus()

        self.b = tk.Button(self._frame, text="Enter Name", command=self.ok,
                           activebackground="#FEFBED", bg="#fff")
        self.b.pack(pady=5)

        self.value = ""

    def ok(self):
        """
        Closes window when user presses ok, setting users name to return value.

        Returns:
             None
        """
        self.value = self.e.get()
        self._top.destroy()

    def get_top(self):
        """
        Returns pop-up window.
        """
        return self._top


def get_student_name():
    """
    Obtains the name of the student via an interactive popup window.

    Returns:
        str: Name of the student (user input).
    """
    name = InputWindow(root)
    root.wait_window(name.get_top())
    return name.value


def sorting_hat(raw_student_list, q_type):
    """
    The sorting hat places student into a separate list and returns it.

    'Or yet in wise old Quick-List or Long-List,
    if you've a ready mind,
    Where those of wit and learning,
    Will always find their kind.”
    Parameters:
        raw_student_list (list<Student>): List containing all students.
        q_type (str): The queue in which the students are to be sorted and returned.
    Returns:
        list<Student>: List containing sorted students in the given queue.
    """
    sorted_list = []
    for student in raw_student_list:
        if student.check_queue() == q_type:
            sorted_list.append(student)
    return sorted(sorted_list)


class MainApplication(object):
    """
    A class for the queue interface consisting of a header and two sub queues.
    """

    def __init__(self, master):
        """
        Constructs a new queue application.

        Parameters:
            master (tk.Tk()): tkinter window
        """

        self._master = master
        self._master.title("CSSE 1001 Queue")
        self._master.minsize(1020, 500)

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
        self._topheader.pack(fill=tk.X)

        self._mainscreen = tk.Frame(self._master, bg="#fff")
        self._mainscreen.pack(expand=1, fill=tk.BOTH)
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
                                            reqbuttonbg="#5cb85c",
                                            command2=lambda: self.request_help("Quick")
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
                                           reqbuttonbg="#5bc0de",
                                           command2=lambda: self.request_help("Long")
                                           )
        self._longquestions.pack()

        self.auto_redraw_queue()  # Initialises the auto redraw timer

        self._reask = True  # Used for the hangman extension, iff True will ask user if they want to play.

    def request_help(self, qtype):
        """
        Activates when a user presses the request help button in a queue, adding them to that queue.

        The request help function will obtain a name from the user then test that name against a list of students
        if the name is in the list it will add that student to the queue or it will create a new student and add
        them to the list.
        There is am easter-egg in which the user can type in hangman and a game of hangman will run. This is helpful
        if the student requests no to being asked to play but still wants to play again.
        Parameters:
            qtype (str): The queue to add the student to.
        Returns:
            None
        """

        name = get_student_name()

        if name.strip() == "":  # Ensure the student enters a name
            tkinter.messagebox.showerror("Name Error", "Please type in a name")
            return

        if name == "HangMan" or name == "PlayGame" or name == "hangman":  # Hangman easter-egg
            GameScreen(tk.Toplevel(self._master))
            return

        for student in students:
            # Check for existing students with the same name who have asked a question before.
            if student.get_name() == name:
                if student.check_queue() != "None":
                    #  If student is in a queue show error.
                    tkinter.messagebox.showerror("Queue Error", "Student already in queue")
                    return
                else:
                    #  If student not in a queue add them to this one.
                    student.change_queue_status(qtype)
                    student.ask_question(qtype, 1)
                    student.set_epoch(time.clock())
                    self.redraw_queue()
                    return

        students.append(Student(name))  # If student doesnt yet exist add them to the list.
        for student in students:
            #  Add the new student to the queue
            if student.get_name() == name:
                student.change_queue_status(qtype)
                student.ask_question(qtype, 1)
                student.set_epoch(time.clock())
                self.redraw_queue()

        if self._reask:
            #  Ask the user if the want to play a game of hangman
            if tk.messagebox.askyesno("Feeling Bored?",
                                      "Do you want to play a game of hangman whilst you wait?",
                                      parent=self._master):
                return GameScreen(tk.Toplevel(self._master))
            # Ensure the user is not asked every-time they ask a question.
            elif not tk.messagebox.askyesno("Getting Annoyed?",
                                            "Would you like to be asked again to play in the future?",
                                            parent=self._master):
                self._reask = False

    def redraw_queue(self):
        """
        The redraw queue function will make all changes visible on the GUI.

        Returns:
            None
        Preconditions:
            All wait time calculations are relative to epoch, therefore if in a queue epoch cannot = 0.
        """

        quick_list = sorting_hat(students, "Quick")  # Creates list of student in the quick queue.
        long_list = sorting_hat(students, "Long")  # Creates list of student in the long queue.

        for student in students:
            # Update the wait times for all students.
            if student.check_queue() != "None":
                student.update_wait_time(time.clock() - student.get_epoch())

        # Add the sorted student lists into each respective GUI.
        self._longquestions.create_dynamic_queue(long_list)
        self._quickquestions.create_dynamic_queue(quick_list)
        self._quickquestions.average_update(quick_list)
        self._longquestions.average_update(long_list)

    def auto_redraw_queue(self):
        """
        Timer set to 30sec that will redraw the queue adding any changes made. Primarily wait times.

        Returns:
            None
        """
        self.redraw_queue()
        self._master.after(30000, self.auto_redraw_queue)


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(background="#fff")
    time.clock()
    app = MainApplication(root)
    root.mainloop()


