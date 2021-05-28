import pygame
import random
from cls import *
import numpy as np
import os
from matplotlib import pyplot as plt

clear = lambda: os.system('cls')

#def init_table was here!!!
def init_table(screen,box_len, matrix_len):
    #window_size = 1000
    #matrix_len = 50
    #box_len = 20

    reward_table = [] # to avoid agents movements outside the map.
                        #there are two more row and column at the edges.
    for i in range(matrix_len + 2):
        line2 = []
        for j in range(matrix_len+2):
            line2.append(-2000)
        reward_table.append(line2)


    matrix = []
    Q = []
    for i in range(matrix_len):
        line = []
        ll = []
        for j in range(matrix_len):
            ll.append(0)
            r = random.randint(0,100)
            if r%4 == 0:
                x = one(j*box_len, i*box_len, box_len-1, i,j, screen,barrier=True)
                line.append(x)
                reward_table[i+1][j+1] = -1000
            else:
                line.append( one(j*box_len, i*box_len, box_len-1, i,j, screen))
                reward_table[i+1][j+1] = -1

        matrix.append(line)
        Q.append(ll)
    
            
    return matrix,reward_table

def convert_dir(index,mode = ""):
    if mode == "to_coordinates":
        if index == 0:
            return [1,0]
        if index == 1:
            return [-1,0]
        if index == 2:
            return [0,-1]
        if index == 3:
            return [0,1]

def update(agent,rewards):
    learning_rate = 0.6 #0.6 is better
    discount = 0.5
    current_state = agent.Q[agent.index[0]][agent.index[1]]
    current_action = max(current_state)
    current_action_index = np.argmax(current_state) # for directioning to the next state
    current_action_dir = convert_dir(current_action_index,mode = "to_coordinates")
    if rewards[agent.index[0] + 2][agent.index[1]+2] <=-1000:
        return True,rewards[agent.index[0] + 2][agent.index[1]+2]
    try:
        next_state = agent.Q[agent.index[0] + current_action_dir[0]][agent.index[1] + current_action_dir[1]]
        current_reward = rewards[agent.index[0] + current_action_dir[0]+2][agent.index[1] + current_action_dir[1] + 2] # reward comes with the result of action.
        if current_reward > 1500:
            agent.Q[agent.index[0]][agent.index[1]][current_action_index] += current_action + learning_rate*( current_reward + discount*max(next_state)) - current_action
            return True,current_reward
        if current_reward <=  -999:
            agent.Q[agent.index[0]][agent.index[1]][current_action_index] += current_action + learning_rate*( current_reward + discount*max(next_state)) - current_action
            return True,current_reward
        else:
            agent.Q[agent.index[0]][agent.index[1]][current_action_index] += current_action + learning_rate*( current_reward + discount*max(next_state)) - current_action
            return False,current_reward
    except IndexError:
        agent.Q[agent.index[0]][agent.index[1]][current_action_index] = 0
        return True,current_reward

   



#def convert was here!!!

        #return 0

##++++++++++++++++++++++++++++ GAME RUNS HERE++++++++++++++++++++++++++++++++++++++++++++++++++++++++


screen = pygame.display.set_mode([1000, 1100]) #1000x1000 window

#define before initialized
x = convert("pixel",100,100)
table,rewards = init_table(screen, 20,50)
after_done = 0
agent = Agent(0,0)
agent.init_Q(50)

start_point = []
finish_point = []
episode = 0
scores = [];episode_scores=[]
start = False
done = False #checks if learning is completed or not
show_path = False
best_path = []
temp_path = []

#start_point_index = (0,0)
start_finish = 1; #to control selecting only two points
start_button_color=(100,100,100)
pause_button_color = (100,100,100)
try_button_color = (100,100,100)
best_path_button_color = (100,100,100)
running = True

