import gspread
from google.oauth2.service_account import Credentials
import time
import os
from datetime import datetime
from colorama import Fore, Back, Style

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
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
    """
    Checks if date is valid
    :returns: True or false

    """
    valid = False
    try:
        datetime.strptime(date_text, "%d/%m/%Y")
        valid = True
    except ValueError:
        print(
            Fore.RED + 'Incorrect data format, '
            'please follow this format DD/MM/YYYY'
        )
        time.sleep(1.5)
        return False

    present = datetime.now()
    dateGiven = datetime.strptime(date_text, "%d/%m/%Y")
    if (dateGiven.date() < present.date()):
        print(Fore.RED + 'Invalid Input, the date should not be a past date\n')
        time.sleep(1.5)
        return False

    return valid


def validateContent(content):
    """
    Checks if content is valid
    :returns: True or false

    """
    if content == '':
        print(Fore.RED + 'Task content should not be empty')
        time.sleep(3)
        return False

    valid = False
    if all(x.isalpha() or x.isspace() for x in content):
        return True
    else:
        print(
            Fore.RED + "Invalid input, content"
            " must only contain alphanumeric letters"
        )
        time.sleep(1.5)
        return False


class Task:

    def __init__(self, content, status, dueDate):
        self.content = content
        self.status = status
        self.dueDate = dueDate

    def UpdateContent(self):
        """
        Updates the content of the task object
        """
        clear()
        valid = False
        print(
            f"Current Task: \nContent: {self.content},\n"
            f"Status: {self.status},\nDue Date: {self.dueDate}\n"
        )
        print('\nEnter the new content for the task\n')
        Content = input('\n')
        while valid is False:
            if validateContent(Content) is True:
                self.content = Content
                valid = True
            else:
                time.sleep(1)
                clear()
                print(
                    Fore.WHITE + f"Current Task:\nContent: {self.content},\n"
                    f"Status: {self.status},\nDue Date: {self.dueDate}\n"
                )
                print('\nEnter the new content for the task\n')
                Content = input('\n')

    def UpdateStatus(self):
        """
        Updates the status of the task object (complete or incomplete)
        """
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
        Status = input('\n')
        while valid is False:
            if Status == str(1):
                self.status = 'Complete'
                valid = True
            elif Status == str(2):
                self.status = 'Incomplete'
                valid = True
            else:
                print(Fore.RED + 'Invalid Input')
                time.sleep(1.5)
                clear()
                print(
                    Fore.WHITE + f"Current Task:\nContent: {self.content},\n"
                    f"Status: {self.status},\nDue Date: {self.dueDate}\n"
                )
                print(
                    'Enter the correspoding number to'
                    ' change the status of the task:\n'
                )
                print('1: Complete')
                print('2: Incomplete\n')
                Status = input('\n')

    def UpdateDueDate(self):
        """
        Updates the date of the task object
        """
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
                clear()
                print(Fore.WHITE + 'Current Task:\n')
                print(
                    f"Content: {self.content},\nStatus: {self.status},\n"
                    f"Due Date: {self.dueDate}\n"
                )
                print('Enter a new due date for the task:')
                DueDate = input('\n')


def applyChanges(task, originalTask):
    """
    Updates the spreadsheet with the new task.
    Takes in the object and list form of the task.
    """
    clear()
    print(Fore.GREEN + 'Applying changes...')
    row_to_match = originalTask

    # Get all rows
    all_rows = info.get_all_values()

    # Locate the row index
    row_index = None
    for i, row in enumerate(all_rows, start=1):
        if row == row_to_match:
            row_index = i
            break

    if row_index:
        # Delete the row
        info.delete_rows(row_index)

    info.append_row([task.content, task.status, task.dueDate])

    clear()
    print(Fore.GREEN + 'Changes have been applied.')
    time.sleep(1)
    main()


