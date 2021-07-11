import torch
import random
import numpy as np
from collections import deque
from my_snake import Snake
from model import Linear_QNet, QTrainer
# from new_model import Linear_QNet, QTrainer
from helper import plot
import os


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
SAVE_INTERVAL = 30

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft
        # self.model = Linear_QNet([11, 256, 256, 3])
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def load(self, path):
        temp = torch.load(path)
        self.model.load_state_dict(temp)
        self.model.eval()

    def get_state(self, game):
        return game.get_state()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, useRandom=True):
        # random moves: tradeoff between exploration and exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if useRandom and random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Snake(game_speed=100)
    
    while True:
        # Get old game state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.step(final_move, agent.n_games)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train the long memory, plot results
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save(file_name='NewRecordModel.pth')
            
            if agent.n_games % SAVE_INTERVAL == 0:
                agent.model.save(file_name='AutoSaveModel.pth')


            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)



def eval(file_name='NewRecordModel.pth'):
    
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Snake()

    # Load saved model
    model_folder_path = './model'
    agent.load(os.path.join(model_folder_path, file_name))
    
    while True:
        # Get old game state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old, random=False)

        # perform move and get new state
        reward, done, score = game.step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        #agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        #agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train the long memory, plot results
            game.reset()
            agent.n_games += 1
            #agent.train_long_memory()

            # if score > record:
            #     record = score
            #     agent.model.save(file_name='NewRecordModel.pth')
            
            # if agent.n_games % SAVE_INTERVAL == 0:
            #     agent.model.save(file_name='AutoSaveModel.pth')


            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()
    # eval(file_name='model.pth')
