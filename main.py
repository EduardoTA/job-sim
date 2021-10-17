import os
from SCA import SCA
from SPA import SPA
from event import Event
from job import Job

def getJobMix():
    jobs = [] # Lista de jobs
    f = open("jobs.txt", "r")
    nJobs = int(f.readline())
    for i in range(nJobs):
        line = (f.readline().split())
        print((line))
        jobs.append(Job(line[0], int(line[1]), int(line[2]), int(line[3])))
    return jobs

# Chamar arquivos com as implementações

while(True):
    print("Selecione a opção de teste:")
    print("1 - Alocação Simples Contígua")
    print("2 - Alocação Particionada Simples")
    print("3 - Sair") 
    selection = input()
    if (selection == "1"):
        SCA(getJobMix())
    if (selection == "2"):
        SCA(getJobMix()))
    if (selection == "3"):
        break