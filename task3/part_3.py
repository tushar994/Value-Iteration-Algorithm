A = []
R = []
alpha = []
number_state_actions = 0
state_action_array = []
# N = 0, S = 1, E = 2, W = 3, C = 4
# Dormant = 0, active = 1
# position, arrows, materials, health, status

from all_states import ret_val
from rewards import ret_val_reward
import cvxpy as cp
import numpy as np
import json

def init_val():
    number_state_actions = 0
    for positions2 in range(0,5):
        for arrows2 in range(0,4):
            for materials2 in range(0,3):
                for health2 in range(0,5):
                    for status2 in range(0,2):
                        for action in all_actions([positions2,arrows2,materials2,health2,status2]):
                            number_state_actions+=1
    return number_state_actions

def all_actions(state):
    actions = []
    if(state[3]==0):
        return ["NONE"]
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

def init_A():
    # A = np.zeros((600,number_state_actions))
    for positions in range(0,5):
        for arrows in range(0,4):
            for materials in range(0,3):
                for health in range(0,5):
                    for status in range(0,2):
                        to_append = []
                        for positions2 in range(0,5):
                            for arrows2 in range(0,4):
                                for materials2 in range(0,3):
                                    for health2 in range(0,5):
                                        for status2 in range(0,2):
                                            for action in all_actions([positions2,arrows2,materials2,health2,status2]):
                                                to_append.append(0)
                        A.append(to_append)


def create_R():
    for positions2 in range(0,5):
        for arrows2 in range(0,4):
            for materials2 in range(0,3):
                for health2 in range(0,5):
                    for status2 in range(0,2):
                        for action in all_actions([positions2,arrows2,materials2,health2,status2]):
                            R.append(ret_val_reward([positions2,arrows2,materials2,health2,status2], action , 0))

def create_alpha():
    for positions2 in range(0,5):
        for arrows2 in range(0,4):
            for materials2 in range(0,3):
                for health2 in range(0,5):
                    for status2 in range(0,2):
                        alpha.append([1/600])

def find_state_index(state):
    index = 0
    for i in range(0,5):
        for j in range(0,4):
            for k in range(0,3):
                for l in range(0,5):
                    for m in range(0,2):
                        for a in all_actions([i,j,k,l,m]):
                            # print(str(index) + ":("+str(i)+","+str(j)+","+str(k)+","+str(l)+","+str(m)+","+str(a)+")")
                            state_action_array.append([i,j,k,l,m,a])
                            index+=1
                        

def find_state_index2(state):
    return state[0]*120 + state[1]*30 + state[2]*10 + state[3]*2 + state[4]

def edit_A():
    start_state_index = 0
    action_state_index = 0
    for positions2 in range(0,5):
        for arrows2 in range(0,4):
            for materials2 in range(0,3):
                for health2 in range(0,5):
                    for status2 in range(0,2):
                        for action2 in all_actions([positions2,arrows2,materials2,health2,status2]):
                            array_fin = ret_val([positions2,arrows2,materials2,health2,status2], action2, 0)
                            # flag_kunwar = 1
                            for end_state in array_fin:
                                # if(find_state_index2(end_state[0])!=start_state_index):
                                A[find_state_index2(end_state[0])][action_state_index] -= end_state[1]
                            # if(flag_kunwar):
                            A[start_state_index][action_state_index] +=1
                            action_state_index+=1
                        start_state_index+=1

# N = 0, S = 1, E = 2, W = 3, C = 4
def bring_string_pos(a):
    if(a==0):
        return 'N'
    if(a==1):
        return 'S'
    if(a==2):
        return 'E'
    if(a==3):
        return 'W'
    else:
        return 'C'

def bring_string_ready(a):
    if(a==0):
        return 'D'
    else:
        return 'R'
def make_action_correct(a):
    if(a=='SHOOT_ARROW'):
        return 'SHOOT'
    elif(a=='HIT_SWORD'):
        return 'HIT'
    elif(a=='CRAFT_ARROWS'):
        return 'CRAFT'
    elif(a=='GATHER_MATERIALS'):
        return 'GATHER'
    else:
        return a


final_print_dict = {}
number_state_actions = init_val()
init_A()
edit_A()


# np.set_printoptions(threshold=np.inf)

# print(np.array(A))
create_R()

# for ele in R:
#     print(ele)
create_alpha()

# print(alpha)
find_state_index("haha")
                        
x = cp.Variable(shape=( number_state_actions, 1), name="x")
# A = np.array(A)
# print(A)

# print(find_state_index([0,0,0,0,0]))
A = np.array(A)
alpha = np.array(alpha)
R = np.array(R)
# print(str(len(A))+","+str(len(A[0])))


# print(number_state_actions)
constraints = [cp.matmul( A, x) == alpha, x>=0]
objective = cp.Maximize(cp.matmul(R,x))
problem = cp.Problem(objective, constraints)

solution = problem.solve()
print(solution)
print(x.value)
final_print_dict['a'] = [list(val) for val in A]
final_print_dict['alpha'] = [val[0] for val in alpha]
final_print_dict['r'] = [ val for val in R]
final_print_dict['x'] = [val[0] for val in x.value]
final_print_dict['objective'] = solution
# for index,value in enumerate(x.value):
#     print(str(state_action_array[index]) + ":" + str(value))
# position, arrows, materials, health, status
final_array = {}
for index,value in enumerate(x.value):
    state_string = str(str(state_action_array[index][0])+","+str(state_action_array[index][1])+","+str(state_action_array[index][2])+","+str(state_action_array[index][3])+","+str(state_action_array[index][4]))
    state_array_to_store = [ bring_string_pos(state_action_array[index][0]) , state_action_array[index][2], state_action_array[index][1], bring_string_ready(state_action_array[index][4]) , 25*state_action_array[index][3]]
    if(state_string in final_array):
        if(final_array[state_string][0]<=value):
            final_array[state_string] = [value,state_action_array[index][5], state_array_to_store]

    else:
        final_array[state_string] = [value,state_action_array[index][5], state_array_to_store]

policy_array = []

for i in final_array.keys():
    # print(str(final_array[i][2]) + ":" + str(final_array[i][1]))
    policy_array.append([final_array[i][2],make_action_correct(final_array[i][1])])

# print(policy_array)
# for val in policy_array:
    # print(val)
final_print_dict['policy'] = policy_array

output = open('part_3_output.json', 'w')
json.dump(final_print_dict, output)