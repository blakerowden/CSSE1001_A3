"""
Assignment 3 - Hangman
.py file 2/3
CSSE1001/7030
Semester 2, 2018
"""

__author__ = "Blake Rowden s4427634"

import tkinter as tk
from support import TopHeader
import tkinter.messagebox
import random


class GameScreen(object):
    """
    An object containing the GUI for a game of hangman.
    """

    def __init__(self, master):
        """
        Create an instance of the hangman game.

        Parameters:
             master (tk.TopLevel()): Root application.
        """
        self._master = master
        self._difficulty = "medium"
        self._word = generate_word(self._difficulty)
        self._guessed = []  # Current ordered list of correct letters guessed.
        self._wins = 0
        self._losses = 0
        self._guess_count = 0
        self._win_test = len(self._word)  # Number of correct guesses needed to win.
        # Create the blank letters for the user to see the length of the word.
        for _ in self._word:
            self._guessed.append("_")

        self._frame = tk.Frame(master)
        self._frame.pack(fill=tk.BOTH, expand=1)

        self._master.title("Hang-Man")
        self._master.minsize(500, 500)

        self._menubar = tk.Menu(self._master)
        self._master.config(menu=self._menubar)
        self._menubar.add_command(label="Exit", command=lambda: self.close_window())
        self._menubar.add_command(label="Reset", command=lambda: self.hard_reset())

        #  Options for the user to select their difficulty level.
        self._difficulty_menu = tk.Menu(self._menubar, tearoff=0)
        self._difficulty_menu.add_command(label="easy", command=lambda: self.change_difficulty("easy"))
        self._difficulty_menu.add_command(label="medium", command=lambda: self.change_difficulty("medium"))
        self._difficulty_menu.add_command(label="hard", command=lambda: self.change_difficulty("hard"))
        self._difficulty_menu.add_command(label="impossible", command=lambda: self.change_difficulty("impossible"))
        self._menubar.add_cascade(label="Difficulty", menu=self._difficulty_menu)

        self._menubar.add_command(label="New Word", command=lambda: self.reset_game())

        self._topheader = TopHeader(self._frame,
                                    bg="#FEFBED",
                                    fg="#C09853",
                                    title="Hangman",
                                    fontsize=10,
                                    text="Please enjoy a game of hangman while you wait for your questions to be"
                                         " answered from a tutor. The rules are simple; try to guess the word "
                                         "before the man is hung. Difficulty settings can be changed in the top ")
        self._topheader.pack(fill=tk.X)

        self._subframe = tk.Frame(self._frame, bg="#fff")
        self._subframe.pack(fill=tk.BOTH, expand=1, pady=2)

        self._lettergrid = LetterGrid(self._subframe, self)
        self._lettergrid.pack(side=tk.LEFT, padx=(50, 0))

        self._display = tk.Frame(self._subframe, bg="#fff")
        self._display.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self._difficult_label = tk.Label(self._frame, bg="#FEFBED", font=("Arial", 10),
                                         text="Difficulty: {0}".format(self._difficulty.upper()),
                                         anchor=tk.W)
        self._difficult_label.pack(fill=tk.X)
        self._wins_label = tk.Label(self._frame, bg="#FEFBED", font=("Arial", 10),
                                    text="Wins: {0}".format(self._wins),
                                    anchor=tk.W)
        self._wins_label.pack(fill=tk.X)
        self._losses_label = tk.Label(self._frame, bg="#FEFBED", font=("Arial", 10),
                                      text="Losses: {0}".format(self._losses),
                                      anchor=tk.W)
        self._losses_label.pack(fill=tk.X)

        # List containing the sprites for the hangman animation.
        self._hangman = [tk.PhotoImage(file="Hangman Sprites\Hangman-0.png"),
                         tk.PhotoImage(file="Hangman Sprites\Hangman-1.png"),
                         tk.PhotoImage(file="Hangman Sprites\Hangman-2.png"),
                         tk.PhotoImage(file="Hangman Sprites\Hangman-3.png"),
                         tk.PhotoImage(file="Hangman Sprites\Hangman-4.png"),
                         tk.PhotoImage(file="Hangman Sprites\Hangman-5.png"),
                         tk.PhotoImage(file="Hangman Sprites\Hangman-6.png")]

        # Currently active sprite.
        self._current_hangman = tk.Label(self._display, image=self._hangman[0], bg="#fff")
        self._current_hangman.pack()

        # Shows all correct letter guesses and _ where the user still hasn't guessed correctly.
        self._visual_word = tk.Frame(self._display)
        self._visual_word.pack(padx=(90, 0))

        for letter in self._guessed:
            tk.Label(self._visual_word, text=letter, bg="#fff", font=("Arial", 20, "bold")).pack(side=tk.LEFT)

    def close_window(self):
        """
        Close the hangman application and return to the queue.

        Returns:
             None
        """
        self._master.destroy()

    def test_letter(self, letter2test):
        """
        Runs the selected letter to see if it is in the word.

        If the word is completed the user wins.
        If the user reached max guesses the user looses.
        If the user guesses correctly the letter is revealed.
        If the user guesses incorrectly the hangman sprite will advance.
        Parameters:
            letter2test (char): The user selected letter.
        Returns:
            None
        """
        tester = letter2test.lower()
        # Disable the pushed button.
        self._lettergrid._buttons[letter2test].config(state=tk.DISABLED, bg="#dff0d8")

        # Check for the letter to test against each letter in the word adding to list.
        correct_index = [i for i, ltr in enumerate(self._word) if ltr == tester]

        if not correct_index:
            # If incorrect letter is guessed check to see if player has lost.
            self._guess_count += 1
            if self._guess_count == 7:
                tk.messagebox.showinfo("YOU LOSE", "The word you were looking for was {0}".format(
                    self._word.upper()), parent=self._master)
                self._losses += 1
                if not tk.messagebox.askyesno("HANGMAN", "Do you want to play again?", parent=self._master):
                    self.close_window()
                    return
                else:
                    self.reset_game()

        for i in correct_index:
            # Add the location of the correct letter at its correct index, check to see if player has won.
            self._win_test -= 1
            self._guessed[i] = letter2test
        self.refresh_canvas()
        if self._win_test == 0:
            tk.messagebox.showinfo("YOU WIN", "Woo Hoo!!! You WIN!!", parent=self._master)
            self._wins += 1
            if not tk.messagebox.askyesno("HANGMAN", "Do you want to play again?", parent=self._master):
                self.close_window()
                return
            else:
                self.reset_game()

    def change_difficulty(self, difficulty):
        """
        Set the new difficulty.

        Parameters:
            difficulty (str): New difficulty setting selected by the user.
        Returns:
            None
        """
        if difficulty != self._difficulty:
            self._difficulty = difficulty
            self.reset_game()

    def refresh_canvas(self):
        """
        Redraws the canvas to show changes in GUI

        Returns:
            None
        """
        self._visual_word.destroy()
        self._visual_word = tk.Frame(self._display)
        self._visual_word.pack(padx=(90, 0))

        for letter in self._guessed:
            tk.Label(self._visual_word, text=letter, bg="#fff", font=("Arial", 20, "bold")).pack(side=tk.LEFT)

        self._current_hangman.config(image=self._hangman[self._guess_count])

        self._difficult_label.configure(text="Difficulty: {0}".format(self._difficulty.upper()))
        self._wins_label.configure(text="Wins: {0}".format(self._wins))
        self._losses_label.configure(text="Losses: {0}".format(self._losses))

    def reset_game(self):
        """
        Resets the game with new word.

        Returns:
            None
        """
        self._lettergrid.button_reset()
        self._word = generate_word(self._difficulty)
        self._win_test = len(self._word)
        self._guessed = []
        self._guess_count = 0
        for _ in self._word:
            self._guessed.append("_")
        self.refresh_canvas()

    def hard_reset(self):
        """
        Resets the game with new word. Clears game data and resets difficulty to easy.

        Returns:
            None
        """
        self._wins = 0
        self._losses = 0
        self._difficulty = "medium"
        self.reset_game()


