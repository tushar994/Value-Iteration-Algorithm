# N = 0, S = 1, E = 2, W = 3, C = 4
# Dormant = 0, active = 1
# position, arrows, materials, health, status

from config import *
from transition_table import *

dif = 0.001
delta = 0.001

def init_V():
    for positions in range(0,5):
        V.append([])
        for arrows in range(0,4):
            V[positions].append([])
            for materials in range(0,3):
                V[positions][arrows].append([])
                for health in range(0,5):
                    V[positions][arrows][materials].append([])
                    for status in range(0,2):
                        V[positions][arrows][materials][health].append([])
                        for index in range(0,1):
                            V[positions][arrows][materials][health][status].append(0)





def all_actions(state):
    actions = []
    if(state[0]==4):
        actions.append('UP')
        actions.append('LEFT')
        actions.append('RIGHT')
        actions.append('DOWN')
        actions.append('STAY')
    if(state[0]==0):
        actions.append('DOWN')
        actions.append('STAY')
    if(state[0]==1):
        actions.append('UP')
        actions.append('STAY')
    if(state[0]==2):
        actions.append('LEFT')
        actions.append('STAY')
    if(state[0]==3):
        actions.append('RIGHT')
        actions.append('STAY')

    if((state[0]==4 or state[0]==3 or state[0]==2) and state[1]>0):
        actions.append('SHOOT_ARROW')
    
    if( (state[0]==4 or state[0]==2) ):
        actions.append('HIT_SWORD')
    
    if( (state[0]==0) and state[2]>0):
        actions.append('CRAFT_ARROWS')
    
    if(state[0]==1):
        actions.append('GATHER_MATERIALS')
    return actions



def value_iterator(index):
    max_dif = 0.001
    for positions in range(0,5):
        for arrows in range(0,4):
            for materials in range(0,3):
                for health in range(0,5):
                    for status in range(0,2):
                        state  = [positions,arrows, materials, health, status]
                        actions = all_actions(state)
                        final = ret_val(state,actions[0],index)
                        # print(final)
                        for action in actions:
                            ret_val_val = ret_val(state,action,index)
                            final = max(final, ret_val_val)
                            print("state: " + str(state), end = "")
                            print(" action: " + action , end = " ")
                            print(ret_val_val)

                        V[positions][arrows][materials][health][status].append(final)
                        max_dif = max(max_dif, abs(V[positions][arrows][materials][health][status][index] - V[positions][arrows][materials][health][status][index-1])  )

    return max_dif

                            


init_V()
# print((V[0][0][0][0][0]))
index = 1
while(dif>=0.001):
    print("index: " + str(index))
    dif = value_iterator(index)
    # print("dif:  " +  str(dif))
    # print("\033[F", end = "")
    if(dif<0.001):
        break
    index += 1

