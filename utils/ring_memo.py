# obtain system prompt

from agent.prompt import PROMPT, TOOLS
import queue

class record_struct():
    def __init__(self, usr_input, agent_output):
        self.usr = usr_input
        self.output = agent_output

    def __str__(self):
        return "user:"+self.usr+"\nbot:"+self.output

class naive_memo():
    def __init__(self, n = 50):
        self.n = n
        self.ring = []
        self.SYS = PROMPT
        self.TOOL = TOOLS
        self.compressed = None

    def __str__(self):
        history = f"Previous {self.n} records: \n"
        for elem in self.ring:
            history += str(elem) + "\n"
        return "sys_prompt:"+self.SYS+"\ntools:"+self.TOOL+"\n"+history

    def compress(self):
        pass

    def add(self, usr_input, agent_output):
        if len(self.ring) == self.n:
            self.ring.pop(0)
        self.ring.append(record_struct(usr_input, agent_output))
