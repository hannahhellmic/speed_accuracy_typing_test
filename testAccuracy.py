import tkinter as tk
from tkinter import font as tkfont
import user_difficulty_textes_level
import random


class SpeedAccuracyTest:
    def __init__(self, display):
        self.display = display
        self.display.geometry('1000x1600')
        self.display.title("Speed Test Accuracy")
        self.display.configure(bg='#bfbfbf')

        self.custom_font_large = tkfont.Font(family="Arial", size=48, weight="bold")
        self.custom_font_medium = tkfont.Font(family="Arial", size=20)
        self.custom_font_button = tkfont.Font(family="Arial", size=14, weight="bold")

        self.text_for_user1 = user_difficulty_textes_level.level1[random.randint(0, len(user_difficulty_textes_level.level1)) - 1]

        self.text_for_user2 = user_difficulty_textes_level.level2[random.randint(0, len(user_difficulty_textes_level.level2)) - 1]
        self.text_for_user3 = user_difficulty_textes_level.level3[random.randint(0, len(user_difficulty_textes_level.level3)) - 1]
        self.current_text = ("")
        self.time_left = 60
        self.is_running = False

        self.label = tk.Label(display, text="01:00", font=self.custom_font_large,
                              bg='#bfbfbf', fg='#000066')  # Changed bg to match main background
        self.label.pack(pady=20)

        self.display_text = tk.Text(height=10, width=60, font=self.custom_font_medium,
                                    wrap="word", padx=15, pady=15, bd=0, highlightthickness=1,
                                    highlightbackground='#a6a6a6', highlightcolor='#a6a6a6',
                                    bg='#d9d9d9', fg='black')  # Added text area background

        self.user_input = tk.Text(height=10, width=60, font=self.custom_font_medium,
                                  wrap="word", padx=15, pady=15, bd=0, highlightthickness=1,
                                  highlightbackground='#a6a6a6', highlightcolor='#a6a6a6',
                                  bg='#d9d9d9', fg='black')  # Added text area background
        self.user_input.config(state=tk.DISABLED)
        self.user_input.pack(pady=20)

        self.start_button = tk.Button(display, text="Start Test", command=self.start_timer,
                                      font=self.custom_font_button, bg='#a6a6a6', fg='#d9d9d9',
                                      activebackground='#808080', activeforeground='#d9d9d9',
                                      bd=0, padx=20, pady=10, relief=tk.FLAT,
                                      highlightthickness=0)
        self.start_button.pack(pady=10)


        button_style = {
            'font': self.custom_font_button,
            'bd': 0,
            'padx': 20,
            'pady': 10,
            'highlightthickness': 0,
            'relief': tk.FLAT
        }

        self.dif1 = tk.Button(display, text="Level 1", command=self.difficulty1,
                              bg='#a6a6a6', fg='#d9d9d9', activebackground='#808080',
                              activeforeground='#d9d9d9', **button_style)
        self.dif2 = tk.Button(display, text="Level 2", command=self.difficulty2,
                              bg='#a6a6a6', fg='#d9d9d9', activebackground='#808080',
                              activeforeground='#d9d9d9', **button_style)
        self.dif3 = tk.Button(display, text="Level 3", command=self.difficulty3,
                              bg='#a6a6a6', fg='#d9d9d9', activebackground='#808080',
                              activeforeground='#d9d9d9', **button_style)

    def start_test(self):
        self.dif1.pack_forget()
        self.dif2.pack_forget()
        self.dif3.pack_forget()
        self.display_text.config(state=tk.NORMAL)
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, self.current_text)
        self.display_text.config(state=tk.DISABLED)
        self.display_text.pack(pady=20)
        self.countdown()

    def difficulty1(self):
        self.current_text = self.text_for_user1
        self.start_test()

    def difficulty2(self):
        self.current_text = self.text_for_user2
        self.start_test()

    def difficulty3(self):
        self.current_text = self.text_for_user3
        self.start_test()

    def finish_test(self):
        self.user_input.config(state=tk.DISABLED)
        self.display_text.pack_forget()
        user_input_text = self.user_input.get(1.0, tk.END).strip().lower().split()
        accuracy = self.check_accuracy(user_input_text)
        return (accuracy, len(user_input_text))

    def check_accuracy(self, user_input):
        correct_count = 0
        text_words = self.current_text.lower().split()
        min_length = min(len(user_input), len(text_words))

        for i in range(min_length):
            if user_input[i] == text_words[i]:
                correct_count += 1

        if min_length > 0 and len(text_words[len(user_input) - 1]) > len(user_input[-1]):
            if text_words[len(user_input) - 1][:len(user_input[-1])] == user_input[-1]:
                correct_count += 1
        accuracy = (correct_count / min_length) * 100
        return accuracy

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.user_input.delete(1.0, tk.END)
            self.label.pack(pady=20)
            self.user_input.config(state=tk.NORMAL)
            self.start_button.pack_forget()

            self.dif1.pack(pady=10)
            self.dif2.pack(pady=10)
            self.dif3.pack(pady=10)

    def countdown(self):
        if self.time_left > 0:
            minutes, seconds = divmod(self.time_left, 60)
            time_format = f"{minutes:02}:{seconds:02}"
            self.label.config(text=time_format)
            self.time_left -= 1
            self.display.after(1000, self.countdown)
        else:
            result = self.finish_test()
            text_format = f"Accuracy: {result[0]:.2f}% \n{result[1]} words per minute"
            text_color = ''

            if result[0] >= 80:
                text_color = '#27ae60'
            elif result[0] >= 60 and result[0] < 80:
                text_color = '#f39c12'
            elif result[0] >= 40 and result[0] < 60:
                text_color = '#e67e22'
            else:
                text_color = '#e74c3c'

            self.label.config(text=text_format, fg=text_color)
            self.start_button.pack(pady=10)
            self.start_button.config(state=tk.NORMAL)

            self.is_running = False
            self.time_left = 60

            self.user_input.config(state=tk.NORMAL)
            self.user_input.delete(1.0, tk.END)
            self.user_input.config(state=tk.DISABLED)


root = tk.Tk()
player = SpeedAccuracyTest(root)

root.mainloop()
