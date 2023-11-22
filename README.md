# Ｋｕｄａ ｐｏｙｔｉ — Ｍｏｓｋｖａ ｇｌａｚａｍｉ Ｖｌａｄｙ

Сервис о самых интересных местах в Москве.

![&#x41A;&#x443;&#x434;&#x430; &#x43F;&#x43E;&#x439;&#x442;&#x438;](.gitbook/assets/places.gif)

[Демка сайта](https://trapeznikovavv.pythonanywhere.com/).

## Как запустить

Для запуска сайта вам понадобится Python третьей версии. (Подойдут 3.10-3.11)


* Скачайте код
```commandline
git clone https://github.com/vlada-97/yandex_afisha_django.git
```

* Установите зависимости проекта
```commandline
pip install -r requirements.txt
```

* Накатите миграции
```commandline
python manage.py migrate
```

* Запустите веб-сервер
```commandline
python manage.py runserver
```
  
* Откройте в браузере


## Настройки

* Переменные окружения
  Чтобы их определить, создайте файл .env рядом с manage.py и запишите туда данные в таком формате: ПЕРЕМЕННАЯ=значение.
```python
DEBUG — режим отладки. Поставьте True, чтобы увидеть отладочную информацию в случае ошибки.
SECRET_KEY — секретный ключ проекта установки Django, должен быть уникальным
ALLOWED_HOSTS — список строк, представляющих имена хостов/доменов, которые может обслуживать этот сайт Django. 
```

[Документация](https://docs.djangoproject.com/en/4.2/ref/settings/) 

## Источники данных

Фронтенд получает данные из JSON-файлов. Ниже представлен правильный формат:

```javascript
{
    "title": "Экскурсионный проект «Крыши24.рф»",
    "imgs": [
        "https://kudago.com/media/images/place/d0/f6/d0f665a80d1d8d110826ba797569df02.jpg",
        "https://kudago.com/media/images/place/66/23/6623e6c8e93727c9b0bb198972d9e9fa.jpg",
        "https://kudago.com/media/images/place/64/82/64827b20010de8430bfc4fb14e786c19.jpg",
    ],
    "description_short": "Хотите увидеть Москву с высоты птичьего полёта?",
    "description_long": "<p>Проект «Крыши24.рф» проводит экскурсии ...</p>",
    "coordinates": {
        "lat": 55.753676,
        "lng": 37.64
    }
}
```

### Для того, чтобы добавить новые места, используется скрипт *load_place.py*

Способ применения:
```
python manage.py load_place --url [some_url] 
```

Предлагаемые к скрипту аргументы:
* *--file* - для загрузки из json-файла
* *--skip_imgs* -  не сохранять картинки
  

## Используемые библиотеки

* [Leaflet](https://leafletjs.com/) — отрисовка карты
* [loglevel](https://www.npmjs.com/package/loglevel) для логгирования
* [Bootstrap](https://getbootstrap.com/) — CSS библиотека
* [Vue.js](https://ru.vuejs.org/) — реактивные шаблоны на фронтенде

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

Тестовые данные взяты с сайта [KudaGo](https://kudago.com).

