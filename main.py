from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import time
import httpx
from string import Template

controller = Controller()

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_CONFIG = {
    "model": "mistral:7b-instruct-q4_K_S",
    "keep_alive": "5m",
    "stream": False
}
PROMPT_TEMPLATE = Template(
    """Fix all the typos, casing and punctuation in this text but preserve all new line characters:
    $text

    Return only the corrected text, don't include the preamble.
"""
)

def fix_test(text):
    prompt = PROMPT_TEMPLATE.substitute(text=text)
    response = httpx.post(
        OLLAMA_ENDPOINT,
        json={
            "prompt": prompt,
            **OLLAMA_CONFIG
        },
        headers={
            "Content-Type": "application/json"
        },
        timeout=10
    )

    if response.status_code != 200:
        return None
    return response.json()["response"].strip()
    pass

def fix_current_line():
    controller.press(Key.ctrl)
    controller.press(Key.shift)
    controller.press(Key.left)

    controller.release(Key.ctrl)
    controller.release(Key.shift)
    controller.release(Key.left)

    fix_selection()

def fix_selection():
    with controller.pressed(Key.ctrl):
        controller.tap('c')

    time.sleep(0.1)
    text = pyperclip.paste()

    fixed_text = fix_test(text)

    pyperclip.copy(fixed_text)
    time.sleep(0.1)
    
    with controller.pressed(Key.ctrl):
        controller.tap('v')

def on_f9():
    fix_current_line()

def on_f10():
    fix_selection()

with keyboard.GlobalHotKeys({
        '<120>': on_f9,
        '<121>': on_f10}) as h:
    h.join()