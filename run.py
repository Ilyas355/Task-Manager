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
    clear()
    print("View All Tasks:")
    print('Xx------------------------------------------------------xX\n')
    tasks = info.get_all_values()
    task_vals = tasks[1:]
    for x in range(0, len(task_vals)):
        print(
            f"Task: {x+1}\nContent: {task_vals[x][0]},\n"
            f"Status: {task_vals[x][1]},\nDue Date: {task_vals[x][2]}\n"
        )

    print("Enter the number of the task below to select a task:")
    print("Enter 0 to return to the main menu:\n")
    choice = input("")

    try:
        if choice == str(0):
            main()
            return
        selection = task_vals[int(choice) - 1]
        valid=False
        while valid is False:
            clear()
            print("View All Tasks:\n")
            print(
                f"Task: {choice},\nContent: {selection[0]},\n"
                f"Status: {selection[1]},\nDue Date: {selection[2]}\n"
            )
            print("\nTo modify the task, enter 1")
            print("To remove the task, enter 2")
            print("To return to the main menu, enter 0\n")
            choice2=input("")
            if choice2 == str(0):
                main()
                valid = True
            if choice2 == str(1):
                print(selection)
                taskObject = Task(selection[0],selection[1],selection[2])
                modifyTask(taskObject, selection)
                valid = True
            elif choice2 == str(2):
                removeTask(selection)
                valid = True
            else:
                print('Invalid input, please enter the correct value:')
                time.sleep(1)
            
    except IndexError as e:
        print(f'{e}, please enter the correct value:')
        time.sleep(1.5)
        viewAllTasks()
        return
    except ValueError as e:
        print(f'{e}, please enter the correct value:')
        time.sleep(1.5)
        viewAllTasks()
        return


def viewLastTask():
    clear()
    print("View Last Task:\n")
    print('Xx------------------------------------------------------xX\n')
    task = info.get_all_values()
    task_vals =task[-1]
    print(
        f"Task:\nContent: {task_vals[0]},\nStatus: {task_vals[1]},"
        f"\nDue Date: {task_vals[2]}\n"
    )
    print("To modify the task, enter 1")
    print("To remove the task, enter 2")
    print("To return to the main menu, enter 0\n")
    choice=input("")

    if choice == str(0):
        main()
        return
    if choice == str(1):
        print(task_vals)
        taskObject = Task(task_vals[0],task_vals[1],task_vals[2])
        modifyTask(taskObject, task_vals)
        return
    elif choice == str(2):
        print(task_vals)
        removeTask(task_vals)
    else:
        print('Invalid input, please enter the correct value:')
        time.sleep(1.5)
        viewLastTask()


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
    clear()
    print('View Task')
    print('Xx------------------------------------------------------xX\n')
    print('Selection an option from those below: \n')
    print('1: View All Tasks\n')
    print('2: View Last Task\n')
    print('3: View Completed Tasks\n')
    print('4: View Incompleted Tasks\n')
    print('5: View Due Tasks\n')
    print('6: View Past Due Tasks\n')
    print('7: Back to main\n')
    choice = input('')
    if choice == str(1):
        viewAllTasks()
    elif choice == str(2):
        viewLastTask()
    elif choice == str(3):
        viewCompletedTasks()
    elif choice == str(4):
        viewIncompletedTasks()
    elif choice == str(5):
        viewDueTasks()
    elif choice == str(6):
        viewPastDueTasks()
    elif choice == str(7):
        backToMain()
    else:
        print('Invalid input, please enter a correct value:')
        viewTask()


def addTask():
    clear()
    valid = False
    valid2=False
    print('Add Task')
    print('Xx------------------------------------------------------xX\n')
    print('Content:')
    taskContent = input("\nEnter the content of the new task:\n")
    print('\nDue Date:')
    print('Enter the due date of the new task:')
    taskDueDate = input("\n")
    while valid is False:
        if validateDate(taskDueDate) is True:
            task = Task(taskContent, 'Incomplete', taskDueDate)
            valid = True
        else:
            taskDueDate = input('\n')
    clear()

    print('Current Task:\n')
    print(f"content: {task.content}")
    print(f"status: {task.status}")
    print(f"due date: {task.dueDate}\n")

    print('Would you like to confirm changes made to the task?\n')
    print('Enter 1 for yes:')
    print('Enter 2 for No:\n')
    confirm = input('')
    while valid2 is False:
        if confirm == str(1):
            info.append_row([task.content, tas.status, task.dueDate])
            valid2 = True
        elif confirm == str(2):
            main()
            break
        else:
            print('Invalid input')
            confirm = input('')
            time.sleep(1)

    main()


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