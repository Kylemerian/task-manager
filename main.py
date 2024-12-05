from TaskManager.taskManager import TaskManager
from TaskCLI.taskCLI import TaskCLI

if __name__ == "__main__":
    manager = TaskManager()
    cli = TaskCLI(manager)
    cli.run()
