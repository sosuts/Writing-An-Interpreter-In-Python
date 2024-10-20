from getpass import getuser

from ponkey.repl import REPL

# if __name__ == "__main__":

user = getuser()
print(f"Hello {user}! This is the Ponkey programming language")
print("Please type in commands")
REPL().start()
