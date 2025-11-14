from locust import SequentialTaskSet, HttpUser, task, between
import time
import uuid

class BlogScenario(SequentialTaskSet):
    
    def on_start(self):
        self.username = f"user_{uuid.uuid4()}"
    
    @task(1)
    def create_and_read_post(self):
        response = self.client.post("/posts", json={
            "author": self.username,
            "title": "Обезьяний побег",
            "content": "14.11.2025 в 12:00 по Гринвичу из Новосибирского зоопарка сбежало три макаки. " 
                       "Их точное местоположение до сих пор неизвестно.",
        })
        
        if response.status_code == 201:
            self.post_id = response.json()["id"]
            self.client.get(f"/posts/{self.post_id}")
            
    @task(3)
    def read_all_posts(self):
        self.client.get("/posts")

    @task(5)
    def read_post_with_postid_1(self):
        self.client.get(f"/posts/1")


class BlogUser(HttpUser):
    wait_time = between(1, 3)
    tasks = [BlogScenario]
            