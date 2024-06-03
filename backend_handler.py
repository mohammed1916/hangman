import sqlite3
from global_data import *
from tabulate import tabulate


class backend:
    def __init__(self):
        self.conn = sqlite3.connect('hangman_records.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS records (level text, player_name text, remaining_lives integer)''')
    
    def update_records(self, player_name, level, remaining_lives):
        # Check if the player already has a record for the level
        print("Player Name: ",player_name)
        print("Level: ",level)
        self.c.execute("SELECT remaining_lives FROM records WHERE level=?", (level,))
        result = self.c.fetchone()

        print("Result: ",result)
        if result is None:
            # Insert a new record for the player and level
            self.c.execute("INSERT INTO records VALUES (?, ?, ?)", (level, player_name, remaining_lives))
        else:
            # Update the existing record if the new remaining lives is higher
            if int(remaining_lives) >= int(result[0]):
                self.c.execute("UPDATE records SET remaining_lives=?, player_name=? WHERE level=?", (remaining_lives, player_name, level))

        # Commit the changes to the database
        self.conn.commit()

    def get_records(self):
        self.c.execute("SELECT * FROM records")
        records = self.c.fetchall()
        print(tabulate(records, headers=["Level", "Player Name", "Remaining Lives"], tablefmt="fancy_grid"))
        return records