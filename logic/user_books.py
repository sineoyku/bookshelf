from db import mycursor, mydb
from datetime import datetime

def add_to_list(user_id, book_id):
    current_date = datetime.now().strftime("%Y-%m-%d")
    sql = """
            INSERT INTO user_books (user_id, book_id, start_date)
            VALUES (%s, %s, %s)
    """
    try:
        mycursor.execute(sql, (user_id, book_id, current_date))
        mydb.commit()
    except Exception as e:
        print(f"Error inserting into user_books: {e}")
        return False
    mycursor.clear_attributes()
    print("Added to your list!")
    return True

def get_user_list(user_id):
    sql = """
         SELECT 
             b.title,
             ub.status,
             ub.start_date,
             ub.end_date
        FROM 
              user_books ub
        JOIN 
            books b ON ub.book_id = b.id
        WHERE 
            ub.user_id = %s
        ORDER BY 
            ub.start_date ASC;
    """
    try:
        mycursor.execute(sql, (user_id,))
        result_set = mycursor.fetchall()
        mydb.commit()
    except Exception as e:
        print(f"Error getting list: {e}")
        return False
    mycursor.clear_attributes()
    return result_set
    

def update_book_status(user_id, book_title, new_status):
    sql = '''
        UPDATE user_books ub
        JOIN books b ON ub.book_id = b.id
        SET ub.status = %s
        WHERE ub.user_id = %s AND b.title = %s
    '''
    try:
        mycursor.execute(sql, (new_status, user_id, book_title))
        mydb.commit()
    except Exception as e:
        print(f"Error updating status: {e}")
        return False
    mycursor.clear_attributes()
    print("Status updated!")
    return True

def log_reading_progress(user_id, book_title, pages_read):
    sql = '''
        UPDATE user_books ub
        JOIN books b ON ub.book_id = b.id
        SET ub.pages_read = %s
        WHERE ub.user_id = %s AND b.title = %s
    '''
    try:
        mycursor.execute(sql, (pages_read, user_id, book_title))
        mydb.commit()
    except Exception as e:
        print(f"Error logging progress: {e}")
        return False
    mycursor.clear_attributes()
    print("Progress logged!")
    return True
    

