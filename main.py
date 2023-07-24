import requests
import sqlite3
import re


def post_comment_to_wordpress(url: str, post_id: int, author_name: str, author_email: str, content: str) -> None:
    if not re.match(r'^https?://', url):
        raise ValueError("Некорректный URL. Должен начинаться с 'https://' или 'http://'.")
    base_url = f'{url.rstrip("/")}/wp-json/wp/v2/comments'
    headers = {'Content-Type': 'application/json'}
    data = {
        'post': post_id,
        'author_name': author_name,
        'author_email': author_email,
        'content': content
    }

    response = requests.post(base_url, headers=headers, json=data)

    if response.status_code == 201:
        print(f'Комментарий успешно опубликован для поста с ID {post_id}.')
    else:
        print(f'Ошибка при публикации комментария: {response.status_code} - {response.text}')


def get_all_comments_from_db() -> [dict]:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments')
    comments = cursor.fetchall()
    conn.close()

    return comments


def get_comment_by_id_from_db(comment_id: int) -> None | dict:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments WHERE id = ?', (comment_id,))
    comment = cursor.fetchone()
    conn.close()
    return comment


def post_posts(url: str, comment_id: int | None = None) -> None:
    if comment_id:
        comment = get_comment_by_id_from_db(comment_id)
        if comment:
            post_comment_to_wordpress(url, comment[1], comment[2], comment[3], comment[4])
        else:
            print(f'Комментарий с ID {comment_id} не найден.')

    else:
        comments_from_db = get_all_comments_from_db()
        for comment in comments_from_db:
            post_comment_to_wordpress(url, comment[1], comment[2], comment[3], comment[4])


post_posts(url='https://some/', comment_id=1)
