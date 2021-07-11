# Snake-Game-AI
In this project, I learned how to make games in Python, made [Snake](https://en.wikipedia.org/wiki/Snake_(video_game_genre)), and how to make an artificial intelligence play Snake.

## Steps
I first learned how to make games with python using pygame, following [this tutorial](https://realpython.com/pygame-a-primer/), which is located in the Learn PyGame folder.

After this, I made my own Snake game, which is in the My Attempt 1 folder.

With this Snake game, I tried to use TensorFlow for the AI. After several attempts, I was unable to do so and so I looked into doing it another way.

I found [this tutorial](https://www.youtube.com/watch?v=PJl4iabBEz0&list=PLqnslRFeH2UrDh7vUmJ60YrmWd64mTTKV), which did work, which is located in the Full Tutorial folder. This tutorial uses PyTorch instead of TensorFlow, which I found much easier to use.

Using what I learned from that tutorial, I added PyTorch to my Snake game, which is in the My Attempt 2 folder.

## About the AI
This AI uses Reinforcement Learning, it learns from the rewards it receives (positive rewards when picking up fruit, negative rewards when losing) when performing actions (moving around the board) to decide how to act in the future. It also uses Deep Q learning because a deep neural network is netword is used to make decisions (a deep neural network is one or more hidden layers between the sensor input and the calculated output).
