import pygame
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

aiScoreVal = 0
aiPreScore = 0

humanScoreVal = 0
humanPreScore = 0

# define main includes the main function of the game
def main():
    # initialize the pygame module
    pygame.init()

    # screen parameters
    scrHeight = 500
    scrWidth = 1000

    # boundary attributes
    boundWidth = 20
    foreColor = pygame.Color("white")
    ballColor = pygame.Color("white")
    paddleColor = pygame.Color("white")
    backColor = pygame.Color("black")

    # clock
    clock = pygame.time.Clock()

    # screen for game
    screen = pygame.display.set_mode((scrWidth,scrHeight))

    # draw boundaries
    pygame.draw.rect(screen,foreColor,pygame.Rect((0,0),(scrWidth,boundWidth)))
    #pygame.draw.rect(screen,foreColor,pygame.Rect((0,boundWidth),(boundWidth,scrHeight-(2*boundWidth))))
    pygame.draw.rect(screen,foreColor,pygame.Rect((0,scrHeight-boundWidth),(scrWidth,boundWidth)))


    # ball object
    class pongBall:
        ballRadius = 15
        veloX = 5
        veloY = 5
        def __init__(self,x,y):
            self.x = x
            self.y = y

        def show(self, color):
            pygame.draw.circle(screen,color,(self.x,self.y),self.ballRadius)

        def update(self):
            self.show(backColor)
            if (self.y == boundWidth + self.ballRadius):
                self.veloY = -self.veloY
            elif (self.y == (scrHeight - boundWidth - self.ballRadius)):
                self.veloY = -self.veloY

            self.x = self.x - self.veloX
            self.y = self.y - self.veloY
            self.show(ballColor)

    # paddle object
    class pongPaddle:
        paddleWidth = 20
        paddleHeight = 100
        #posX = scrWidth - paddleWidth

        def __init__(self,x,y):
            self.y = y
            self.x = x
        
        def show(self,color):
            pygame.draw.rect(screen,color,pygame.Rect((self.x, self.y),(self.paddleWidth,self.paddleHeight)))

        def update_human(self):
            keys = pygame.key.get_pressed()
            self.show(backColor)
            if keys[pygame.K_w] and self.y != boundWidth:
                self.y = self.y - 5
            elif keys[pygame.K_s] and self.y != (scrHeight - boundWidth - self.paddleHeight):
                self.y = self.y + 5
            self.show(paddleColor)
            
        #def update_human2(self):
        #   keys = pygame.key.get_pressed()
        #   self.show(backColor)
        #   if keys[pygame.K_UP] and self.y != boundWidth:
        #       self.y = self.y - 5
        #   elif keys[pygame.K_DOWN] and self.y != (scrHeight - boundWidth - self.paddleHeight):
        #       self.y = self.y + 5
        #    self.show(paddleColor)

        def update_ai(self,prediction):
            self.show(backColor)
            self.y = prediction
            self.show(paddleColor)

    def collision_ai(ball,paddle):
        global aiScoreVal
        if(ball.x == scrWidth - paddle.paddleWidth - ball.ballRadius) and (ball.y <= paddle.y + paddle.paddleHeight and ball.y >= paddle.y):
            ball.veloX = -ball.veloX
            ball.show(backColor)
            ball.x = ball.x - ball.veloX
            ball.y = ball.y - ball.veloY
            ball.show(ballColor)
            aiScoreVal += 1

    def collision_human(ball,paddle):
        global humanScoreVal
        if(ball.x == paddle.paddleWidth + ball.ballRadius) and (ball.y <= paddle.y + paddle.paddleHeight and ball.y >= paddle.y):
            ball.veloX = -ball.veloX
            ball.show(backColor)
            ball.x = ball.x - ball.veloX
            ball.y = ball.y - ball.veloY
            ball.show(ballColor)
            humanScoreVal += 1

    def endGame(ball):
        if(ball.x > scrWidth - ball.ballRadius) or ball.x < ball.ballRadius:
            pygame.quit()

    newBall = pongBall((scrWidth-pongBall.ballRadius-pongPaddle.paddleWidth),(scrHeight//2))
    newBall.show(ballColor)

    hpaddleX = scrWidth - pongPaddle.paddleWidth
    hpaddleY = scrHeight//2 - (pongPaddle.paddleHeight//2)

    aipaddleX = 0
    aipaddleY = scrHeight//2 - (pongPaddle.paddleHeight//2)

    humanPaddle = pongPaddle(aipaddleX,aipaddleY)
    humanPaddle.show(paddleColor)

    aiPaddle = pongPaddle(hpaddleX,hpaddleY)
    aiPaddle.show(paddleColor)

    aiTextX = scrWidth - 200
    aiTextY = 25

    humanTextX = 25
    humanTextY = 25

    font = pygame.font.Font('arial_narrow_7.ttf',25)

    def showAiScore(x,y):
        global aiPreScore
        if(aiPreScore != aiScoreVal):
            delAiScore(x,y,aiPreScore)

        score = font.render("Ai Score : "+str(aiScoreVal),True,[255,255,255])
        aiPreScore = aiScoreVal
        screen.blit(score,(x,y))

    def delAiScore(x,y,presc):
        score = font.render("Ai Score : "+str(presc),True,[0,0,0])
        screen.blit(score,(x,y))

    def showHumanScore(x,y):
        global humanPreScore
        if(humanPreScore != humanScoreVal):
            delHumanScore(x,y,humanPreScore)

        score = font.render("Human Score : "+str(humanScoreVal),True,[255,255,255])
        humanPreScore = humanScoreVal
        screen.blit(score,(x,y))

    def delHumanScore(x,y,presc):
        score = font.render("Human Score : "+str(presc),True,[0,0,0])
        screen.blit(score,(x,y))
        
    #game_data = open("game_data.csv","a")
    #print("x,y,vx,vy,paddle.y",file=game_data)
    
    data_ai = pd.read_csv("game_data.csv")
    data_ai = data_ai.drop_duplicates()

    input_data = data_ai.drop(columns=['paddle.y'])
    output_data = data_ai['paddle.y']

    algo = KNeighborsRegressor(n_neighbors=5)
    algo.fit(input_data,output_data)

    dataframe = pd.DataFrame(columns=['x','y','vx','vy'])
    
    while True:
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            break
        pygame.display.flip()
        humanPaddle.update_human()
        to_predict = dataframe.append({'x':newBall.x,'y':newBall.y,'vx':newBall.veloX,'vy':newBall.veloY},ignore_index=True)
        move_ai = algo.predict(to_predict)
        aiPaddle.update_ai(move_ai)
        newBall.update()
        pygame.display.flip()
        collision_human(newBall,humanPaddle)
        collision_ai(newBall,aiPaddle)
        endGame(newBall)
        showAiScore(aiTextX,aiTextY)
        showHumanScore(humanTextX,humanTextY)
        pygame.display.flip()
        clock.tick_busy_loop(60)
        #print("{},{},{},{},{}".format(newBall.x,newBall.y,newBall.veloX,newBall.veloY,humanPaddle.y), file=game_data)


if __name__ == "__main__":
    main()
    