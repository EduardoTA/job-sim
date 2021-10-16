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

jobs = [] # Lista de jobs
jobs.append(job1)
jobs.append(job2)
jobs.append(job3)

