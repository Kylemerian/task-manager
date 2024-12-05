import pytest
from unittest.mock import MagicMock, patch
from Command.command import (
    AddTaskCommand,
    DeleteTaskCommand,
    ViewTasksCommand,
    ViewTasksByCategoryCommand,
    CompleteTaskCommand,
    SearchTasksCommand
)
from TaskManager.taskManager import TaskManager
from Task.task import Task
import io


@pytest.fixture
def task_manager():
    manager = MagicMock(spec=TaskManager)
    manager.get_all_tasks = MagicMock()
    manager.get_tasks_by_category = MagicMock()
    manager.add_task = MagicMock()
    manager.complete_task = MagicMock()
    manager.update_task = MagicMock()
    manager.delete_task = MagicMock()
    manager.search_tasks = MagicMock()
    return manager


def test_view_tasks_command(task_manager):
    """Тест для команды просмотра всех задач"""
    
    tasks = [
        Task(
            title="Task 1",
            description="Description 1",
            category="Category 1",
            due_date="2024-12-31",
            priority="низкий"
        ),
        Task(
            title="Task 2",
            description="Description 2",
            category="Category 2",
            due_date="2025-01-15",
            priority="средний"
        )
    ]
    
    task_manager.view_tasks.return_value = tasks
    
    command = ViewTasksCommand(manager=task_manager)
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        command.execute()

    task_manager.view_tasks.assert_called_once()
    output = mock_stdout.getvalue()
    assert "Task 1" in output
    assert "Task 2" in output


def test_view_tasks_by_category_command(task_manager):
    """Тест для команды просмотра задач по категории"""
    
    category = "Category 1"
    tasks = [
        Task(
            title="Task 1",
            description="Description 1",
            category=category,
            due_date="2024-12-31",
            priority="низкий"
        ),
        Task(
            title="Task 2",
            description="Description 2",
            category=category,
            due_date="2025-01-15",
            priority="средний"
        )
    ]
    
    task_manager.view_tasks.return_value = tasks
    
    with patch("builtins.input", return_value=category):
        command = ViewTasksByCategoryCommand(manager=task_manager)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            command.execute()

    output = mock_stdout.getvalue()
    assert "Task 1" in output
    assert "Task 2" in output


def test_add_task_command(task_manager):
    """Тест для команды добавления задачи"""
    
    expected_task = Task(
        title="Test Task",
        description="Test Description",
        category="Test Category",
        due_date="2024-12-31",
        priority="низкий"
    )

    with patch("builtins.input", side_effect=["Test Task", "Test Description", "Test Category", "2024-12-31", "низкий"]):
        command = AddTaskCommand(manager=task_manager)
        command.execute()

    called_args = task_manager.add_task.call_args[0][0]
    assert called_args.title == expected_task.title
    assert called_args.description == expected_task.description
    assert called_args.category == expected_task.category
    assert called_args.due_date == expected_task.due_date
    assert called_args.priority == expected_task.priority


def test_complete_task_command(task_manager):
    """Тест для команды завершения задачи"""
    
    task_id = "task-id-123"
    task = Task(
        title="Test Task",
        description="Test Description",
        category="Test Category",
        due_date="2024-12-31",
        priority="низкий"
    )
    
    task_manager.get_task_by_id.return_value = task
    
    with patch("builtins.input", return_value=task_id):
        command = CompleteTaskCommand(manager=task_manager)
        command.execute()

    task_manager.mark_completed.assert_called_once_with(task_id)


def test_delete_task_command(task_manager):
    """Тест для команды удаления задачи"""
    
    task_id = "task-id-123"
    
    with patch("builtins.input", return_value=task_id):
        command = DeleteTaskCommand(manager=task_manager)
        command.execute()


def test_search_tasks_command(task_manager):
    """Тест для команды поиска задач"""
    
    query = "Test"
    tasks = [
        Task(
            title="Test Task 1",
            description="Description 1",
            category="Category 1",
            due_date="2024-12-31",
            priority="низкий"
        ),
        Task(
            title="Test Task 2",
            description="Description 2",
            category="Category 2",
            due_date="2025-01-15",
            priority="средний"
        )
    ]
    
    task_manager.search_tasks.return_value = tasks
    
    with patch("builtins.input", return_value=query):
        command = SearchTasksCommand(manager=task_manager)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            command.execute()

    task_manager.search_tasks.assert_called_once_with(query)
    output = mock_stdout.getvalue()
    assert "Test Task 1" in output
    assert "Test Task 2" in output