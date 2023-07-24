import sqlite3
import random
import string


def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def generate_random_email():
    domain = generate_random_string(5) + '.com'
    username = generate_random_string(8)
    return f'{username}@{domain}'


def generate_random_comment():
    post_id = random.randint(1, 10)  # ID записи, к которой относится комментарий
    author_name = generate_random_string(10)
    author_email = generate_random_email()
    content = generate_random_string(50)
    return post_id, author_name, author_email, content


def add_comment(post_id, author_name, author_email, content):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO comments (post_id, author_name, author_email, content) VALUES (?, ?, ?, ?)',
                   (post_id, author_name, author_email, content))
    conn.commit()
    conn.close()


for _ in range(50):  # Создаем 50 случайных комментариев
    comment_data = generate_random_comment()
    add_comment(*comment_data)

print("Автогенерация комментариев и добавление их в базу данных успешно завершены.")


