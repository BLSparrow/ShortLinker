import sqlite3
# создание таблиц
def db_create():
    try:
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT));""")
        con.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS links(
            id INTEGER,
            user_id INTEGER,
            psevdonim TEXT NOT NULL,
            link TEXT NOT NULL,
            status TEXT NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT),
            FOREIGN KEY(user_id) REFERENCES users(id));""")
        con.commit()
    except sqlite3.Error:
        print("Ошибка создание бд")
    finally:
        con.close()


# Проверка
def db_loginId(login):
    try:
        print("Проверка")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        user = cursor.execute("""SELECT login FROM users WHERE login = ?""",(login,)).fetchone()
        if not user:
            print("Можно регаться!")
            return 0
        else:
            print("Такой логин уже есть!")
            return 1
    except sqlite3.Error:
        print("Ошибка в авторизации")
    finally:
        con.close()

# создание пользователя
def db_reg_user(login, password):
    try:
        print("Регистрация")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        cursor.execute("""INSERT INTO users (login, password) VALUES(?, ?)""",(login, password,))
        con.commit()
        print("Вы зарегистрировались!")
    except sqlite3.Error:
        print("Ошибка в регистрации")
        print(login)
    finally:
        con.close()


# авторизация
def db_auth(login, password):
    try:
        print("Авторизация")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        user = cursor.execute("""SELECT * FROM users WHERE login = ? AND password = ?""",(login, password,)).fetchall()
        if len(user) == 0:
            print("Неверный логин или пароль!")
            return 0
        else:
            print(user)
            print("Вы вошли!")
            return 1
    except sqlite3.Error:
        print("Ошибка в авторизации")
    finally:
        con.close()


def getUserByLogin(login):
    try:
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        res = cursor.execute("""SELECT * FROM users WHERE login = ? LIMIT 1""",(login,)).fetchone()
        if not res:
            print('Пользователь не найден!')
            return False   
        return res
    except sqlite3.Error as e:
        print('Ошибка получения данных из БД - getUserByLogin - ' + str(e))
    return False


def getUser(user_id):
    try:
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        res = cursor.execute("""SELECT * FROM users WHERE id = ? LIMIT 1""",(user_id,)).fetchone()
        if not res:
            print('Пользователь не найден!')
            return False   
        return res
    except sqlite3.Error as e:
        print('Ошибка получения данных из БД - getUser - ' + str(e))
    return False


# сокращение ссылки
def db_short(user_id, psevdonim, link, status):
    try:
        print("Идёт сокращение ссылки")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        cursor.execute("""INSERT INTO links (user_id, psevdonim, link, status) VALUES(?, ?, ?, ?)""",(user_id, psevdonim, link, status,))
        con.commit()
        print("Вы сократили ссылку!")
    except sqlite3.Error:
        print("Ошибка в сокращении")
    finally:
        con.close()

# Показать мои ссылки
def db_getLinkPrivate(user_id):
    try:
        print("Ваши (приватные) ссылки")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        links = cursor.execute("""SELECT * FROM links WHERE user_id = ?""",(user_id,)).fetchall()
        con.commit()
        print(links)
        return links
    except sqlite3.Error:
        print("Ошибка при выводе ссылок")
    finally:
        con.close()

# Показать ссылки
def db_getLinkPublic():
    try:
        print("Ваши ссылки")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        links = cursor.execute("""SELECT * FROM links WHERE status = 'Публичная'""").fetchall()
        con.commit()
        print(links)
        return links
    except sqlite3.Error:
        print("Ошибка при выводе ссылок")
    finally:
        con.close()


# Показать ссылки Общего доступа
def db_getLinkOBD():
    try:
        print("Ваши ссылки")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        links = cursor.execute("""SELECT * FROM links WHERE status = 'Общего доступа'""").fetchall()
        con.commit()
        print(links)
        return links
    except sqlite3.Error:
        print("Ошибка при выводе ссылок")
    finally:
        con.close()

# Удалить ссылку
def db_deleteLink(user_id,id):
    try:
        print("Удаление")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        cursor.execute("""DELETE FROM links WHERE user_id = ? AND id = ?""",(user_id,id,)).fetchone()
        con.commit()
    except sqlite3.Error:
        print("Ошибка при удалении")
    finally:
        con.close()


