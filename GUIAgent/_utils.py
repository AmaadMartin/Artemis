from ._prompts import *
from ._config import *
import json
from Utils.ScreenShot import screen_shot
import base64
import tempfile


def set_task(self, task):
    self.task = task
    self.update_screen()

    messages = [
        {"role": "user",
        "content": [
            {"type": "text", 
                "text": self.prompt}
        ],
        }
    ] + [{
            "role": "user",
            "content": [
                {"type": "text", "text": f"Given the task \"{self.task}\" create an initial subtask to complete as a step in completing the task. Put the subtask in json format with the key being \"subtask\" and the value being the subtask"},
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{self.image}",
                    "detail" : "high"
                }
                }
            ],
            }]
    
    response = self.client.chat.completions.create(
        model=PLANNING_AGENT_MODEL,
        response_format={ "type": "json_object" },
        messages= messages,
        max_tokens=300,
        )
    
    json_string = response.choices[0].message.content
    subtask = json.loads(json_string)
    self.subtasks.append(subtask["subtask"])
    print(subtask)


def update_screen(self):
    new_state = screen_shot()
    self.image = new_state

    self.trace.append(
        {
            "role": "user",
            "content": [
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{new_state}",
                        "detail" : "high"
                    }
                    }
            ]
        }
    )

def print_messages(self):
    messages = self.client.beta.threads.messages.list(
        thread_id=self.threadId,
        order="asc"
    )
    
    messages = list(map(lambda x: {"role": x.role, "value": x.content[0].text.value} if x.content[0].type == "text" else " ", messages.data))

    for message in messages:
        if message != " ":
            print(message["role"] + ": " + message["value"])

def print_trace(self):    
    for message in self.trace:
        if message["content"][0]["type"] == "text":
            print(message["content"][0]["text"])


def print_subtasks(self):
    for subtask in self.subtasks:
        print(subtask)