import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('Creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('TaskManager')

info = SHEET.worksheet('Tasks')


def clear():

    """
    Clears the screen
    :return:

    """
    os.system("clear")


class Task:

    def __init__(self, content, status, dueDate):
        self.content = content
        self.status = status
        self.dueDate = dueDate

    def UpdateContent(self):
        clear()
        valid = False
        print(
            f"Current Task: \nContent: {self.content},\n"
            f"Status: {self.status},\nDue Date: {self.dueDate}\n"
        )
        print('\nEnter the new content for the task\n')
        Content = input('')
        while valid is False:
            if validateContent(Content):
                self.content = Content
                valid = True
            else:
                print('Invalid Input')
                time.sleep(1)
                clear()
                print(
                    f"Current Task:\nContent: {self.content},\n"
                    f"Status: {self.status},\nDue Date: {self.dueDate}\n"
                )
                print('\nEnter the new content for the task\n')
                Content = input('')

    def UpdateStatus(self):
        clear()
        valid = False
        print(
            f"Current Task: \nContent: {self.content},\n"
            f"Status: {self.status},\nDue Date: {self.dueDate}\n"
        )
        print(
            "Enter the correspoding number to change" 
            "the status of the task:\n"
        )
        print('1: Complete')
        print('2: Incomplete\n')
        Status = input('')
        while valid is False:
            if Status == str(1):
                self.status = 'Complete'
                valid = True
            elif Status == str(2):
                self.status = 'Incomplete'
                valid = True
            else:
                print('Invalid Input')
                time.sleep(1)
                clear()
                print(
                    f"Current Task:\nContent: {self.content},\n"
                    f"Status: {self.status},\nDue Date: {self.dueDate}\n"
                )
                print(
                    'Enter the correspoding number to'
                    ' change the status of the task:\n'
                )
                print('1: Complete')
                print('2: Incomplete\n')
                Status = input('')

    def UpdateDueDate(self):
        clear()
        valid = False
        print('Current Task:\n')
        print(
            f"Content: {self.content},\nStatus: {self.status},\n"
            f"Due Date: {self.dueDate}\n"
        )
        print('Enter a new due date for the task:')
        DueDate = input('\n')
        while valid is False:
            if validateDate(DueDate) is True:
                self.dueDate = DueDate
                valid = True
            else:
                DueDate = input('')