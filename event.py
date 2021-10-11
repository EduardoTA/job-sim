# Esta classe representa um evento
# type: tipo do evento de um job
# tipos:
# Chegada de job, Fim de job
# Requisição de memória, liberaçào de memória
# Encerramento
#
# duration: duração do evento
# elapsed: tempo decorrido de execução
# value: se for evento de alocação de memória, esse é o valor alocado

class Event:
    eventType = ""
    duration = 0
    elapsed = 0
    value = 0


    # Inicializa o evento
    def __init__(self, eventType, duration, value):
        self.eventType = eventType
        self.duration = duration
        self.elapsed = 0
        self.value = value
    
    # Realiza uma iteração de relógio no evento
    def iterate(self):
        self.elapsed += 1
    
    # Verifica se o evento acabou
    def isOver(self):
        if self.elapsed >= self.duration:
            return True
        else:
            return False
