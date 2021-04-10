import random
from locust import HttpUser, task, between
import json
import os
import numpy as np


#data = [0.132]*(224*224*4)
#target_ip = 'http://107.20.58.60'
target_ip = "http://127.0.0.1:8000"


class Load_tester(HttpUser):
    def inferance_endpoint(self):
        response = self.client.post(
            f"{target_ip}/api/v2/nfl", data=4, headers={"content-type": "application/json"})
        if response.status_code != 200:
            print("error")
