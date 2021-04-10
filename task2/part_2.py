# N = 0, S = 1, E = 2, W = 3, C = 4
# Dormant = 0, active = 1
# position, arrows, materials, health, status

from config import *
from transition_table import *
import matplotlib.pyplot as plt

dif = 0.001
delta = 0.001

def init_V():
    for positions in range(0,5):
        V.append([])
        Act.append([])
        for arrows in range(0,4):
            V[positions].append([])
            Act[positions].append([])
            for materials in range(0,3):
                V[positions][arrows].append([])
                Act[positions][arrows].append([])
                for health in range(0,5):
                    V[positions][arrows][materials].append([])
                    Act[positions][arrows][materials].append([])
                    for status in range(0,2):
                        V[positions][arrows][materials][health].append([])
                        Act[positions][arrows][materials][health].append([])
                        for index in range(0,1):
                            V[positions][arrows][materials][health][status].append(0)
                            Act[positions][arrows][materials][health][status].append(0)





def all_actions(state):
    actions = []
    if(state[3]==0):
        return []
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

def state_string(state):
    position = ""
    if(state[0]==0):
        position="(N"
    elif(state[0]==1):
        position="(S"
    elif(state[0]==2):
        position="(E"
    elif(state[0]==3):
        position="(W"
    elif(state[0]==4):
        position="(C"
    
    position += ","
    position+= str(state[2])
    position += ","
    position+= str(state[1])
    position += ","
    if(state[4]):
        position+="A,"
    else:
        position+="D,"
    position+=str(25*state[3])
    position+=")"
    return position

max_difs = []
x_inverse = []
def value_iterator(index):
    max_dif = 0.00001
    avg_dif = 0
    avg_index = 0
    for positions in range(0,5):
        for arrows in range(0,4):
            for materials in range(0,3):
                for health in range(0,5):
                    for status in range(0,2):
                        state  = [positions,arrows, materials, health, status]
                        actions = all_actions(state)
                        if(len(actions)>0):
                            final = ret_val(state,actions[0],index)
                            pref_action = actions[0]
                            # print(final)
                            for action in actions:
                                ret_val_val = ret_val(state,action,index)
                                final = max(final, ret_val_val)
                                if(final==ret_val_val):
                                    pref_action = action
                                # print("state: " + str(state), end = "")
                                # print(" action: " + action , end = " ")
                                # print(ret_val_val)

                            V[positions][arrows][materials][health][status].append(final)
                            Act[positions][arrows][materials][health][status].append(pref_action)
                            print(state_string([positions,arrows,materials,health,status]), end ="")
                            print(":" + pref_action + "=[",end = "")
                            print(round(final,3), end = "")
                            print("]")
                            max_dif = max(max_dif, abs(V[positions][arrows][materials][health][status][index] - V[positions][arrows][materials][health][status][index-1])  )
                            avg_dif += abs(V[positions][arrows][materials][health][status][index] - V[positions][arrows][materials][health][status][index-1])
                            avg_index+=1
                        else:
                            V[positions][arrows][materials][health][status].append(0)
                            Act[positions][arrows][materials][health][status].append("NONE")
                            print(state_string([positions,arrows,materials,health,status]), end ="")
                            print(":" + "NONE" + "=[",end = "")
                            print(0, end = "")
                            print("]")
                            avg_index+=1
    # print(max_dif)
    max_difs.append(avg_dif/avg_index)
    return max_dif

                            


init_V()

index = 1
while(dif>=0.001):
    # print("index: " + str(index))
    print("iteration="+str(index-1))
    dif = value_iterator(index)
    if(dif<0.001):
        break
    index += 1

# plt.plot(max_difs)
# plt.show()