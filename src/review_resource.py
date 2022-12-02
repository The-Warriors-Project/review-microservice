from datetime import datetime

import pymysql


class ReviewResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        # usr = os.environ.get("DBUSER")
        # pw = os.environ.get("DBPW")
        # h = os.environ.get("DBHOST")
        usr = "admin"
        pw = "the_warriors"
        h = "books.c4m5teyjg8v7.us-east-1.rds.amazonaws.com"

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_book_id(book_id):
        sql = "SELECT *  FROM reviews_db.reviews AS t JOIN (SELECT user_id as user_id, count(*) AS num_reviews FROM reviews_db.reviews GROUP BY user_id) AS review_count ON review_count.user_id = t.user_id WHERE book_id=%s" 
        avg = "SELECT AVG(SCORE) as average_score FROM reviews_db.reviews where book_id=%s";
        #sql = "SELECT *, AVG(Score) AS average_score FROM reviews_db.reviews where book_id=%s";
        conn = ReviewResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=book_id)
        sql_result = cur.fetchall()
        res2 = cur.execute(avg, args=book_id)
        avg_result = cur.fetchone()

        return sql_result, avg_result["average_score"] 

    @staticmethod
    def get_by_user_id(user_id):
        sql = "SELECT * FROM reviews_db.reviews where user_id=%s";
        conn = ReviewResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=user_id)
        result = cur.fetchall()

        return result

    @staticmethod
    def get_by_review_id(review_id):
        sql = "SELECT * FROM reviews_db.reviews where _id=%s";
        conn = ReviewResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=review_id)
        result = cur.fetchall()

        return result

    @staticmethod
    def get_by_book_and_user_id(book_id, user_id):
        sql = "SELECT * FROM reviews_db.reviews where book_id=%s and user_id=%s"
        conn = ReviewResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, [book_id, user_id])
        result = cur.fetchall()

        return result

    @staticmethod
    def get_all_reviews():
        sql = "SELECT * FROM reviews_db.reviews";
        conn = ReviewResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()
        return result

    @staticmethod
    def create_review(book_id, review_text, user_id, score):
        t = datetime.now()
        sql = "INSERT INTO reviews_db.reviews (book_id, review_text, user_id, score, date) VALUES (%s, %s, %s, %s, %s)"
        conn = ReviewResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, [book_id, review_text, user_id, score, t])
        result = ReviewResource.get_by_review_id(cur.lastrowid)[0]
        result["status"] = "SUCCESS"

        return result
