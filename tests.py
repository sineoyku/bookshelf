import unittest
from db import mydb, mycursor

class db_test(unittest.TestCase):
    
    def test_inseriton(self):
        query = "INSERT INTO users (id, username, password_hash) VALUES (%s, %s, %s) "
        val = ("0", "testuser", "0000")
        mycursor.execute(query, val)

        mydb.commit()

        self.assertEqual(mycursor.rowcount, 1)
        print(mycursor.rowcount, "record inserted.")
    
    def test_deletion(self):
        query = "DELETE FROM users WHERE username = 'testuser' "
        mycursor.execute(query)

        mydb.commit()

        self.assertEqual(mycursor.rowcount, 0)
        print(mycursor.rowcount+1, "record deleted.")

if __name__ == '__main__':
    unittest.main() 
        
