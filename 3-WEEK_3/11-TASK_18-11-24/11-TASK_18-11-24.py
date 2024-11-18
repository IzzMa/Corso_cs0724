import matplotlib.pyplot as plt
import os

#colori per processo
colors = {
    'P1': 'yellow', 
    'P2': 'blue', 
    'P3': 'purple', 
    'P4': 'orange'
}
wait_color = 'green'  #colore attesa

fig, axs = plt.subplots(3, 1, figsize=(12, 12))
fig.suptitle("Esempio di Grafici di Scheduling della CPU - MonoTasking, TimeSharing e MultiTasking")

#MonoTasking
axs[0].barh(['P1', 'P2', 'P3', 'P4'], [3, 2, 1, 4], left=[0, 7, 10, 11], 
            color=[colors['P1'], colors['P2'], colors['P3'], colors['P4']])
axs[0].barh(['P1', 'P2', 'P3', 'P4'], [2, 1, 0, 1], left=[3, 5, 7, 10], color=wait_color)
axs[0].set_title("MonoTasking")
axs[0].set_xlabel("Tempo (t)")
axs[0].set_ylabel("Processo")
axs[0].set_xlim(0, 15)

#TimeSharing (Quantum di 1s)
axs[1].barh(['P1', 'P2', 'P3', 'P4', 'P1', 'P2', 'P3', 'P4', 'P1', 'P2'], 
            [1] * 10, 
            left=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 
            color=[colors['P1'], colors['P2'], colors['P3'], colors['P4'], 
                   colors['P1'], colors['P2'], colors['P3'], colors['P4'], 
                   colors['P1'], colors['P2']])
axs[1].set_title("TimeSharing (Quantum = 1s)")
axs[1].set_xlabel("Tempo (t)")
axs[1].set_ylabel("Processo")
axs[1].set_xlim(0, 15)

#MultiTasking (Quantum di 2s per esempio)
axs[2].barh(['P1', 'P2', 'P3', 'P4', 'P1', 'P2', 'P3', 'P4', 'P1', 'P2'], 
            [2] * 10, 
            left=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18], 
            color=[colors['P1'], colors['P2'], colors['P3'], colors['P4'], 
                   colors['P1'], colors['P2'], colors['P3'], colors['P4'], 
                   colors['P1'], colors['P2']])
axs[2].barh(['P1', 'P2', 'P3', 'P4', 'P1', 'P2', 'P3', 'P4', 'P1', 'P2'], 
            [1] * 10, 
            left=[1, 3, 5, 7, 9, 11, 13, 15, 17, 19], color=wait_color)
axs[2].set_title("MultiTasking (Quantum = 2s)")
axs[2].set_xlabel("Tempo (t)")
axs[2].set_ylabel("Processo")
axs[2].set_xlim(0, 20)

plt.tight_layout(rect=[0, 0, 0.85, 0.96])

#aggiunge la legenda
fig.legend(['Tempo utilizzo CPU', 'Tempo attesa eventi esterni', 'P1 (yellow)', 'P2 (blue)', 'P3 (purple)', 'P4 (orange)'], 
           loc="center left", bbox_to_anchor=(1, 0.5), borderaxespad=0.2)

#salva l-immagine dei grafici nella directory del file .py
current_directory = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_directory, "cpu_scheduling_plot.png")
plt.savefig(file_path)

#Output a schermo
plt.show()
