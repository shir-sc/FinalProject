import cellular


class HumanRobot(cellular.Agent):
    def __init__(self, ball):
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
        if gameOver:
            self.reset()
        self.cell = self.world.getCell(self.R_cell_x, self.R_cell_y)  # printing the robot in the game (x,y)--> grid[y,x]
        # print ('update human')
        return gameOver

    def ChooseAndTakeAction (self):
        if self.R_cell_x == 18:
            self.R_cell_x = 19
        self.R_cell_y = 5 # in this game the human Robot is always in the middle position
        if self.ball.x_cell==18:
            if self.ball.y_cell ==4 or self.ball.y_cell ==5 or self.ball.y_cell ==6:
                self.R_cell_x=self.ball.x_cell
                self.R_cell_y=self.ball.y_cell
                self.ball.ballIsKicked('Human')
                cellular.Agent.numMesirot +=1
                # print ('Human kick: '+ str(cellular.Agent.numMesirot))
        self.cell = self.world.getCell(self.R_cell_x, self.R_cell_y)  # printing the robot in the game (x,y)--> grid[y,x]

    def reset (self):
        self.ball.randomRelocate()
        self.R_cell_y = 5
        self.R_cell_x = 19
        cellular.Agent.mesirotScore.append(cellular.Agent.numMesirot)
        cellular.Agent.numMesirot = 0
        # print('mesirotScore = ' + str(cellular.Agent.mesirotScore))
        # print('Human reset')

    def IsGameOver(self):
        # If the ball is in the next to leftmost column of the board.
        # round over
        # Need to relocate the ball in a new random location.
        if self.ball.x_cell == self.R_cell_x and self.ball.y_cell==self.R_cell_y and self.R_cell_x==18: # the robot and the ball are on the same cell = hit the ball
            return False
        elif self.ball.x_cell >= self.boundLine:
            return True
        return False # the ball is not in the robot area