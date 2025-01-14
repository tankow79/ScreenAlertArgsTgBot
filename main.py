import telebot
import configparser
import PIL.ImageGrab
import os
import sys

# --- Завантаження налаштувань із файлу конфігурації ---
# Використовуємо `configparser` для читання налаштувань із файлу `config.ini`,
# який повинен містити параметри `bot_token` (токен бота) і `chat_id` (ідентифікатор чату).
config = configparser.ConfigParser()
try:
    config.read('config.ini', encoding='utf-8')  # Вказуємо кодування UTF-8
except Exception as e:
    print(f"Помилка при зчитуванні файлу конфігурації: {e}")
    sys.exit(1)

# Зчитуємо токен бота та chat_id з конфігураційного файлу
try:
    # Читаємо параметри з файлу конфігурації
    bot_token = config['telegram']['bot_token'].strip()  # Токен Telegram бота
    chat_id = config['telegram']['chat_id'].strip()  # Ідентифікатор чату
    computer_name = config['telegram']['computer_name'].strip()  # Назва ПК
except KeyError as e:
    print(f"Відсутній параметр у файлі конфігурації: {e}")
    sys.exit(1)

# Перевіряємо довжину параметрів токена та ідентифікатора чату
if not bot_token or not chat_id:
    print("Токен або chat_id не задано у файлі конфігурації.")
    sys.exit(1)

print(bot_token)
print(chat_id)
print(computer_name)

# Створення об'єкта бота TeleBot
bot = telebot.TeleBot(bot_token)


# --- Функція для отримання тексту повідомлення з аргументів командного рядка ---
def get_message_from_args() -> str:
    """
    Повертає текст повідомлення, переданий через аргументи командного рядка.
    Якщо аргументи не передано, програма завершує виконання.
    :return: Текст повідомлення з аргументів командного рядка
    """
    if len(sys.argv) < 2:
        # Завершуємо виконання, якщо не було передано повідомлення
        sys.exit(1)
    # Об'єднуємо усі аргументи в один текст повідомлення
    return ' '.join(sys.argv[1:])


# --- Функція для відправки текстового повідомлення в Telegram ---
def send_message_to_telegram(message) -> None:
    """
    Відправляє текстове повідомлення до Telegram через API бота.

    :param message: Текст повідомлення, який потрібно відправити
    """
    try:
        bot.send_message(chat_id, f"{computer_name}: {message}")  # Відправка повідомлення до чату
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Помилка при відправці повідомлення до Telegram: {e}")
        # Специфічна обробка помилки
        if e.result.status_code == 400:
            print("Опис помилки: Bad Request. Причини:")
            print("1. Неправильний chat_id.")
            print("2. Бот не має доступу до чату. Переконайтеся, що додали бота до чату або почали діалог із ботом.")
        elif e.result.status_code == 401:
            print("Опис помилки: Unauthorized. Причина: Неправильний чи недійсний токен бота.")
    except Exception as e:
        # У разі виникнення помилки повідомлення про це буде надіслано до чату
        print(f"Error: {e}")


# --- Функція для створення та відправки скріншоту ---
def send_screenshot(msg_text=None) -> None:
    """
    Знімає скріншот екрана, зберігає його у файл `screenshot.png`,
    та відправляє до Telegram. Після відправки файл видаляється.

    :param msg_text: Текст (підпис), який буде додано до скріншоту
    """
    screenshot_path = 'screenshot.png'  # Локальне ім'я файлу для скріншоту

    try:
        # 1. Знімаємо скріншот екрана
        try:
            screenshot = PIL.ImageGrab.grab()  # Знімає поточний стан екрану
        except Exception as e:
            raise RuntimeError(f"Помилка при створенні скріншоту: {e}")

        # 2. Зберігаємо скріншот у локальний файл
        try:
            screenshot.save(screenshot_path)
        except Exception as e:
            raise RuntimeError(f"Помилка при збереженні скріншоту у файл: {e}")

        # 3. Надсилаємо скріншот до Telegram
        try:
            with open(screenshot_path, 'rb') as file:
                if msg_text is None:
                    # Відправляємо без тексту (тільки зображення)
                    bot.send_photo(chat_id, file, caption=f"{computer_name}")
                else:
                    # Відправляємо з підписом
                    bot.send_photo(chat_id, file, caption=f"{computer_name}: {msg_text}")
        except telebot.apihelper.ApiTelegramException as e:
            raise RuntimeError(f"Помилка при відправці скріншоту до Telegram: {e}")
        except Exception as e:
            raise RuntimeError(f"Невідома помилка при відправці скріншоту: {e}")

    finally:
        # 4. Видаляємо локальний файл після відправки
        try:
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)  # Видаляємо файл
        except OSError as e:
            print(f"Помилка при видаленні скріншоту: {e}")

def main():
    # --- Основна логіка скрипту ---
    # Отримання тексту повідомлення з аргументів командного рядка
    message_text = get_message_from_args().strip()

    # --- Перевірка на наявність ключових слів ---
    if "screen" in message_text or "png" in message_text:
        """
        Якщо текст повідомлення має ключові слова, як-от "screen" або "png",
        то ці ключові слова видаляються, і виконується зняття/відправка скріншоту.
        """
        # Перелік ключових слів для видалення
        keywords_to_remove = ["screen", "png"]
        for keyword in keywords_to_remove:
            # Замінюємо ключові слова на порожній рядок
            message_text = message_text.replace(keyword, "")

        # Додаткове очищення повідомлення від зайвих пробілів
        message_text = message_text.strip()

        # Відправка скріншоту з очищеним текстом
        send_screenshot(message_text)
    else:
        """
        Якщо ключових слів немає, текст надсилається у вигляді звичайного повідомлення.
        """
        send_message_to_telegram(message_text)


if __name__ == '__main__':
    main()