def removeTask(task):
    """
    Removes the task passed into the function from the spreadsheet
    """
    valid = False
    clear()
    print('Xx------------------------------------------------------xX\n')
    print('Delete Task\n')
    while valid is False:
        clear()
        print(
            Fore.WHITE + 'Would you like to confirm'
            ' changes made to the task?\n'
        )
        print('Enter 1 for yes:')
        print('Enter 2 for No:\n')
        confirm = input('\n')
        if confirm == str(1):

            row_to_match = task

            # Get all rows
            all_rows = info.get_all_values()

            # Locate the row index
            row_index = None
            for i, row in enumerate(all_rows, start=1):
                if row == row_to_match:
                    row_index = i
                    break

            if row_index:
                # Delete the row
                info.delete_rows(row_index)
                print(
                    Fore.GREEN + f"The task with content:{task[0]},\n"
                    f"status:{task[1]}\n, due date: {task[2]}"
                    f"has been removed\n"
                )
                time.sleep(1.5)
                main()
            valid = True
        elif confirm == str(2):
            main()
            valid = True
        else:
            print(Fore.RED + 'Invalid input')
            time.sleep(1.5)


def modifyTask(taskObject, originalTask):
    """
    Takes in the object and list version of the task to be changed.
    Then displays the modify task menu to change the given task.
    """
    valid = False
    clear()
    print(Fore.WHITE + 'Xx------------------------------------------------------xX\n')
    print(Fore.WHITE + 'Modify Task\n')
    print(
        f"Task:\nContent: {taskObject.content},\nStatus: {taskObject.status},"
        f"\nDue Date: {taskObject.dueDate}\n"
    )
    print('Selection an option to contine:\n')
    print('1: Change the Content\n')
    print('2: Change the Status\n')
    print('3: Change the due date\n')
    print('4: Confirm changes\n')
    print('5: Return to main menu\n')
    choice = input('\n')
    if choice == str(1):
        taskObject.UpdateContent()
        modifyTask(taskObject, originalTask)
    elif choice == str(2):
        taskObject.UpdateStatus()
        modifyTask(taskObject, originalTask)
    elif choice == str(3):
        taskObject.UpdateDueDate()
        modifyTask(taskObject, originalTask)
    elif choice == str(4):
        while valid is False:
            clear()
            print(
                Fore.WHITE + 'Would you like to confirm'
                ' changes made to the task?\n'
            )
            print('Enter 1 for yes:')
            print('Enter 2 for No:\n')
            confirm = input('\n')
            if confirm == str(1):
                applyChanges(taskObject, originalTask)
                break
            elif confirm == str(2):
                modifyTask(taskObject, originalTask)
                break
            else:
                print(Fore.RED + 'Invalid input')
                time.sleep(1)

    elif choice == str(5):
        main()
        return
    else:
        print(Fore.RED + 'Invalid input, please choose a correct option')
        time.sleep(1.5)
        clear()
        modifyTask(taskObject, originalTask)


def viewAllTasks():
    """
    Displays all tasks in the spreadsheet and prompt user to select a task.
    """
    clear()
    print(Fore.WHITE + 'Xx------------------------------------------------------xX\n')
    print(Fore.WHITE + "View All Tasks:\n")
    tasks = info.get_all_values()
    task_vals = tasks[1:]
    dates = sorted(
        task_vals, key=lambda x: datetime.strptime(x[2], "%d/%m/%Y")
    )
    task_vals = dates

    for x in range(0, len(task_vals)):
        print(
            f"Task: {x+1}\nContent: {task_vals[x][0]},\n"
            f"Status: {task_vals[x][1]},\nDue Date: {task_vals[x][2]}\n"
        )

    print(Fore.WHITE + "Enter the number of the task below to select a task:")
    print(Fore.WHITE + "Enter 0 to return to the main menu:\n")
    choice = input("\n")

    try:
        if choice == str(0):
            main()
            return
        selection = task_vals[int(choice) - 1]
        valid = False
        while valid is False:
            clear()
            print(
                Fore.WHITE + "Xx-------------------------"
                "-----------------------------xX\n"
            )
            print(Fore.WHITE + "View All Tasks:\n")
            print(
                f"Task: {choice},\nContent: {selection[0]},\n"
                f"Status: {selection[1]},\nDue Date: {selection[2]}\n"
            )
            print(Fore.WHITE + "\nTo modify the task, enter 1")
            print(Fore.WHITE + "To remove the task, enter 2")
            print(Fore.WHITE + "To return to the main menu, enter 0\n")
            choice2 = input("\n")
            if choice2 == str(0):
                main()
                valid = True
            if choice2 == str(1):
                print(selection)
                taskObject = Task(selection[0], selection[1], selection[2])
                modifyTask(taskObject, selection)
                valid = True
            elif choice2 == str(2):
                removeTask(selection)
                valid = True
            else:
                print(
                    Fore.RED + 'Invalid input, please enter'
                    ' the correct value:'
                )
                time.sleep(1.5)

    except IndexError as e:
        print(Fore.RED + f'{e}, please enter the correct value:')
        time.sleep(1.5)
        viewAllTasks()
        return
    except ValueError as e:
        print(Fore.RED + f'{e}, please enter the correct value:')
        time.sleep(1.5)
        viewAllTasks()
        return