def magic_button(master, letter, controller):
    """
    Creates a virtual keyboard button.

    Parameters:
        master (tk.Frame): The buttons container.
        letter (char): The buttons letter.
        controller (GameScreen): Application controlling the keyboard.
    Returns:
         tk.Button: A button representing a key on a keyboard.
    """
    return tk.Button(master, text=letter, activebackground="palegreen", bg="palegreen", relief=tk.FLAT,
                     command=lambda: controller.test_letter(letter),
                     width=2, height=2)


class LetterGrid(tk.Frame):
    """
    A virtual keyboard.
    """
    def __init__(self, master, controller):
        """
        Create an instance of a virtual keyboard.

        Parameters:
            master (tk.Frame): The keyboards container.
            controller (GameScreen): Application controlling the keyboard.
        """
        super().__init__(master)
        self.configure(bg="#fff")

        # Searchable library of buttons.
        self._buttons = {"A": magic_button(self, "A", controller),
                         "B": magic_button(self, "B", controller),
                         "C": magic_button(self, "C", controller),
                         "D": magic_button(self, "D", controller),
                         "E": magic_button(self, "E", controller),
                         "F": magic_button(self, "F", controller),
                         "G": magic_button(self, "G", controller),
                         "H": magic_button(self, "H", controller),
                         "I": magic_button(self, "I", controller),
                         "J": magic_button(self, "J", controller),
                         "K": magic_button(self, "K", controller),
                         "L": magic_button(self, "L", controller),
                         "M": magic_button(self, "M", controller),
                         "N": magic_button(self, "N", controller),
                         "O": magic_button(self, "O", controller),
                         "P": magic_button(self, "P", controller),
                         "Q": magic_button(self, "Q", controller),
                         "R": magic_button(self, "R", controller),
                         "S": magic_button(self, "S", controller),
                         "T": magic_button(self, "T", controller),
                         "U": magic_button(self, "U", controller),
                         "V": magic_button(self, "V", controller),
                         "W": magic_button(self, "W", controller),
                         "X": magic_button(self, "X", controller),
                         "Y": magic_button(self, "Y", controller),
                         "Z": magic_button(self, "Z", controller)}

        # Pack all buttons into a visual gris.
        self._buttons["A"].grid(row=0, column=0, padx=1, pady=1)
        self._buttons["B"].grid(row=0, column=1, padx=1, pady=1)
        self._buttons["C"].grid(row=0, column=2, padx=1, pady=1)
        self._buttons["D"].grid(row=0, column=3, padx=1, pady=1)
        self._buttons["E"].grid(row=0, column=4, padx=1, pady=1)
        self._buttons["F"].grid(row=0, column=5, padx=1, pady=1)
        self._buttons["G"].grid(row=1, column=0, padx=1, pady=1)
        self._buttons["H"].grid(row=1, column=1, padx=1, pady=1)
        self._buttons["I"].grid(row=1, column=2, padx=1, pady=1)
        self._buttons["J"].grid(row=1, column=3, padx=1, pady=1)
        self._buttons["K"].grid(row=1, column=4, padx=1, pady=1)
        self._buttons["L"].grid(row=1, column=5, padx=1, pady=1)
        self._buttons["M"].grid(row=2, column=0, padx=1, pady=1)
        self._buttons["N"].grid(row=2, column=1, padx=1, pady=1)
        self._buttons["O"].grid(row=2, column=2, padx=1, pady=1)
        self._buttons["P"].grid(row=2, column=3, padx=1, pady=1)
        self._buttons["Q"].grid(row=2, column=4, padx=1, pady=1)
        self._buttons["R"].grid(row=2, column=5, padx=1, pady=1)
        self._buttons["S"].grid(row=3, column=0, padx=1, pady=1)
        self._buttons["T"].grid(row=3, column=1, padx=1, pady=1)
        self._buttons["U"].grid(row=3, column=2, padx=1, pady=1)
        self._buttons["V"].grid(row=3, column=3, padx=1, pady=1)
        self._buttons["W"].grid(row=3, column=4, padx=1, pady=1)
        self._buttons["X"].grid(row=3, column=5, padx=1, pady=1)
        self._buttons["Y"].grid(row=4, column=2, padx=1, pady=1)
        self._buttons["Z"].grid(row=4, column=3, padx=1, pady=1)

    def button_reset(self):
        """
        Re-enables all buttons for a new game.

        Returns:
             None
        """
        for button in self._buttons:
            self._buttons[button].config(bg="palegreen", state=tk.ACTIVE)


