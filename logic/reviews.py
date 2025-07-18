from db import mycursor, mydb
from datetime import datetime

def add_review(user_id, book_id, rating, review_text):
    current_date = datetime.now().strftime("%Y-%m-%d")
    sql = '''
        INSERT INTO reviews (user_id, book_id, rating, comment, review_date)
        VALUES (%s, %s, %s, %s, %s)
    '''
    try:
        mycursor.execute(sql, (user_id, book_id, rating, review_text, current_date))
        mydb.commit()
    except Exception as e:
        print(f"Error adding review: {e}")
        return False
    mycursor.clear_attributes()
    print("Review added!")
    return True

def get_reviews(book_id):
    sql = '''
        SELECT u.username, r.rating, r.comment, r.review_date
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.book_id = %s
        ORDER BY r.review_date DESC
    '''
    try:
        mycursor.execute(sql, (book_id,))
        result = mycursor.fetchall()
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return []
    mycursor.clear_attributes()
    return result

def get_recent_reviews(limit=20):
    sql = '''
        SELECT b.title, u.username, r.rating, r.comment, r.review_date
        FROM reviews r
        JOIN books b ON r.book_id = b.id
        JOIN users u ON r.user_id = u.id
        ORDER BY r.review_date DESC
        LIMIT %s
    '''
    try:
        mycursor.execute(sql, (limit,))
        result = mycursor.fetchall()
    except Exception as e:
        print(f"Error fetching recent reviews: {e}")
        return []
    mycursor.clear_attributes()
    return result
