import imaplib
import email
from pathlib import Path

# Базовая директория, от которой считаем все пути
BASE_DIR = Path(__file__).resolve().parent

# Учетные данные для почты
username = 'rsk-rasp@yandex.com'
password = 'nipyovoisqymdhfl'

# Подключение к Yandex почте
mail = imaplib.IMAP4_SSL('imap.yandex.com')
mail.login(username, password)
mail.select('inbox')

# Получение UID всех писем
result, data = mail.uid('search', None, 'ALL')

try:
    # Попытка получить последний UID письма
    latest_email_uid = data[0].split()[-1]
except (IndexError, AttributeError):
    print("Обновлений нет — новых писем не найдено.")
    mail.close()
    mail.logout()
    exit()

# Получение последнего письма
result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')

# Обработка содержимого письма
raw_email = email_data[0][1].decode('utf-8')
email_message = email.message_from_string(raw_email)

# Пути к папкам
resources_xl_path = BASE_DIR / 'resources' / 'xl'
output_dir = BASE_DIR / 'resources' / 'web' / 'output'

# Имя сохраняемого Excel-файла
xlsx_filename = 'raspisanie.xlsx'
xlsx_path = resources_xl_path / xlsx_filename

# Поиск и сохранение .xlsx вложения
for part in email_message.walk():
    if part.get_content_type() == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        # Удаление старого файла, если он есть
        if xlsx_path.exists():
            xlsx_path.unlink()
            print('Старый файл удалён.')
        else:
            print('Файл для удаления не найден.')

        # Убедимся, что папка существует
        resources_xl_path.mkdir(parents=True, exist_ok=True)

        # Сохраняем вложение
        with open(xlsx_path, 'wb') as f:
            f.write(part.get_payload(decode=True))
        print('Новый файл успешно загружен.')

        # Очистка папки output от файлов
        if output_dir.exists():
            for file in output_dir.glob('*'):
                if file.is_file():
                    file.unlink()
            print('Папка output очищена.')
        else:
            print('Папка output не найдена.')
        break

# Очистка входящих писем
mail.store('1:*', '+FLAGS', '\\Deleted')
mail.expunge()
print('Входящие письма удалены.')

# Завершение сессии
mail.close()
mail.logout()
