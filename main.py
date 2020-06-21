#!/usr/bin/python3
import gi
import signal
import sys
from storage import Storage
from gi.repository import Gtk
gi.require_version("Gtk", "3.0")


class AddNewTaskBoxRow(Gtk.ListBoxRow):
    def __init__(self):
        super(Gtk.ListBoxRow, self).__init__()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        hbox.add(Gtk.Label("+ Add new task"))
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)
        self.add(hbox)


class TaskListBoxRow(Gtk.ListBoxRow):
    def __init__(self, task):
        super(Gtk.ListBoxRow, self).__init__()
        self.task = task
        self.add(Gtk.Label(task["name"]))
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.add(hbox)


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Today's tasks")
        self.set_default_size(600, 300)
        self.set_border_width(5)
        self.storage = Storage("./_storage.json")
        grid = Gtk.Grid()
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        grid.attach(box_outer, 0, 0, 1, 2)
        task_list_box = self.create_task_list_box(
            self.storage.get_tasks())
        box_outer.pack_start(task_list_box, True, True, 0)
        task_details = self.create_task_details(None)
        grid.attach(task_details, 0, 1, 1, 1)
        self.add(grid)

    def create_task_list_box(self, tasks):
        task_list_box = Gtk.ListBox()
        task_list_box.add(AddNewTaskBoxRow())
        for task in tasks:
            task_list_box.add(TaskListBoxRow(task))
        task_list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        return task_list_box

    def create_task_details(self, task):
        return Gtk.Box(orientation=Gtk.Orientation.VERTICAL)


def handle_termination(self, *args):
    Gtk.main_quit()
    sys.exit()


signal.signal(signal.SIGTERM, handle_termination)
signal.signal(signal.SIGINT, handle_termination)

window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