def viewLastTask():
    """
    Displays the last task in the spreadsheet and prompt user to select a task.
    """
    clear()
    print(Fore.WHITE + 'Xx------------------------------------------------------xX\n')
    print(Fore.WHITE + "View Last Task:\n")
    task = info.get_all_values()
    task_vals = task[-1]
    print(
        f"Task:\nContent: {task_vals[0]},\nStatus: {task_vals[1]},"
        f"\nDue Date: {task_vals[2]}\n"
    )
    print(Fore.WHITE + "To modify the task, enter 1")
    print(Fore.WHITE + "To remove the task, enter 2")
    print(Fore.WHITE + "To return to the main menu, enter 0\n")
    choice = input("\n")

    if choice == str(0):
        main()
        return
    if choice == str(1):
        print(task_vals)
        taskObject = Task(task_vals[0], task_vals[1], task_vals[2])
        modifyTask(taskObject, task_vals)
        return
    elif choice == str(2):
        print(task_vals)
        removeTask(task_vals)
    else:
        print(Fore.RED + 'Invalid input, please enter the correct value:')
        time.sleep(1.5)
        viewLastTask()


def viewCompletedTasks():
    """
    Displays the completed tasks in the spreadsheet
    and prompt user to select a task.
    """
    clear()
    print(
        Fore.WHITE + 'Xx-----------------------------'
        '-------------------------xX\n'
    )
    print(Fore.WHITE + "View Completed Tasks:\n")
    tasks = info.get_all_values()

    tasks_vals = tasks[1:]
    completeList = []
    for val in tasks_vals:
        if val[1] == 'Complete':
            completeList.append(val)

    dates = sorted(
        completeList, key=lambda x: datetime.strptime(x[2], "%d/%m/%Y")
    )
    completeList = dates

    for x in range(0, len(completeList)):
        print(
            f"Task: {x+1}\nContent: {completeList[x][0]},\n"
            f"Status: {completeList[x][1]},\nDue Date: {completeList[x][2]}\n"
        )

    print(Fore.WHITE + "Enter the number of the task below to select a task:")
    print(Fore.WHITE + "Enter 0 to return to the main menu:\n")
    choice = input("\n")

    try:
        if choice == str(0):
            main()
            return
        selection = completeList[int(choice) - 1]
        valid = False
        while valid is False:
            clear()
            print(
                Fore.WHITE + "Xx--------------------------"
                "----------------------------xX\n"
            )
            print(Fore.WHITE + "View Completed Tasks:\n")
            print(
                f"Task: {choice},\nContent: {selection[0]},\n"
                f"Status: {selection[1]},\nDue Date: {selection[2]}\n"
            )
            print(Fore.WHITE + "\nTo modify the task, enter 1")
            print(Fore.WHITE + "To remove the task, enter 2")
            print(Fore.WHITE + "To return to the main menu, enter 0\n")
            choice2 = input("\n")
            if choice2 == str(0):
                main()
                valid = True
            if choice2 == str(1):
                print(selection)
                taskObject = Task(selection[0], selection[1], selection[2])
                modifyTask(taskObject, selection)
                valid = True
            elif choice2 == str(2):
                removeTask(selection)
                valid = True
            else:
                print(
                    Fore.RED + 'Invalid input, please'
                    ' enter the correct value:'
                )
                time.sleep(1.5)

    except IndexError as e:
        print(Fore.RED + f'{e}, please enter the correct value:')
        time.sleep(1.5)
        viewCompletedTasks()
        return


