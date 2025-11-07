import tkinter as tk
from math import sin, cos, pow, sqrt, floor, ceil


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")

        self.current_input = tk.StringVar(value="0")
        self.memory = 0
        self.pending_operation = None
        self.previous_value = 0

        self.create_widgets()

    def create_widgets(self):
        display = tk.Entry(self.root, textvariable=self.current_input,
                           font=('Arial', 14), justify='right')
        display.grid(row=0, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('x^y', 5, 2), ('√', 5, 3),
            ('%', 6, 0), ('floor', 6, 1), ('ceil', 6, 2), ('M+', 6, 3),
            ('MC', 7, 0), ('MR', 7, 1)
        ]

        for (text, row, col) in buttons:
            btn = tk.Button(self.root, text=text, command=lambda t=text: self.button_click(t))
            btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)

        for i in range(8):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def button_click(self, value):
        # БАЗОВЫЕ ОПЕРАЦИИ - реализует ИЛЬЯ
        if value == '=':
            self.calculate()
        elif value in ['+', '-', '*', '/']:
            self.operation_click(value)
        # НАУЧНЫЕ ОПЕРАЦИИ - реализует ЕГОР
        elif value in ['sin', 'cos', 'x^y', '√', '%', 'floor', 'ceil']:
            self.scientific_operation(value)
        # ПАМЯТЬ - реализует ЕГОР
        elif value in ['M+', 'MC', 'MR']:
            self.memory_operation(value)
        # ЦИФРЫ - реализует ИЛЬЯ
        else:
            self.number_click(value)

    def number_click(self, value):
        # TODO: ИЛЬЯ - реализовать ввод чисел
        pass

    def operation_click(self, operation):
        # TODO: ИЛЬЯ - реализовать базовые операции
        pass

    def calculate(self):
        # TODO: ИЛЬЯ - реализовать вычисление
        pass

    def scientific_operation(self, operation):
        # TODO: ЕГОР - реализовать научные операции
        pass

    def memory_operation(self, operation):
        # TODO: ЕГОР - реализовать работу с памятью
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()