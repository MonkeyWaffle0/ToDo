from tkinter import *
import json


class Task:
    """Represents a task."""
    def __init__(self, mainWindow, task, state):
        self.task = task   # Description of the task
        self.state = state   # State the task is (to do, working, done)
        self.mainWindow = mainWindow
        # Task is a button so it is moveable across states.
        self.button = Button(mainWindow.frame, text=self.task, command=self.left)
        self.button.bind("<Button-3>", self.right)

        # Place the button in the corresponding column depending on the task's state.
        if state == "todo":
            self.button.grid(row=self.mainWindow.check("todo"), column=0)
        elif state == "working":
            self.button.grid(row=self.mainWindow.check("working"), column=1)
        elif state == "done":
            self.button.grid(row=self.mainWindow.check("done"), column=2)

    def left(self):
        """Move the task to the next state when clicked on."""
        if self.state == "todo":
            self.button.grid(row=self.mainWindow.check("working"), column=1)
            self.state = "working"
        elif self.state == "working":
            self.button.grid(row=self.mainWindow.check("done"), column=2)
            self.state = "done"
        elif self.state == "done":
            self.button.grid(row=self.mainWindow.check("todo"), column=0)
            self.state = "todo"

        self.mainWindow.update()

    def right(self, event):
        self.button.destroy()
        self.mainWindow.tasks.remove(self)
        self.mainWindow.update()


class SaveWindow(object):
    """Popup window when clicked on the save button."""
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.label = Label(top, text="Name your list :")
        self.label.pack()
        self.entry = Entry(top)
        self.entry.pack()
        self.button = Button(top, text="Save", command=self.cleanup)
        self.button.pack()

    def cleanup(self):
        """Get the entry value and close the popup window."""
        self.value = self.entry.get()
        self.top.destroy()


class NewTaskWindow(object):
    """Popup window when clicked on the add button."""
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.label = Label(top, text="Enter your task :")
        self.label.pack()
        self.entry = Entry(top)
        self.entry.pack()
        self.button = Button(top, text="Add", command=self.cleanup)
        self.button.pack()

    def cleanup(self):
        """Get the entry value and close the popup window."""
        self.value = self.entry.get()
        self.top.destroy()


class MainWindow(object):
    """Main window"""
    def __init__(self, master):
        self.master = master
        self.frame = Frame(master, width=600, height=600)
        self.frame.pack()

        # Button to add a new task.
        self.addButton = Button(self.frame, text="Add", command=self.popup)
        self.addButton.grid(row=0, column=1, padx=1, pady=1)

        # Button to save the current list.
        self.saveButton = Button(self.frame, text="Save", command=self.save)
        self.saveButton.grid(row=0, column=0)

        #Button to load a saved list.
        self.loadButton = Button(self.frame, text="Load", command=lambda:self.load(self.entry.get()))
        self.loadButton.grid(row=0, column=2)
        # Entry to load the list from.
        self.entry = Entry(self.frame)
        self.entry.grid(row=0, column=3)

        # Text displaying "To do", "Working on" and "Done".
        self.todoText = Label(self.frame, text="To do :").grid(row=1, column=0, padx=1, pady=1)
        self.workingText = Label(self.frame, text="Working on :").grid(row=1, column=1, padx=1, pady=1)
        self.doneText = Label(self.frame, text="Done !").grid(row=1, column=2, padx=1, pady=1)

        # List of the tasks on the window.
        self.tasks = []
        # Tasks that will be saved in a json file.
        self.save = {}

    def popup(self):
        """Popup window to add a new task."""
        # Creating the window.
        self.window = NewTaskWindow(self.master)
        # Disabling the add button until the popup window is closed.
        self.addButton["state"] = "disabled"
        self.master.wait_window(self.window.top)
        self.addButton["state"] = "normal"
        try:
            # Append the tasks to the tasks list.
            task = Task(self, self.entryValue(), "todo")
            self.tasks.append(task)
        except AttributeError:
            pass

    def entryValue(self):
        """Get the value in the entry field."""
        return self.window.value

    def check(self, state):
        """Check the state of each task and returns the row where to put the new task."""
        row = 0
        for task in self.tasks:
            if task.state == state:
                row += 1
        # Add 2 to the row number because the first two rows are the add/save/load buttons and the text.
        return row + 2

    def update(self):
        """Update the window when a task has been moved so there is no empty space."""
        row = 0
        for task in self.tasks:
            if task.state == "todo":
                task.button.grid(row=row+2, column=0)
                row += 1
        row = 0
        for task in self.tasks:
            if task.state == "working":
                task.button.grid(row=row+2, column=1)
                row += 1
        row = 0
        for task in self.tasks:
            if task.state == "done":
                task.button.grid(row=row+2, column=2)
                row += 1

    def save(self):
        """Popup window to save the current list."""
        # Creating the window.
        self.window = SaveWindow(self.master)

        # Disable the save button until the popup is closed.
        self.saveButton["state"] = "disabled"
        self.master.wait_window(self.window.top)
        self.saveButton["state"] = "normal"

        # Add every task to self.save and dump it to a file.
        for task in self.tasks:
            self.save[task.task] = task.state
        with open(self.entryValue(), "w") as outfile:
            json.dump(self.save, outfile)

    def load(self, file):
        """Load the file in the load entry field."""
        with open(file, "r") as readFile:
            jsonStr = readFile.read()
            loadedTasks = json.loads(jsonStr)
            for task, state in loadedTasks.items():
                new = Task(self, task, state)
                self.tasks.append(new)


if __name__ == "__main__":
    root = Tk()
    root.title("ToDo")
    root.geometry("300x300")
    main = MainWindow(root)
    root.mainloop()