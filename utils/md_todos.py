import os
import re

def get_todo_items(directory):
    todo_items = []
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                todos = re.findall(r'^.*(?:todo|TODO).*$', content, re.MULTILINE)
                for todo in todos:
                    todo_items.append((filename, todo.strip()))
    return todo_items

