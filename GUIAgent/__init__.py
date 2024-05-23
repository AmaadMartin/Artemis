from ._config import *
from ._tools import *
from ._prompts import *
from ._utils import *

import time

from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = OPENAI_KEY

class GUIAgent:
    def __init__(self):
        self.tools = tools
        self.client = OpenAI()
        self.system_prompt = GUI_agent_prompt(self)
        self.image = None
        self.task = None
        self.finished = False
        self.subtasks = []
        self.trace = []


    
    def make_context(self, query):
        messages = [
            {"role": "system",
            "content": [
                {"type": "text", 
                    "text": self.system_prompt}
            ],
            }
        ] + self.trace + [
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": query}
                ],
                }
            ]

        return messages

    def act(self):
        response = self.client.chat.completions.create(
            model=ACTION_AGENT_MODEL,
            response_format={ "type": "json_object"},
            messages=self.make_context(action_agent_query(self)),
            max_tokens=300,
            )
        
        json_string = response.choices[0].message.content
        response = json.loads(json_string)
        print(response)

        self.trace.append(
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": f"ACTION: {response}"}
                ]
            }
        )
        for action in response['actions']:
            execute_action(self, action)
            time.sleep(0.25)

    def plan(self):
        response = self.client.chat.completions.create(
            model=PLANNING_AGENT_MODEL,
            response_format={ "type": "json_object" },
            messages=self.make_context(planning_agent_query(self)),
            max_tokens=300,
            )

        json_string = response.choices[0].message.content
        response = json.loads(json_string)
        print(response)

        if "finished" in response:
            self.finished = True
            self.trace.append(
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": "PLAN: task finished"}
                    ]
                }
            )
        elif "subtask" in response:
            self.subtasks.append(response["subtask"])
            self.trace.append(
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": f"PLAN: {response['subtask']}"}
                    ]
                }
            )

    def reflect(self):
        response = self.client.chat.completions.create(
            model=REFLECTION_AGENT_MODEL,
            response_format={ "type": "json_object" },
            messages=self.make_context(reflection_agent_query(self)),
            max_tokens=300,
            )

        json_string = response.choices[0].message.content
        response = json.loads(json_string)
        print(response)
        
        finished = False
        if "finished" in response and response["finished"]:
            self.trace.append(
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": "REFLECTION: subtask finished"}
                    ]
                }
            )
            finished = True
        if "feedback" in response:
            self.trace.append(
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": f"REFLECTION: {response['feedback']}"}
                    ]
                }
            )
        if "change" in response and response["change"]:
            self.trace.append(
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": f"REFLECTION: change subtask"}
                    ]
                }
            )
            finished = True
        return finished

    def complete_task(self, task):
        self.task = task
        update_screen(self)

        while not self.finished:
            self.plan()
            subtask_finished = False
            while not subtask_finished:
                self.act()
                
                time.sleep(0.5)
                update_screen(self)

                subtask_finished = self.reflect()

    def print_trace(self):
        print_trace(self)