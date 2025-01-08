from openai import OpenAI
import re
import requests
import wikipedia


SYSTEM_PROMPT="""
    You run in a loop of Thought, Action, PAUSE, Observation.
    At the end of the loop, you output an Answer.  
    Use Thought to describe your reasoning about the input or question you have received.  
    Use Action to run one of the available actions, then return PAUSE.  
    Observation will be the result of running those actions.  
    
    Your available actions are:
    dictionary_lookup:  
    e.g. dictionary_lookup: "ephemeral"  
    Returns the meaning of the word from a dictionary.  
    
    wikipedia:  
    e.g. wikipedia: "Quantum Mechanics"  
    Returns a summary of the topic by searching Wikipedia.  
    
    grammar_check:  
    e.g. grammar_check: "I has a pen."  
    Checks the grammar of the sentence and returns the corrected version.  
    
    Always perform the action most relevant to the question or input provided.  
    
    Example session:
    Input: "Define serendipity."  
    Thought: I should look up the meaning of the word "serendipity" in the dictionary.  
    Action: dictionary_lookup: "serendipity"  
    PAUSE  
    You will be called again with this:  
    Observation: Serendipity means the occurrence of events by chance in a happy or beneficial way.  
    You then output:  
    Answer: Serendipity means the occurrence of events by chance in a happy or beneficial way.  
    
    ---
    
    Input: "Tell me about Artificial Intelligence."  
    Thought: I should search for "Artificial Intelligence" on Wikipedia.  
    Action: wikipedia: "Artificial Intelligence"  
    PAUSE  
    You will be called again with this:  
    Observation: Artificial Intelligence is the simulation of human intelligence in machines that are programmed to think and learn.  
    You then output:  
    Answer: Artificial Intelligence is the simulation of human intelligence in machines that are programmed to think and learn.  
    
    ---
    
    Input: "She go to school every day."  
    Thought: I should check the grammar of the given sentence and correct it.  
    Action: grammar_check: "She go to school every day."  
    PAUSE  
    You will be called again with this:  
    Observation: She goes to school every day.  
    You then output:  
    Answer: She goes to school every day.
    """.strip()


class EducationalBot:

    def __init__(self):
        self.client=OpenAI(base_url="http://127.0.0.1:1234/v1/",api_key="none")
        self.system=SYSTEM_PROMPT
        self.messages=[]
        self.messages.append({"role":"system","content":self.system})
        self.known_action={
            "dictionary_lookup":self.dictionary_lookup,
            "wikipedia":self.wikipedia,
            "grammar_check":self.grammar_check
}

    def __call__(self,message:str):
        self.messages.append({"role":"user","content":message})
        result= self.execute()
        self.messages.append({"role":"assistant","content":result})
        return result
    
    def execute(self):
        completion=self.client.chat.completions.create(
            model="opensource",
            messages=self.messages
        )
        return completion.choices[0].message.content
    
    def dictionary_lookup(sefl,word:str)->str:
        response=requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        response.raise_for_status()
        data=response.json()
        return data[0]["meanings"][0]["definitions"][0]["definition"]

    def wikipedia(self,topic:str)->str:
       return wikipedia.summary(topic,sentences=10)

    def grammar_check(self,text:str)->str:
        response=requests.post("https://api.languagetool.org/v2/check",params={"text":text,"language":"en-US"})
        response.raise_for_status()
        data=response.json()
        return data["matches"][0]["message"]

    def query(self,question:str,max_turns=5):
       i=0
       action_re=re.compile('^Action: (\w+): (.*)$')
       bot=EducationalBot()
       next_prompt=question
       while i<max_turns:
        i+=1
        result=bot(next_prompt)
        actions=[action_re.match(a)for a in result.split('\n')if action_re.match(a)]
        if actions:
            action,action_input=actions[0].groups()
            if action not in self.known_action:
                raise Exception(f"Unknown action :{action}:{action_input}")
            print(f"--running {action} {action_input}")
            observation=self.known_action[action](action_input)
            next_prompt=f"Observation:{observation}"
        else:
            return result
        return result