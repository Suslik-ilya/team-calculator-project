import unittest
import tkinter as tk
from calculator import Calculator
from math import sin, cos, sqrt, floor, ceil, pow
import sys


class TestCalculator(unittest.TestCase):
    """Тесты для калькулятора"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.calc = Calculator()  # Создаем без GUI для тестов

    def tearDown(self):
        """Очистка после каждого теста"""
        self.calc.destroy()

    def test_initial_state(self):
        """Тест начального состояния калькулятора"""
        self.assertEqual(self.calc.get_current_value(), "0")
        self.assertEqual(self.calc.memory, 0)
        self.assertIsNone(self.calc.pending_operation)

    def test_number_input(self):
        """Тест ввода чисел"""
        # Тест ввода первой цифры
        self.calc.number_click('5')
        self.assertEqual(self.calc.get_current_value(), '5')

        # Тест добавления цифр
        self.calc.number_click('3')
        self.assertEqual(self.calc.get_current_value(), '53')

    def test_number_input_after_error(self):
        """Тест ввода после ошибки"""
        self.calc.set_current_value("Error")
        self.calc.number_click('7')
        self.assertEqual(self.calc.get_current_value(), '7')

    def test_addition(self):
        """Тест операции сложения"""
        # Устанавливаем первое число
        self.calc.set_current_value('10')
        self.calc.operation_click('+')

        # Проверяем сброс дисплея
        self.assertEqual(self.calc.get_current_value(), '0')
        self.assertEqual(self.calc.previous_value, 10)
        self.assertEqual(self.calc.pending_operation, '+')

        # Вводим второе число и вычисляем
        self.calc.set_current_value('5')
        result = self.calc.calculate()

        # Проверяем результат
        self.assertEqual(result, 15)
        self.assertEqual(self.calc.get_current_value(), '15.0')

    def test_subtraction(self):
        """Тест операции вычитания"""
        self.calc.set_current_value('20')
        self.calc.operation_click('-')
        self.calc.set_current_value('8')
        result = self.calc.calculate()

        self.assertEqual(result, 12)
        self.assertEqual(self.calc.get_current_value(), '12.0')

    def test_multiplication(self):
        """Тест операции умножения"""
        self.calc.set_current_value('6')
        self.calc.operation_click('*')
        self.calc.set_current_value('7')
        result = self.calc.calculate()

        self.assertEqual(result, 42)
        self.assertEqual(self.calc.get_current_value(), '42.0')

    def test_division(self):
        """Тест операции деления"""
        # Нормальное деление
        self.calc.set_current_value('15')
        self.calc.operation_click('/')
        self.calc.set_current_value('3')
        result = self.calc.calculate()

        self.assertEqual(result, 5)
        self.assertEqual(self.calc.get_current_value(), '5.0')

        # Деление на ноль
        self.calc.set_current_value('10')
        self.calc.operation_click('/')
        self.calc.set_current_value('0')
        result = self.calc.calculate()

        self.assertEqual(result, "Error")
        self.assertEqual(self.calc.get_current_value(), "Error")

    def test_sin_operation(self):
        """Тест функции синуса"""
        self.calc.set_current_value('0')
        result = self.calc.scientific_operation('sin')

        self.assertEqual(result, 0)
        self.assertEqual(self.calc.get_current_value(), '0.0')

    def test_cos_operation(self):
        """Тест функции косинуса"""
        self.calc.set_current_value('0')
        result = self.calc.scientific_operation('cos')

        self.assertEqual(result, 1)
        self.assertEqual(self.calc.get_current_value(), '1.0')

    def test_square_root(self):
        """Тест квадратного корня"""
        # Нормальный корень
        self.calc.set_current_value('16')
        result = self.calc.scientific_operation('√')

        self.assertEqual(result, 4)
        self.assertEqual(self.calc.get_current_value(), '4.0')

        # Корень из отрицательного числа
        self.calc.set_current_value('-4')
        result = self.calc.scientific_operation('√')

        self.assertEqual(result, "Error")
        self.assertEqual(self.calc.get_current_value(), "Error")

    def test_power_operation(self):
        """Тест возведения в степень"""
        self.calc.set_current_value('2')
        self.calc.scientific_operation('x^y')  # Устанавливаем основание

        self.assertEqual(self.calc.previous_value, 2)
        self.assertEqual(self.calc.pending_operation, 'pow')

        self.calc.set_current_value('3')
        result = self.calc.calculate()  # Вычисляем степень

        self.assertEqual(result, 8)
        self.assertEqual(self.calc.get_current_value(), '8.0')

    def test_percentage_operation(self):
        """Тест операции процента"""
        self.calc.set_current_value('50')
        result = self.calc.scientific_operation('%')

        self.assertEqual(result, 0.5)
        self.assertEqual(self.calc.get_current_value(), '0.5')

    def test_floor_operation(self):
        """Тест округления в меньшую сторону"""
        self.calc.set_current_value('3.7')
        result = self.calc.scientific_operation('floor')

        self.assertEqual(result, 3)
        self.assertEqual(self.calc.get_current_value(), '3')

    def test_ceil_operation(self):
        """Тест округления в большую сторону"""
        self.calc.set_current_value('3.2')
        result = self.calc.scientific_operation('ceil')

        self.assertEqual(result, 4)
        self.assertEqual(self.calc.get_current_value(), '4')

    def test_memory_operations(self):
        """Тест операций с памятью"""
        # M+ - добавление в память
        self.calc.set_current_value('25')
        result = self.calc.memory_operation('M+')

        self.assertEqual(result, 25)
        self.assertEqual(self.calc.memory, 25)

        # MR - чтение из памяти
        self.calc.set_current_value('0')
        result = self.calc.memory_operation('MR')

        self.assertEqual(result, 25)
        # Принимаем оба формата '25' и '25.0'
        current_value = self.calc.get_current_value()
        self.assertTrue(current_value in ['25', '25.0'])

    def test_error_handling(self):
        """Тест обработки ошибок"""
        # Ошибка при операции с нечисловым вводом
        self.calc.set_current_value('abc')
        success = self.calc.operation_click('+')

        self.assertFalse(success)
        self.assertEqual(self.calc.get_current_value(), "Error")

    def test_complex_operation_chain(self):
        """Тест цепочки операций"""
        # (10 + 5) * 2
        self.calc.set_current_value('10')
        self.calc.operation_click('+')
        self.calc.set_current_value('5')
        self.calc.calculate()  # 15

        self.calc.operation_click('*')
        self.calc.set_current_value('2')
        result = self.calc.calculate()

        self.assertEqual(result, 30)
        self.assertEqual(self.calc.get_current_value(), '30.0')


def run_tests():
    """Запуск тестов с подробным выводом"""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    run_tests()