import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def memPlot(jobs, memoryAcc):
    plt.figure(figsize=(20,10))

    plt.imshow([list(i) for i in zip(*memoryAcc)], aspect='auto', origin='lower', interpolation='none', extent=[0, len(memoryAcc), 0, len(memoryAcc[0])])
    cmap = plt.cm.get_cmap('viridis')
    legends = []
    for job in jobs:
        legends.append(mpatches.Patch(color=cmap(job.index/(len(jobs))), label=f"""{job.name} (init={job.initTime}, start={job.start}, end={job.end}, mem={job.mem})"""))
    plt.grid()
    plt.legend(handles=legends)
    plt.xlabel('tempo')
    plt.ylabel('endereço')
    plt.show()
