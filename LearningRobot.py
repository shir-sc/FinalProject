import numpy as np
import cellular
import TileCoding_QLearn
import Basic_QLearn

debug = False


class LearningRobot(cellular.Agent): # Robot is the the secones agent togever with ball. He learning during the game to hit the ball.
    def __init__(self,ball, isTileCoding, learning_rate = 0.1, discount_rate = 0.9, epsilon = 0.1):
        super(LearningRobot,self).__init__()

        if (isTileCoding):
            self.ai = TileCoding_QLearn.TileCodingQLearn(actions=range(6), alpha = learning_rate, gamma =discount_rate,\
                                                         epsilon = epsilon)
        else:
            self.ai = Basic_QLearn.BasicQLearn(actions=range(6), alpha = learning_rate, gamma = discount_rate,\
                                               epsilon = epsilon)  # Q-learning (off policy)
        self.lastAction = None
        self.R_cell_y = 5
        self.R_cell_x = 0

        self.good_score = 0 # succeed in hitting the ball
        self.bad_score = 0 # failed in hitting the ball
        self.no_score =0 # the ball haven't arrived to the robot
        self.vainMoveReward = -1  # prevent in vain moving
        self.zeroReward = 0  # No reward
        self.missReward = -10  # the ball passes the robot
        self.hitReward = 10  # The robot hitted the ball
        self.boundLine = 1
        self.turn = 0
        self.ball = ball
        # self.maxMesirot = []
        # self.NumberOfMesirot = 0

    def color(self):
        return 'red'

    # The robot update. This is being called from the world update, that happen every second
    # def update(self, isMesirot):
    #     # self.turn += 1
    #     #print('Robot before reward '+str(self.R_cell_x)+ str(self.R_cell_y))
    #     #print('Ball before reward '+ str(self.ball.x_cell) + str(self.ball.y_cell)+ str(self.ball.va_categorial)+ str(self.ball.vd_categorial))
    #     # reward = self.calcReward(isMesirot) # reward for arriving to this state by takingthe action in the last itteration. 'Bediavad'
    #     # state = self.ai.calcState(robot=self, ball=self.ball)  # find in what state i am now
    #     # #print('State after reward '+str(state))
    #     # action = self.ai.chooseAction(state)  # Choose the next move from this state, by the policy algorithm
    #     # if self.lastAction is not None:  # learn from the state and action that brought you here (anyway. also if game is over in the next check)
    #     #     self.ai.updateQTable(self.lastState, self.lastAction, reward, state)
    #     # self.lastAction = action  # update the last state action to be the current for learnning in the next iteration
    #     # self.lastState = state
    #     # After learning from the past action (good or bad) we check if game was over. if not, we take the chosen action
    #     gameOver = self.IsGameOver(isMesirot)
    #     # if not gameOver:
    #     self.take_action(action=action)
    #         # self.reset()
    #     # else:
    #     #     self.take_action(action=action)
    #              # printing the robot in the game (x,y)--> grid[y,x]
    #     # print ('update learning')
    #     return gameOver

    def reset (self):
        self.R_cell_y = 5
        self.R_cell_x = 0
        self.lastAction = None
        self.num_kicks = 0
        # self.turn = 0
        # cellular.Agent.mesirotScore.append(cellular.Agent.numMesirot)
        # cellular.Agent.numMesirot = 0
        # print('mesirotScore = ' + str(cellular.Agent.mesirotScore))
        #print('Robot before reset '+str(self.R_cell_x)+ str(self.R_cell_y))
        #print('Ball before reset '+ str(self.ball.x_cell) + str(self.ball.y_cell)+ str(self.ball.va_categorial)+ str(self.ball.vd_categorial))
        # print('Learning reset')

    def update_cell(self):
        self.cell = self.world.getCell(self.R_cell_x, self.R_cell_y)

    def update(self,isMesirot):
        reward = self.calcReward(isMesirot) # reward for arriving to this state by takingthe action in the last itteration. 'Bediavad'
        state = self.ai.calcState(robot=self, ball=self.ball)  # find in what state i am now
        #print('State after reward '+str(state))
        action = self.ai.chooseAction(state)  # Choose the next move from this state, by the policy algorithm
        if self.lastAction is not None:  # learn from the state and action that brought you here (anyway. also if game is over in the next check)
            self.ai.updateQTable(self.lastState, self.lastAction, reward, state)
        self.lastAction = action  # update the last state action to be the current for learnning in the next iteration
        self.lastState = state
        if not self.IsGameOver(isMesirot):
            self.take_action(action=action)

    def IsGameOver (self, isMesirot):
        # If the ball is in the next to leftmost column of the board,
        # round over - It means that the ball arrived to the wall or that the ball was hit by the robot
        # Need to relocate the ball in a new random location.
        #hit the ball


        if not hasattr(self.ball,'x_cell'):
            return False
        if self.ball.x_cell == self.R_cell_x and self.ball.y_cell==self.R_cell_y and self.R_cell_x==1: # the robot and the ball are on the same cell = hit the ball
            if isMesirot:
                return False
            else:
                if debug: print ('GO, learning kick ')
                return True
        #miss the ball
        elif self.ball.x_cell <= self.boundLine:
            if debug: print ('GO, learning bound line ')
            return True
        # The ball stopped before it arrived to the robot area
        elif int(self.ball.Va) == 0:
            self.no_score +=1
            if debug: print ('GO, learning Va ==0 ')
            return True
        else:
            return False

    def take_action (self, action):
        # return to goal position, if needed
        if self.R_cell_x == 1:
            self.R_cell_x = 0
        # self.cell_y, after assignment is 2,5, or 8 ,# this done anyway
        self.R_cell_y = 3 * int((3 * (self.R_cell_y - 1)) / 9) + 2 # Make sure the robot Y is in one of the 3 base locations

        # This section calculates the next location of the robot, according to the action taken
        # move 3 down
        if action == 0:
            if self.R_cell_y < 8:
                self.R_cell_y +=3
        # Move 3 up
        elif action == 1:
            if self.R_cell_y > 2:
                self.R_cell_y -=3
        # Don't move
        elif action == 2:
            self.R_cell_y += 0
        # Move diagonally
        elif action == 3:
            self.R_cell_y += 1
            self.R_cell_x += 1
        # Move straight in x direction
        elif action == 4:
            self.R_cell_y += 0
            self.R_cell_x += 1
        # Move diagonally in other direction.
        elif action == 5:
            self.R_cell_y -= 1
            self.R_cell_x += 1

    # Reward calculation,
    # and increase of the robot score for printing the results of the game.... shouldn't it be in the read csv only?
    def calcReward(self, isMesirot):
        # Reached a cell that the ball is in. good score incremented
        if [self.R_cell_x, self.R_cell_y] == [self.ball.x_cell, self.ball.y_cell] and self.R_cell_x==1:
            self.good_score += 1
            # print('Robot before kick: '+str(self.R_cell_x)+','+ str(self.R_cell_y))
            # print('Ball before kick: '+ str(self.ball.x_cell) +','+ str(self.ball.y_cell)+','+ str(self.ball.va_categorial)+','+ str(self.ball.vd_categorial))
            # if debug: print ('Learning kick: ' + str(cellular.Agent.numMesirot))
            if isMesirot:
                self.ball.ballIsKicked('Learning')
                self.num_kicks += 1
                self.turn=0
                # if debug: print('Learning kick: '+ str( cellular.Agent.numMesirot))
                # print('Robot after kick: ' + str(self.R_cell_x)+',' + str(self.R_cell_y))
                # print('Ball after kick: ' + str(self.ball.x_cell)+',' + str(self.ball.y_cell) + ',' +str(self.ball.va_categorial) +',' + str(self.ball.vd_categorial))
            numMesirot = 2*self.num_kicks
            return self.hitReward + numMesirot

        # The robot missed the ball. The ball Arrived to the 'Gate'. Bad score incremented
        elif self.ball.x_cell <= self.boundLine: #case that game over, the kearning obot missed the ball
            self.bad_score += 1
            return self.missReward
        # Get 0 reward for doing nothing
        elif self.lastAction == 2:
            return self.zeroReward
        elif isMesirot and self.ball.x_cell >= 18: # This condition will be true only in case of mesirot and the human robot wasn't able to reach the ball.
            return self.missReward
        else:
        # get minus 1 for unnecessary movments
            return self.vainMoveReward