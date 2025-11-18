import tkinter as tk
from tkinter import messagebox
import json
import os

FILE = "notes.json"

# -------------------------------------------------------------
# JSON HELPER FUNCTIONS (SAFE & STABLE)
# -------------------------------------------------------------

def load_notes_from_file():
    """Loads notes safely. Returns a list always."""
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r") as f:
            data = json.load(f)

        # If file contains dict or anything wrong → reset to list
        if not isinstance(data, list):
            return []

        return data

    except json.JSONDecodeError:
        # Corrupt JSON → reset
        return []

def save_notes_to_file(notes):
    """Writes notes (list) to JSON."""
    with open(FILE, "w") as f:
        json.dump(notes, f, indent=4)

# -------------------------------------------------------------
# BUTTON FUNCTIONS
# -------------------------------------------------------------

def refresh_listbox():
    listbox.delete(0, tk.END)
    notes = load_notes_from_file()
    for note in notes:
        listbox.insert(tk.END, note["title"])

def new_note():
    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)
    listbox.selection_clear(0, tk.END)

def save_note():
    title = title_entry.get().strip()
    content = content_text.get("1.0", tk.END).strip()

    if title == "":
        messagebox.showwarning("Error", "Title cannot be empty!")
        return

    notes = load_notes_from_file()

    selected = listbox.curselection()
    if selected:
        # Update existing note
        notes[selected[0]] = {"title": title, "content": content}
    else:
        # Add new note
        notes.append({"title": title, "content": content})

    save_notes_to_file(notes)
    refresh_listbox()
    messagebox.showinfo("Saved", "Note saved successfully!")

def delete_note():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Error", "Select a note to delete!")
        return

    notes = load_notes_from_file()
    notes.pop(selected[0])
    save_notes_to_file(notes)

    refresh_listbox()
    new_note()
    messagebox.showinfo("Deleted", "Note deleted successfully.")

def load_note(event=None):
    selected = listbox.curselection()
    if not selected:
        return

    notes = load_notes_from_file()
    note = notes[selected[0]]

    title_entry.delete(0, tk.END)
    title_entry.insert(0, note["title"])

    content_text.delete("1.0", tk.END)
    content_text.insert("1.0", note["content"])

# -------------------------------------------------------------
# UI SETUP
# -------------------------------------------------------------

root = tk.Tk()
root.title("Notes App")
root.geometry("650x420")

# ---- Toolbar ----
toolbar = tk.Frame(root, bg="#ececec", pady=5)
toolbar.pack(fill="x")

tk.Button(toolbar, text="New", width=10, command=new_note).pack(side="left", padx=5)
tk.Button(toolbar, text="Save", width=10, command=save_note).pack(side="left", padx=5)
tk.Button(toolbar, text="Delete", width=10, command=delete_note).pack(side="left", padx=5)

# ---- Left Listbox ----
left_frame = tk.Frame(root)
left_frame.pack(side="left", fill="y")

listbox = tk.Listbox(left_frame, width=25, font=("Arial", 11))
listbox.pack(fill="y", padx=10, pady=10)
listbox.bind("<<ListboxSelect>>", load_note)

# ---- Right Section ----
right_frame = tk.Frame(root)
right_frame.pack(side="right", fill="both", expand=True)

# Title
tk.Label(right_frame, text="Title:", font=("Arial", 12)).pack(anchor="nw", padx=10, pady=(10, 0))
title_entry = tk.Entry(right_frame, font=("Arial", 12), bd=2)
title_entry.pack(fill="x", padx=10, pady=(0, 10))

# Content
tk.Label(right_frame, text="Content:", font=("Arial", 12)).pack(anchor="nw", padx=10)
content_text = tk.Text(right_frame, font=("Arial", 12))
content_text.pack(fill="both", expand=True, padx=10, pady=10)

# INITIAL LOAD
refresh_listbox()

root.mainloop()

