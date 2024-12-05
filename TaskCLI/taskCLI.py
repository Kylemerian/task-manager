from Command.command import *

class TaskCLI:
    def __init__(self, manager: TaskManager):
        self.manager = manager
        self.commands = {
            "1": ViewTasksCommand(manager),
            "2": ViewTasksByCategoryCommand(manager),
            "3": AddTaskCommand(manager),
            "4": CompleteTaskCommand(manager),
            "5": EditTaskCommand(manager),
            "6": DeleteTaskCommand(manager),
            "7": SearchTasksCommand(manager),
            "8": ExitCommand()
        }

    def run(self):
        while True:
            print("\nМенеджер задач:")
            print("1. Просмотр всех задач")
            print("2. Просмотр задач по категории")
            print("3. Добавление новой задачи")
            print("4. Выполнение задачи")
            print("5. Редактирование задачи")
            print("6. Удаление задачи")
            print("7. Поиск задач")
            print("8. Выход")

            choice = input("Выберите действие: ").strip()
            command = self.commands.get(choice)
            if command:
                command.execute()
            else:
                print("Неверная команда. Попробуйте снова")
