import numpy as np
import os

epsilons = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
gammas = [0.5, 0.6, 0.7, 0.8, 0.9]
alphas = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
VaMaxs = [30, 35, 40]
program = 'C:\Users\Shir.Sc\PycharmProjects\FinalProject\Game_Qlearning.py'
interpreter = 'C:\Users\Shir.Sc\\anaconda2\python.exe '
filename = 'results.csv'
for alpha in alphas:
# for v in VaMaxs:
# for gamma in gammas:

# for epsilon in epsilons:

            # command =  interpreter + program+' --alpha {} --gamma {} --epsilon {}'.format(alpha,gamma,epsilon)
            command = interpreter + program + ' --alpha {} --results_file {}'.format(alpha,filename)
            os.system(command)