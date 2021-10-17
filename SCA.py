from event import Event
from job import Job

# Implementação da Alocação Simples Contígua
def SCA(jobs):
    t = 0 # Tempo atual de simulação
    tant = 0
    flagOver = False # Flag que indica fim de execução
    flagEndEvent = False # Flag que indica que o evento END foi pushed
    flagBusy = False # Flag verdadeira se o processador está ocupado

    N = 100 # Tamanho da memória
    memory = [None]*N # Memória física

    mallocDuration = 0 # Duração do evento de alocação de memória
    inicDuration = 0 # Duração do evento de inicialização de job
    mfreeDuration = 0 # Duração do evento de liberação de memória
    jentDuration = 0 # Duração de finalizaçao de job

    min_job = 0 # Job com menor tempo de inicialização

    curEvent = None # Evento que está atualmente sendo executado

    tExec = 0

    # Job handler
    for job in jobs:
        job.spawnEvents(inicDuration, mallocDuration, mfreeDuration, jentDuration) # Cria os eventos do job
        
    # While que itera toda iteração de simulação
    while(flagOver == False):

        tant = t
        # Event handler
        if len(jobs) > 0:
            if len(jobs[0].events) > 0:
                # Tipo de evento sendo executado no momento
                curEventType = jobs[0].events[0].eventType
                if curEventType == "MALLOC":
                    emptyStart = memory.index(None)
                    for i in range(emptyStart, jobs[0].mem+emptyStart):
                        memory[i] = jobs[0].name  
                if curEventType == "MFREE":
                    emptyStart = memory.index(jobs[0].name)
                    for i in range(emptyStart, jobs[0].mem+emptyStart):
                        memory[i] = None        
                if jobs[0].events[0].isOver():
                    jobs[0].events.pop(0)
                else:
                    jobs[0].events[0].iterate()
                    t += 1

                if t != tant and jobs[0].events[0].eventType == "EXEC":
                    tExec += 1
            else:
                t += 1
                jobs.pop(0)
        else:
            flagOver = True
