from numpy import inf
from event import Event

class Job:
    initTime = 0 # Tempo de início do job
    name = "" # Nome do job
    duration = 0 # Duração do job
    mem = 0 # Memória alocada para o job
    events = [] # Eventos pendentes relacionados ao job
    index = 0

    start = inf
    end = 0

    # Inicializa o evento
    def __init__(self, index, name, initTime, duration, mem):
        self.index = index
        self.duration = duration
        self.mem = mem
        self.initTime = initTime
        self.name = name

    # Cria os eventos iniciais
    def spawnEvents(self, inicDuration, mallocDuration, mfreeDuration, jentDuration):
        self.events = []
        event = Event("INIC", inicDuration, 0, self)
        self.events.append(event)
        event = Event("MALLOC", mallocDuration, self.mem, self)
        self.events.append(event)
        event = Event("EXEC", self.duration, 0, self)
        self.events.append(event)
        event = Event("MFREE", mfreeDuration, 0, self)
        self.events.append(event)
        event = Event("JEND", jentDuration, 0, self)
        self.events.append(event)

    def __str__(self):
        return str(self.name)