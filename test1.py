import unittest
from task_1 import sum, sub, mul, div, mod


class TestTask1(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum(1, 2), 3)
        self.assertEqual(sum(0, 0), 0)
        self.assertEqual(sum(-1, 1), 0)
        self.assertEqual(sum(-1, -1), -2)
        # Дополнительные проверки
        self.assertNotEqual(sum(1, 2), 4)  # не должно быть 4
        self.assertTrue(sum(5, 5) == 10)   # должно быть истинно
        self.assertFalse(sum(1, 1) == 3)   # не должно быть 3 → False

    def test_sub(self):
        self.assertEqual(sub(1, 2), -1)
        self.assertEqual(sub(0, 0), 0)
        self.assertEqual(sub(-1, 1), -2)
        self.assertEqual(sub(-1, -1), 0)
        self.assertEqual(sub(1, -1), 2)
        # Дополнительные проверки
        self.assertNotEqual(sub(10, 5), 10)  # очевидно не 10
        self.assertTrue(sub(10, 5) == 5)     # должно быть 5 → True
        self.assertFalse(sub(0, 1) > 0)      # 0 - 1 = -1 → не > 0 → False

    def test_mul(self):
        self.assertEqual(mul(1, 2), 2)
        self.assertEqual(mul(0, 0), 0)
        self.assertEqual(mul(-1, 1), -1)
        self.assertEqual(mul(-1, -1), 1)
        # Дополнительные проверки
        self.assertNotEqual(mul(3, 3), 6)    # 3*3 ≠ 6
        self.assertTrue(mul(7, 1) == 7)      # 7*1 == 7 → True
        self.assertFalse(mul(2, 2) == 5)     # 2*2 ≠ 5 → False

    def test_div(self):
        # Нормальные случаи
        self.assertEqual(div(1, 2), 0.5)
        self.assertEqual(div(-1, 1), -1)
        self.assertEqual(div(-1, -1), 1)
        # Проверка исключений на assertRaises — способ проверить в тестах, что функция действительно корректно сигнализирует об ошибке.
        with self.assertRaises(ZeroDivisionError): # self.assertRaises(ZeroDivisionError) Это — метод из unittest.TestCase, который говорит:
            # «Я ожидаю, что в следующем блоке кода будет выброшено именно это исключение — ZeroDivisionError».
            div(1, 0) # Если ничего не происходит — assertRaises говорит: «А где ошибка? Я же ждал ZeroDivisionError!» → тест падает.
        with self.assertRaises(ZeroDivisionError):
            div(0, 0) # но здесь диление на 0, поэтому тест не падает
        # Дополнительные проверки
        self.assertNotEqual(div(10, 2), 3)   # 10/2 ≠ 3
        self.assertTrue(div(9, 3) == 3)      # 9/3 == 3 → True
        # Проверка типа результата (если не ошибка — должен быть float или int)
        result = div(6, 2)
        self.assertIsInstance(result, (int, float))

    def test_mod(self):

        # Дополнительные проверки
        self.assertNotEqual(mod(5, 3), 0)    # 5 % 3 = 2 ≠ 0
        self.assertTrue(mod(4, 2) == 0)      # 4 % 2 == 0 → True
        self.assertFalse(mod(7, 4) == 1)     # 7 % 4 = 3 ≠ 1 → False

        # Нормальные случаи
        self.assertEqual(mod(1, 2), 1)
        self.assertEqual(mod(-1, 1), 0)
        self.assertEqual(mod(-1, -1), 0)
        # Проверка исключений
        with self.assertRaises(ZeroDivisionError):
            mod(5, 0)
        with self.assertRaises(ZeroDivisionError):
            mod(0, 0)



if __name__ == '__main__':
    unittest.main()