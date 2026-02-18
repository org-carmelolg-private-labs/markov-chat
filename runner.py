#!/usr/bin/env python3
import random
from time import sleep

from html_sanitizer import Sanitizer
from nicegui import ui
from lib.MarkovGenerator import run as markov_run

def root():
    # Add custom terminal-style CSS
    ui.add_head_html('''
        <style>
            body {
                background-color: #0c0c0c !important;
                color: #00ff00 !important;
                font-family: 'Courier New', Courier, monospace !important;
            }
            
            .q-page {
                background-color: #0c0c0c !important;
            }
            
            .q-footer {
                background-color: #1a1a1a !important;
                border-top: 1px solid #00ff00 !important;
            }
            
            .q-field__control {
                background-color: #000000 !important;
                color: #00ff00 !important;
                border: 1px solid #00ff00 !important;
                border-radius: 0 !important;
                font-family: 'Courier New', Courier, monospace !important;
            }
            
            .q-field__native,
            .q-field__input {
                color: #00ff00 !important;
                font-family: 'Courier New', Courier, monospace !important;
            }
            
            .q-field__label {
                color: #00aa00 !important;
                font-family: 'Courier New', Courier, monospace !important;
            }
            
            .q-btn {
                background-color: #000000 !important;
                color: #00ff00 !important;
                border: 1px solid #00ff00 !important;
                border-radius: 0 !important;
                font-family: 'Courier New', Courier, monospace !important;
            }
            
            .q-btn:hover {
                background-color: #00ff00 !important;
                color: #000000 !important;
            }
            
            .q-chat__message {
                background-color: transparent !important;
                font-family: 'Courier New', Courier, monospace !important;
            }
            
            .q-chat__message-text {
                background-color: transparent !important;
                color: #00ff00 !important;
                font-family: 'Courier New', Courier, monospace !important;
            }
            
            .q-chat__message-name {
                color: #00aa00 !important;
                font-family: 'Courier New', Courier, monospace !important;
                font-weight: bold !important;
            }
            
            .q-spinner {
                color: #00ff00 !important;
            }
            
            a {
                color: #00ff00 !important;
                text-decoration: underline !important;
            }
            
            .terminal-prompt::before {
                content: '$ ';
                color: #00ff00;
                font-weight: bold;
            }
        </style>
    ''')

    async def send() -> None:
        question = text.value
        text.value = ''
        with message_container:
            ui.chat_message(text=f'$ {question}', name='user@terminal', sent=True)
            response_message = ui.chat_message(name='anti-agent@system', sent=False)
            spinner = ui.spinner(type='dots', size='lg', color='green')

        await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        response = markov_run()
        sleep(random.randint(1, 3))
        await ui.run_javascript('window.scrollTo(0, 0)')
        with response_message.clear():
            ui.html(f'> {response}', sanitize=Sanitizer().sanitize)
            await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

    message_container = ui.column().classes('w-full max-w-2xl mx-auto flex-grow items-stretch')

    with (ui.footer(), ui.column().classes('w-full max-w-3xl mx-auto my-6')):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = '> Enter command...'
            text = ui.input(placeholder=placeholder).props('dark outlined square dense input-class=mx-3').classes('w-full self-center').on('keydown.enter', send)
            button = ui.button(text="SEND", on_click=send).props('dark outlined square dense').classes('self-center')

        ui.markdown('Made with 🔥 by [carmelolg](https://carmelolg.github.io)') \
            .classes('text-xs self-center mr-12 m-[-1em]') \
            .classes('[&_a]:text-inherit [&_a]:no-underline [&_a]:font-medium') \
            .style('color: #00aa00')


ui.run(root, title='Anti Agent Chatbot', favicon='', show_welcome_message=True, reconnect_timeout=60, dark=True)
