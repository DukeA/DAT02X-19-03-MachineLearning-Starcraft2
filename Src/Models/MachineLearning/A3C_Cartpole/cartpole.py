import gym
import numpy as np
import random



from A3C_agent import A3CAgent
from collections import deque

num_iters = 100000
training_interval = 1
batch_size = 20
action_space = [0, 1]
discount_factor = 0.95
exploration_factor = 0.9
min_exploration_rate = 0.01

env = gym.make("CartPole-v1")
observation = env.reset()
iter = 0
episode = 0

agent = A3CAgent(state_dim=4, action_dim=2, action_space=action_space, discount_factor=discount_factor)
#buffer = Buffer(size=10000)
buffer = deque(maxlen=100)

next_state = [0, 0, 0, 0]
total_reward = 0

#plt.axis([0, num_iters/100, 0, 1000])

while iter < num_iters:

  iter += 1
  env.render()

  state = next_state
  r = random.random()
  if r < exploration_factor:
    action = env.action_space.sample() # your agent here (this takes random actions)
  else:
    action = agent.predict_action(state)
  next_state, reward, done, info = env.step(action)
  reward = reward if not done else -reward
  buffer.append([state, action, reward, next_state, done])
  total_reward += reward

  if iter % training_interval == 0 and iter >= batch_size:
    #training_batch = buffer.get_random_batch(batch_size)
    training_batch = random.sample(buffer, batch_size)
    agent.train(training_batch)

  if done:
    observation = env.reset()
    print("Total reward: ", total_reward)

    total_reward = 0
    episode += 1
    if episode % 100 == 0:
      print('#################')
      print('Exploration factor: ', exploration_factor)
      print('#################')

  if iter == num_iters:
    env.close()


  if exploration_factor > min_exploration_rate:
    exploration_factor *= 0.995




env.close()
