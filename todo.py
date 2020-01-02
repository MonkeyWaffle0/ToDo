from tkinter import *
import json


class Task:
    def __init__(self, mainWindow, task, state):
        self.task = task
        self.state = state
        self.mainWindow = mainWindow
        self.button = Button(mainWindow.topFrame, text=self.task, command=self.click)

        if state == "todo":
            self.button.grid(row=self.mainWindow.check("todo"), column=0)
        elif state == "working":
            self.button.grid(row=self.mainWindow.check("working"), column=1)
        elif state == "done":
            self.button.grid(row=self.mainWindow.check("done"), column=2)

    def click(self):
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


class SaveWindow(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.label = Label(top, text="Name of your list :")
        self.label.pack()
        self.entry = Entry(top)
        self.entry.pack()
        self.button = Button(top, text="Save", command=self.cleanup)
        self.button.pack()

    def cleanup(self):
        self.value = self.entry.get()
        self.top.destroy()


class NewTaskWindow(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.label = Label(top, text="Enter your task :")
        self.label.pack()
        self.entry = Entry(top)
        self.entry.pack()
        self.button = Button(top, text="Add", command=self.cleanup)
        self.button.pack()

    def cleanup(self):
        self.value = self.entry.get()
        self.top.destroy()


class mainWindow(object):
    def __init__(self, master, tasks):
        self.master = master
        self.topFrame = Frame(master, width=600, height=600)
        self.topFrame.pack()

        self.addButton = Button(self.topFrame, text="Add", command=self.popup)
        self.addButton.grid(row=0, column=1, padx=1, pady=1)

        self.saveButton = Button(self.topFrame, text="Save", command=self.save)
        self.saveButton.grid(row=0, column=0)

        self.loadButton = Button(self.topFrame, text="Load", command=lambda:self.load(self.entry.get()))
        self.loadButton.grid(row=0, column=2)
        self.entry = Entry(self.topFrame)
        self.entry.grid(row=0, column=3)

        self.todoText = Label(self.topFrame, text="To do :").grid(row=1, column=0, padx=1, pady=1)
        self.workingText = Label(self.topFrame, text="Working on :").grid(row=1, column=1, padx=1, pady=1)
        self.doneText = Label(self.topFrame, text="Done :").grid(row=1, column=2, padx=1, pady=1)

        self.tasks = tasks
        self.save = {}

    def popup(self):
        self.window = NewTaskWindow(self.master)
        self.addButton["state"] = "disabled"
        self.master.wait_window(self.window.top)
        self.addButton["state"] = "normal"
        try:
            task = Task(self, self.entryValue(), "todo")
            self.tasks.append(task)
        except AttributeError:
            pass

    def entryValue(self):
        return self.window.value

    def check(self, state):
        row = 0
        for task in self.tasks:
            if task.state == state:
                row += 1
        return row + 2

    def update(self):
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
        self.window = SaveWindow(self.master)
        self.saveButton["state"] = "disabled"
        self.master.wait_window(self.window.top)
        self.saveButton["state"] = "normal"
        for task in self.tasks:
            self.save[task.task] = task.state
        with open(self.entryValue(), "w") as outfile:
            json.dump(self.save, outfile)

    def load(self, file):
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
    main = mainWindow(root, [])
    root.mainloop()