from requests import get, delete


print(get('http://127.0.0.1:8080/api/profile/Alice').json())
print(get('http://127.0.0.1:8080/api/movies/all').json())
print(get('http://127.0.0.1:8080/api/map/cinema').json())
print()

#  Пустой запрос
print(delete('http://127.0.0.1:8080/api/movies/delete', json={}).json())


#  Отсутствующие значения в запросе
print(delete('http://127.0.0.1:8080/api/movies/delete', json={'movie_id': '1'}).json())


#  Неправильные значения аккаунта администратора
print(delete('http://127.0.0.1:8080/api/movies/delete', json={
    'admin_email': 'AAdmin@mail.ru',
    'admin_password': 'qwerty',
    'movie_id': '9',
}).json())


#  Отсутствие фильма
print(delete('http://127.0.0.1:8080/api/movies/delete', json={
    'admin_email': 'a@a',
    'admin_password': 'a',
    'movie_id': '9',
}).json())