while running:
  
    end_button_color = (100,100,100)
             
    #mouse = pygame.mouse.get_pos()
    
    #-------------GAME CALCULATIONS AND ACTIONS START ------------------------------------
    
    # Did the user click the window close button?
    for event in pygame.event.get():
        (mx,my) = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mx<200 and mx>=100:#checkes if start_button pressed
                if my<1070 and my>=1030:
                    start_button_color=(160,160,160)
                    print("-->",mx,my)
            if mx>350 and mx<450: # checks pause_button pressed
                if my>1030 and my<1070:
                    pause_button_color = (160,160,160)
            if mx>600 and mx<700:
                    if my>1030 and my<1070:
                        try_button_color = (160,160,160)
                        plt.plot(scores)
                        plt.show()
            if mx > 850 and mx < 950:#show_best_path_button
                if my > 1030 and my < 1070:
                    best_path_button_color = (160,160,160)
                    show_path = True
        if event.type == pygame.MOUSEBUTTONUP:
            if my<1000 and mx < 1000: #there are no indexes on map beside those pixel coordinates
                (i,j) = convert("pixel",mx,my)
                #i = (my-my%20)/20
                #j = (mx-mx%20)/20
                i = int(i);j = int(j)
                #print(j,i)
                if table[i][j].barrier == False and start_finish !=3: #this part will be activated after learning completed
                    if start_finish == 1:
                        table[i][j].color=(140,140,255)
                        table[i][j].role = start_finish
                        start_point = [i,j]
                        #start_point.append(i);start_point.append(j)
                        agent.index = [i,j]
                    if start_finish == 2:
                        table[i][j].color=(90,90,255)
                        table[i][j].role = start_finish
                        finish_point.append(i);finish_point.append(j)
                        rewards[i+2][j+2] = 2000 #finish point reward
                    start_finish+=1
            else:
                if mx<200 and mx>=100:
                    if my<1070 and my>=1030: #checks start_button press release
                        start_button_color=(100,100,100)
                        agent.update_coor()
                        start = True
                if mx>350 and mx<450: # checks pause_button press release
                    if my>1030 and my<1070:
                        pause_button_color = (100,100,100)
                        start = False
                if mx>600 and mx<700:
                    if my>1030 and my<1070:
                        try_button_color = (100,100,100)
                if mx > 850 and mx < 950:
                    if my > 1030 and my < 1070:
                        best_path_button_color = (100,100,100)
                        show_path = False
                print("->",mx,my)
                
#-----------------learning will be done here-----------------------------------------------------------------------


    if start == True: # when the start_button press released
        
        ep = False
        if episode < 1000:
            if after_done == 0:
                with open("table.txt","w") as f:
                    for i in range(len(rewards)):
                        f.write(str(rewards[i]))
                        f.write("\n")
                after_done = 1
            if not ep: #if episode not finished #agent,reward,learning_rate,discount,start,end
                #print(f"---->>>>{agent.index} agent index")
                temp_path.append(agent.index.copy())
                ep,score = update(agent,rewards)
                episode_scores.append(score)
                #print(f"where to->{np.argmax(agent.Q[agent.index[0]][agent.index[1]])}")
                #print(f"current score -> {score}")
                agent.move()
            if ep: # if episode finished
                clear()
                print(f"episode = {episode}")
                scores.append(sum(episode_scores))
                print(f"episode scores -> {sum(episode_scores)}")
                episode_scores = []
                ep = False
                agent.start_over(start_point)
                if len(scores) > 5:
                    if scores[episode-1] > scores[episode-2]:
                        best_path = temp_path.copy()
                temp_path = []
                episode+=1
        else:
            print("training completed...")
            
        # after some iteration: start = False; done=True
        #agent.move([random.randint(-1,1),random.randint(-1,1)]) # moves agent.
                
                        
                
                
    ##--------------- GAME CALCULATIONS AND ACTIONS END------------------------------------------
            
    
    ##--------------START RENDERING------------------------------------------------------------------------------
            
    # Fill the background with white
    screen.fill((0, 0, 0))
    
    
    #Draw table
    for i in range(50):
        for j in range(50):
            
            pygame.draw.rect(screen,table[i][j].color, table[i][j].coordinates )
    
    #Draw best path
    if show_path:
        print(len(best_path))
        for i in best_path:
            if True:
                #path_coor = convert("index",i[0],i[1])
                pygame.draw.rect(screen,(255,255,0), (i[1]*20,i[0]*20,20,20) )
            
    #Draw agent        
    pygame.draw.circle(screen, (0,255,0),agent.coordinates,8)
    
    #Draw buttons and interface
    pygame.draw.rect(screen,start_button_color,(100,1030,100,40))
    pygame.draw.rect(screen,pause_button_color,(350,1030,100,40))
    pygame.draw.rect(screen,try_button_color,(600,1030,100,40))
    pygame.draw.rect(screen,best_path_button_color, (850,1030,100,40))
            

    # Flip the display
    pygame.display.flip()
    
    #------------END RENDERING---------------------------------------------------------------------------------------
    
    
# Done! Time to quit.
pygame.quit()