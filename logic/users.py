import bcrypt
from db import mydb, mycursor

def signup(username, password):
    
    mycursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if mycursor.fetchone():
        print("Username unavailable.")
        return False
    
    passw_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(passw_bytes, bcrypt.gensalt())

    mycursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
        (username, hashed)
    )

    mydb.commit()
    mycursor.clear_attributes()

    print("Registered successfully!")
    return True

def login(username, password):
    mycursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    user = mycursor.fetchone()

    if user is None:
        print("User not found.")
        return None
    
    password_bytes = password.encode("utf-8")
    if bcrypt.checkpw(password_bytes, user[1].encode("utf-8")):
        print("Login successful!")
        return user[0]
    
    else:
        print("Incorrect password.")
        return None