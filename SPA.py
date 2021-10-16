from event import Event
from job import Job

def checkAllJobsExec(jobs):
    flag = True
    for job in jobs:
        if job.events[0].eventType != "EXEC":
            flag = False
    return flag

def firstFit(size, memory): # Retorna o índice do endereço de memória onde começa com espaço vazio com tamanho pelo menos igual a size
    emptyLen = 0 # Tamanho do espaço vazio
    emptyStart = 0 # Começo do espaço vazio
    i = 0 # Índice que vai marchando pelo vetor de memória
    flagFoundEmpty = False # Flag que indica que espaço vazio foi encontrado
    while emptyLen < size and i < len(memory):
        if memory[i] == None:
            if flagFoundEmpty == False:
                flagFoundEmpty = True
                emptyStart = i
                emptyLen = 1
            else:
                emptyLen += 1
        else:
            emptyLen = 0
            flagFoundEmpty = False
        i += 1
    if emptyLen >= size:
        return emptyStart
    else:
        return -1

# Implementação da Alocação Particionada Simples
t = 0 # Tempo atual de simulação
flagOver = False # Flag que indica fim de execução
flagEndEvent = False # Flag que indica que o evento END foi pushed
flagBusy = False # Flag verdadeira se o processador está ocupado

N = 100 # Tamanho da memória
memory = [None]*N # Memória física

mallocDuration = 0 # Duração do evento de alocação de memória
inicDuration = 0 # Duração do evento de inicialização de job
mfreeDuration = 0 # Duração do evento de liberação de memória
jentDuration = 0 # Duração de finalizaçao de job

job1 = Job("Job1", 77, 397, 90) # Job 1
job1.spawnEvents(inicDuration, mallocDuration, mfreeDuration, jentDuration) # Cria os eventos do job
job2 = Job("Job2", 373, 73, 5) # Job 2
job2.spawnEvents(inicDuration, mallocDuration, mfreeDuration, jentDuration) # Cria os eventos do job
job3 = Job("Job3", 77,  88, 20) # Job 2
job3.spawnEvents(inicDuration, mallocDuration, mfreeDuration, jentDuration) # Cria os eventos do job

jobsFIFO = [] # Fila de jobs que não estão sendo executados
jobsFIFO.append(job1)
jobsFIFO.append(job2)
jobsFIFO.append(job3)

# Ordenar fila
jobsFIFO.sort(key=lambda x: x.initTime)

# Fila de eventos
eventsFIFO = []

curEvent = None # Evento que está atualmente sendo executado

multi = 2 # Grau máximo de multiprogramação

jobFetchFIFO = [] # Fila com os jobs cujo tempo de início passou

jobExecFIFO = [] # Fila com os jobs alocados no momento (sendo executados)
jobExecFIFOIndex = 0 # Elemento da fila que está sendo executado no momento

turnoverTime = 20 # Número de ciclos de clock para trocar de job

# While que itera toda iteração de simulação
while(flagOver == False and t<10001):
    # Job fetcher
    if len(jobsFIFO) > 0:
        while(len(jobsFIFO) > 0 and jobsFIFO[0].initTime == t):
            jobFetchFIFO.append(jobsFIFO[0])
            jobsFIFO.pop(0)

    #emptyStart = 0 # Posição de início de espaço vazio
    # Job issuer
    if len(jobFetchFIFO) > 0 and len(jobExecFIFO) < multi:
        if len(jobExecFIFO) == 0:
            jobExecFIFO.append(jobFetchFIFO[0])
            jobFetchFIFO.pop(0)
        else:
            if checkAllJobsExec(jobExecFIFO):
                emptyStart = firstFit(jobFetchFIFO[0].mem, memory)
                print(emptyStart)
                if emptyStart > -1:
                    jobExecFIFO.append(jobFetchFIFO[0])
                    jobFetchFIFO.pop(0)
                else:
                    pass

    # Job scheduler
    # if len(jobExecFIFO) > 0 and (flagBusy == False or t % multi == 0):
    #     #if len(eventsFIFO) 
    #     if len(jobExecFIFO) == 1:
    #         flagBusy == True

    #         eventsFIFO = [] # Limpar fila de eventos
    #         jobExecFIFO[0].spawnEvents(inicDuration, mallocDuration, mfreeDuration, jentDuration)
    #         eventsFIFO += jobExecFIFO[0].events
    #     else:
    #         flagBusy == True
    #         eventsFIFO = [] # Limpar fila de eventos
    #         jobExecFIFO[jobExecFIFOIndex].spawnEvents(inicDuration, mallocDuration, mfreeDuration, jentDuration)
    #         eventsFIFO += jobExecFIFO[jobExecFIFOIndex].events

    #         # Index do job a ser executado no próximo turnover
    #         if jobExecFIFOIndex == len(jobExecFIFO)-1:
    #             jobExecFIFOIndex = 0
    #         else:
    #             jobExecFIFOIndex += 1

            


    t += 1

print('\njobsFIFO[]:')
for job in jobsFIFO:   
    print(job) 

print('\njobFetchFIFO[]:')
for job in jobFetchFIFO:   
    print(job) 

print('\njobExecFIFO[]:')
for job in jobExecFIFO:   
    print(job) 

print('\neventsFIFO[]:')
for event in eventsFIFO:   
    print(event)