def viewIncompletedTasks():
    """
    Displays the incompleted tasks in the spreadsheet
    and prompt user to select a task.
    """
    clear()
    print(
        Fore.WHITE + 'Xx---------------------------'
        '---------------------------xX\n'
    )
    print(Fore.WHITE + "View Incompleted Tasks:\n")
    tasks = info.get_all_values()

    tasks_vals = tasks[1:]
    completeList = []
    for val in tasks_vals:
        if val[1] == 'Incomplete':
            completeList.append(val)

    dates = sorted(
        completeList, key=lambda x: datetime.strptime(x[2], "%d/%m/%Y")
    )
    completeList = dates

    for x in range(0, len(completeList)):
        print(
            f"Task: {x+1}\nContent: {completeList[x][0]},\n"
            f"Status: {completeList[x][1]},\nDue Date: {completeList[x][2]}\n"
        )

    print(Fore.WHITE + "Enter the number of the task below to select a task:")
    print(Fore.WHITE + "Enter 0 to return to the main menu:\n")
    choice = input("\n")

    try:
        if choice == str(0):
            main()
            return
        selection = completeList[int(choice) - 1]
        valid = False
        while valid is False:
            clear()
            print(
                Fore.WHITE + "Xx-------------------------"
                "-----------------------------xX\n"
            )
            print(Fore.WHITE + "View Incompleted Tasks:\n")
            print(
                f"Task: {choice},\nContent: {selection[0]},\n"
                f"Status: {selection[1]},\nDue Date: {selection[2]}\n"
            )
            print(Fore.WHITE + "\nTo modify the task, enter 1")
            print(Fore.WHITE + "To remove the task, enter 2")
            print(Fore.WHITE + "To return to the main menu, enter 0\n")
            choice2 = input("\n")
            if choice2 == str(0):
                main()
                valid = True
            if choice2 == str(1):
                print(selection)
                taskObject = Task(selection[0], selection[1], selection[2])
                modifyTask(taskObject, selection)
                valid = True
            elif choice2 == str(2):
                removeTask(selection)
                valid = True
            else:
                print(
                    Fore.RED + 'Invalid input, please enter'
                    ' the correct value:'
                )
                time.sleep(1.5)

    except IndexError as e:
        print(Fore.RED + f'{e}, please enter the correct value:')
        time.sleep(1.5)
        viewIncompletedTasks()
        return


def viewDueTasks():
    """
    Displays the due tasks in the spreadsheet
    and prompt user to select a task.
    """
    clear()
    print(
        Fore.WHITE + 'Xx--------------------------'
        '----------------------------xX\n'
    )
    print(Fore.WHITE + "View Due Tasks:\n")
    tasks = info.get_all_values()

    tasks_vals = tasks[1:]
    DueTaskList = []
    present = datetime.now()
    for val in tasks_vals:
        dateGiven = datetime.strptime(val[2], "%d/%m/%Y")
        if (dateGiven.date() > present.date()):
            DueTaskList.append(val)

    dates = sorted(
        DueTaskList, key=lambda x: datetime.strptime(x[2], "%d/%m/%Y")
    )
    DueTaskList = dates

    for x in range(0, len(DueTaskList)):
        print(
            f"Task: {x+1}\nContent: {DueTaskList[x][0]},\n"
            f"Status: {DueTaskList[x][1]},\nDue Date: {DueTaskList[x][2]}\n"
        )

    print(Fore.WHITE + "Enter the number of the task below to select a task:")
    print(Fore.WHITE + "Enter 0 to return to the main menu:\n")
    choice = input("\n")

    try:
        if choice == str(0):
            main()
            return
        selection = DueTaskList[int(choice) - 1]
        valid = False
        while valid is False:
            clear()
            print(
                Fore.WHITE + "Xx---------------------------"
                "---------------------------xX\n"
            )
            print(Fore.WHITE + "View Due Tasks:\n")
            print(
                f"Task: {choice},\nContent: {selection[0]},\n"
                f"Status: {selection[1]},\nDue Date: {selection[2]}\n"
            )
            print(Fore.WHITE + "\nTo modify the task, enter 1")
            print(Fore.WHITE + "To remove the task, enter 2")
            print(Fore.WHITE + "To return to the main menu, enter 0\n")
            choice2 = input("\n")
            if choice2 == str(0):
                main()
                valid = True
            if choice2 == str(1):
                print(selection)
                taskObject = Task(selection[0], selection[1], selection[2])
                modifyTask(taskObject, selection)
                valid = True
            elif choice2 == str(2):
                removeTask(selection)
                valid = True
            else:
                print(
                    Fore.RED + 'Invalid input, please enter'
                    ' a correct value:'
                )
                time.sleep(1.5)

    except IndexError as e:
        print(Fore.RED + f'{e}, please enter the correct value:')
        time.sleep(1.5)
        viewDueTasks()
        return


