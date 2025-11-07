import tkinter as tk
from math import sin, cos, pow, sqrt, floor, ceil


class Calculator:
    def __init__(self, root=None):
        # Создаем корневое окно если его нет (для тестов)
        self.has_gui = root is not None
        if not self.has_gui:
            self.root = tk.Tk()
            self.root.withdraw()  # Скрываем окно
        else:
            self.root = root
            self.root.title("Calculator")
            self.root.geometry("300x400")

        self.current_input = tk.StringVar(self.root, value="0")
        self.memory = 0
        self.pending_operation = None
        self.previous_value = 0

        if self.has_gui:
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
        if value == '=':
            self.calculate()
        elif value in ['+', '-', '*', '/']:
            self.operation_click(value)
        elif value in ['sin', 'cos', 'x^y', '√', '%', 'floor', 'ceil']:
            self.scientific_operation(value)
        elif value in ['M+', 'MC', 'MR']:
            self.memory_operation(value)
        else:
            self.number_click(value)

    def number_click(self, value):
        current = self.current_input.get()
        if current == "0" or current == "Error":
            self.current_input.set(value)
        else:
            self.current_input.set(current + value)
        return self.current_input.get()

    def operation_click(self, operation):
        try:
            self.previous_value = float(self.current_input.get())
            self.pending_operation = operation
            self.current_input.set("0")
            return True
        except:
            self.current_input.set("Error")
            return False

    def calculate(self):
        try:
            current_value = float(self.current_input.get())
            if self.pending_operation == '+':
                result = self.previous_value + current_value
            elif self.pending_operation == '-':
                result = self.previous_value - current_value
            elif self.pending_operation == '*':
                result = self.previous_value * current_value
            elif self.pending_operation == '/':
                if current_value == 0:
                    result = "Error"
                else:
                    result = self.previous_value / current_value
            elif self.pending_operation == 'pow':
                result = pow(self.previous_value, current_value)
            else:
                result = current_value

            self.current_input.set(str(result))
            self.pending_operation = None
            return result
        except:
            self.current_input.set("Error")
            return "Error"

    def scientific_operation(self, operation):
        try:
            current_value = float(self.current_input.get())
            if operation == 'sin':
                result = sin(current_value)
            elif operation == 'cos':
                result = cos(current_value)
            elif operation == 'x^y':
                self.previous_value = current_value
                self.pending_operation = 'pow'
                self.current_input.set("0")
                return None
            elif operation == '√':
                if current_value < 0:
                    result = "Error"
                else:
                    result = sqrt(current_value)
            elif operation == '%':
                result = current_value / 100
            elif operation == 'floor':
                result = floor(current_value)
            elif operation == 'ceil':
                result = ceil(current_value)
            else:
                result = current_value

            self.current_input.set(str(result))
            return result
        except:
            self.current_input.set("Error")
            return "Error"

    def memory_operation(self, operation):
        try:
            current_value = float(self.current_input.get())
            if operation == 'M+':
                self.memory += current_value
                return self.memory
            elif operation == 'MC':
                self.memory = 0
                return self.memory
            elif operation == 'MR':
                self.current_input.set(str(self.memory))
                return self.memory
        except:
            self.current_input.set("Error")
            return "Error"

    def get_current_value(self):
        """Вспомогательный метод для тестов"""
        return self.current_input.get()

    def set_current_value(self, value):
        """Вспомогательный метод для тестов"""
        self.current_input.set(str(value))

    def destroy(self):
        """Уничтожение окна для тестов"""
        if not self.has_gui:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()