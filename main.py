from InquirerPy.utils import color_print
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from logic import users, books

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
    
       users.login(username, password) 

    action = inquirer.select(
        message="[Main Menu]",
        choices=[
            "My List",
            "Search for Books",
            Choice(value=None, name="Exit"),
        ],
        default=None,
    ).execute()
    
    if action == "Search for Books":
        title = inquirer.text(message="Title: ").execute()
        results = books.search_by_title(title)
        for 



if __name__ == "__main__":
    starter()
        