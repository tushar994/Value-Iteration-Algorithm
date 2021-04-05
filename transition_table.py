
from config import *

gamma = 0.999
step_cost = -10

# N = 0, S = 1, E = 2, W = 3, C = 4
# Dormant = 0, active = 1
# position, arrows, materials, health, status

# state is an array with 5 values that tells us current state
# action is a string
# assume the action state pair is valid

def gain_arrows(cur_number):
    if(cur_number >=3):
        return 3
    else:
        return cur_number

def gain_materials(cur_number):
    if(cur_number >=2):
        return 2
    else:
        return cur_number

def kill_monster_reward(health):
    if(health<=0):
        return 50
    else:
        return 0
    


def dormant_to_active(state, prob, index):
    return ( prob*0.2*(step_cost + kill_monster_reward(state[3]) + gamma*( V[state[0]][state[1]][state[2]][state[3]][1][index-1]  )) + prob*0.8*( step_cost + kill_monster_reward(state[3]) + gamma*( V[state[0]][state[1]][state[2]][state[3]][0][index-1] )) )

def active_to_dormant(init_pos, init_state ,state, prob, index):
    if(init_pos==4 or init_pos==2):
        return ( 0.5*prob*( -40 + gamma*(  V[init_pos][0][init_state[2]][min(4,init_state[3] + 1)][0][index-1]  )  ) + 0.5*prob*( step_cost + kill_monster_reward(state[3]) + gamma*(  V[state[0]][state[1]][state[2]][state[3]][state[4]][index-1]  )) )
    else:
        return ( 0.5*prob*( step_cost + kill_monster_reward(state[3]) + gamma*(  V[state[0]][state[1]][state[2]][state[3]][0][index-1]  )  ) + 0.5*prob*( step_cost + kill_monster_reward(state[3]) + gamma*(  V[state[0]][state[1]][state[2]][state[3]][state[4]][index-1]  )) )