def viewPastDueTasks():
    """
    Displays the past due tasks in the spreadsheet
    and prompt user to select a task.
    """
    clear()
    print(
        Fore.WHITE + 'Xx--------------------------'
        '----------------------------xX\n'
    )
    print(Fore.WHITE + "View Past Due Tasks:\n")
    tasks = info.get_all_values()

    tasks_vals = tasks[1:]
    DueTaskList = []
    present = datetime.now()
    for val in tasks_vals:
        dateGiven = datetime.strptime(val[2], "%d/%m/%Y")
        if (dateGiven.date() < present.date()):
            DueTaskList.append(val)

    dates = sorted(
        DueTaskList, key=lambda x: datetime.strptime(x[2], "%d/%m/%Y")
    )
    DueTaskList = dates

    for x in range(0, len(DueTaskList)):
        print(
            f"Task: {x+1}\nContent: {DueTaskList[x][0]},\n"
            f"Status: {DueTaskList[x][1]},\nDue Date: {DueTaskList[x][2]}\n"
        )

    print(Fore.WHITE + "Enter the number of the task below to select a task:")
    print(Fore.WHITE + "Enter 0 to return to the main menu:\n")
    choice = input("\n")

    try:
        if choice == str(0):
            main()
            return
        selection = DueTaskList[int(choice) - 1]
        valid = False
        while valid is False:
            clear()
            print(
                "Xx----------------------------"
                "--------------------------xX\n"
            )
            print(Fore.WHITE + "View Past Due Tasks:\n")
            print(
                f"Task: {choice},\nContent: {selection[0]},\n"
                f"Status: {selection[1]},\nDue Date: {selection[2]}\n"
            )
            print(Fore.WHITE + "\nTo modify the task, enter 1")
            print(Fore.WHITE + "To remove the task, enter 2")
            print(Fore.WHITE + "To return to the main menu, enter 0\n")
            choice2 = input("\n")
            if choice2 == str(0):
                main()
                valid = True
            if choice2 == str(1):
                print(selection)
                taskObject = Task(selection[0], selection[1], selection[2])
                modifyTask(taskObject, selection)
                valid = True
            elif choice2 == str(2):
                removeTask(selection)
                valid = True
            else:
                print(
                    Fore.RED + 'Invalid input, please'
                    ' enter the correct value:'
                )
                time.sleep(1.5)

    except IndexError as e:
        print(Fore.RED + f'{e}, please enter the correct value:')
        time.sleep(1.5)
        viewPastDueTasks()
        return


def viewTask():
    """
    Displays the view task menu and prompts user to select a choice.
    """
    clear()
    print(Fore.WHITE + 'View Tasks Menu')
    print(
        Fore.WHITE + 'Xx--------------------------'
        '----------------------------xX\n'
    )
    print(Fore.WHITE + 'Selection an option from those below: \n')
    print(Fore.WHITE + '1: View All Tasks\n')
    print(Fore.WHITE + '2: View Last Task\n')
    print(Fore.WHITE + '3: View Completed Tasks\n')
    print(Fore.WHITE + '4: View Incompleted Tasks\n')
    print(Fore.WHITE + '5: View Due Tasks\n')
    print(Fore.WHITE + '6: View Past Due Tasks\n')
    print(Fore.WHITE + '7: Back to main\n')
    choice = input('\n')
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
        main()
    else:
        print(Fore.RED + 'Invalid input, please enter a correct value:')
        time.sleep(1.5)
        viewTask()


