from event import Event
from job import Job

# Implementação da Alocação Simples Contígua
t = 0 # Tempo atual de simulação
flagOver = False # Flag que indica fim de execução
flagEndEvent = False # Flag que indica que o evento END foi pushed
flagBusy = False # Flag verdadeira se o processador está ocupado

N = 100 # Tamanho da memória
memory = [None]*N # Memória física

job1 = Job("Job1", 77, 397, 90) # Job 1
job2 = Job("Job2", 373, 73, 5) # Job 2
job3 = Job("Job3", 77,  88, 20) # Job 2

jobs = [] # Lista de jobs
jobs.append(job1)
jobs.append(job2)
jobs.append(job3)

eventsFIFO = []

mallocDuration = 0 # Duração do evento de alocação de memória
inicDuration = 0 # Duração do evento de inicialização de job
mfreeDuration = 0 # Duração do evento de liberação de memória
jentDuration = 0 # Duração de finalizaçao de job

min_job = 0 # Job com menor tempo de inicialização

curEvent = None # Evento que está atualmente sendo executado

# While que itera toda iteração de simulação
while(flagOver == False):
    # Job handler
    if len(jobs) > 0:
        # Escolhe o job com menor tempo de inicialização
        min_job = jobs[0]
        for job in jobs:
            if job.initTime <= min_job.initTime:
                min_job = job
            if min_job.initTime == t:
                jobs.remove(min_job)
                event = Event("INIC", inicDuration, 0, min_job)
                eventsFIFO.append(event)
                event = Event("MALLOC", mallocDuration, min_job.mem, min_job)
                eventsFIFO.append(event)
                event = Event("EXEC", min_job.duration, 0, min_job)
                eventsFIFO.append(event)
                event = Event("MFREE", mfreeDuration, 0, min_job)
                eventsFIFO.append(event)
                event = Event("JEND", jentDuration, 0, min_job)
                eventsFIFO.append(event)
    else:
        if flagEndEvent == False:
            event = Event("END", 0, 0, 0)
            eventsFIFO.append(event)
            flagEndEvent = True
    
    # Event handler
    
    if len(eventsFIFO) > 0 and flagBusy == False: # Se a fila de eventos tiver algum evento e o processador não está ocupado
        curEvent = eventsFIFO.pop(0) # Dequeue de um evento da fila
        if curEvent.eventType == "MALLOC": # Se for evento de alocação
          startPosition = 0
          for i in range(len(memory)): # Encontra espaço livre
            if (memory[i] != None):
              startPosition = i+1
          for j in range(startPosition,curEvent.value + startPosition):
            memory[j] = curEvent.job.name # Preenche memória
        if curEvent.eventType == "MFREE": # Se for evento de liberação 
          for j in range(startPosition,curEvent.value + firstFree):
            memory[j] = None # Libera memória
        if curEvent.eventType == "END": # Se for evento de finalização
            print("Evento "+curEvent.__str__()+" terminado em t = "+str(t))
            flagOver = True # O processador deve finalizar atividades
        if curEvent.isOver(): # Se o evento que entrou já começar terminado
            print("Evento "+curEvent.__str__()+" terminado em t = "+str(t))
        else:
            flagBusy = True
    
    if flagBusy == True:
        if curEvent.isOver():
            #print("Evento "+curEvent.__str__()+" terminado em t = "+str(t))
            print(memory)
            flagBusy = False
        else:
            t += 1
            curEvent.iterate()
    if len(eventsFIFO) <= 0:
        t += 1
    
        
        

    


for event in eventsFIFO:
    print(event)