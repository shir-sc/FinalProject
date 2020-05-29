import cellular
from numpy import argmin
debug= False

class HumanRobot(cellular.Agent):
    def __init__(self, ball):
        super(HumanRobot,self).__init__()
        self.R_cell_y = 5
        self.R_cell_x = 19
        self.boundLine = 18
        self.ball = ball
        # self.maxMesirot = []
        # self.NumberOfMesirot = 0

    def color(self):
        return 'green'


    def update(self, isMesirot):
        self.ChooseAndTakeAction()
        gameOver = self.IsGameOver()
        # if gameOver:
        #     self.reset()
        # self.cell = self.world.getCell(self.R_cell_x, self.R_cell_y)  # printing the robot in the game (x,y)--> grid[y,x]
        # print ('update human')
        return gameOver

    def get_closest_gate(self):
        ball_y_pos = self.ball.y_cell
        distance_from_gate_2 = abs(ball_y_pos - 2)
        distance_from_gate_5 = abs(ball_y_pos - 5)
        distance_from_gate_8 = abs(ball_y_pos - 8)
        return argmin([distance_from_gate_2,distance_from_gate_5,distance_from_gate_8])

    def ChooseAndTakeAction (self):
        #If the robot kicked, this sends him back in place.
        if self.R_cell_x == 18:
            self.R_cell_x = 19
            # Make sure the robot Y is in one of the 3 base locations
            self.R_cell_y = 3 * int((3 * (self.R_cell_y - 1)) / 9) + 2

        #ball is already at the gate
        if self.ball.x_cell==18:
            #The ball is right next to the gate. If X is in a position to kick it it should
            in_position_to_kick = abs(self.R_cell_y-self.ball.y_cell) < 2
            if in_position_to_kick:
                self.R_cell_x = self.ball.x_cell
                self.R_cell_y = self.ball.y_cell
                self.ball.ballIsKicked('Human')
                self.num_kicks += 1
                cellular.Agent.numMesirot += 1
                if debug: print ('Human kick: '+ str(cellular.Agent.numMesirot))


        elif self.ball.x_cell == 17:
            #The ball is close enough to the gate column for the player to choose the right
            #gate to come out of (gate 2/5/8)
            next_x, next_y = self.ball.next_step()
            if next_x == 18:
                if (next_y >=1 and next_y<=3):
                    self.R_cell_y = 2
                elif (next_y >=4 and next_y<=6):
                    self.R_cell_y = 5
                else:
                    self.R_cell_y = 8

        # self.cell = self.world.getCell(self.R_cell_x, self.R_cell_y)  # printing the robot in the game (x,y)--> grid[y,x]

    def reset (self):
        # self.ball.randomRelocate()
        self.R_cell_y = 5
        self.R_cell_x = 19
        self.num_kicks = 0
        # cellular.Agent.mesirotScore.append(cellular.Agent.numMesirot)
        # cellular.Agent.numMesirot = 0
        # print('mesirotScore = ' + str(cellular.Agent.mesirotScore))
        # print('Human reset')

    def IsGameOver(self):
        # If the ball is in the next to leftmost column of the board.
        # round over
        # Need to relocate the ball in a new random location.
        if self.ball.x_cell == self.R_cell_x and self.ball.y_cell==self.R_cell_y and self.R_cell_x==18: # the robot and the ball are on the same cell = hit the ball
            return False
        elif self.ball.x_cell >= self.boundLine:
            if debug: print ('human GO bound line')
            return True
        return False # the ball is not in the robot area

    def update_cell(self):
        self.cell = self.world.getCell(self.R_cell_x, self.R_cell_y)