def addTask():
    """
    Prompts user to enter the task content and date.
    Display confirmation screen to confirm changes.
    """
    clear()
    valid = False
    valid2 = False
    valid3 = False
    print(Fore.WHITE + 'Add Task')
    print(
        Fore.WHITE + 'Xx--------------------------'
        '----------------------------xX\n'
    )
    print(Fore.WHITE + 'Content:')
    taskContent = input(Fore.WHITE + "\nEnter the content of the new task:\n")
    while valid is False:
        if validateContent(taskContent) is True:
            valid = True
        else:
            clear()
            print(Fore.WHITE + 'Add Task')
            print(
                Fore.WHITE + 'Xx---------------------------'
                '---------------------------xX\n'
            )
            print(Fore.WHITE + 'Content:')
            taskContent = input(
                Fore.WHITE + "\nEnter the content of the new task:\n"
            )
    print(Fore.WHITE + '\nDue Date:')
    print('Enter the due date of the new task:')
    taskDueDate = input("\n")
    while valid2 is False:
        if validateDate(taskDueDate) is True:
            task = Task(taskContent, 'Incomplete', taskDueDate)
            print(task.content)
            valid2 = True
        else:
            clear()
            print(Fore.WHITE + 'Add Task')
            print(
                Fore.WHITE + 'Xx---------------------------'
                '---------------------------xX\n'
            )
            print(Fore.WHITE + 'Content:')
            print(Fore.WHITE + "\nEnter the content of the new task:")
            print(f"{taskContent}\n")
            print(Fore.WHITE + 'Due Date:')
            print('Enter the due date of the new task:')
            taskDueDate = input(Fore.WHITE + '\n')
    clear()
    print(Fore.WHITE + 'Current Task:\n')
    print(Fore.WHITE + f"content: {task.content}")
    print(Fore.WHITE + f"status: {task.status}")
    print(Fore.WHITE + f"due date: {task.dueDate}\n")

    print(Fore.WHITE + 'Would you like to confirm changes made to the task?\n')
    print(Fore.WHITE + 'Enter 1 for yes:')
    print(Fore.WHITE + 'Enter 2 for No:\n')
    confirm = input('\n')
    while valid3 is False:
        if confirm == str(1):
            clear()
            print(Fore.GREEN + "Applying Changes")
            time.sleep(1)
            clear()
            info.append_row([task.content, task.status, task.dueDate])
            print(Fore.GREEN + "Changes have been applied")
            time.sleep(1)
            valid3 = True
        elif confirm == str(2):
            main()
            break
        else:
            print(Fore.RED + 'Invalid input, please enter either 1 or 2')
            time.sleep(1)
            clear()
            print(Fore.WHITE + 'Current Task:\n')
            print(Fore.WHITE + f"content: {task.content}")
            print(Fore.WHITE + f"status: {task.status}")
            print(Fore.WHITE + f"due date: {task.dueDate}\n")

            print(Fore.WHITE + 'Would you like to confirm changes made to the task?\n')
            print(Fore.WHITE + 'Enter 1 for yes:')
            print(Fore.WHITE + 'Enter 2 for No:\n')
            confirm = input(Fore.WHITE + '\n')

    main()


def main():
    """
    Displays the main menu.
    """
    clear()
    print(Fore.WHITE + 'Main Menu')
    print(
        Fore.WHITE + 'Xx--------------------------'
        '----------------------------xX\n'
    )
    print(Fore.WHITE + 'Selection an option from those below: \n')
    print(Fore.WHITE + '1: Add Task\n')
    print(Fore.WHITE + '2: View Tasks\n')
    choice = input('\n')

    if choice == str(1):
        addTask()
    elif choice == str(2):
        viewTask()
    else:
        print(Fore.RED + 'Invalid entry, please try again')
        time.sleep(1.5)
        main()


if __name__ == "__main__":
    print(Fore.WHITE + """\

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
    time.sleep(1.5)
    clear()
    main()
