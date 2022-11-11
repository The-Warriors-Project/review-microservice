import pymysql
from datetime import datetime

import os


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
        h =  "books.c4m5teyjg8v7.us-east-1.rds.amazonaws.com"

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
        sql = "SELECT * FROM reviews_db.reviews where _id=%s";
        conn = ReviewResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=book_id)
        result = cur.fetchall()

        return result

    @staticmethod
    def get_by_user_id(user_id):
        sql = "SELECT * FROM reviews_db.reviews where user_id=%s";
        conn = ReviewResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=user_id)
        result = cur.fetchall()

        return result

    @staticmethod
    def get_by_book_and_user_id(book_id, user_id):
        sql = "SELECT * FROM reviews_db.reviews where _id=%s and review_id=%s"
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
        sql = "INSERT INTO reviews_db.reviews (_id, review_text, user_id, score, date) VALUES (%s, %s, %s, %s, %s)"
        conn = ReviewResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql,[book_id,review_text,user_id,score, t])
        print("What's happening y'all!")
        
        return "success" 
