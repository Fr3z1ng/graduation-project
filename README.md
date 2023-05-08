# Веб-сайт для мастера по тейпированию
Описание проекта: Веб-сайт мастера красоты для записи на услуги. Пользователь может зарегистрироваться,авторизироваться,разлогироваться.
При регистрации отправляется письмо на почту. Изменять пароль аккаунта, восстанавливать пароль через почту, так же редактировать свой профиль.
Может записываться на определенное время и дату у мастера. Добавлять отзывы и редактировать их, просматривать фотогаларею.
***
* Статус разработки: разработан.
* Статус билда: N/A.
* Процент покрытия тестами: N/A.

## Содержание
- [Технологии](#технологии)
- [Начало работы](#использование)
- [Contributing](#contributing)
- [To do](#to-do)

## Технологии
- <a href="https://imgbb.com/"><img src="https://i.ibb.co/nMvphPm/Python-Logo.jpg" alt="Python-Logo" border="0" width="64" height="64"></a>
- <a href="https://ibb.co/b3cCNDW"><img src="https://i.ibb.co/b3cCNDW/Django-logo-474x360-1.jpg" alt="Django-logo-474x360-1" border="0" width="64" height="64"></a>
- <a href="https://ibb.co/LJZ0nrd"><img src="https://i.ibb.co/LJZ0nrd/redis.png" alt="redis" border="0" width="64" height="64"></a>
- <a href="https://ibb.co/FxTVQSx"><img src="https://i.ibb.co/FxTVQSx/postgres.png" alt="postgres" border="0" width="64" height="64"></a>
- <a href="https://imgbb.com/"><img src="https://i.ibb.co/TcLrtwr/D0fda7227a74173d75a467fe0838d080.jpg" alt="D0fda7227a74173d75a467fe0838d080" border="0"></a>


## Использование
1. Запустите pip install -r requirements.txt

2. Запустите django
   ```
   python3 manage.py runserver
   ```
3. Запустите Redis
   ```
   start redis-server  
   ```
4. Запустите Celery
   ```
   python3 -m celery -A online worker  
   ```
5. Запустите Celery-beat
   ```
   celery -A online  beat -l info   
   ```

## TO DO
* Система оплаты
* Добавление API
* Разделение ролей
- [x] Добавить крутое README
- [ ] Система оплаты
- [ ] Добавление API
- [ ] Разделение ролей


## Contributing
Чтобы помочь в разботке или сообщить о баге отправляйте на этот гитхаб https://github.com/Fr3z1ng


## Лицензия

Distributed under the MIT License. See `LICENSE.txt` for more information.


## Контакты

Alexander Shauro - [@linkendin](https://www.linkedin.com/in/alexander-shauro-1430b0274)

### Зачем вы разработали этот проект?
Проект поможет мастерам в сфере красоты, использовать этот проект для записи своих клиентов.

## Источники
Документация django - https://docs.djangoproject.com/en/4.2/
