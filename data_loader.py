import pandas as pd
import requests
import os


def read_from_YD(url: str, filename: str) -> pd.DataFrame:
    # URL для загрузки файла с Яндекс.Диска
    download_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'
    # Параметры запроса
    params = {'public_key': url, 'path': '/' + filename}
    # Отправляем GET-запрос для получения ссылки на скачивание файла
    response = requests.get(download_url, params=params)

    # Если в ответе не была найдена ссылка на скачивание файла
    try:
        # Получаем ссылку на скачивание файла
        download_link = response.json()['href']
    # Если в ответе не была найдена ссылка на скачивание файла
    except KeyError:
        # Проверяем, существует ли файл в текущей директории
        if os.path.isfile(filename):
            # Если файл существует, читаем его и возвращаем как DataFrame
            df = pd.read_csv(filename, sep=';', comment='#', on_bad_lines='skip')
            return df
        else:
            # Если файл не существует, выводим сообщение об ошибке и выходим из программы
            print("Ссылка не работает и данный файл не обнаружен в рабочей директории")
            exit(1)

    # Отправляем GET-запрос для скачивания файла
    r = requests.get(download_link)

    # Сохраняем скачанный файл
    with open(filename, 'wb') as f:
        f.write(r.content)

    # Читаем скачанный файл и возвращаем его как DataFrame
    df = pd.read_csv(filename, sep=';', comment='#', on_bad_lines='skip')
    return df










