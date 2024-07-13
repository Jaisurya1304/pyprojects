import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")

        self.create_table()
        self.create_menu()
        self.create_widgets()
        self.load_data()

    def create_table(self):
        self.tree = ttk.Treeview(
            self.root, columns=("Name", "Course", "Mobile"), show="headings"
        )
        self.tree.heading("Name", text="Name")
        self.tree.heading("Course", text="Course")
        self.tree.heading("Mobile", text="Mobile")
        self.tree.pack(expand=True, fill="both")

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Student", command=self.insert)

        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.about)

        edit_menu = tk.Menu(menu)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Search", command=self.search)

    def create_widgets(self):
        self.status = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.bind("<Double-1>", self.on_item_double_click)

    def on_item_double_click(self, event):
        item = self.tree.selection()[0]
        self.edit(item)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, course, mobile FROM students")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row[1:])  # Exclude ID
        connection.close()

    def insert(self):
        dialog = InsertDialog(self)
        self.root.wait_window(dialog.top)

    def edit(self, item):
        dialog = EditDialog(self, item)
        self.root.wait_window(dialog.top)

    def delete(self, item):
        student_id = self.tree.item(item)["values"][0]
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()
        connection.close()
        self.load_data()

    def search(self):
        dialog = SearchDialog(self)
        self.root.wait_window(dialog.top)

    def about(self):
        messagebox.showinfo("About", "This app is about student management system.")


class InsertDialog:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(parent.root)
        self.top.title("Insert Student Data")
        self.top.geometry("300x300")

        self.student_name = tk.StringVar()
        self.course_name = tk.StringVar()
        self.mobile = tk.StringVar()

        tk.Label(self.top, text="Name").pack()
        tk.Entry(self.top, textvariable=self.student_name).pack()

        tk.Label(self.top, text="Course").pack()
        tk.Entry(self.top, textvariable=self.course_name).pack()

        tk.Label(self.top, text="Mobile").pack()
        tk.Entry(self.top, textvariable=self.mobile).pack()

        tk.Button(self.top, text="Register", command=self.add_student).pack()

    def add_student(self):
        name = self.student_name.get()
        course = self.course_name.get()
        mobile = self.mobile.get()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
            (name, course, mobile),
        )
        connection.commit()
        connection.close()

        self.parent.load_data()
        self.top.destroy()


class EditDialog:
    def __init__(self, parent, item):
        self.parent = parent
        self.item = item
        self.top = tk.Toplevel(parent.root)
        self.top.title("Update Student Data")
        self.top.geometry("300x300")

        values = parent.tree.item(item)["values"]
        self.student_id = values[0]
        self.student_name = tk.StringVar(value=values[1])
        self.course_name = tk.StringVar(value=values[2])
        self.mobile = tk.StringVar(value=values[3])

        tk.Label(self.top, text="Name").pack()
        tk.Entry(self.top, textvariable=self.student_name).pack()

        tk.Label(self.top, text="Course").pack()
        tk.Entry(self.top, textvariable=self.course_name).pack()

        tk.Label(self.top, text="Mobile").pack()
        tk.Entry(self.top, textvariable=self.mobile).pack()

        tk.Button(self.top, text="Update", command=self.update_student).pack()

    def update_student(self):
        name = self.student_name.get()
        course = self.course_name.get()
        mobile = self.mobile.get()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
            (name, course, mobile, self.student_id),
        )
        connection.commit()
        connection.close()

        self.parent.load_data()
        self.top.destroy()


class SearchDialog:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(parent.root)
        self.top.title("Search Student")
        self.top.geometry("300x150")

        self.student_name = tk.StringVar()

        tk.Label(self.top, text="Name").pack()
        tk.Entry(self.top, textvariable=self.student_name).pack()

        tk.Button(self.top, text="Search", command=self.search).pack()

    def search(self):
        name = self.student_name.get()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute(
            "SELECT name, course, mobile FROM students WHERE name LIKE ?",
            ("%" + name + "%",),
        )

        for item in self.parent.tree.get_children():
            self.parent.tree.delete(item)

        for row in result.fetchall():
            self.parent.tree.insert("", "end", values=row)

        connection.close()
        self.top.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()
