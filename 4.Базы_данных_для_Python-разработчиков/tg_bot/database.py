import psycopg2

def create_db():
    params = {
        "database": "english_card",
        "user": "postgres",
        "password": "123",
        "host": "localhost",
        "port": "5432"
    }
    conn = psycopg2.connect(**params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS common_words (
                id SERIAL PRIMARY KEY,
                target_word VARCHAR(50) NOT NULL,
                translate_word VARCHAR(50) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS personal_words (
                id SERIAL PRIMARY KEY,
                target_word VARCHAR(50) NOT NULL,
                translate_word VARCHAR(50) NOT NULL,
                user_id INTEGER REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS user_word_relation (
                user_id INTEGER REFERENCES users(id),
                word_id INTEGER REFERENCES common_words(id),
                is_learned BOOLEAN DEFAULT FALSE,
                PRIMARY KEY (user_id, word_id)
            );
        """)

        base_words = [
            ('Red', 'Красный'), ('Green', 'Зеленый'), ('Blue', 'Синий'),
            ('White', 'Белый'), ('Black', 'Черный'), ('I', 'Я'),
            ('You', 'Ты'), ('He', 'Он'), ('She', 'Она'), ('It', 'Оно')
        ]

        # Добавляем слова через ON CONFLICT, чтобы не плодить дубли
        for target, translate in base_words:
            cur.execute("""
                INSERT INTO common_words (target_word, translate_word) 
                SELECT %s, %s WHERE NOT EXISTS (
                    SELECT 1 FROM common_words WHERE target_word = %s
                );
            """, (target, translate, target))

    conn.commit()
    conn.close()
    print("База данных готова!")

def add_user(chat_id):
    conn = psycopg2.connect(database="english_card", user="postgres", password="123", host="localhost")
    with conn.cursor() as cur:
        cur.execute("INSERT INTO users (chat_id) VALUES (%s) ON CONFLICT (chat_id) DO NOTHING;", (chat_id,))
    conn.commit()
    conn.close()

def get_random_word(cid):
    conn = psycopg2.connect(database="english_card", user="postgres", password="123", host="localhost")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT target_word, translate_word FROM (
                -- Берем общие слова
                SELECT target_word, translate_word FROM common_words
                WHERE target_word NOT IN (
                    -- Исключаем те ИМЕНА слов, которые пользователь скрыл
                    SELECT cw.target_word 
                    FROM common_words cw
                    JOIN user_word_relation uwr ON cw.id = uwr.word_id
                    WHERE uwr.user_id = (SELECT id FROM users WHERE chat_id = %s LIMIT 1)
                )
                UNION
                -- Добавляем личные слова
                SELECT target_word, translate_word FROM personal_words
                WHERE user_id = (SELECT id FROM users WHERE chat_id = %s LIMIT 1)
            ) AS combined
            ORDER BY RANDOM() 
            LIMIT 1;
        """, (cid, cid))
        word = cur.fetchone()
    conn.close()
    return word

def get_wrong_words(correct_word):
    conn = psycopg2.connect(database="english_card", user="postgres", password="123", host="localhost")
    with conn.cursor() as cur:
        cur.execute("SELECT translate_word FROM common_words WHERE target_word != %s ORDER BY RANDOM() LIMIT 3;", (correct_word,))
        data = cur.fetchall()
    conn.close()
    return [row[0] for row in data]

def add_word_to_db(cid, target_word, translate):
    conn = psycopg2.connect(database="english_card", user="postgres", password="123", host="localhost")
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO personal_words (user_id, target_word, translate_word) 
            VALUES ((SELECT id FROM users WHERE chat_id = %s LIMIT 1), %s, %s)
        """, (cid, target_word, translate))
    conn.commit()
    conn.close()

def get_user_words(cid):
    conn = psycopg2.connect(database="english_card", user="postgres", password="123", host="localhost")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT target_word FROM personal_words 
            WHERE user_id = (SELECT id FROM users WHERE chat_id = %s LIMIT 1)
        """, (cid,))
        words = [row[0] for row in cur.fetchall()]
    conn.close()
    return words

def delete_word_from_db(cid, word):
    conn = psycopg2.connect(database="english_card", user="postgres", password="123", host="localhost")
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM personal_words 
            WHERE target_word = %s 
            AND user_id = (SELECT id FROM users WHERE chat_id = %s LIMIT 1)
        """, (word, cid))
    conn.commit()
    conn.close()

def get_all_common_words():
    conn = psycopg2.connect(database="english_card", user="postgres", password="123", host="localhost")
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT target_word FROM common_words ORDER BY target_word;")
        words = [row[0] for row in cur.fetchall()]
    conn.close()
    return words

def get_excluded_words(cid):
    conn = psycopg2.connect(database="english_card", user="postgres", password="123", host="localhost")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT cw.target_word FROM common_words cw
            JOIN user_word_relation uwr ON cw.id = uwr.word_id
            WHERE uwr.user_id = (SELECT id FROM users WHERE chat_id = %s LIMIT 1)
        """, (cid,))
        words = [row[0] for row in cur.fetchall()]
    conn.close()
    return words

def toggle_word_exclusion(cid, word_text):
    conn = psycopg2.connect(database="english_card", user="postgres", password="123", host="localhost")
    with conn.cursor() as cur:
        # Проверяем наличие по тексту слова, а не по ID
        cur.execute("""
            SELECT 1 FROM user_word_relation 
            WHERE user_id = (SELECT id FROM users WHERE chat_id = %s LIMIT 1)
            AND word_id IN (SELECT id FROM common_words WHERE target_word = %s);
        """, (cid, word_text))
        exists = cur.fetchone()

        if exists:
            # Если хоть один экземпляр слова в исключениях — удаляем ВСЕ связи с этим словом
            cur.execute("""
                DELETE FROM user_word_relation 
                WHERE user_id = (SELECT id FROM users WHERE chat_id = %s LIMIT 1)
                AND word_id IN (SELECT id FROM common_words WHERE target_word = %s);
            """, (cid, word_text))
            action = "returned"
        else:
            # Если слова нет в исключениях — добавляем (берем первый попавшийся ID этого слова)
            cur.execute("""
                INSERT INTO user_word_relation (user_id, word_id, is_learned)
                VALUES (
                    (SELECT id FROM users WHERE chat_id = %s LIMIT 1), 
                    (SELECT id FROM common_words WHERE target_word = %s LIMIT 1), 
                    TRUE
                );
            """, (cid, word_text))
            action = "excluded"
    conn.commit()
    conn.close()
    return action

def cleanup_duplicates():
    conn = psycopg2.connect(
        database="english_card",
        user="postgres",
        password="123",
        host="localhost"
    )
    with conn.cursor() as cur:
        # запрос на удаление дублей
        cur.execute("""
            DELETE FROM common_words 
            WHERE id NOT IN (
                SELECT MIN(id) FROM common_words 
                GROUP BY target_word
            );
        """)
        print(f"Очистка завершена: удалено {cur.rowcount} дубликатов.")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    cleanup_duplicates()