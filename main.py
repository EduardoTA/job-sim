from event import Event
from job import Job

t = 0 # Tempo atual de simulação
flag_Over = False # Flag que indica fim de execução

N = 10000 # Tamanho da memória
memory = [None]*N # Memória física

# Job 1
job1 = Job("Job1", 77, 397, 1000)
job2 = Job("Job2", 373, 73, 1000)

jobs = []

jobs.append(job1)
jobs.append(job2)

min_job = 0
# While que itera toda iteração de simulação
while(t <= 100):
    # Escolhe o job com menor tempo de inicilização
    min_job = jobs[0]
    for job in jobs:
      if job.initTime < min_job.initTime:
        min_job = job

    
    
    t += 1

print(min_job.name)