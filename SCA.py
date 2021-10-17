from event import Event
from job import Job
import matplotlib.pyplot as plt


# Implementação da Alocação Simples Contígua
def SCA(jobs, N):
    t = 0 # Tempo atual de simulação
    tant = 0
    flagOver = False # Flag que indica fim de execução
    flagEndEvent = False # Flag que indica que o evento END foi pushed
    flagBusy = False # Flag verdadeira se o processador está ocupado

    memory = [0]*N # Memória física

    mallocDuration = 0 # Duração do evento de alocação de memória
    inicDuration = 0 # Duração do evento de inicialização de job
    mfreeDuration = 0 # Duração do evento de liberação de memória
    jentDuration = 0 # Duração de finalizaçao de job

    min_job = 0 # Job com menor tempo de inicialização

    curEvent = 0 # Evento que está atualmente sendo executado
    
    # Métricas
    timeMemQueue = 0 # Tempo de espera em fila de espera

    memUsage = 0 # Taxa média de ocupação de memória atual
    memUsageant = 0 # Taxa média de ocupação de memória anterior

    memSucRate = 1 # Taxa média de atendimento às solicitações de alocação
    memSucRateant = 1 # Taxa média de atendimento às solicitações de alocação anterior
    nSucRate = 0 # Número de solicitações de alocação de memória

    tExec = 0 # Tempo que o processador está em EXEC

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
                    emptyStart = memory.index(0)
                    for i in range(emptyStart, jobs[0].mem+emptyStart):
                        memory[i] = jobs[0].index  
                if curEventType == "MFREE":
                    emptyStart = memory.index(jobs[0].index)
                    for i in range(emptyStart, jobs[0].mem+emptyStart):
                        memory[i] = 0        
                if jobs[0].events[0].isOver():
                    jobs[0].events.pop(0)
                else:
                    jobs[0].events[0].iterate()
                    t += 1

                if t != tant and jobs[0].events[0].eventType == "EXEC":
                    tExec += 1
            else:
                jobs.pop(0)
        else:
            flagOver = True
        
        if tant != t:
            memUsageant = memUsage
            memUsage = memUsageant + ((sum(x is not None for x in memory)/len(memory)) - memUsageant)/t

    
    print('\njobs[]:')
    for job in jobs:   
        print(job) 

    print('\nMemória:')
    print(memory)

    print('\n----#Métricas#----')
    print(f'Tempo de espera em fila de memória = {timeMemQueue}')
    print(f'Taxa de ocupação de memória = {memUsage}')
    print(f'Taxa de atendimento às solicitações de alocação = {memSucRate}')
    idle = 1-tExec/t
    print(f'Taxa de ociosidade do processador = {idle}')
    print(f'Tempo de execução = {t}')
    print(f'Taxa de multiprogramação = 1')

    plt.imshow(memory)