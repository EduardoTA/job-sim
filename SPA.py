from event import Event
from job import Job

# Implementação da Alocação Particionada Simples
t = 0 # Tempo atual de simulação
flagOver = False # Flag que indica fim de execução
flagEndEvent = False # Flag que indica que o evento END foi pushed
flagBusy = False # Flag verdadeira se o processador está ocupado

N = 100 # Tamanho da memória
memory = [None]*N # Memória física

job1 = Job("Job1", 77, 397, 90) # Job 1
job2 = Job("Job2", 373, 73, 5) # Job 2
job3 = Job("Job3", 77,  88, 20) # Job 2

jobsFIFO = [] # Fila de jobs que não estão sendo executados
jobsFIFO.append(job1)
jobsFIFO.append(job2)
jobsFIFO.append(job3)

# Ordenar fila
jobsFIFO.sort(key=lambda x: x.initTime)

# Fila de eventos
eventsFIFO = []

mallocDuration = 0 # Duração do evento de alocação de memória
inicDuration = 0 # Duração do evento de inicialização de job
mfreeDuration = 0 # Duração do evento de liberação de memória
jentDuration = 0 # Duração de finalizaçao de job

curEvent = None # Evento que está atualmente sendo executado

multi = 2 # Grau máximo de multiprogramação

jobFetchFIFO = [] # Fila com os jobs na fila para execução

jobExecFIFO = [] # Fila com os jobs sendo executados no momento
jobExecFIFOIndex = 0 # Elemento da fila que está sendo executado no momento

turnoverTime = 20 # Número de ciclos de clock para trocar de job

# While que itera toda iteração de simulação
while(flagOver == False and t<100021):
    # Job fetcher
    if len(jobsFIFO) > 0:
        while(len(jobsFIFO) > 0 and jobsFIFO[0].initTime == t):
            jobFetchFIFO.append(jobsFIFO[0])
            jobsFIFO.pop(0)

    # Job issuer
    if len(jobFetchFIFO) > 0 and len(jobExecFIFO) < multi:
        jobExecFIFO.append(jobFetchFIFO[0])
        jobFetchFIFO.pop(0)
    
    # Job scheduler
    if len(jobExecFIFO) > 0 and (flagBusy == False or t % multi == 0):
        if len(jobExecFIFO) == 1:
            flagBusy == True

            eventsFIFO = [] # Limpar fila de eventos
            event = Event("INIC", inicDuration, 0, jobExecFIFO[0])
            eventsFIFO.append(event)
            event = Event("MALLOC", mallocDuration, jobExecFIFO[0].mem, jobExecFIFO[0])
            eventsFIFO.append(event)
            event = Event("EXEC", jobExecFIFO[0].duration, 0, jobExecFIFO[0])
            eventsFIFO.append(event)
            event = Event("MFREE", mfreeDuration, 0, jobExecFIFO[0])
            eventsFIFO.append(event)
            event = Event("JEND", jentDuration, 0, jobExecFIFO[0])
            eventsFIFO.append(event)
        else:
            flagBusy == True
            # Index do job a ser executado no próximo turnover
            if jobExecFIFOIndex == len(jobExecFIFO)-1:
                jobExecFIFOIndex = 0
            else:
                jobExecFIFOIndex += 1

            eventsFIFO = [] # Limpar fila de eventos
            event = Event("INIC", inicDuration, 0, jobExecFIFO[jobExecFIFOIndex])
            eventsFIFO.append(event)
            event = Event("MALLOC", mallocDuration, jobExecFIFO[jobExecFIFOIndex].mem, jobExecFIFO[jobExecFIFOIndex])
            eventsFIFO.append(event)
            event = Event("EXEC", jobExecFIFO[jobExecFIFOIndex].duration, 0, jobExecFIFO[jobExecFIFOIndex])
            eventsFIFO.append(event)
            event = Event("MFREE", mfreeDuration, 0, jobExecFIFO[jobExecFIFOIndex])
            eventsFIFO.append(event)
            event = Event("JEND", jentDuration, 0, jobExecFIFO[jobExecFIFOIndex])
            eventsFIFO.append(event)


    t += 1

print('\njobExecFIFO[]:')
for job in jobExecFIFO:   
    print(job) 

print('\neventsFIFO[]:')
for event in eventsFIFO:   
    print(event)