import json
import os
import datetime

class Note:
    def __init__(self, id, title, body, timestamp):
        self.id = id
        self.title = title
        self.body = body
        self.timestamp = timestamp

class NoteManager:
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                notes_json = json.load(file)
                return [Note(n['id'], n['title'], n['body'], n['timestamp']) for n in notes_json]
        else:
            return [] 