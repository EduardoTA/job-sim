# Esta classe representa um evento
# type: tipo do evento de um job
# tipos:
# Chegada de job, Fim de job
# Requisição de memória, liberaçào de memória
# Encerramento
#
# duration: duração do evento
# elapsed: tempo decorrido de execução

class Event:
    type = ""
    duration = 0
    elapsed = 0

    # Inicializa o evento
    def __init__(self, type, duration):
        self.type = type
        self.duration = duration
        self.elapsed = 0
    
    # Realiza uma iteração de relógio no evento
    def iterate(self):
        self.elapsed -= 1
    
    # Verifica se o evento acabou
    def isOver(self):
        if self.elapsed >= self.duration:
            return True
        else:
            return False
