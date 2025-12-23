"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from reflex_todo.states.task import TasksState


@rx.page(route='/add-task', title='Add Task')
def add() -> rx.Component:
    # Add task page at /add
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Add Task", size='8'),
            rx.input(
                placeholder="Enter task ...",
                value=TasksState.new_task,
                on_change=TasksState.set_new_task,
                width='100%',
            ),
            rx.cond(
                TasksState.error,
                rx.text(TasksState.error, color='red', size='2'),
            ),
            rx.hstack(
                rx.button(
                    "Add Task",
                    on_click=TasksState.add_task,
                    color_scheme='blue'
                ),
                rx.link(
                    rx.button(
                        "Cancel",
                        on_click=TasksState.reset_form
                    ),
                    href="/",
                ),
                spacing='4',
            ),
            spacing='4',
            align='start',
            width='100%',
            max_width='600px',
        ),
    )


@rx.page(route='/settings', title='Settings')
def settings() -> rx.Component:
    return rx.container(
        rx.heading("Settings", size='8'),
    )


def render_task(task):
    # safely get text and state from object, dict or plain string
    text = getattr(task, "text", None)
    if text is None:
        if isinstance(task, dict):
            text = task.get("text", str(task))
        else:
            text = str(task)
    state = getattr(task, "state", None)
    if state is None and isinstance(task, dict):
        state = task.get("state", "open")

    color = rx.cond(state == 'open', 'green', 'gray')  # blue for todo, green for in progress, gray for closed
    badge_label = state

    return rx.box(
        rx.hstack(
            rx.text(
                text,
                size='5',
                font_weight='semibold',
                no_of_lines=2,
                color='gray.800',
                padding_left='10px',
                padding_top='10px',
            ),
            rx.badge(
                badge_label,
                color_scheme=color,
                variant='soft',
                border_radius='full',
                padding_x='2',
                font_size='xs',
            ),
            justify='between',
            align='center',
            width='100%',
        ),
        padding='3px',
        bg='gray.50',                # contrast with page background
        border='1px solid',
        border_color='gray.200',
        border_radius='lg',
        box_shadow='sm',
        width='100%',
        min_height='56px',           # prevents collapsed/zero-height rows
        transition='all 0.12s ease',
        cursor='pointer',
        _hover={'transform': 'translateY(-4px)', 'boxShadow': 'md'},
    )


@rx.page(route='/', title='My Tasks')
def tasks() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading('This is my basic task reflex app', size='9'),
            rx.text('Manage your tasks here', size='4'),
            justify='center',
        ),

        # menu options to manage the tasks
        rx.hstack(
            rx.link(
                rx.button("Add Task"),
                href="/add-task",
            ),
            rx.link(
                rx.button("Settings"),
                href="/settings",
            ),
            spacing="4",
            align='start',
        ),

        # list tasks
        rx.vstack(
            rx.vstack(
                margin_top='6',
            ),
            rx.heading('Your Tasks', size='7'),
            rx.vstack(
                rx.cond(
                    TasksState.tasks,
                    rx.foreach(
                        TasksState.tasks,
                        render_task,
                    ),
                    rx.text('No tasks yet.', size='5'),
                ),
                spacing='3',
                align='stretch',
                width='100%',
                max_width='600px',
                margin_top='4',
                justify='center',
            ),
            spacing='3',
            justify='center',
        ),
        on_mount=TasksState.load_tasks,
    )


app = rx.App()
