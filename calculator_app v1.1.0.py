import tkinter as tk
from tkinter import ttk
import datetime
import re


class StandardCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Bhalchandra's Calculator")
        self.root.geometry("400x600")

        # Color scheme
        self.DISPLAY_BG = "#2C3E50"
        self.DISPLAY_FG = "#ECF0F1"
        self.NUM_BTN_BG = "#34495E"
        self.NUM_BTN_FG = "#ECF0F1"
        self.OP_BTN_BG = "#E74C3C"
        self.OP_BTN_FG = "#FFFFFF"
        self.CLEAR_BTN_BG = "#C0392B"

        # Variables
        self.current = ""
        self.number_count = 0

        # Create display frame
        display_frame = tk.Frame(root, bg=self.DISPLAY_BG)
        display_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        # Main display
        self.display = tk.Entry(display_frame,
                                width=25,
                                justify="right",
                                font=('Arial', 24),
                                bg=self.DISPLAY_BG,
                                fg=self.DISPLAY_FG,
                                insertbackground=self.DISPLAY_FG)
        self.display.pack(fill=tk.X, pady=(5, 5))

        # Result display
        self.result_display = tk.Entry(display_frame,
                                       width=25,
                                       justify="right",
                                       font=('Arial', 18),
                                       bg=self.DISPLAY_BG,
                                       fg=self.DISPLAY_FG)
        self.result_display.pack(fill=tk.X)

        # Number counter
        self.counter_label = tk.Label(root,
                                      text="Numbers used: 0",
                                      font=('Arial', 12),
                                      bg=self.NUM_BTN_BG,
                                      fg=self.NUM_BTN_FG)
        self.counter_label.grid(row=1, column=0, columnspan=5, pady=5)

        # Regular calculator buttons
        buttons = [
            '7', '8', '9', '/', 'C',
            '4', '5', '6', '*', 'CE',
            '1', '2', '3', '-', '(',
            '.', '0', '=', '+', ')'
        ]

        # Add regular buttons
        row = 2
        col = 0
        for button in buttons:
            command = lambda x=button: self.click(x)
            bg_color = self.NUM_BTN_BG if button.isdigit() or button == '.' else \
                self.CLEAR_BTN_BG if button in ['C', 'CE'] else self.OP_BTN_BG
            fg_color = self.NUM_BTN_FG if button.isdigit() or button == '.' else self.OP_BTN_FG

            btn = tk.Button(root,
                            text=button,
                            font=('Calibri', 18, 'bold'),
                            bg=bg_color,
                            fg=fg_color,
                            command=command)
            btn.grid(row=row + (col // 5), column=col % 5, padx=2, pady=2, sticky='nsew')
            col += 1

        # History section
        self.history_frame = ttk.Frame(root)
        self.history_frame.grid(row=row + 4, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        self.history_text = tk.Text(self.history_frame,
                                    width=40,
                                    height=8,
                                    font=('Arial', 12),
                                    bg=self.DISPLAY_BG,
                                    fg=self.DISPLAY_FG)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.history_frame, command=self.history_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=scrollbar.set)

        # Configure grid weights
        for i in range(10):
            root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            root.grid_columnconfigure(i, weight=1)

        # Bind keyboard events
        self.bind_keyboard()

    def bind_keyboard(self):
        self.root.bind('<Return>', lambda event: self.click('='))
        self.root.bind('<BackSpace>', lambda event: self.click('CE'))
        self.root.bind('<Escape>', lambda event: self.click('C'))

        # Bind numbers and operators
        for key in '0123456789+-*/().':
            self.root.bind(key, lambda event, k=key: self.click(k))

    def count_numbers(self, expression):
        expression = expression.rstrip('+-/*')
        numbers = re.split(r'[+\-*/]', expression)
        numbers = [n for n in numbers if n]
        return len(numbers)

    def calculate_result(self, expression):
        try:
            if expression and expression[-1] not in '+-/*':
                return eval(expression)
            return None
        except:
            return None

    def click(self, key):
        if key == '=':
            try:
                result = eval(self.current)
                self.number_count = self.count_numbers(self.current)
                self.counter_label.config(text=f"Numbers used: {self.number_count}")

                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                self.history_text.insert(tk.END, f"[{timestamp}]: {self.current} = {result}\n")
                self.history_text.see(tk.END)

                self.current = str(result)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, self.current)
                self.result_display.delete(0, tk.END)

            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.result_display.delete(0, tk.END)

        elif key == 'C':
            self.current = ""
            self.display.delete(0, tk.END)
            self.result_display.delete(0, tk.END)
            self.number_count = 0
            self.counter_label.config(text=f"Numbers used: {self.number_count}")

        elif key == 'CE':
            self.current = self.current[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current)
            self.number_count = self.count_numbers(self.current)
            self.counter_label.config(text=f"Numbers used: {self.number_count}")
            result = self.calculate_result(self.current)
            self.result_display.delete(0, tk.END)
            if result is not None:
                self.result_display.insert(tk.END, str(result))

        else:
            self.current += key
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current)
            self.number_count = self.count_numbers(self.current)
            self.counter_label.config(text=f"Numbers used: {self.number_count}")
            result = self.calculate_result(self.current)
            self.result_display.delete(0, tk.END)
            if result is not None:
                self.result_display.insert(tk.END, str(result))


if __name__ == "__main__":
    root = tk.Tk()
    calculator = StandardCalculator(root)
    root.mainloop()
