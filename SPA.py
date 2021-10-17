from event import Event
from job import Job
from memPlot import memPlot


def SPA(jobsFIFO, N, multi):
    def checkAllJobsExec(jobs):
        flag = True
        for job in jobs:
            if len(job.events) == 0 or job.events[0].eventType != "EXEC":
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
    tant = 0 # Tempo de simulação na iteração anterior do while externo

    flagOver = False # Flag que indica fim de execução

    memory = [None]*N # Memória física

    mallocDuration = 0 # Duração do evento de alocação de memória
    inicDuration = 0 # Duração do evento de inicialização de job
    mfreeDuration = 0 # Duração do evento de liberação de memória
    jentDuration = 0 # Duração de finalizaçao de job

    for job in jobsFIFO:
        job.spawnEvents(inicDuration, mallocDuration, mfreeDuration, jentDuration) # Cria os eventos do job

    # Ordenar fila
    jobsFIFO.sort(key=lambda x: x.initTime)

    jobFetchFIFO = [] # Fila com os jobs cujo tempo de início passou

    jobExecFIFO = [] # Fila com os jobs alocados no momento (sendo executados)
    jobExecFIFOIndex = 0 # Elemento da fila que está sendo executado no momento

    turnoverTime = 20 # Número de ciclos de clock para trocar de job

    # Métricas
    timeMemQueue = 0 # Tempo de espera em fila de espera

    memUsage = 0 # Taxa média de ocupação de memória atual
    memUsageant = 0 # Taxa média de ocupação de memória anterior

    memSucRate = 1 # Taxa média de atendimento às solicitações de alocação
    memSucRateant = 1 # Taxa média de atendimento às solicitações de alocação anterior
    nSucRate = 0 # Número de solicitações de alocação de memória

    tExec = 0 # Tempo que o processador está em EXEC

    multitask = 1 # Taxa média de multiprogramação atual
    multitaskant = 1 # Taxa média de multiprogramação anterior

    # While que itera toda iteração de simulação
    while(flagOver == False):
        # Job fetcher
        if len(jobsFIFO) > 0:
            while(len(jobsFIFO) > 0 and jobsFIFO[0].initTime == t):
                jobFetchFIFO.append(jobsFIFO[0])
                jobsFIFO.pop(0)

        emptyStart = 0 # Posição de início de espaço vazio

        # Job issuer
        if len(jobFetchFIFO) > 0 and len(jobExecFIFO) < multi:
            if len(jobExecFIFO) == 0:
                jobExecFIFO.append(jobFetchFIFO[0])
                jobFetchFIFO.pop(0)
            else:
                if checkAllJobsExec(jobExecFIFO):
                    emptyStart = firstFit(jobFetchFIFO[0].mem, memory)
                    if emptyStart > -1:
                        jobExecFIFO.append(jobFetchFIFO[0])
                        jobFetchFIFO.pop(0)
                    else:
                        nSucRate += 1
                        memSucRateant = memSucRate
                        memSucRate = memSucRateant + (1 - memSucRateant)/nSucRate

                        timeMemQueue += t-tant
                else:
                    timeMemQueue += t-tant

        # Cálculo da taxa de multiprogramação (só leva em conta momentos em que existem jobs na memória)
        if tant < t and len(jobExecFIFO) > 0 and checkAllJobsExec(jobExecFIFO):
            multitaskant = multitask
            multitask = multitaskant + (len(jobExecFIFO) - multitaskant)/t

        # Job scheduler
        if len(jobExecFIFO) > 0 and (t % turnoverTime == 0): 
            # Index do job a ser executado no próximo turnover
            if jobExecFIFOIndex >= len(jobExecFIFO)-1:
                jobExecFIFOIndex = 0
            else:
                jobExecFIFOIndex += 1

        tant = t

        # Event handler
        if len(jobExecFIFO) > 0 or len(jobFetchFIFO) > 0 or len(jobsFIFO) > 0:
            if len(jobExecFIFO) > 0:
                if len(jobExecFIFO[jobExecFIFOIndex].events) > 0:
                    # Tipo de evento sendo executado no momento
                    curEventType = jobExecFIFO[jobExecFIFOIndex].events[0].eventType
                    if curEventType == "MALLOC":
                        emptyStart = memory.index(None)
                        for i in range(emptyStart, jobExecFIFO[jobExecFIFOIndex].mem+emptyStart):
                            memory[i] = jobExecFIFO[jobExecFIFOIndex].name  
                    if curEventType == "MFREE":
                        emptyStart = memory.index(jobExecFIFO[jobExecFIFOIndex].name)
                        for i in range(emptyStart, jobExecFIFO[jobExecFIFOIndex].mem+emptyStart):
                            memory[i] = None        
                    if jobExecFIFO[jobExecFIFOIndex].events[0].isOver():
                        jobExecFIFO[jobExecFIFOIndex].events.pop(0)
                    else:
                        jobExecFIFO[jobExecFIFOIndex].events[0].iterate()
                        t += 1

                    if t != tant and jobExecFIFO[jobExecFIFOIndex].events[0].eventType == "EXEC":
                        tExec += 1
                else:
                    oldIndex = jobExecFIFOIndex
                    if jobExecFIFOIndex == len(jobExecFIFO)-1:
                        jobExecFIFOIndex = 0
                    else:
                        jobExecFIFOIndex += 1
                    jobExecFIFO.pop(oldIndex)
            else:
                t += 1  
        else:
            flagOver = True
        
        if tant != t:
            memUsageant = memUsage
            memUsage = memUsageant + ((sum(x is not None for x in memory)/len(memory)) - memUsageant)/t


    print('\njobsFIFO[]:')
    for job in jobsFIFO:   
        print(job) 

    print('\njobFetchFIFO[]:')
    for job in jobFetchFIFO:   
        print(job) 

    print('\njobExecFIFO[]:')
    for job in jobExecFIFO:   
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
    print(f'Taxa de multiprogramação = {multitask}')