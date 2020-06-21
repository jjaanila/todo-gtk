from datetime import datetime
import json
import uuid


class Storage():
    def __init__(self, file_path):
        self.file_path = file_path
        self.state = {
            "tasks": []
        }
        self._load()

    def _load(self):
        with open(self.file_path) as json_file:
            self.state = json.load(json_file)

    def _save(self, content):
        with open(self.file_path, "w") as json_file:
            return json_file.write(json.dumps(self.state))

    def add_task(self, name, description, is_completed):
        task = {
            "id": uuid.uuid1(),
            "name": name,
            "description": description,
            "is_completed": is_completed,
            "created_at": datetime.now()
        }
        self.state["tasks"].append(task)
        self.save()
        return task

    def remove_task(self, task_id):
        self.state["tasks"] = [
            x for x in self.state["tasks"] if x["id"] != task_id]
        self.save()

    def compete_task(self, task_id):
        for task, index in enumerate(self.state["tasks"]):
            if task["id"] == task_id:
                self.state["tasks"][index]["is_completed"] = True
            return

    def get_tasks(self):
        return self.state["tasks"] if "tasks" in self.state else []
