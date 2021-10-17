import os
from SCA import SCA
from SPA import SPA
from event import Event
from job import Job

def getJobMix(file):
    jobs = [] # Lista de jobs
    f = open(str(file), "r")
    nJobs = int(f.readline())
    print("\nJobs carregados com sucesso:")
    for i in range(nJobs):
        line = (f.readline().split())
        print((line))
        jobs.append(Job(i+1, line[0], int(line[1]), int(line[2]), int(line[3])))

        jobs.sort(key=lambda x: x.initTime)
    print("\n")
    return jobs

# Chamar arquivos com as implementações

while(True):
    N = input('Tamanho da memória = ')
    multi = input('Multiprogramação máxima (somente para a alocação particionada simples) = ')
    try:
        N = int(N)
        multi = int(multi)
        if N <= 0 or multi <= 0:
            raise Exception
    except:
        print("Digite números inteiros estritamente positivos!")
        break
    
    jobMix = input("Caminho do arquivo com o job mix: ")
    try:
        jobMix = getJobMix(jobMix)
    except:
        print("Arquivo inválido ou inexistente")
        break
    

    print("Selecione a opção de teste:")
    print("1 - Alocação Simples Contígua")
    print("2 - Alocação Particionada Simples")
    print("3 - Sair") 
    selection = input("> ")
    if (selection == "1"):
        SCA(jobMix, N)
    elif (selection == "2"):
        SPA(jobMix, N, multi)
    elif (selection == "3"):
        break
    print('\n\nNova Execução:\n')