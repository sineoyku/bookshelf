from db import mycursor

def search_by_title(title):
    sql = "SELECT title, author, num_pages, average_rating FROM books WHERE title LIKE '%s%' ORDER BY ratings_count"
    mycursor.execute(sql, title)
    result = mycursor.fetchall()
    return result