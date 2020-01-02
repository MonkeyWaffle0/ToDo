from tkinter import *


class Task:
    def __init__(self, task, mainWindow):
        self.task = task
        self.state = "todo"
        self.mainWindow = mainWindow

    def add(self):
        taskButton = Button(self.mainWindow.bottomFrame, text=self.task)
        taskButton.pack(anchor="w")

    def done(self):
        self.state = "done"

    def working(self):
        self.state = "working"


class NewTask(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.label = Label(top, text="Enter your task :")
        self.label.pack()
        self.entry = Entry(top)
        self.entry.pack()
        self.button = Button(top, text='Add', command=self.cleanup)
        self.button.pack()

    def cleanup(self):
        self.value = self.entry.get()
        self.top.destroy()


class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.topFrame = Frame(master).pack()
        self.bottomFrame = Frame(master).pack(side="bottom")
        self.addButton = Button(self.topFrame,text="Add",command=self.popup)
        self.addButton.pack()
        self.tasks = []

    def popup(self):
        self.window = NewTask(self.master)
        self.addButton["state"] = "disabled"
        self.master.wait_window(self.window.top)
        self.addButton["state"] = "normal"
        try:
            task = Task(self.entryValue(), self)
            task.add()
            self.tasks.append(task)
        except AttributeError:
            pass

    def entryValue(self):
        return self.window.value


if __name__ == "__main__":
    root = Tk()
    root.geometry("600x600")
    root.title("ToDo")
    main = mainWindow(root)
    root.mainloop()