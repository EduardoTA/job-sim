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
    job = 0

    # Inicializa o evento
    def __init__(self, eventType, duration, value, job):
        self.eventType = eventType
        self.duration = duration
        self.elapsed = 0
        self.value = value
        self.job = job

    # Realiza uma iteração de relógio no evento
    def iterate(self):
        self.elapsed += 1
    
    # Verifica se o evento acabou
    def isOver(self):
        if self.elapsed >= self.duration:
            return True
        else:
            return False
    
    def __str__(self):
        return str("Job name: "+self.job.__str__()+", type: "+self.eventType+", duration: "+str(self.duration)+", elapsed: "+str(self.elapsed)+", value: "+str(self.value))
