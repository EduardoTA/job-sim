from event import Event
from job import Job

# Implementação da Alocação Simples Contígua
t = 0 # Tempo atual de simulação
flagOver = False # Flag que indica fim de execução
flagEndEvent = False # Flag que indica que o evento END foi pushed

N = 10000 # Tamanho da memória
memory = [None]*N # Memória física

job1 = Job("Job1", 77, 397, 1000) # Job 1
job2 = Job("Job2", 373, 73, 1000) # Job 2

jobs = [] # Lista de jobs
jobs.append(job1)
jobs.append(job2)

eventsFIFO = []

mallocDuration = 0 # Duração do evento de alocação de memória
inicDuration = 0 # Duração do evento de inicialização de job
jentDuration = 0 # Duração de finalizaçao de job

min_job = 0
# While que itera toda iteração de simulação
while(flagOver == False):

    if len(jobs) > 0:
        # Escolhe o job com menor tempo de inicialização
        min_job = jobs[0]
        for job in jobs:
            if job.initTime < min_job.initTime:
                min_job = job
            if min_job.initTime == t:
                jobs.remove(min_job)
                event = Event("INIC", inicDuration, None, min_job)
                eventsFIFO.append(event)
                event = Event("MALLOC", mallocDuration, min_job.mem, min_job)
                eventsFIFO.append(event)
                event = Event("EXEC", min_job.duration, None, min_job)
                eventsFIFO.append(event)
                event = Event("JEND", jentDuration, None, min_job)
                eventsFIFO.append(event)
    else:
        if flagEndEvent == False:
            event = Event("END", None, None, None)
            eventsFIFO.append(event)
            flagEndEvent = True
            flagOver = True # Para testes
    t += 1


for event in eventsFIFO:
    print(event)