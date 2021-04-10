## Procedure to make A matrix

We initialise an array with dimensions `number of states`,`number of state action pairs`, with every entry in the array being zero. This is done by the `init_A()` function.

``` code
def init_A():
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
```

Then for each state action pair **k**, we subtract the probability **p** of **k** leading to state **s** from the entry in A that represents the state action pair **k** with the state **s**. i.e. A[**s**][**k**] -= **p**.

Now, say we are at state action pair **k**. **k**'s corresponding state, i.e. the state at which this state action occurs, is say **h**. Then we add 1 to the entry in A represents the state action pair **k** with the state **h**.
i.e. A[**h**][**k**] += **1**.

All of this is done in the in `edit_A()` function

``` code
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
```

## Procedure to find policy

We get a value associated with every state action pair. We group the state action pairs by state, and choose the state action pair with the maximum value associated to it when compared to the other state action pairs in its group.

## Policy analysis

We compared this policy to the policy obtained by value iteration. There were differences only for two states. We associate these differences to inaccuracy due to gamma, in value iteration. The action chosen via value iteration, had very similar value to the action chosen by LP in the LP's state-action table. 

In North state, we observe that if he has enough arrows to kill the dragon, the dragon is dormant, or if he can't craft arrows, he will go DOWN. If he doesnt have enough arrows to kill the dragon but he has materials, he prefers to CRAFT. If he can't craft, and the dragon is active, and he can't kill the dragon with his current set of arrows, then he will STAY.

In South state, we observe that if the dragon is active, and he can gather, he prefers to GATHER. If he can't gather but the dragon is active, then he STAYS. When he dragon is dormant, he mostly goes UP.

In East state, if he has arrows, and the dragon has a low health, he will SHOOT. If he doesnt have any arrows or if the dragon has high health, he will HIT.

In West state, if he has arrows, sometimes he will SHOOT, but most of the time, he simply goes RIGHT.

In Center state, if the dragon is active, then he will either go DOWN or UP or WEST, depending on the number of materials and arrows he has. If the dragon is dormant, he will go RIGHT mostly, but depending on the dragon's health, he might go UP or DOWN to get materials or to craft arrows.


## Multiple Policy Analysis

For the same A, R and alpha there can only be multiple policies if two state action pairs for the same state have the same value. Then we can choose which action to take, as both are equally favorable.

Other than that we can change alpha such that instead of making all the states equally likely to start with, we have a initial pool of some states from where we can start.