def get_hangman_words(word_file):
    """
    Gets all the words used in the game hangman from a file into a list.

    Parameter:
        word_file (str): The filename of the word file.
    """
    with open(word_file) as raw_file:
        lines = [line.strip() for line in raw_file]
        return [word.strip() for word in lines if word]


def generate_word(difficulty):
    """
    Generates a random word from the word list using the difficulty setting.

    Easy to Hard is based of length of word however; impossible is based of complexity of word structure.
    Parameters:
        difficulty (string): Current difficulty setting.
    Returns:
        string: Randomly generated word.
    """
    if difficulty == "easy":
        easy_word = WORDLIST[random.randint(1, 853)].lower()
        if 0 < len(easy_word) <= 4:
            return easy_word
        else:
            return generate_word("easy")
    elif difficulty == "medium":
        med_word = WORDLIST[random.randint(1, 852)].lower()
        if 4 < len(med_word) <= 6:
            return med_word
        else:
            return generate_word("medium")
    elif difficulty == "hard":
        hard_word = WORDLIST[random.randint(1, 852)].lower()
        if 6 < len(hard_word):
            return hard_word
        else:
            return generate_word("hard")
        # Impossible words are generated from a separate list of difficult words at the end of the list.
    elif difficulty == "impossible":
        impossible_word = WORDLIST[random.randint(855, 902)].lower()
        return impossible_word


# The list of words obtained from the file.
WORDLIST = get_hangman_words('words.txt')



