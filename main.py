import os
# Chamar arquivos com as implementações

while(True):
    print("Selecione a opção de teste:")
    print("1 - Alocação Simples Contígua")
    print("2 - Alocação Particionada Simples")
    print("3 - Sair") 
    selection = input()
    if (selection == "1"):
        os.system("SCA.py")
    if (selection == "2"):
        os.system("SPA.py")
    if (selection == "3"):
        break