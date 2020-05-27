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
import csv

# For debugging of csv2game. given a state returns the line in the csv file
def state2line(state):
    lineNumber = state[0]+6*state[1]+6*9*state[2]+6*9*4*state[3]+6*9*4*8*state[4]
    return lineNumber

    # # This section handle the cvs file for submission
def trainTheRobot(pretraining, world, isMesirot):
    for i in range(pretraining): # fast learning before the board is display
        # print the success percentage of the robot (per 10000 round )
        if i % 100000 == 0 and i > 0:
            print("round number: " + str(i))
            if isMesirot:
                total_mesirot = 0
                for a in world.agents:
                    total_mesirot += a.num_kicks
                # print (cellular.Agent.mesirotScore)
                mesirot_avg = np.average(world.mesirotScore)
                print ('Mesirot Avg is: '+ str(mesirot_avg))
                print ('array length: ' +str(len(world.mesirotScore)))
                world.mesirotScore =[]
            else:
                print ('Good score: ' + str(LearningRobot.good_score) + ". Bad score: " + str(
                    LearningRobot.bad_score) + ". No score: " + str(LearningRobot.no_score))
                print ('Good score percent: ' + str(100 * LearningRobot.good_score / (LearningRobot.no_score + LearningRobot.bad_score + LearningRobot.good_score)))
                LearningRobot.good_score = 0
                LearningRobot.bad_score = 0
                LearningRobot.no_score = 0
        world.update(isMesirot)
        #time.sleep(1)

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

def calcTheMadad(isMesirot, filename = ''):
    while len(world.mesirotScore) < 1000: #create an array with 1000 minigames scores
        world.update(isMesirot)
    print (world.mesirotScore)
    data = pd.Series(world.mesirotScore)
    print(data.describe()) #show stats an that data
    bin_values = np.arange(start=0, stop=200, step=1)
    data.plot(kind='hist', bins=bin_values)  # `bins` defines the start and end points of bins
    # plt.show()
    return data.mean()

# def exportToCsv():
#     filename = "C:/Users/roni.ravina/Desktop/wb.csv"
#     with open(filename, 'wb') as csvfile:
#         solwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         row = ['0','0','0','0','0','0']
#         jj=0  # runs on all possible states
#         if isTileCoding:
#             states = np.array(np.meshgrid([0, 1, 2, 3], [0, 1], [0, 1, 2, 3], [0, 1], [0, 1, 2, 3], [0, 1], [0, 1, 2, 3],[0, 1, 2, 3, 4, 5, 6, 7],[0, 1, 2])).T.reshape(-1, 9)
#             while jj <49152:
#                 state = states[jj]
#                 for i in range(len(row)):
#                     row[i] = str(LearningRobot.ai.getQValue(state=([[state[0], state[1]], [state[2], state[3]], [state[4], state[5]]], state[6], state[7], state[8]), action=i))
#                 solwriter.writerow(row)
#                 jj += 1
#
#         else:
#             states = np.array(np.meshgrid([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3], [0, 1, 2, 3, 4, 5, 6, 7],[0, 1, 2])).T.reshape(-1, 5)
#             while jj < 5148:
#                 state = states[jj]
#                 for i in range(len(row)):
#                     row[i] = str(LearningRobot.ai.getQValue(state= ((state[0], state[1]), state[2], state[3], state[4]), action= i))
#                 solwriter.writerow(row)
#                 jj +=1
#     csvfile.close()

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

def write_to_csv(line,column_names ,filename = 'results.csv'):
    import os.path
    from os import path
    file_exists = path.isfile(results_file)
    with open(filename, 'a+') as f:
        if not file_exists:
            f.write(column_names+'\n')
        f.write(line+'\n')



if __name__== '__main__':
# Initiate the parameters and the objects of the game
# Rewards, World, ball, robots
# Then, adding the robots and the ball into the world
    parser = argparse.ArgumentParser()
    parser.add_argument('--alpha', type=float,default = 0.1,
                    help='learning rate')
    parser.add_argument('--gamma', type=float,default = 0.9,
                    help='discount rate')
    parser.add_argument('--dbg', type = bool, default= False)
    parser.add_argument('--tile_coding', type=bool, default=True)
    parser.add_argument('--is_mesirot', type=bool, default=True)
    parser.add_argument('--epsilon', type=float, default= 0.1)
    parser.add_argument('--VaMax', type=float, default=80,
                    help='Maximal Angular Velocity')
    parser.add_argument('--damp_acc', type=float, default= -0.075,
                    help='damp accelaration')
    parser.add_argument('--damp_wall', type=float, default= 0.8,
                    help='damp wall hit')
    parser.add_argument('--results_file', type=str, default= 'results.csv',
                    help='file to save results')


    args = parser.parse_args()

    results_file = args.results_file

    isMesirot = args.is_mesirot

    if isMesirot:
        world = cellular.World(Cell, directions=4, filename='soccerField.txt')
        ball = BallSimulation.Ball(world, 1, 18, 9, Va_max = args.VaMax,\
            damp_acc = args.damp_acc, damp_wall_hit = args.damp_wall)
        world.addAgent(ball)
        LearningRobot = LearningRobot.LearningRobot(ball, args.tile_coding, learning_rate = args.alpha, \
                                                    discount_rate = args.gamma, epsilon = args.epsilon)
        world.addAgent(LearningRobot)
        HumanRobot = HumanRobot.HumanRobot(ball)
        world.addAgent(HumanRobot)
        # diaplayGUI()
        trainTheRobot(101, world ,isMesirot)
        print ('I am trained now in mesirot. Validation:')
        trainTheRobot(101, world ,isMesirot)
        # exportToCsv()
    else:
        world = cellular.World(Cell, directions=4, filename='soccerField.txt')
        ball = BallSimulation.Ball(world, 1, 18, 9)
        world.addAgent(ball)
        LearningRobot = LearningRobot.LearningRobot(ball, args.tile_coding)
        world.addAgent(LearningRobot)
        #diaplayGUI()
        trainTheRobot(100001, world,isMesirot)
        print ('I am trained now in kicking. Validation:')
        calcTheMadad(args.is_mesirot)
        trainTheRobot(100001, world,isMesirot)
        isMesirot =True
        HumanRobot = HumanRobot.HumanRobot(ball)
        world.addAgent(HumanRobot)
        print ('now lets play mesirot')
        trainTheRobot(100001, world ,isMesirot)
        print ('I am trained now in kicking and mesirot. Validation:')
        trainTheRobot(100001, isMesirot)
    mesirot_avg = calcTheMadad(isMesirot)
    column_names = 'VaMax,alpha,gamma,epsilon,mesirot_avg'
    # column_names = ['vaMax','alpha','epsilon','gamma','mesirot_avg']
    line = '{},{},{},{},{}'.format(args.VaMax,args.alpha,args.epsilon,args.gamma,mesirot_avg)
    # column_names = ['vaMax','alpha','epsilon','gamma','mesirot_avg']
    # write_to_csv(line,column_names = column_names,filename = results_file)
        # exportToCsv()

# Activate the game
    while 1:
        diaplayGUI()
        world.update(isMesirot)
        time.sleep(1)
