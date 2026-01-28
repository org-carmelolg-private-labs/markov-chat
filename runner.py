#!/usr/bin/env python3
from html_sanitizer import Sanitizer
from nicegui import ui
from lib.markov import MarkovGenerator

def root():

    async def send() -> None:
        question = text.value
        text.value = ''
        with message_container:
            ui.chat_message(text=question, name='You', sent=True)
            response_message = ui.chat_message(name='Anti-Agent', sent=False)
            spinner = ui.spinner(type='dots', size='lg', color='primary')

        await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        response = ''
        response = MarkovGenerator.run()
        with response_message.clear():
            ui.html(response, sanitize=Sanitizer().sanitize)
            await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

    message_container = ui.column().classes('w-full max-w-2xl mx-auto flex-grow items-stretch')

    with (ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6')):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'Message'
            text = ui.input(placeholder=placeholder).props('outlined input-class=mx-3').classes('w-full self-center').on('keydown.enter', send)
            button = ui.button(text="Send", color="primary", on_click=send).props('outlined input-class=mx-3').classes('self-center')

        ui.markdown('Made with 🔥 by [carmelolg](https://carmelolg.github.io)') \
            .classes('text-xs self-center mr-12 m-[-1em] text-primary') \
            .classes('[&_a]:text-inherit [&_a]:no-underline [&_a]:font-medium')


ui.run(root, title='Anti Agent Chatbot', favicon='', show_welcome_message=True, reconnect_timeout=60)
