# How To Play Tetris With Deep-Q-Learning


# Overview

Our initial goal in this project was to get acquainted with the idea of Reinforcement Learning, ideally via progamming it with a simple example. Inspired as many others by DeepMind and their success with letting Neural Networks play Atari-Games, we decided to choose a similar example. Since we both weren't familiar with importing these games directly, emulators and stuff, we chose a game that is relatively easy to implement, Tetris. Writing the game ourselves allowed us to directly implement all the functions, which made the training process easier (but debugging harder...). We followed the approach of **DeepMind**, namely using Deep-Q-Learning and directly feeding the raw pixels of our game into the Convolutional Neural Network. I will describe the theory and the architecture used in the next paragraph. As it turns out (so far at least), Tetris was a bad choice (It would have been worth it to check for existing papers before programming the stuff for weeks..). The game structure (obviously) asks for relatively long-term decisions, since you cannot really associate a reward with a decision immediately. Blinded by all the Machine Learning Magic, we thought that it will somehow work, I mean we're using a Convolutional Neural Net, nothing can go wrong, right?


# The Theory of Reinforcement Learning

Let's first get to dry theory. How the hack is it possible to let an agent learn how to play games??
We first need to introduce some definitions. I will always give an example for these definitions using our implementation of Tetris.
  * **Agent**:  Our AI that will learn to play the game. 
               
  * **Environment**: The system our agent interacts with, sometimes it can be stochastic a.k.a. include a portion of randomness.
  * **State**:  An instance $S_{t}$ of the environment that our agent will be able to observe at time t. 
                
  * **Action**: An action $A_{t}$ that our agent can take in order to change the current state. 
  * **Reward**: The points r_{t} that our agent gets for changing the current state by performing a certain action.
  * **Total Future Reward**: The future points we get at time t: $R_{t} = r_{t} + r_{t+1} + ... + r_{n}$
  * **Discounted Future Reward**: The future points we get at time t: $R_{t} = r_{t} + \gamma * r_{t+1} + ... + \gamma^{n} * r_{n}$
  * **Episode**: One complete walk through the environment until the agent reaches a final state.
  
Don't worry about these rather technical definitions, they are all actually very natural to our problem.\
In the case of Tetris, the agent will be our Convolutional Neural Network. \
The environment is the game itself with which the agent can interact. It is partly stochastic as we never know what new block will appear at the top when we place the block before on the bottom.\
The states are given by snapshots of the game, a.k.a. the image one sees when playing the game. \
The possible actions that our agent can perform are *Wait*, *Left*, *Right* and *Rotate*. \
The rewards are the points you get when playing Tetris, e.g. for completing a row or when the blocks reach the top. \
The total future reward is all the rewards we will collect starting from time t until our agent loses. \
The discounted version tries to include the uncertainty in future rewards due to the randomness of our game, letting them count less by multiplying them by $\gamma < 1$ \
The episode is simply one round of Tetris until our agent loses. (GameOver)

A complete summary of the game is therefore given by the following sequence:

${S_{0}, A_{0}, r_{0}, ... , S_{n}, A_{n}, r_{n}}$

What will be very important later is the following observation:
$R_{t} = r_{t} + R_{t+1}$
In words we can write the total future reward at time t as the sum of the reward we get for going from $S_{t}$ to $S_{t+1}$ plus the total future reward at time t+1.
Makes perfect sense so far.


Having these definitions now out of the way, let's get our hands dirty with the actual theory behind Reinforcement Learning.

The goal for our agent is to be able to decide what action $A_{t}$ it should use at time t, given the current state $S_{t}$.
At first glance, this sounds like a classification problem: Given the state $S_{t}$, decide what action $A_{t}$ is best.
The first surprise is that we will treat it as a Regression Problem!
Imagine the following:\
What if we could predict the future reward we get if we choose action $A_{t}$ given that we are in state $S_{t}$?<br/>
Namely if we had a function Q(S,A) that maps state and action pairs $(S_{t}, A_{t})$ to future rewards, we could always choose the action
that maximizes this function and the problem would be solved.<br/>
This function is defined on the space of all possible states and actions, which is immensive since the number of possible states is given
by 3^(20 * 10). (We model our Tetris game as an 20x10 array containing either 1,0,-1)<br/>
This makes it impossible to determine Q exactly, that's where our beloved Neural Nets come into play!

We use a Convolutional Neural Network as a function approximator to our so called **Q-Function**, imitating it better and better with every game our agent plays. These very imprecise statements require preciser explanation.

Usually a Neural Net (or any Machine Learning algorithm stemming from the Supervised Learning Region) requires targets that it needs to approximate. Think of classification problems such as recognizing dogs from pictures or determining the age of a patient based on his brain scan etc, all these problems require training data, where we know what our true targets are.<br/>
A very important observation is that we are not able to provide that to our network:<br/>
Imagine we have some state S and choose to perform action A. We are able to observe the immediate reward but in order to calculate the true total reward, we would need to try all the combinations of actions until the terminal time n to find the maximizing sequence that gives us the true total reward. A computational burden that my computer surely cannot stomach (and neither EulerCluster).<br/>
At this moment, you should really be stunned by the difficulty of this problem.


