import numpy as np
import cellular
import TileCoding_QLearn
import Basic_QLearn

class LearningRobot(cellular.Agent): # Robot is the the secones agent togever with ball. He learning during the game to hit the ball.
    def __init__(self,ball, isTileCoding):
        if (isTileCoding):
            self.ai = TileCoding_QLearn.TileCodingQLearn(actions=range(6))
        else:
            self.ai = Basic_QLearn.BasicQLearn(actions=range(6))  # Q-learning (off policy)
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
    def update(self, isMesirot):
        # self.turn += 1
        reward = self.calcReward(isMesirot) # reward for arriving to this state by takingthe action in the last itteration. 'Bediavad'
        state = self.ai.calcState(robot=self, ball=self.ball)  # find in what state i am now
        if self.lastAction is not None:  # learn from the state and action that brought you here (anyway. also if game is over in the next check)
            self.ai.updateQTable(self.lastState, self.lastAction, reward, state)
        # After learning from the past action (good or bad) we check if game was over. if not, we take the chosen action
        gameOver = self.IsGameOver(isMesirot)
        if gameOver:
            self.reset()
        else:
            action = self.ai.chooseAction(state)  # Choose the next move from this state, by the policy algorithm
            self.lastAction = action  # update the last state action to be the current for learnning in the next iteration
            self.lastState = state
            self.take_action(action=action)
        self.cell = self.world.getCell(self.R_cell_x, self.R_cell_y)         # printing the robot in the game (x,y)--> grid[y,x]
        # print ('update learning')
        return gameOver

    def reset (self):
        self.ball.randomRelocate()
        self.R_cell_y = 5
        self.R_cell_x = 0
        self.lastAction = None
        self.turn = 0
        cellular.Agent.mesirotScore.append(cellular.Agent.numMesirot)
        cellular.Agent.numMesirot = 0
        #print('mesirotScore = ' + str(cellular.Agent.mesirotScore))
        print('Learning reset')


    def IsGameOver (self, isMesirot):
        # If the ball is in the next to leftmost column of the board,
        # round over - It means that the ball arrived to the wall or that the ball was hit by the robot
        # Need to relocate the ball in a new random location.
        #hit the ball
        if self.ball.x_cell == self.R_cell_x and self.ball.y_cell==self.R_cell_y: # the robot and the ball are on the same cell = hit the ball
            if isMesirot:
                return False
            else:
                return True
        #miss the ball
        elif self.ball.x_cell<=self.boundLine:
            return True
        # The ball stopped before it arrived to the robot area
        elif int(self.ball.Va) == 0: #Need to make sure the ball is arriving. and cancel it ----------?????
            self.no_score +=1
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
        if [self.R_cell_x, self.R_cell_y] == [self.ball.x_cell, self.ball.y_cell]:
            self.good_score += 1
            self.ball.ballIsKicked('Learning')
            if isMesirot:
                cellular.Agent.numMesirot +=1
                self.turn=0
                print ('Learning kick: '+ str( cellular.Agent.numMesirot))
            return self.hitReward + cellular.Agent.numMesirot
        # The robot missed the ball. The ball Arrived to the 'Gate'. Bad score incremented
        elif self.ball.x_cell <= self.boundLine: #case that game over
            self.bad_score += 1
            return self.missReward
        # Get 0 reward for doing nothing
        elif self.lastAction == 2:
            return self.zeroReward
        else:
        # get minus 1 for unnecessary movments
            return self.vainMoveReward