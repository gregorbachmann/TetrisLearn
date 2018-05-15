# How To Play Tetris With Deep-Q-Learning


# Overview

Our initial goal in this project was to get acquainted with the idea of Reinforcement Learning, ideally via progamming it with a simple example. Inspired as many others by DeepMind and their success with letting Neural Networks play Atari-Games, we decided to choose a similar example. Since we both weren't familiar with importing these games directly, emulators and stuff, we chose a game that is relatively easy to implement, Tetris. Writing the game ourselves allowed us to directly implement all the functions, which made the training process easier (but debugging harder...). We followed the approach of **DeepMind**, namely using Deep-Q-Learning and directly feeding the raw pixels of our game into the Convolutional Neural Network. I will describe the theory and the architecture used in the next paragraph. As it turns out (so far at least), Tetris was a bad choice (It would have been worth it to check for existing papers before programming the stuff for weeks..). The game structure (obviously) asks for relatively long-term decisions, since you cannot really associate a reward with a decision immediately. Blinded by all the Machine Learning Magic, we thought that it will somehow work, I mean we're using a Convolutional Neural Net, nothing can go wrong, right?


# The Theory of Reinforcement Learning

Let's first get to dry theory. How the hack is it possible to let an agent learn how to play games??
We first need to introduce some definitions. I will always give an example for these definitions using our implementation of Tetris.
  * **Agent**:  Our AI that will learn to play the game. 
                In the case of Tetris this will be our Convolutional Neural Network. 
  * **Environment**: The system our agent interacts with. This will simply be the Tetris Game.
  * **State**:  An instance of the environment that our agent will be able to observe at time t.
                In the case of Tetris, this will be a snapshot of the game.
  * **Action**: Actions that our agent can take in order to change the current state. In Tetris, this will either be *Wait*, *Left*, 
                *Right* or *Rotate*.
  * **Reward**: The points that our agent gets for changing the current state by performing a certain action. In our case the agent gets   
                points if it places the current element in the row.
  
