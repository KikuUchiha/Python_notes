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
    #загружает заметки из файла JSON
    def load_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                notes_json = json.load(file)
                return [Note(n['id'], n['title'], n['body'], n['timestamp']) for n in notes_json]
        else:
            return [] 
    #сохраняет заметки в файл JSON
    def save_notes(self):
        with open(self.filename, 'w') as file:
            notes_json = [{'id': note.id, 'title': note.title, 'body': note.body, 'timestamp': note.timestamp} for note in self.notes]
            json.dump(notes_json, file, indent=4)
    #добавление
    def add_note(self, title, body):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        id = len(self.notes) + 1
        self.notes.append(Note(id, title, body, timestamp))
        self.save_notes()
    #удаление
    def delete_note(self, id):
        self.notes = [note for note in self.notes if note.id != id]
        self.save_notes()
    #редактирование
    def edit_note(self, id, title, body):
        for note in self.notes:
            if note.id == id:
                note.title = title
                note.body = body
                note.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                return True
        return False
    #возвращает список заметок, с фильтрацией по дате
    def list_notes(self, date_filter=None):
        if date_filter:
            filtered_notes = [note for note in self.notes if note.timestamp.startswith(date_filter)]
            return filtered_notes
        else:
            return self.notes
        
def main():
    note_manager = NoteManager()

    while True:
        print("Введите команду: (add, edit, delete, list, exit)")
        command = input()

        if command == "add":
            title = input("Введите заголовок заметки: ")
            body = input("Введите тело заметки: ")
            note_manager.add_note(title, body)
            print("Заметка успешно добавлена!")

        elif command == "edit":
            id = int(input("Введите ID заметки для редактирования: "))
            title = input("Введите новый заголовок заметки: ")
            body = input("Введите новое тело заметки: ")
            if note_manager.edit_note(id, title, body):
                print("Заметка успешно отредактирована!")
            else:
                print("Заметка с таким ID не найдена.")

        elif command == "delete":
            id = int(input("Введите ID заметки для удаления: "))
            note_manager.delete_note(id)
            print("Заметка успешно удалена!")
        
        elif command == "list":
            date_filter = input("Введите фильтр даты (гггг-мм-дд) или оставьте пустым: ")
            notes = note_manager.list_notes(date_filter)
            if notes:
                for note in notes:
                    print(f"ID: {note.id}, Заголовок: {note.title}, Тело: {note.body}, Время создания: {note.timestamp}")
            else:
                print("Заметок не найдено.")