class Job:
  initTime = 0 # Tempo de início do job
  name = "" # Nome do job
  duration = 0 # Duração do job
  mem = 0 # Memória alocada para o job
  state = "INIC"

  # Inicializa o evento
  def __init__(self, name, initTime, duration, mem):
    self.duration = duration
    self.mem = mem
    self.initTime = initTime
    self.name = name