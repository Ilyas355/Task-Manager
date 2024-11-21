import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import time
import os
from datetime import datetime

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

def validateDate(date_text):
    valid = False
    try:
        datetime.strptime(date_text, "%d/%m/%Y")
        valid = True
    except ValueError:
        print('Incorrect data format, please follow this format DD/MM/YYYY')
        return False

    present = datetime.now()
    dateGiven = datetime.strptime(date_text, "%d/%m/%Y")
    if (dateGiven.date() < present.date()):
        print('The date should not be a past date\n')
        return False

    return valid

def validateContent(content):
    valid = False
    if all(x.isalpha() or x.isspace() for x in content):
        return True
    else:
        return False


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


def applyChanges(task, originalTask):
    pass


def removeTask(task):
    pass


def modifyTask(taskObject, originalTask):
    pass


def viewAllTasks():
    pass


def viewLastTask():
    pass


def viewCompletedTasks():
    pass


def viewIncompletedTasks():
    pass


def viewDueTasks():
    pass


def viewPastDueTasks():
    pass


def backToMain():
    main()


def viewTask():
    pass


def addTask():
    pass


def main():
    clear()
    print('Main Menu')
    print('Xx------------------------------------------------------xX\n')
    print('Selection an option from those below: \n')
    print('1: Add Task\n')
    print('2: View Tasks\n')
    choice = input('')

    if choice == str(1):
        addTask()
    elif choice == str(2):
        viewTask()
    else:
        print('Invalid Entry Please Try again')
        time.sleep(1)
        main()


if __name__ == "__main__":
    print("""\

    XX         XX XXXXXXX XX      XXXXXXX XXXXXXXX     XX   XX     XXXXXXX
     XX   X   XX  XX      XX      XX      XX    XX    XXXX XXXX    XX     
      XX XXX XX   XXXXXXX XX      XX      XX    XX   XX  XXX  XX   XXXXXXX
       XXX XXX    XX      XX      XX      XX    XX  XX    X    XX  XX     
        X   X     XXXXXXX XXXXXXX XXXXXXX XXXXXXXX XX           XX XXXXXXX

                                                                                       
                                                                       
     XXXXXXXX XXXXXXX    XXXXXXXX    XX     XXXXXXX XX  XXX                
        XX    XX   XX       XX      XXXX    XX      XX XXX                 
        XX    XX   XX       XX     XX  XX   XXXXXXX XXXXX                  
        XX    XX   XX       XX    XXXXXXXX       XX XX XXX                 
        XX    XXXXXXX       XX   XX      XX XXXXXXX XX  XXX                



         XX   XX         XX     XXX   XX     XX     XXXXXXXX XXXXXXX XXXXXXX
        XXXX XXXX       XXXX    XXXX  XX    XXXX    XX       XX      XX   XX
       XX  XXX  XX     XX  XX   XX XX XX   XX  XX   XX XXXXX XXXXXXX XX XXXX
      XX    X    XX   XXXXXXXX  XX  XXXX  XXXXXXXX  XX     X XX      XX  XX 
     XX           XX XX      XX XX   XXX XX      XX XXXXXXXX XXXXXXX XX   XX


    """)
    time.sleep(3)
    main()