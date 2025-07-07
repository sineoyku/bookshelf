from tabulate import tabulate
from InquirerPy.utils import color_print
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from logic import users, books, user_books
import textwrap

color_print([("#ffffff", "Welcome to "), ("#fda0de", "Bookshelf!")])
color_print([("#828181", "----------------------- ")])

def starter():
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Sign-up",
            "Login",
            Choice(value=None, name="Exit"),
        ],
        default=None,
    ).execute()

    if action == "Sign-up":
        username = inquirer.text(message="Username:").execute()
        password = inquirer.secret(
            message="Password:",
            transformer=lambda _: "[hidden]").execute() 
    
        users.signup(username, password)

    elif action == "Login":
       username = inquirer.text(message="Username").execute()
       max_attempts = 3
       attempts = 0
       user_id = None
       while attempts < max_attempts:
           password = inquirer.secret(
                message="Password",
                transformer=lambda _: "[hidden]").execute() 
           user_id = users.login(username, password)
           if user_id is not None:
               break
           else:
               attempts += 1
               print(f"Incorrect password. Attempts left: {max_attempts - attempts}")
       if user_id is None:
           print("Too many incorrect attempts. Exiting.")
           exit()

    action = inquirer.select(
        message="What are you looking for?",
        choices=[
            "My list",
            "Log reading progress",
            "Search for books",
            Choice(value=None, name="Exit"),
        ],
        default=None,
    ).execute()
    
    if action == "My list":
        results = user_books.get_user_list(user_id)
        if not results:
            print("Your list is empty.")
            return
        headers = ["Title", "Status", "Start Date", "End Date"]
        print(tabulate(results, headers=headers, tablefmt="grid"))
        book_titles = [row[0] for row in results]
        selected_title = inquirer.select(
            message="Select a book to manage:",
            choices=book_titles + [Choice(value=None, name="Back")],
            default=None,
        ).execute()
        if selected_title:
            action2 = inquirer.select(
                message="What would you like to do?",
                choices=[
                    "Change status",
                    "Add review",
                    "Log reading progress",
                    Choice(value=None, name="Back")
                ],
                default=None,
            ).execute()
            if action2 == "Change status":
                new_status = inquirer.select(
                    message="Select new status:",
                    choices=["want to read", "reading", "read"],
                    default="reading",
                ).execute()
                user_books.update_book_status(user_id, selected_title, new_status)
            elif action2 == "Add review":
                from logic import reviews, books as books_logic
                # Find book_id by title
                book_search = books_logic.search_by_title(selected_title)
                if book_search:
                    book_id = book_search[0][0]
                    rating = int(inquirer.text(message="Rating (1-5):").execute())
                    review_text = inquirer.text(message="Your review:").execute()
                    reviews.add_review(user_id, book_id, rating, review_text)
                else:
                    print("Book not found.")
            elif action2 == "Log reading progress":
                pages_read = int(inquirer.text(message="Pages read:").execute())
                user_books.log_reading_progress(user_id, selected_title, pages_read)
        return
    elif action == "Log reading progress":
        # Shortcut for logging progress
        results = user_books.get_user_list(user_id)
        if not results:
            print("Your list is empty.")
            return
        book_titles = [row[0] for row in results]
        selected_title = inquirer.select(
            message="Select a book to log progress:",
            choices=book_titles + [Choice(value=None, name="Back")],
            default=None,
        ).execute()
        if selected_title:
            pages_read = int(inquirer.text(message="Pages read:").execute())
            user_books.log_reading_progress(user_id, selected_title, pages_read)
        return
    elif action == "Search for books":

        title = inquirer.text(message="Title: ").execute()
        results = books.search_by_title(title)

        if not results:
            print("No books found.")
            return

        headers = ["Book ID", "Title", "Authors", "Pages", "Avg Rating"]
        table = []
        for book in results:
            book_id = book[0]
            wrapped_title = "\n".join(textwrap.wrap(str(book[1]), width=30))
            wrapped_authors = "\n".join(textwrap.wrap(str(book[2]), width=25))
            table.append([book_id, wrapped_title, wrapped_authors, book[3], book[4]])
        print(tabulate(table, headers=headers, tablefmt="grid"))

        book_id = inquirer.text(message="Which book would you like to choose:").execute()

        action = inquirer.select(
            message="",
            choices=[
                "Add to my List",
                "Look at reviews",
                "List book's reviews",
                Choice(value=None, name="Exit"),
            ],
            default=None,
            ).execute()
        
        if action == "Add to my List":
            user_books.add_to_list(user_id, book_id)
        elif action == "Look at reviews":
            from logic import reviews
            reviews_list = reviews.get_reviews(book_id)
            if not reviews_list:
                print("No reviews yet.")
            else:
                headers = ["User", "Rating", "Review", "Date"]
                print(tabulate(reviews_list, headers=headers, tablefmt="grid"))
        elif action == "List book's reviews":
            from logic import reviews
            reviews_list = reviews.get_reviews(book_id)
            if not reviews_list:
                print("No reviews yet.")
            else:
                headers = ["User", "Rating", "Review", "Date"]
                print(tabulate(reviews_list, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    starter()
        