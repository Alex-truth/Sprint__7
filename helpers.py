import allure
import random
import string

allure.title('Генерирует случайную строку из букв и цифр')
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))