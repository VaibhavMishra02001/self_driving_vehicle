import highway_env
import numpy as np
import random
import gym
import highway_env
from matplotlib import pyplot as plt


#constants
alpha = 0.1
gamma = 0.9
epsilon = 1.0

env = gym.make('highway-v0')
env.configure({
    "observation": {
        "type": "LidarObservation",
        "vehicles_count": 15,
        "maximum_range" : 20,
        "cells" : 8,
    },
    "absolute": False,
    "action" : {
        "type" : "DiscreteMetaAction",
        "lateral" : True,
        "target_speed" :30
    }
})


#def discretizeDistance(d):
 #   if(d>=0 and d<0.33):
  #      return 2
   # elif(d>=0.33 and d<0.67):
    #    return 1
    #elif(d>=0.67 and d<=1):
     #   return 0

#def hashing(a,b,c,d,e):
 #    return(a +(3*b)+(9*c)+(27*d)+(81*e))
     
def epsilon_greedy(hash ,epsilon):
    action = 0
    
    #explore:
    if np.random.uniform(0,1) < epsilon:
        action = random.choice([0,1,2])
        
    #greedy policy:
    else:
        t= max(q[hash])
        action = q[hash].index(t)
    return action
s =[]
q={}
ep = []
ep_rew =[]


for episode in range(3000):
    obs=env.reset()
    currentState = [(obs[0][0]), (obs[1][0]),(obs[2][0]), obs[6][0], (obs[7][0])]

    S = min(currentState)
        

   # p= hashing(discretizeDistance(obs[0][0]), discretizeDistance(obs[2][0]), discretizeDistance(obs[4][0]), discretizeDistance(obs[12][0]), discretizeDistance(obs[14][0]))    
    
    ep_reward = 0
    epsilon = epsilon- (1/2000)
    #if currentState not in s:
        #s.append(currentState)
    #if q.get(p) is None: 
    q[S]=[0.0,0.0,0.0]
        
    
   

    
    truncated = False
    while(not truncated):
        a1 = epsilon_greedy(S, epsilon)
        env.render()
        #if episode%200==0:
         #   env.render()
        obs ,reward, truncated,info= env.step(a1)
        
        nextState= [(obs[0][0]), (obs[1][0]), (obs[2][0]), (obs[6][0]), (obs[7][0])]
        #r= hashing(discretizeDistance(obs[0][0]), discretizeDistance(obs[2][0]), discretizeDistance(obs[4][0]), discretizeDistance(obs[12][0]), discretizeDistance(obs[14][0]))    
        nS = min(nextState)
        
        #if nextState not in s:
          #s.append(nextState) 
        #if q.get(r) is  None :  
        q[nS]=[0.0,0.0,0.0]


    
        
        a2 = epsilon_greedy(nS, 0)


        q[S][a1]=  q[S][a1]+ alpha*(reward + gamma*(max(q[nS]))-q[S][a1])

        #print(q)
        S= nS
        #currentState = nextState
        #a1 =a2
        #action1 =  epsilon_greedy(r, epsilon)
        ep_reward +=reward
        #plt.imshow(env.render(mode="rgb_array")) 
    print(episode)
    print(ep_reward)
    #if(len(ep)%250==0):
     # plt.figure()
      #plt.plot(ep, ep_rew)
      #plt.show()   
    ep_rew.append(ep_reward)
    ep.append(episode)
plt.figure()
plt.plot(ep, ep_rew)
plt.show()
     

   
        




   