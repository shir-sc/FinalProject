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
from statsmodels.stats.weightstats import ttest_ind

GAMMA_ITERATION = 100000
EPSILON_ITERATION = 300000
ALPHA_ITERATION = 100000
# For debugging of csv2game. given a state returns the line in the csv file
def state2line(state):
    lineNumber = state[0]+6*state[1]+6*9*state[2]+6*9*4*state[3]+6*9*4*8*state[4]
    return lineNumber

    # # This section handle the cvs file for submission
def trainTheRobot(pretraining, isMesirot, learning_robot, world):
    for i in range(pretraining+1): # fast learning before the board is display
        # print the success percentage of the robot (per 10000 round )
        if i % 100000 == 0 and i > 0:
            print("round number: " + str(i))
            learning_robot.ai.gamma = np.amin([learning_robot.ai.gamma*1.05,0.9])
            learning_robot.ai.alpha = np.amin([learning_robot.ai.gamma*0.95,0.05])
            if i% 200000 ==0 and i > 0:
                learning_robot.ai.epsilon*=0.5
                print('epsilon = {}'.format(learning_robot.ai.epsilon))
            print('gamma = {}'.format(learning_robot.ai.gamma))
            print('alpha = {}'.format(learning_robot.ai.alpha))


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
                print ('Good score: ' + str(learning_robot.good_score) + ". Bad score: " + str(
                    learning_robot.bad_score) + ". No score: " + str(learning_robot.no_score))
                print ('Good score percent: ' + str(100 * learning_robot.good_score / (learning_robot.no_score + learning_robot.bad_score + learning_robot.good_score)))
                learning_robot.good_score = 0
                learning_robot.bad_score = 0
                learning_robot.no_score = 0
        world.update(isMesirot)
        # diaplayGUI()
        # time.sleep(3)

def calc_t_test_for_kicks(x0):
    tile_coding_scores = get_good_score_mean(x0, True)
    print('got tile coding scores')
    print('tile coding scores average is {}'.format(np.mean(tile_coding_scores)))
    basic_scores = get_good_score_mean(x0, False)
    print('got basic scores')
    print('basic scores average is {}'.format(np.mean(basic_scores)))
    t_stat, pval, df = ttest_ind(tile_coding_scores, basic_scores, alternative='larger', value=0)
    print(t_stat, pval, df)

def get_good_score_mean(x0,isTileCoding):

    world = cellular.World(Cell, directions=4, filename='soccerField.txt')
    ball = BallSimulation.Ball(world, 1, 18, 9)
    world.addAgent(ball)
    human_robot = HumanRobot.HumanRobot(ball)
    learning_robot = LearningRobot.LearningRobot(ball, isTileCoding, human_robot, \
                                                alpha=alpha, gamma=gamma, epsilon=epsilon)
    world.addAgent(learning_robot)
    average_good_score = calculate_good_score_average(x0, learning_robot, world)
    return average_good_score

def calculate_good_score_average(x0, learning_robot,world):

    print ('I am trained now in kicking.')
    # world.mesirotScore = []
    good_score_arr = []
    for i in range(10):
        trainTheRobot(x0, False, learning_robot, world)
        for i in range(100000):  # fast learning before the board is display
            world.update(False)
        good_score_percent = 100 * learning_robot.good_score / (
                    learning_robot.no_score + learning_robot.bad_score + learning_robot.good_score)
        print ('Good score percent: ' + str(good_score_percent))
        learning_robot.good_score = 0
        learning_robot.bad_score = 0
        learning_robot.no_score = 0
        good_score_arr += [good_score_percent]
        # print (good_score_arr)
    return good_score_arr


def calcTheMadad(isMesirot, world):
    while len(world.mesirotScore) < 1000: #create an array with 1000 minigames scores
        world.update(isMesirot)
    print (world.mesirotScore)
    data = pd.Series(world.mesirotScore)
    print(data.describe()) #show stats an that data
    bin_values = np.arange(start=0, stop=200, step=1)
    data.plot(kind='hist', bins=bin_values)  # `bins` defines the start and end points of bins
    # plt.show()
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

def diaplayGUI(world):
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
    parser.add_argument('--alpha', type=float,default = 0.2,
                    help='learning rate')
    parser.add_argument('--gamma', type=float,default = 0.5,
                    help='discount rate')
    parser.add_argument('--epsilon', type=float, default=0.25)
    parser.add_argument('--dbg', type = bool, default= False)
    parser.add_argument('--tile_coding', type=bool, default=True)
    parser.add_argument('--is_mesirot', type=bool, default=True)
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
    kicking_test = False
    # x0=1000000
    # x1= 1200000
    # x2= 2000000
    x0=100
    x1= 120
    x2= 200

    if kicking_test:
        calc_t_test_for_kicks(x0)
    else:
        if isMesirot:
            world = cellular.World(Cell, directions=4, filename='soccerField.txt')
            ball = BallSimulation.Ball(world, 1, 18, 9)
            world.addAgent(ball)
            human_robot = HumanRobot.HumanRobot(ball)
            learning_robot = LearningRobot.LearningRobot(ball, isTileCoding, human_robot,\
                                                        alpha = alpha,gamma = gamma, epsilon = epsilon)

            world.addAgent(learning_robot)
            world.addAgent(human_robot)
            # diaplayGUI()
            # time.sleep(1)
            trainTheRobot(x1, isMesirot, learning_robot, world)
            print ('I am still learning mesirot.')
            calcTheMadad(isMesirot, world)
            trainTheRobot(x2-x1, isMesirot, learning_robot, world)
            print ('I am trained now in mesirot.')
            # exportToCsv()
        else:
            world = cellular.World(Cell, directions=4, filename='soccerField.txt')
            ball = BallSimulation.Ball(world, 1, 18, 9)
            world.addAgent(ball)
            human_robot = HumanRobot.HumanRobot(ball)
            learning_robot = LearningRobot.LearningRobot(ball, isTileCoding,human_robot,\
                                                        alpha = alpha,gamma = gamma, epsilon = epsilon)
            world.addAgent(learning_robot)
            #diaplayGUI()
            trainTheRobot(x0, isMesirot, learning_robot, world)
            print ('I am trained now in kicking.')
            isMesirot =True
            world.addAgent(human_robot)
            print ('now lets play mesirot')
            trainTheRobot(x1-x0, isMesirot, learning_robot, world)
            print ('I am still learning mesirot.')
            calcTheMadad(isMesirot, world)
            trainTheRobot(x2-x1, isMesirot, learning_robot, world)
            print('I am trained now in kicking and mesirot')
        mesirot_avg = calcTheMadad(isMesirot, world)
        column_names = 'VaMax,alpha,gamma,epsilon,mesirot_avg'
        line = '{},{},{},{},{}'.format(args.VaMax, args.alpha, args.epsilon, args.gamma, mesirot_avg)
        write_to_csv(line, column_names=column_names, filename=results_file)
        # exportToCsv()
#
# # Activate the game
#     while 1:
#         diaplayGUI()
#         world.update(isMesirot)
#         time.sleep(1)
