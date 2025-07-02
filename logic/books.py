from db import mycursor

def search_by_title(title):
    sql = """
        SELECT id, title, authors, num_pages, average_rating
        FROM books
        WHERE title LIKE %s
        ORDER BY ratings_count DESC
    """
    search_term = f"%{title}%"
    mycursor.execute(sql, (search_term,))
    result = mycursor.fetchall()
    mycursor.clear_attributes()
    return result
