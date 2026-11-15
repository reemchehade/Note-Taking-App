import tkinter as tk
from tkinter import messagebox
import json
import os

PASSWORD = "reem123"
NOTES_FILE = "notes.json"

notes = []
selected_note_index = None


def load_notes_from_file():
    global notes
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            notes = json.load(file)
    else:
        notes = []


def save_notes_to_file():
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)


def save_note():
    global selected_note_index

    title = title_entry.get()
    category = category_var.get()
    content = note_text.get("1.0", tk.END).strip()

    if title == "":
        messagebox.showwarning("Warning", "Please enter a title")
        return

    note = {
        "title": title,
        "category": category,
        "content": content
    }

    if selected_note_index is None:
        notes.append(note)
        messagebox.showinfo("Saved", "Note saved successfully!")
    else:
        notes[selected_note_index] = note
        messagebox.showinfo("Updated", "Note updated successfully!")
        selected_note_index = None
        save_button.config(text="Save Note")

    save_notes_to_file()
    clear_fields()
    refresh_notes_list()


def clear_fields():
    global selected_note_index
    title_entry.delete(0, tk.END)
    note_text.delete("1.0", tk.END)
    category_var.set("Study")
    selected_note_index = None
    save_button.config(text="Save Note")


def refresh_notes_list():
    notes_listbox.delete(0, tk.END)

    for note in notes:
        notes_listbox.insert(tk.END, note["title"] + " - " + note["category"])


def select_note(event):
    global selected_note_index

    selected = notes_listbox.curselection()

    if selected:
        selected_note_index = selected[0]
        note = notes[selected_note_index]

        title_entry.delete(0, tk.END)
        title_entry.insert(0, note["title"])

        category_var.set(note["category"])

        note_text.delete("1.0", tk.END)
        note_text.insert(tk.END, note["content"])

        save_button.config(text="Update Note")


def delete_note():
    global selected_note_index

    selected = notes_listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a note to delete")
        return

    index = selected[0]
    notes.pop(index)

    save_notes_to_file()
    clear_fields()
    refresh_notes_list()

    messagebox.showinfo("Deleted", "Note deleted successfully!")


def search_notes():
    keyword = search_entry.get().lower()

    notes_listbox.delete(0, tk.END)

    for note in notes:
        if keyword in note["title"].lower() or keyword in note["content"].lower() or keyword in note["category"].lower():
            notes_listbox.insert(tk.END, note["title"] + " - " + note["category"])


def show_all_notes():
    search_entry.delete(0, tk.END)
    refresh_notes_list()


def check_password():
    if password_entry.get() == PASSWORD:
        login_window.destroy()
        open_main_app()
    else:
        messagebox.showerror("Error", "Incorrect password")


def open_main_app():
    global root
    global title_entry, note_text, category_var, save_button
    global notes_listbox, search_entry

    root = tk.Tk()
    root.title("Note Taking App")
    root.geometry("850x600")
    root.config(bg="#FFDDEE")

    load_notes_from_file()

    title = tk.Label(root, text="Note Taking App", font=("Arial", 20, "bold"), bg="#FFDDEE", fg="#D53592")
    title.pack(pady=10)

    main_frame = tk.Frame(root, bg="#FFDDEE")
    main_frame.pack()

    left_frame = tk.Frame(main_frame, bg="#FFE5EC", padx=15, pady=15)
    left_frame.grid(row=0, column=0, padx=10)

    right_frame = tk.Frame(main_frame, bg="#FFE5EC", padx=15, pady=15)
    right_frame.grid(row=0, column=1, padx=10)

    
    tk.Label(left_frame, text="Note Title", bg="#FFE5EC", fg="#2B6777").pack()
    title_entry = tk.Entry(left_frame, width=40)
    title_entry.pack(pady=5)

    tk.Label(left_frame, text="Category", bg="#FFE5EC", fg="#2B6777").pack()
    category_var = tk.StringVar()
    category_var.set("Study")

    categories = ["Study", "Tasks", "Work"]
    category_menu = tk.OptionMenu(left_frame, category_var, *categories)
    category_menu.pack(pady=5)

    tk.Label(left_frame, text="Note Content", bg="#FFE5EC", fg="#2B6777").pack()
    note_text = tk.Text(left_frame, width=45, height=15)
    note_text.pack(pady=5)

    save_button = tk.Button(left_frame, text="Save Note", command=save_note, bg="#FF8FAB", fg="white", width=15)
    save_button.pack(pady=5)

    clear_button = tk.Button(left_frame, text="Clear", command=clear_fields, bg="#FFB3C6", fg="white", width=15)
    clear_button.pack(pady=5)

    delete_button = tk.Button(left_frame, text="Delete Selected Note", command=delete_note, bg="#D9534F", fg="white", width=18)
    delete_button.pack(pady=5)

    
    tk.Label(right_frame, text="Search Notes", bg="#CDEAE5", fg="#E82858").pack()
    search_entry = tk.Entry(right_frame, width=35)
    search_entry.pack(pady=5)

    search_button = tk.Button(right_frame, text="Search", command=search_notes, bg="#FF8FAB", fg="white", width=15)
    search_button.pack(pady=5)

    show_all_button = tk.Button(right_frame, text="Show All Notes", command=show_all_notes, bg="#FFB3C6", fg="white", width=15)
    show_all_button.pack(pady=5)

    tk.Label(right_frame, text="Saved Notes", bg="#CDEAE5", fg="#E82858").pack(pady=5)

    notes_listbox = tk.Listbox(right_frame, width=40, height=20)
    notes_listbox.pack(pady=5)

    notes_listbox.bind("<<ListboxSelect>>", select_note)

    refresh_notes_list()

    root.mainloop()


login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("350x200")
login_window.config(bg="#FFDDEE")

tk.Label(login_window, text="Enter Password", font=("Arial", 16, "bold"), bg="#FFDDEE", fg="#C75B7A").pack(pady=20)

password_entry = tk.Entry(login_window, show="*", width=25,bg="#FFF0F5")
password_entry.pack(pady=5)

login_button = tk.Button(login_window, text="Login", command=check_password, bg="#FF8FAB", fg="white", width=12)
login_button.pack(pady=15)

login_window.mainloop()