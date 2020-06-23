import uuid
import json


class Storage():
    def __init__(self, file_path):
        self.file_path = file_path
        self.state = {
            "tasks": []
        }
        self._load()

    def _load(self):
        try:
            with open(self.file_path) as json_file:
                self.state = json.load(json_file)
        except (IOError, json.JSONDecodeError):
            self.state = {
                "tasks": []
            }
        if "tasks" not in self.state or not self.state["tasks"]:
            self.state["tasks"] = []

    def _save(self):
        with open(self.file_path, "w") as json_file:
            return json_file.write(json.dumps(self.state))

    def add_task(self, name):
        task = {
            "id": str(uuid.uuid1()),
            "name": name,
            "is_completed": False
        }
        self.state["tasks"].append(task)
        self._save()
        return task

    def remove_task(self, task_id):
        self.state["tasks"] = [
            x for x in self.state["tasks"] if x["id"] != task_id]
        self._save()

    def update_task(self, new_task):
        for index, task in enumerate(self.state["tasks"]):
            if task["id"] == new_task["id"]:
                self.state["tasks"][index] = new_task
                self._save()
                return


    def get_tasks(self):
        return self.state["tasks"]
