import customtkinter as ctk
import sqlite3

# Tema ayarları
ctk.set_appearance_mode("dark")      # "light", "dark", "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

# -------------------- Veritabanı --------------------
def connect_db():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM todos")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task(title):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def complete_task(task_id):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET done=1 WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

# -------------------- Modern Arayüz --------------------
class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("✅ Modern TO-DO Uygulaması")
        self.geometry("500x600")
        self.resizable(False, False)

        self.task_entry = ctk.CTkEntry(self, placeholder_text="Yeni görev girin...", width=300)
        self.task_entry.pack(pady=15)

        self.add_button = ctk.CTkButton(self, text="➕ Görev Ekle", command=self.add_task_gui, width=200)
        self.add_button.pack(pady=5)

        self.complete_button = ctk.CTkButton(self, text="✅ Tamamla", command=self.complete_task_gui, width=200, fg_color="#3498db")
        self.complete_button.pack(pady=5)

        self.delete_button = ctk.CTkButton(self, text="🗑️ Sil", command=self.delete_task_gui, width=200, fg_color="#e74c3c")
        self.delete_button.pack(pady=5)

        self.task_listbox = ctk.CTkTextbox(self, width=400, height=300, font=("Courier", 14))
        self.task_listbox.pack(pady=20)

        self.refresh_tasks()

    def refresh_tasks(self):
        self.task_listbox.delete("1.0", "end")
        for task in get_tasks():
            status = "✔️" if task[2] else "❌"
            self.task_listbox.insert("end", f"{task[0]} - {task[1]} [{status}]\n")

    def add_task_gui(self):
        title = self.task_entry.get()
        if title.strip():
            add_task(title.strip())
            self.task_entry.delete(0, "end")
            self.refresh_tasks()

    def delete_task_gui(self):
        selection = self.task_listbox.get("sel.first", "sel.last")
        if selection:
            try:
                task_id = int(selection.split(" - ")[0])
                delete_task(task_id)
                self.refresh_tasks()
            except:
                pass

    def complete_task_gui(self):
        selection = self.task_listbox.get("sel.first", "sel.last")
        if selection:
            try:
                task_id = int(selection.split(" - ")[0])
                complete_task(task_id)
                self.refresh_tasks()
            except:
                pass

# -------------------- Başlatıcı --------------------
if __name__ == "__main__":
    connect_db()
    app = TodoApp()
    app.mainloop()
