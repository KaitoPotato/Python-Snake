#STEP 1: IMPORT AND SETUP

#importing libraries
import pygame
import time
import random

#set snake speed
snake_speed = 15

#setting game window size
window_x = 720
window_y = 480

#defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

#STEP 2: INITIALIZE PYGAME

#initializing pygame
pygame.init()

#initializing game window
pygame.display.set_caption("'Jack's snake game")
game_window = pygame.display.set_mode((window_x,window_y))

#FPS controller
fps = pygame.time.Clock()

#STEP 3: INITIALIZE SNAKE 

#defining snake's initial/default positon
snake_position = [100,50]

#defining first four block of snake
#body
snake_body = [  [100,50],
                [90,50],
                [80,50],
                [70,50]
                ]

#intialize fruit position
fruit_position = [random.randrange(1,(window_x//10)) * 10, 
                  random.randrange(1,(window_y//10)) * 10]
fruit_spawn =  True #default spawning status

#set default snake direction to RIGHT
direction  = 'RIGHT'
change_to  = direction


#STEP 4: Create a function to display the score of player

#intialize score
score = 0

#displaying score function

#choice is not used for current implementation; could be edited for further expansion, such as choosing the position of showing score
def showscore(choice, color, font, size):
    
    #creating font object 
    score_font = pygame.font.SysFont(font,size)
    
    #create the display surface object
    #score_surface
    score_surface = score_font.render ('Score: ' + str(score), True, color)
    
    #create a rectangular object for holding text/score surface
    score_rect = score_surface.get_rect()
    
    #displaying text
    game_window.blit(score_surface, score_rect)
    
    
#STEP 5: Create game_over function
#game_over function
def game_over():
    #create font
    my_font = pygame.font.SysFont('times new roman', 50)
    
    #create text surface
    game_over_surface = my_font.render('Your Score is: ' + str(score), True, red)
    
    #creating a rectangle object for the text surface
    game_over_rect = game_over_surface.get_rect()
    
    #setting the position of the rectangle object
    game_over_rect.midtop = (window_x/2, window_y/2)
    
    #use blit to draw text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    #after two seconds, close the program
    time.sleep(2)
    
    #deactivating pygame library
    pygame.quit()
    
    #quit the program
    quit()
    
    
#STEP 6: MAIN FUNCTION
while True:
    #handling key controll/events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:  # Check if a key is pressed
            if event.key == pygame.K_UP:      # Check which key is pressed
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            
    #make sure snakes don't move in opposite direction simutaneously
    if (change_to == 'UP' and direction != 'DOWN'):
        direction = 'UP'
    if (change_to == 'DOWN' and direction != 'UP'):
        direction = 'DOWN'
    if (change_to == 'LEFT' and direction != 'RIGHT'):
        direction = 'LEFT'
    if (change_to == 'RIGHT' and direction !=  'LEFT'):
        direction = 'RIGHT'
        
    #moving the snake (moving head position)
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10
        
    #implementing snake body growing mechanism
    #if snake and fruit collide then the score will be incremented by 10
    snake_body.insert(0,list(snake_position)) #snake moving forward
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]: #if eat fruit, grows, spawn new fruit
        score+= 10
        fruit_spawn = False
    else: #if didn't eat fruit, remove tail block of snake (moving frame by frame)
        snake_body.pop()
    
    if not fruit_spawn: #regenerating a new fruit position
        fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                          random.randrange(1, (window_y//10)) * 10]
        
    fruit_spawn = True #reset fruit status 
    
    # clears the screen by filling it with black beore 
    # redrawing the snake and other elements like the fruit. 
    # It ensures that as the snake moves, its previous position is erased, 
    # and only the updated positions of the snake and fruit are drawn on a clean background.
    game_window.fill(black)
    
    #redraw the snake block by block
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    
    #redraw fruit in its regenerated new position (10 in width and height)
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0],fruit_position[1], 10 , 10))
    
    #game over condition
    #out of bound case
    if snake_position[0] < 0  or  snake_position[0] > window_x - 10: #snake head has width 10, so we subtract 10 as we measure from left
        game_over()
    if snake_position[1] < 0  or  snake_position[1] > window_y - 10:
        game_over()
        
    #snake head touching body case
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
        
    #displaying score continuously
    showscore(1, white, 'times new roman',20)
    
    #refresh game screen
    pygame.display.update()
    
    #frame Per Second /Refresh Rate
    fps.tick(snake_speed)
    