# Показать ссылки по id
def db_getLink(id):
    try:
        print("Ваша ссылка")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        link = cursor.execute("""SELECT * FROM links WHERE id = ?""",(id,)).fetchone()
        con.commit()
        print(link)
        return link
    except sqlite3.Error:
        print("Ошибка при выводе ссылки")
    finally:
        con.close()


# Редактирование
def db_update(psevdonim, status, id):
    try:
        print("Редактирование ссылки")
        con = sqlite3.connect('shortlink.db')
        cursor = con.cursor()
        link = cursor.execute("""UPDATE links SET psevdonim = ?, status = ? WHERE id = ?""",(psevdonim, status, id,)).fetchone()
        con.commit()
        print(link)
        return link
    except sqlite3.Error:
        print("Ошибка при редактировании ссылки")
    finally:
        con.close()



# # Выбор категории  
# def db_user_sub(login_id, name):
#     try:
#         print("Выбор категории")
#         con = sqlite3.connect('users.db')
#         cursor = con.cursor()
#         user_id = cursor.execute("""SELECT * FROM users WHERE login_id = ?""",(login_id,)).fetchone()
#         category_id = cursor.execute("""SELECT * FROM category WHERE name = ?""",(name,)).fetchone()
#         subscription = cursor.execute("""SELECT * FROM subscription  WHERE user_id = ? AND category_id = ?""",(user_id[0],category_id[0],)).fetchone()
#         if not subscription:
#             cursor.execute("""INSERT INTO subscription (user_id, category_id) VALUES(?, ?)""",(user_id[0], category_id[0],))
#             con.commit()
#             print("Категория выбрана!")
#             s = "Категория выбрана!"
#             return s
#         elif subscription[1]==user_id[0] and subscription[2]==category_id[0]:
#             print("Вы уже подписан на эту категорию")
#             s = "Вы уже подписан на эту категорию"
#             return s
#     except sqlite3.Error:
#         print("Ошибка в выборе категории")
#     finally:
#         con.close()




# # Категории пользователей
# def db_user_get_sub(login_id):
#     try:
#         print("Все данные")
#         con = sqlite3.connect('users.db')
#         cursor = con.cursor()
#         info = cursor.execute("""SELECT category.name FROM category 
#                                 JOIN users ON subscription.user_id = users.id
#                                 JOIN subscription ON subscription.category_id = category.id where login_id = ?""",(login_id,)).fetchall()
#         print(info)
#         return info
#     except sqlite3.Error:
#         print("Ошибка в заполнении")
#     finally:
#         con.close()

# # удаление категории
# def db_user_del_sub(category_id):
#     try:
#         print("Удаление категории")
#         con = sqlite3.connect('users.db')
#         cursor = con.cursor()
#         sub = cursor.execute("""SELECT * FROM subscription WHERE category_id = ?""",(category_id,)).fetchone()
#         if not sub:
#             print("Вы не подписаны на эту категорию!")
#             s = "Вы не подписаны на эту категорию!"
#             return s
#         else:
#             cursor.execute("""DELETE FROM subscription WHERE category_id = ?""",(category_id,)).fetchall()
#             con.commit()
#             print("Вы отписались от категории!")
#             s = "Вы отписались от категории!"
#             return s
#     except sqlite3.Error:
#         print("Ошибка в удалении")
#     finally:
#         con.close()

# # Все категории
# def db_get_news(login_id):
#     try:
#         print("Все новости")
#         con = sqlite3.connect('users.db')
#         cursor = con.cursor()
#         categories = cursor.execute("""SELECT category.name FROM category 
#                                 JOIN users ON subscription.user_id = users.id
#                                 JOIN subscription ON subscription.category_id = category.id where login_id = ?""",(login_id,)).fetchall()
#         if not categories:
#             print(categories)
#             print("Вы не подписаны на новости")
#         else:
#             print(categories)
#             return categories
#     except sqlite3.Error:
#         print("Ошибка вывода новостей")
#     finally:
#         con.close()