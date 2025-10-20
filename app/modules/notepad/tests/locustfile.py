from locust import HttpUser, TaskSet, task, between
from core.environment.host import get_host_for_locust_testing
from core.locust.common import get_csrf_token


class NotepadBehavior(TaskSet):
    def on_start(self):
        self.login()

    def login(self):
        response = self.client.get("/login")
        csrf_token = get_csrf_token(response)
        self.client.post(
            "/login",
            data={"email": "user1@example.com", "password": "1234", "csrf_token": csrf_token},
        )

    @task
    def view_notepad_index(self):
        response = self.client.get("/notepad")
        if response.status_code != 200:
            print(f"Index failed: {response.status_code}")

    @task
    def create_note(self):
        response = self.client.get("/notepad/create")
        csrf_token = get_csrf_token(response)
        data = {"title": "nota simple", "body": "contenido simple", "csrf_token": csrf_token}
        response = self.client.post("/notepad/create", data=data)
        if response.status_code != 200:
            print(f"Create note failed: {response.status_code}")


class NotepadUser(HttpUser):
    tasks = [NotepadBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()
