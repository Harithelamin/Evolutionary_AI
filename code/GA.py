#Genetic algorithm
#- population size: 50
# generation: 2000
#- mutation rate: 0.3
#- crossover rate: 0.9
import gym
import itertools
import numpy as np
import pandas as pd
import random 
import pygame
import time

def run_episode(env, policy, episode_len=100):
    total_reward = 0
    obs = env.reset()
    for t in range(episode_len):
        # env.render()
        action = policy[obs]
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        if done:
            print('Epside finished after {} timesteps.'.format(t+1))
            break
    return total_reward


def evaluate_policy(env, policy, n_episodes=100):
    total_rewards = 0.0
    for _ in range(n_episodes):
        total_rewards += run_episode(env, policy)
    return total_rewards / n_episodes

def gen_random_policy():
    return np.random.choice(4, size=((16)))

def crossover(policy1, policy2):
    new_policy = policy1.copy()
    for i in range(16):
        rand = np.random.uniform()
        if rand > 0.5:
            new_policy[i] = policy2[i]
    return new_policy

def mutation(policy, p=0.05):
    new_policy = policy.copy()
    for i in range(16):
        rand = np.random.uniform()
        if rand < p:
            new_policy[i] = np.random.choice(4)
    return new_policy

if __name__ == '__main__':
    random.seed(1234)
    np.random.seed(1234)
    env = gym.make("CartPole-v1", render_mode="human")
    env.seed()
    n_policy = 100
    n_steps = 20
    start = time.time()
    policy_pop = [gen_random_policy() for _ in range(n_policy)]
    for idx in range(n_steps):
        scores = [evaluate_policy(env, p) for p in policy_pop]
        print('Generation %d : max score = %0.2f' %(idx+1, max(scores)))
        policy_ranks = list(reversed(np.argsort(scores)))
        elite_set = [policy_pop[x] for x in policy_ranks[:5]]
        select_probs = np.array(scores) / np.sum(scores)
        child_set = [crossover(
            policy_pop[np.random.choice(range(n_policy), p=select_probs)], 
            policy_pop[np.random.choice(range(n_policy), p=select_probs)])
            for _ in range(n_policy - 5)]
        mutated_list = [mutation(p) for p in child_set]
        policy_pop = elite_set
        policy_pop += mutated_list
    score = [evaluate_policy(env, p) for p in policy_pop]
    best_policy = policy_pop[np.argmax(score)]

    end = time.time()
    print('Best policy score = %0.2f. Time taken = %4.4f'
            %(np.max(score), (end-start)))    

    ## Evaluation
    env = gym.make("CartPole-v1", render_mode="human")
    for _ in range(200):
        run_episode(env, best_policy)
    env.close()
    
