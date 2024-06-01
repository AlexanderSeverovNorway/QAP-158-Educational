from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Замените 'path_to_chromedriver' на путь к вашему chromedriver
driver = webdriver.Chrome('path_to_chromedriver')

# Устанавливаем неявные ожидания
driver.implicitly_wait(10)

# Открываем страницу
driver.get('https://petfriends.skillfactory.ru/login')

# Авторизация (замените на свои логин и пароль)
driver.find_element(By.ID, 'email').send_keys('your_email')
driver.find_element(By.ID, 'pass').send_keys('your_password')
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

# Переход на страницу со списком питомцев
driver.get('https://petfriends.skillfactory.ru/my_pets')

# Явные ожидания для таблицы питомцев
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

# Проверка, что присутствуют все питомцы
pet_cards = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
assert len(pet_cards) > 0, "На странице нет питомцев"

# Проверка, что хотя бы у половины питомцев есть фото
photos = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr img')
photo_count = sum(1 for photo in photos if photo.get_attribute('src') != '')
assert photo_count >= len(pet_cards) / 2, "Фото есть менее чем у половины питомцев"

# Проверка, что у всех питомцев есть имя, возраст и порода
names = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr td:nth-child(1)')
breeds = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr td:nth-child(2)')
ages = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr td:nth-child(3)')

for name, breed, age in zip(names, breeds, ages):
    assert name.text != '', "У одного из питомцев нет имени"
    assert breed.text != '', "У одного из питомцев нет породы"
    assert age.text != '', "У одного из питомцев нет возраста"

# Проверка, что у всех питомцев разные имена
name_texts = [name.text for name in names]
assert len(name_texts) == len(set(name_texts)), "Есть питомцы с одинаковыми именами"

# Проверка, что в списке нет повторяющихся питомцев
pets_info = [(name.text, breed.text, age.text) for name, breed, age in zip(names, breeds, ages)]
assert len(pets_info) == len(set(pets_info)), "Есть повторяющиеся питомцы"

print("Все проверки пройдены")

# Закрываем браузер
driver.quit()
