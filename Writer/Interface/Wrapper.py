import Writer.Config

import ollama



def InitClient(_ClientHost:str = "http://10.1.65.4:11434"):
    return ollama.Client(host=_ClientHost)


def ChatAndStreamResponse(_Client, _Messages, _Model:str="llama3"):
    Stream = _Client.chat(
        model=_Model,
        messages=_Messages,
        stream=True,
        options=dict(seed=Writer.Core.Config.SEED)
    )
    print(f"DEBUG: Using Model {_Model}")
    _Messages.append(StreamResponse(Stream))

    return _Messages

def StreamResponse(_Stream):
  
    Response:str = ""
    for chunk in _Stream:
        ChunkText = chunk['message']['content']
        Response += ChunkText

        print(ChunkText, end='', flush=True)
    print("\n\n\n")
    return {'role': 'assistant', 'content': Response}

def BuildUserQuery(_Query:str):
    return {'role': 'user', 'content': _Query}

def GetLastMessageText(_Messages:list):
    return _Messages[-1]["content"]



class Interface:

    def __init__(self, _Client, _Model:str = "llama3", _Seed:int = 0):
        self.Client = _Client
        self.Model = _Model
        self.Seed = _Seed
        self.History = []

    def SetHistory(self, _History):
        self.History = _History

    def GetHistory(self):
        return self.History

    def GetLastResponse(self):
        if (len(self.History) == 0):
            return None

        return self.History[-1]

    def AddMessage(self, _Message):
        self.History.append({'role': 'user', 'content': _Message})
    
    def StreamMessage(self):
        Stream = self.Client.chat(
            model=self.Model,
            messages=self.History,
            stream=True,
            options=dict(seed=self.Seed)
        )

        Response:str = ""
        for Chunk in Stream:
            ChunkText = Chunk['message']['content']
            Response += ChunkText

            print(ChunkText, end='', flush=True)

        self.History.append({'role': 'assistant', 'content': Response})

    def AddMessageAndStream(self, _Message):
        self.AddMessage(_Message)
        self.StreamMessage()