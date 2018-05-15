# How To Play Tetris With Deep-Q-Learning


# Overview

Our initial goal in this project was to get acquainted with the idea of Reinforcement Learning, ideally via progamming it with a simple example. Inspired as many others by DeepMind and their success with letting Neural Networks play Atari-Games, we decided to choose a similar example. Since we both weren't familiar with importing these games directly, emulators and stuff, we chose a game that is relatively easy to implement, Tetris. Writing the game ourselves allowed us to directly implement all the functions, which made the training process easier (but debugging harder...). We followed the approach of **DeepMind**, namely using Deep-Q-Learning and directly feeding the raw pixels of our game into the Convolutional Neural Network. I will describe the theory and the architecture used in the next paragraph. As it turns out (so far at least), Tetris was a bad choice (It would have been worth it to check for existing papers before programming the stuff for weeks..). The game structure (obviously) asks for relatively long-term decisions, since you cannot really associate a reward with a decision immediately. Blinded by all the Machine Learning Magic, we thought that it will somehow work, I mean we're using a Convolutional Neural Net, nothing can go wrong, right?


# The Theory of Reinforcement Learning

Let's first get to dry theory. How the hack is it possible to let an agent learn how to play games??
We first need to introduce some definitions. I will always give an example for these definitions using our implementation of Tetris.
  * **Agent**:  Our AI that will learn to play the game. 
               
  * **Environment**: The system our agent interacts with. This will simply be the Tetris Game.
  * **State**:  An instance $S_{t}$ of the environment that our agent will be able to observe at time t. 
                
  * **Action**: An action $A_{t}$ that our agent can take in order to change the current state. 
  * **Reward**: The points R_{t} that our agent gets for changing the current state by performing a certain action.
  * **Episode**: One complete walk through the environment until the agent reaches a final state.
  
In the case of Tetris, the agent will be our Convolutional Neural Network. The environment is the game itself with which the agent can interact. The states are given by snapshots of the game, a.k.a. the image one sees when playing the game. The possible actions that our agent can perform are *Wait*, *Left*, *Right* and *Rotate*.
The rewards are the points you get when playing Tetris, e.g. for completing a row or when the blocks reach the top.
The episode is simply one round of Tetris until our agent loses. (GameOver)

One episode will therefore be described by the following sequence where $S_{n}$ will be the final state:

${S_{0}, A_{0}, R_{0}, ... , S_{n}, A_{n}, R_{n}}$


Having these definitions now out of the way, we can start with the actual theory behind Reinforcement Learning.

The goal for our agent is to be able to decide what action $A_{t}$ it should use at time t, given the current state $S_{t}$.
At first glance, this sounds like a classification problem: Given the state $S_{t}$, decide what action $A_{t}$ is best.
The first surprise is that we will treat it as a Regression Problem!
Imagine the following:

What if we could predict the future reward we get if we choose action $A_{t}$ given that we are in state $S_{t}$?
Namely if we had a function that maps state and action pairs $(S_{t}, A_{t})$ to future rewards, we could always choose the action
that maximizes this function and the problem would be solved.

Let's call this function **Q-Function**:
