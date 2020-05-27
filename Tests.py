import numpy as np
import os

epsilons = [0.1,0.2]
gammas = [0.9,0.8]
alphas = [0.1]
vaMaxs = [60,70,80]
program = 'C:\Users\NIR\PycharmProjects\FinalProject_shir\Game_Qlearning.py'
interpreter = 'C:\Users\NIR\Anaconda3\envs\shir_proj\python.exe '
filename = 'results.csv'
# for alpha in alphas:
for v in vaMaxs:
    # for gamma in gammas:

        # for epsilon in epsilons:

            # command =  interpreter + program+' --alpha {} --gamma {} --epsilon {}'.format(alpha,gamma,epsilon)
            command = interpreter + program + ' --VaMax {} --results_file {}'.format(v,filename)
            os.system(command)