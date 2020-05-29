import cellular
import time
import sys
import random
import BallSimulation
import csv
import numpy as np
import LearningRobot
import HumanRobot
import pandas as pd
import matplotlib.pyplot as plt
import argparse

GAMMA_ITERATION = 100000
EPSILON_ITERATION = 300000
ALPHA_ITERATION = 100000
# For debugging of csv2game. given a state returns the line in the csv file
def state2line(state):
    lineNumber = state[0]+6*state[1]+6*9*state[2]+6*9*4*state[3]+6*9*4*8*state[4]
    return lineNumber

    # # This section handle the cvs file for submission
def trainTheRobot(pretraining, isMesirot):
    for i in range(pretraining+1): # fast learning before the board is display
        # print the success percentage of the robot (per 10000 round )
        if i % 100000 == 0 and i > 0:
            print("round number: " + str(i))
            LearningRobot.ai.gamma = np.amin([LearningRobot.ai.gamma*1.05,0.9])
            LearningRobot.ai.alpha = np.amin([LearningRobot.ai.gamma*0.95,0.05])
            if i% 200000 ==0 and i > 0:
                LearningRobot.ai.epsilon*=0.5
                print('epsilon = {}'.format(LearningRobot.ai.epsilon))
            print('gamma = {}'.format(LearningRobot.ai.gamma))
            print('alpha = {}'.format(LearningRobot.ai.alpha))


            if isMesirot:
                # print (cellular.Agent.mesirotScore)
                # maxMesirotAvg = np.average(cellular.Agent.mesirotScore)
                # print ('max Mesirot Avg old is: '+ str(maxMesirotAvg))
                # print ('array length: ' +str(len(cellular.Agent.mesirotScore)))
                # cellular.Agent.mesirotScore =[]
                mesirot_avg = np.average(world.mesirotScore+[world.getNumMesirot()])
                print ('Mesirot Avg is: ' + str(mesirot_avg))
                print ('array length: ' + str(len(world.mesirotScore)))
                world.mesirotScore = []

            else:
                print ('Good score: ' + str(LearningRobot.good_score) + ". Bad score: " + str(
                    LearningRobot.bad_score) + ". No score: " + str(LearningRobot.no_score))
                print ('Good score percent: ' + str(100 * LearningRobot.good_score / (LearningRobot.no_score + LearningRobot.bad_score + LearningRobot.good_score)))
                LearningRobot.good_score = 0
                LearningRobot.bad_score = 0
                LearningRobot.no_score = 0
        world.update(isMesirot)
        # diaplayGUI()
        # time.sleep(3)


def calcTheMadad(isMesirot):
    while len(cellular.Agent.mesirotScore) < 1000: #create an array with 1000 minigames scores
        world.update(isMesirot)
    print (cellular.Agent.mesirotScore)
    data = pd.Series(cellular.Agent.mesirotScore)
    print(data.describe()) #show stats an that data
    bin_values = np.arange(start=0, stop=200, step=1)
    data.plot(kind='hist', bins=bin_values)  # `bins` defines the start and end points of bins
    plt.show()
    print ('close the plot popup to continue')

def exportToCsv():
    filename = "C:/Users/roni.ravina/Desktop/wb.csv"
    with open(filename, 'wb') as csvfile:
        solwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        row = ['0','0','0','0','0','0']
        jj=0  # runs on all possible states
        if isTileCoding:
            states = np.array(np.meshgrid([0, 1, 2, 3], [0, 1], [0, 1, 2, 3], [0, 1], [0, 1, 2, 3], [0, 1], [0, 1, 2, 3],[0, 1, 2, 3, 4, 5, 6, 7],[0, 1, 2])).T.reshape(-1, 9)
            while jj <49152:
                state = states[jj]
                for i in range(len(row)):
                    row[i] = str(LearningRobot.ai.getQValue(state=([[state[0], state[1]], [state[2], state[3]], [state[4], state[5]]], state[6], state[7], state[8]), action=i))
                solwriter.writerow(row)
                jj += 1

        else:
            states = np.array(np.meshgrid([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3], [0, 1, 2, 3, 4, 5, 6, 7],[0, 1, 2])).T.reshape(-1, 5)
            while jj < 5148:
                state = states[jj]
                for i in range(len(row)):
                    row[i] = str(LearningRobot.ai.getQValue(state= ((state[0], state[1]), state[2], state[3], state[4]), action= i))
                solwriter.writerow(row)
                jj +=1
    csvfile.close()

