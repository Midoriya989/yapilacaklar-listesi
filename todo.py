import sqlite3

# Veritabanı bağlantısı
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

# Tablo oluştur (ilk çalıştırmada)
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0
)
""")
conn.commit()

def listele():
    cursor.execute("SELECT id, title, done FROM todos")
    for row in cursor.fetchall():
        durum = "✔️" if row[2] else "❌"
        print(f"{row[0]}. {row[1]} - {durum}")

def ekle(gorev):
    cursor.execute("INSERT INTO todos (title) VALUES (?)", (gorev,))
    conn.commit()
    print("✅ Görev eklendi!")

def sil(id):
    cursor.execute("DELETE FROM todos WHERE id=?", (id,))
    conn.commit()
    print("🗑️ Görev silindi!")

def tamamla(id):
    cursor.execute("UPDATE todos SET done=1 WHERE id=?", (id,))
    conn.commit()
    print("🎉 Görev tamamlandı!")

def menu():
    while True:
        print("\n--- TO-DO Uygulaması ---")
        print("1. Görevleri Listele")
        print("2. Yeni Görev Ekle")
        print("3. Görev Sil")
        print("4. Görevi Tamamla")
        print("5. Çıkış")

        secim = input("Seçiminiz: ")

        if secim == "1":
            listele()
        elif secim == "2":
            gorev = input("Yeni görev girin: ")
            ekle(gorev)
        elif secim == "3":
            id = int(input("Silinecek görev ID'si: "))
            sil(id)
        elif secim == "4":
            id = int(input("Tamamlanan görev ID'si: "))
            tamamla(id)
        elif secim == "5":
            print("Çıkılıyor...")
            break
        else:
            print("❗Geçersiz seçim.")

menu()
conn.close()
