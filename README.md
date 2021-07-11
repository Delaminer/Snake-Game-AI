# Snake-Game-AI
In this project, I learned how to make games in Python, made [Snake](https://en.wikipedia.org/wiki/Snake_(video_game_genre)), and how to make an artificial intelligence play Snake.

## Steps
I first learned how to make games with python using pygame, following [this tutorial](https://realpython.com/pygame-a-primer/), which is located in the [Learn PyGame](https://github.com/Delaminer/Snake-Game-AI/tree/master/Learn%20PyGame) folder.

After this, I made my own Snake game, which is in the [My Attempt 1](https://github.com/Delaminer/Snake-Game-AI/tree/master/My%20Attempt%201) folder.

With this Snake game, I tried to use TensorFlow for the AI. After several attempts, I was unable to do so and so I looked into doing it another way.

I found [this tutorial](https://www.youtube.com/watch?v=PJl4iabBEz0&list=PLqnslRFeH2UrDh7vUmJ60YrmWd64mTTKV), which did work, which is located in the [Full Tutorial](https://github.com/Delaminer/Snake-Game-AI/tree/master/Full%20tutorial) folder. This tutorial uses PyTorch instead of TensorFlow, which I found much easier to use.

Using what I learned from that tutorial, I added PyTorch to my Snake game, which is in the [My Attempt 2](https://github.com/Delaminer/Snake-Game-AI/tree/master/My%20Attempt%202) folder.

## About the AI
This AI uses Reinforcement Learning, it learns from the rewards it receives (positive rewards when picking up fruit, negative rewards when losing) when performing actions (moving around the board) to decide how to act in the future. It also uses Deep Q learning because a deep neural network is netword is used to make decisions (a deep neural network is one or more hidden layers between the sensor input and the calculated output).

## Performance
It usually takes the snake around 80 games to become good. This could be because after 80 games, the snake never takes random moves (it initially moves randomly to learn more about the environment, called 'exploration vs exploitation').

Here is a graph of its results after 100 games (the blue line is each game's score, the orange line is the average score over time):

![Graph of 100 games](https://github.com/Delaminer/Snake-Game-AI/blob/master/Media/Graph%20100.png)

After around 100 games, the snake does not improve its score- the score varies between 10 and 60, averaging around 35.

Here is a graph of its results after 750 games:

![Graph of 750 games](https://github.com/Delaminer/Snake-Game-AI/blob/master/Media/Graph%20after%20game%20750.png)

Here it is playing after around 600 rounds:

![late game](https://github.com/Delaminer/Snake-Game-AI/blob/master/Media/ending.gif)

Its highest score I have seen has been 75, after 128 games. Here is a screenshot of it and a GIF of the game:

![Highscore image](https://github.com/Delaminer/Snake-Game-AI/blob/master/Media/highscore.png)
![Highscore image](https://github.com/Delaminer/Snake-Game-AI/blob/master/Media/highscore%20game.gif)

You can see all of the recordings I took in the [Media](https://github.com/Delaminer/Snake-Game-AI/tree/master/Media) folder.
