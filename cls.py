import random

class Agent:
    def __init__(self,i,j):
        #q_table is the matrix that contains values of qs
        self.index = [i,j]
        self.coordinates = [self.index[1]*20,self.index[0]*20]
        self.Q = []
    
    def init_Q(self,len):
        for i in range(len):
            line = []
            for j in range(len):
                # [up,down,left,right]
                line.append( [random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)] )
            self.Q.append(line)

    def update_coor(self):
        self.coordinates = [self.index[1]*20+10,self.index[0]*20+10]

    def start_over(self,start_point):
        #self.index = start_point
        self.index[0] = start_point[0]
        self.index[1] = start_point[1]
        self.update_coor()
    

    def pick_way(self): # determines the way of the agent based on the q table.
        #this is also the policy for agents movement

        e = 15 #this will be taken as a parameter. #e means epsilon as exploration rate!!!
        e = 100-e
        way = [0,0]
        #exploration in a 15/100 chance
        if random.randint(0,20) < 18:
            biggest_q = max( self.Q[self.index[0]][self.index[1]] )
            for n,i in enumerate(self.Q[ self.index[0]][self.index[1] ] ):
                if i == biggest_q:
                    if n == 0:
                        way[0] = 1
                    if n == 1:
                        way[0] = -1
                    if n == 2:
                        way[1] = -1
                    if n == 3:
                        way[1] = 1
                    return way
        else:
            n = random.randint(0,3)
            if n == 0:
                way[0] = 1
            if n == 1:
                way[0] = -1
            if n == 2:
                way[1] = -1
            if n == 3:
                way[1] = 1
            return way

    def move(self): #way = [1 for up -1 for down, 1 for right -1 for left] 


        way = self.pick_way()
        #checks if agent goes beyond the map or not.
        if self.index[0] + way[0] < 0:
            self.index[0] = 0
        if self.index[0] + way[0] > 49:
            self.index[0] = 49
        if self.index[1] + way[1] < 0:
            self.index[1] = 0
        if self.index[1] + way[1] > 49:
            self.index[1] = 49
        else:
            self.index[0] += way[0] #vertical movement on the matrix
            self.index[1] += way[1] #horizontal movement on the matrix
        self.update_coor()


class one:
    def __init__(self,tx,ly,length,i,j,screen,barrier=False):
        self.tx=tx
        self.ly=ly
        self.length=length
        self.barrier=barrier
        #self.draw = self.rect(barrier,tx,ly,length,screen)
        
        self.index = (j,i)
        self.color = self.mode(barrier)
        self.coordinates = (tx,ly,length,length)
        self.role = 0 #if role is 0, box is just a path. if role is 1 start if 2 finish part.
        self.Q = [0,0,0,0] #[up,down,left,right] if a value is -2 that means agent is not able to move that direction
                           #like corners.
                           #if all is -2 that means is a barrier.
    def mode(self,barrier):
        if barrier:
            return (255,0,0) #red
        else:
            return (255,255,255) #white


def convert(mode,x,y):
    #NOTE:fixed for 50x50 matrix and 1000x1100 window
    if(mode == "pixel"): #converts pixel coorinates into matrix indexes
        #round() function can also be used
        i = (y-y%20)/20
        j = (x-x%20)/20
        return (int(i),int(j))
    if(mode == "index"):
        i = y*20
        j = x*20
        return (i,j)
    else:
        print("convert mode typed wrong")
