import reflex as rx
from sqlalchemy import case

from reflex_todo.models.task import Task


class TasksState(rx.State):
    tasks: list[Task] = []
    new_task: str = ''
    error: str = ''

    @rx.event
    def load_tasks(self):
        with rx.session() as session:
            order = case(
                (Task.state == "open", 1),
                (Task.state == "in_progress", 2),
                (Task.state == "done", 3),
                (Task.state == "canceled", 4),
                else_=99
            )

            self.tasks = (
                session.exec(
                    Task.select()
                    .order_by(order, Task.text)
                ).all()
            )

        if not self.tasks:
            with rx.session() as session:
                for task in [
                    Task(text='Walk the dog', state='open'),
                    Task(text='Write Code', state='in_progress'),
                    Task(text='Get up!', state='done'),
                ]:
                    session.add(task)
                    session.commit()

    @rx.event
    def set_new_task(self, value: str):
        self.new_task = value

    @rx.event
    def add_task(self):
        if not self.new_task.strip():
            self.error = 'Task cannot be empty'
            return

        with rx.session() as session:
            task = Task(text=self.new_task, state='open')
            session.add(task)
            session.commit()

        self.reset_form()
        self.load_tasks()

        return rx.redirect('/')

    @rx.event
    def update_task_state(self, task_id: int, new_state: str):
        with rx.session() as session:
            task = session.get(Task, task_id)
            if task:
                task.state = new_state
                session.add(task)
                session.commit()

                self.load_tasks()

    @rx.event
    def delete_task(self, task_id: int):
        with rx.session() as session:
            task = session.get(Task, task_id)
            if task:
                session.delete(task)
                session.commit()

                self.load_tasks()

    @rx.event
    def reset_form(self):
        self.error = ''
        self.new_task = ''