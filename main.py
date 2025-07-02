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
       password = inquirer.secret(
            message="Password",
            transformer=lambda _: "[hidden]").execute() 
    
       user_id = users.login(username, password) 

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
                Choice(value=None, name="Exit"),
            ],
            default=None,
            ).execute()
        
        if action == "Add to my List":
            user_books.add_to_list(user_id, book_id)
        

if __name__ == "__main__":
    starter()
        