def diaplayGUI():
    world.display.activate(size=40)
    world.display.delay = 0

class Cell(cellular.Cell):
    def __init__(self):
        self.wall = False
        self.robot = False

    def colour(self):
        if self.wall:
            return 'black'
        elif self.robot:
            return 'red'
        else:
            return 'white'

    def load(self, data):
        global startCell
        if data == 'R':
            startCell = self
        if data == '.':
            self.wall = True
            

if __name__== '__main__':
# Initiate the parameters and the objects of the game
# Rewards, World, ball, robots
# Then, adding the robots and the ball into the world


    parser = argparse.ArgumentParser()
    parser.add_argument('--alpha', type=float,default = 0.2,
                    help='learning rate')
    parser.add_argument('--gamma', type=float,default = 0.5,
                    help='discount rate')
    parser.add_argument('--dbg', type = bool, default= False)
    parser.add_argument('--tile_coding', type=bool, default=True)
    parser.add_argument('--is_mesirot', type=bool, default=True)
    parser.add_argument('--epsilon', type=float, default= 0.25)
    parser.add_argument('--VaMax', type=float, default=80,
                    help='Maximal Angular Velocity')
    parser.add_argument('--damp_acc', type=float, default= -0.075,
                    help='damp accelaration')
    parser.add_argument('--damp_wall', type=float, default= 0.8,
                    help='damp wall hit')
    parser.add_argument('--results_file', type=str, default= 'results.csv',
                    help='file to save results')


    args = parser.parse_args()
    alpha = args.alpha
    epsilon = args.epsilon
    gamma = args.gamma
    results_file = args.results_file

    isTileCoding = True
    isMesirot= True
    x0=1000000
    x1= 1200000
    x2= 2000000
    gamma = 0.5
    if isMesirot:
        world = cellular.World(Cell, directions=4, filename='soccerField.txt')
        ball = BallSimulation.Ball(world, 1, 18, 9)
        world.addAgent(ball)
        HumanRobot = HumanRobot.HumanRobot(ball)
        LearningRobot = LearningRobot.LearningRobot(ball, isTileCoding, HumanRobot,\
                                                    alpha = alpha,gamma = gamma, epsilon = epsilon)
        world.addAgent(LearningRobot)
        world.addAgent(HumanRobot)
        # diaplayGUI()
        # time.sleep(1)
        trainTheRobot(x1, isMesirot)
        print ('I am still learning mesirot.')
        # calcTheMadad(isMesirot)
        trainTheRobot(x2-x1, isMesirot)
        print ('I am trained now in mesirot.')
        # exportToCsv()
    else:
        world = cellular.World(Cell, directions=4, filename='soccerField.txt')
        ball = BallSimulation.Ball(world, 1, 18, 9)
        world.addAgent(ball)
        HumanRobot = HumanRobot.HumanRobot(ball)
        LearningRobot = LearningRobot.LearningRobot(ball, isTileCoding,HumanRobot)
        world.addAgent(LearningRobot)
        #diaplayGUI()
        trainTheRobot(x0, isMesirot)
        print ('I am trained now in kicking.')
        isMesirot =True
        world.addAgent(HumanRobot)
        print ('now lets play mesirot')
        trainTheRobot(x1-x0, isMesirot)
        print ('I am still learning mesirot.')
        # calcTheMadad(isMesirot)
        trainTheRobot(x2-x1, isMesirot)
        print('I am trained now in kicking and mesirot')
    # calcTheMadad(isMesirot)
        # exportToCsv()

# Activate the game
    while 1:
        diaplayGUI()
        world.update(isMesirot)
        time.sleep(1)