def ret_val(state, action, index):
    # print(state)
    # print(action)
    if(state[4]==0):
        if(state[0] == 4):
            if(action=='UP'):
                return (dormant_to_active([0,state[1],state[2],state[3],state[4]], 0.85, index ) + dormant_to_active([2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='DOWN'):
                return (dormant_to_active([1,state[1],state[2],state[3],state[4]], 0.85, index ) + dormant_to_active([2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='RIGHT'):
                return (dormant_to_active([2,state[1],state[2],state[3],state[4]], 0.85, index ) + dormant_to_active([2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='LEFT'):
                return (dormant_to_active([3,state[1],state[2],state[3],state[4]], 0.85, index ) + dormant_to_active([2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='STAY'):
                return (dormant_to_active([4,state[1],state[2],state[3],state[4]], 0.85, index ) + dormant_to_active([2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='SHOOT_ARROW'):
                return (dormant_to_active([4,state[1]-1,state[2],state[3]-1,state[4]], 0.5, index ) + dormant_to_active([4,state[1]-1,state[2],state[3],state[4]], 0.5, index ))
            if(action=='HIT_SWORD'):
                return (dormant_to_active([4,state[1],state[2],state[3]-2,state[4]], 0.1, index ) + dormant_to_active([4,state[1],state[2],state[3],state[4]], 0.9, index ))
            
        if(state[0]== 0):
            # print("whlo1")
            if(action=='DOWN'):
                # print("hello")
                return (dormant_to_active([4,state[1],state[2],state[3],state[4]], 0.85, index ) + dormant_to_active([2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='STAY'):
                return (dormant_to_active([0,state[1],state[2],state[3],state[4]], 0.85, index ) + dormant_to_active([2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='CRAFT_ARROWS'):
                return (dormant_to_active([0,gain_arrows(state[1]+1),state[2]-1,state[3],state[4]], 0.5, index ) + dormant_to_active([0,gain_arrows(state[1]+2),state[2]-1,state[3],state[4]], 0.35, index ) + dormant_to_active([0,gain_arrows(state[1]+3),state[2]-1,state[3],state[4]], 0.15, index ))
            
        if(state[0]==1):
            if(action=='UP'):
                return (dormant_to_active([4,state[1],state[2],state[3],state[4]], 0.85, index ) + dormant_to_active([2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='STAY'):
                return (dormant_to_active([1,state[1],state[2],state[3],state[4]], 0.85, index ) + dormant_to_active([2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='GATHER_MATERIALS'):
                return (dormant_to_active([1,state[1],gain_materials(state[2]+1),state[3],state[4]], 0.75, index ) + dormant_to_active([1,state[1],state[2],state[3],state[4]], 0.25, index ))

        if(state[0]==2):
            if(action=='LEFT'):
                return (dormant_to_active([4,state[1],state[2],state[3],state[4]], 1, index ) )
            if(action=='STAY'):
                return (dormant_to_active([2,state[1],state[2],state[3],state[4]], 1, index ) )
            if(action=='SHOOT_ARROW'):
                return (dormant_to_active([2,state[1]-1,state[2],state[3]-1,state[4]], 0.9, index ) + dormant_to_active([2,state[1]-1,state[2],state[3],state[4]], 0.1, index ))
            if(action=='HIT_SWORD'):
                return (dormant_to_active([2,state[1],state[2],state[3]-2,state[4]], 0.2, index ) + dormant_to_active([2,state[1],state[2],state[3],state[4]], 0.8, index ))
        
        if(state[0]==3):
            if(action=='RIGHT'):
                return (dormant_to_active([4,state[1],state[2],state[3],state[4]], 1, index ) )
            if(action=='STAY'):
                return (dormant_to_active([3,state[1],state[2],state[3],state[4]], 1, index ) )
            if(action=='SHOOT_ARROW'):
                return (dormant_to_active([3,state[1]-1,state[2],state[3]-1,state[4]], 0.25, index ) + dormant_to_active([3,state[1]-1,state[2],state[3],state[4]], 0.75, index ))
    
        # print("what2")
    # =============================================================================================================================now active to dormant =============================================================================================================================
    else:
        if(state[0] == 4):
            if(action=='UP'):
                return (active_to_dormant(4, state, [0,state[1],state[2],state[3],state[4]], 0.85, index ) + active_to_dormant(4, state,[2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='DOWN'):
                return (active_to_dormant(4, state,[1,state[1],state[2],state[3],state[4]], 0.85, index ) + active_to_dormant(4, state,[2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='RIGHT'):
                return (active_to_dormant(4, state,[2,state[1],state[2],state[3],state[4]], 0.85, index ) + active_to_dormant(4, state,[2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='LEFT'):
                return (active_to_dormant(4, state,[3,state[1],state[2],state[3],state[4]], 0.85, index ) + active_to_dormant(4, state,[2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='STAY'):
                return (active_to_dormant(4, state,[4,state[1],state[2],state[3],state[4]], 0.85, index ) + active_to_dormant(4, state,[2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='SHOOT_ARROW'):
                return (active_to_dormant(4, state,[4,state[1]-1,state[2],state[3]-1,state[4]], 0.5, index ) + active_to_dormant(4, state,[4,state[1]-1,state[2],state[3],state[4]], 0.5, index ))
            if(action=='HIT_SWORD'):
                return (active_to_dormant(4, state,[4,state[1],state[2],state[3]-2,state[4]], 0.1, index ) + active_to_dormant(4, state,[4,state[1],state[2],state[3],state[4]], 0.9, index ))
            
        if(state[0]== 0):
            if(action=='DOWN'):
                return (active_to_dormant(0, state,[4,state[1],state[2],state[3],state[4]], 0.85, index ) + active_to_dormant(0, state,[2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='STAY'):
                return (active_to_dormant(0, state,[0,state[1],state[2],state[3],state[4]], 0.85, index ) + active_to_dormant(0, state,[2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='CRAFT_ARROWS'):
                return (active_to_dormant(0, state,[0,gain_arrows(state[1]+1),state[2]-1,state[3],state[4]], 0.5, index ) + active_to_dormant(0, state,[0,gain_arrows(state[1]+2),state[2]-1,state[3],state[4]], 0.35, index ) + active_to_dormant(0, state,[0,gain_arrows(state[1]+3),state[2]-1,state[3],state[4]], 0.15, index ))
            
        if(state[0]==1):
            if(action=='UP'):
                return (active_to_dormant(1, state,[4,state[1],state[2],state[3],state[4]], 0.85, index ) + active_to_dormant(1, state,[2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='STAY'):
                return (active_to_dormant(1, state,[1,state[1],state[2],state[3],state[4]], 0.85, index ) + active_to_dormant(1, state,[2,state[1],state[2],state[3],state[4]], 0.15, index ))
            if(action=='GATHER_MATERIALS'):
                return (active_to_dormant(1, state,[1,state[1],gain_materials(state[2]+1),state[3],state[4]], 0.75, index ) + active_to_dormant(1, state,[1,state[1],state[2],state[3],state[4]], 0.25, index ))

        if(state[0]==2):
            if(action=='LEFT'):
                return (active_to_dormant(2, state,[4,state[1],state[2],state[3],state[4]], 1, index ) )
            if(action=='STAY'):
                return (active_to_dormant(2, state,[2,state[1],state[2],state[3],state[4]], 1, index ) )
            if(action=='SHOOT_ARROW'):
                return (active_to_dormant(2, state,[2,state[1]-1,state[2],state[3]-1,state[4]], 0.9, index ) + active_to_dormant(2, state,[2,state[1]-1,state[2],state[3],state[4]], 0.1, index ))
            if(action=='HIT_SWORD'):
                return (active_to_dormant(2, state,[2,state[1],state[2],state[3]-2,state[4]], 0.2, index ) + active_to_dormant(2, state,[2,state[1],state[2],state[3],state[4]], 0.8, index ))
        
        if(state[0]==3):
            if(action=='RIGHT'):
                return (active_to_dormant(3,state, [4,state[1],state[2],state[3],state[4]], 1, index ) )
            if(action=='STAY'):
                return (active_to_dormant(3,state,[3,state[1],state[2],state[3],state[4]], 1, index ) )
            if(action=='SHOOT_ARROW'):
                return (active_to_dormant(3,state,[3,state[1]-1,state[2],state[3]-1,state[4]], 0.25, index ) + active_to_dormant(3,state,[3,state[1]-1,state[2],state[3],state[4]], 0.75, index ))

        # print("what")