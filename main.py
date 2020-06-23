#!/usr/bin/python3

import gi
import signal
import sys
from storage import Storage
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

ROW_MARGIN = 5

class TaskListBoxRow(Gtk.ListBoxRow):

    def __init__(self, task, on_task_removed, on_task_completion_toggled):
        super(Gtk.ListBoxRow, self).__init__()
        self.task = task
        self.on_task_completion_toggled = on_task_completion_toggled
        complete_checkbox = Gtk.CheckButton("Completed")
        complete_checkbox.set_active(task["is_completed"])
        complete_checkbox.connect("toggled", self.on_complete_checkbox_toggle)
        complete_checkbox.set_margin_right(5)
        remove_button = Gtk.Button("Remove")
        remove_button.connect("clicked", lambda self: on_task_removed(task))
        label = Gtk.Label(task["name"])
        label.set_hexpand(True)
        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.attach(label, 0, 0, 8, 1)
        grid.attach(complete_checkbox, 8, 0, 1, 1)
        grid.attach(remove_button, 9, 0, 1, 1)
        self.set_margin_top(ROW_MARGIN)
        self.set_margin_right(ROW_MARGIN)
        self.set_margin_left(ROW_MARGIN)
        self.add(grid)

    def on_complete_checkbox_toggle(self, button):
        self.task["is_completed"] = button.get_active()
        self.on_task_completion_toggled(self.task)


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Today's tasks")
        self.set_default_size(600, 500)
        self.set_border_width(5)
        self.storage = Storage("./_storage.json")
        new_task_label = Gtk.Label("New task:")
        self.new_task_entry = Gtk.Entry()
        self.new_task_entry.connect(
            "activate", self.on_new_task_entry_activated)

        self.create_task_list_box()
        list_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        list_container.set_margin_top(5)
        list_container.pack_start(self.task_list_box, True, True, 0)
        list_container.set_hexpand(True)
        list_container.set_vexpand(True)

        grid = Gtk.Grid()
        grid.attach(new_task_label, 1, 0, 1, 1)
        grid.attach_next_to(
            self.new_task_entry, new_task_label, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach(list_container, 0, 1, 6, 2)
        self.add(grid)

    def on_new_task_entry_activated(self, entry):
        task_name = entry.get_text()
        if task_name:
            task = self.storage.add_task(task_name)
            self.refresh_task_list_box()
            entry.set_text("")

    def on_task_removed(self, task):
        self.storage.remove_task(task["id"])
        self.refresh_task_list_box()

    def on_task_completion_toggled(self, task):
        self.storage.update_task(task)
        self.refresh_task_list_box()

    def create_task_list_box(self):
        self.task_list_box = Gtk.ListBox()
        self.task_list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.refresh_task_list_box()

    def refresh_task_list_box(self):
        for task_row in self.task_list_box.get_children():
            self.task_list_box.remove(task_row)
        for task in self.storage.get_tasks():
            self.task_list_box.add(TaskListBoxRow(task, self.on_task_removed, self.on_task_completion_toggled))
        self.task_list_box.show_all()


def handle_termination(self, *args):
    Gtk.main_quit()
    sys.exit()

# Without this the program may freeze after SIGINT
signal.signal(signal.SIGINT, handle_termination)

window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
