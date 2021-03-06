# import gym

import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from utilities import *
from models import *
# problem = "Pendulum-v0"
# model = gym.make(problem)
dt = 0.5
# num_states = model.observation_space.shape[0]
# num_actions = model.action_space.shape[0]

# upper_bound = model.action_space.high[0]
# lower_bound = model.action_space.low[0]
# state = model.reset()

# next_state, reward, done, info =model.step([0])
# print(next_state)
# Create an agent instance
from pylab import *

tf = 5
steps = 0.05
ttt = np.arange(0, tf + steps, steps)
controls = np.array([[1]])  # for _ in range(ttt.size-1)]])
x0 = np.array([0, 0])

m = simple_CSTR()
m.reset()
print(m.reset())
model = simple_CSTR()  # model_double_intergator()
N_h = 5
store_u = True
history = cosntract_history(model, N_h, store_u=store_u)
agent = ActorCriticAgent(history, network=PTACNetwork)
print(2)
# Define number of episodes to train for
num_episodes = 500
# Create a buffer for calculating the last 100 episode average reward
scores_buffer = deque(maxlen=150)
# List to store each episode's total reward
scores = []
# List to store the average reward after each episode
avg_scores = []
# Run the training loop
u_his = np.zeros([model.nu,501,num_episodes])
x_his = np.zeros([model.nx,501,num_episodes])

for ep in range(num_episodes):
    # Save the initial state
    x0 = model.reset()
    t = 0
    # Reset the total reward
    hist_states = cosntract_history(model, N_h, store_u=store_u)
    state       = (hist_states.history).copy()
    total_reward = 0
    # Reset the episode terminal condition
    done = False
    i = 0
    d = 0.
    if ep == num_episodes - 1:
        states = []
        uu = []

    while t < 10:  # not done:
        # if t%100==0:
        #   state = xx[ep*t+1]
        # Query the agent for an action to take in the state
        # Change the state to get previous states and deviations
        # for ii in range(100):




        u = agent.get_action(np.array(state))#state))



        #     k = 0
        #     for i in range(model.nu):
        #         if u[i]>model.u_min-0.00001 and u[i]<model.u_max+0.00001:
        #            k+=1
        #     if k==model.nu:
        #         break
        # Take the action in the environment
        # next_state, reward, done, info =model.step(u)  # Change this to run with the regular funcs
        # print('before: ', u)
        # if ep >3:


        # print('after: ', u)
        for k in range(model.nu):
            if u[k]<model.u_min:
                u[k] = model.u_min
            elif u[k]>model.u_max:
                u[k] = model.u_max
        u_his[:,i,ep] = u
        x_his[:,i,ep] = x0
        i+=1

        if ep == num_episodes - 1:
            uu += [u]
            states += [x0]

        x1, reward, done = model.simulation(u.reshape((-1,)), model.dt, np.array([x0[0]]).reshape((-1,)))
        x0 = x1.copy()

        next_state = hist_states.append_history(x1, u)
        #next_state = x1
        # next_state, reward, done =model.simulate(state, u, t, 0.0)# model.step(u)  # Change this to run with the regular funcs
        # next_state += 0.2*np.random.rand()
        # Train the agent with the new time step experience
        agent.train(state, u, next_state, reward, int(done))
        # Update the episode's total reward
        total_reward += reward
        # Update the current state
        state = next_state.copy()

        # algebraic equations


        t += model.dt



    # Store the last episode's total reward
    scores.append(total_reward)
    # Add the total reward to the buffer for calculating average reward
    scores_buffer.append(total_reward)
    # Store the new average reward
    avg_scores.append(np.mean(scores_buffer))
    print("Episode: ", ep, "Score: ", scores[ep], "Avg reward: ", avg_scores[ep])

plt.plot(states)
print(2)



u_test = np.zeros([model.nu,501,num_episodes])
x_test = np.zeros([model.nx,501,num_episodes])
for ep in range(1):
    # Save the initial state
    x0 = model.reset()
    t = 0
    # Reset the total reward
    hist_states = cosntract_history(model, N_h, store_u=store_u)
    state       = (hist_states.history).copy()
    total_reward = 0
    # Reset the episode terminal condition
    done = False
    i = 0
    d = 0.
    if ep == num_episodes - 1:
        states = []
        uu = []

    while t < 10:  # not done:
        # if t%100==0:
        #   state = xx[ep*t+1]
        # Query the agent for an action to take in the state
        # Change the state to get previous states and deviations
        # for ii in range(100):




        u = agent.get__deterministic_action(np.array(state))#state))



        #     k = 0
        #     for i in range(model.nu):
        #         if u[i]>model.u_min-0.00001 and u[i]<model.u_max+0.00001:
        #            k+=1
        #     if k==model.nu:
        #         break
        # Take the action in the environment
        # next_state, reward, done, info =model.step(u)  # Change this to run with the regular funcs
        # print('before: ', u)
        # if ep >3:


        # print('after: ', u)
        # for k in range(model.nu):
        #     if u[k]<model.u_min:
        #         u[k] = model.u_min
        #     elif u[k]>model.u_max:
        #         u[k] = model.u_max
        u_test[:,i,ep] = u
        x_test[:,i,ep] = x0
        i+=1

        if ep == num_episodes - 1:
            uu += [u]
            states += [x0]

        x1, reward, done = model.simulation(u.reshape((-1,)), model.dt, np.array([x0[0]]).reshape((-1,)))
        x0 = x1.copy()

        next_state = hist_states.append_history(x1, u)
        #next_state = x1
        # next_state, reward, done =model.simulate(state, u, t, 0.0)# model.step(u)  # Change this to run with the regular funcs
        # next_state += 0.2*np.random.rand()
        # Train the agent with the new time step experience
        agent.train(state, u, next_state, reward, int(done))
        # Update the episode's total reward
        total_reward += reward
        # Update the current state
        state = next_state.copy()

        # algebraic equations


        t += model.dt
