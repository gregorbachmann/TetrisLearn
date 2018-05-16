import tensorflow as tf
from collections import deque
import numpy as np
import random

# Define all parameters needed for DeepQNet
wait = [1, 0, 0, 0]
left = [0, 1, 0, 0]
right = [0, 0, 1, 0]
rotate = [0, 0, 0, 1]
possible_actions = [wait,left, right, rotate]

# Model parameters
state_size = [10, 20, 1]  # Our state is a 10x20 matrix with only one channel
action_size = 4  # We have always 4 actions to choose from
learning_rate = 0.0002  # Choose some learning rate
training = True

# Training parameters
total_episodes = 1  # Run 1000 Tetris games to train
max_steps = 2000
batch_size = 64

# Exploration parameters
explore_start = 1.0  # Exploring parameters at start
explore_stop = 0.1  # At least this probability
decay_rate = 0.0001  # Exponential decay

# Q-Learning parameters:
gamma = 0.99

# Memory parameters
pretrain_length = batch_size  # Number of elements needed at start in memory queue
memory_size = 5000


# Now populate the memory by random actions

game = tetris()  # Initialize a Tetris game
game.reset()
memory = Memory(max_size=memory_size)  # Initialize the Memory queue
# Reset the graph
tf.reset_default_graph()

# Instantiate the DQNetwork

deepqnet1 = DeepQNet(state_size=state_size,action_size=action_size,learning_rate=learning_rate)
# Fill the queue up:
for i in range(pretrain_length):
    # First create initial state
    if i == 0:
        game.project()
        state = game.field.reshape(state_size)

    action = random.choice(possible_actions)  # Sample random action

    current_points = game.points
    if action == 0:
        game.wait()
    if action == 1:
        game.translate_left()
    if action == 2:
        game.translate_right()
    if action == 3:
        game.rotate()
    if i % 2 == 0:
        game.gravitate()


    # Determine wheter episode has finished
    if game.block == None:
        done = True
        reward = game.points-current_points  # When n
        game = tetris()
        game.reset()  # Initialize new game
        game.project()
        next_state = game.field.reshape(state_size)
        memory.add((state, action, reward, next_state, done))  # Add experience to memory
        state = next_state

    else:
        done = False
        game.project()
        next_state = game.field.reshape(state_size)
        reward = game.points - current_points
        memory.add((state, action, reward, next_state, done))  # Add experience to memory
        state = next_state


# Start training the model

saver = tf.train.Saver()

if training == True:
    rewards_list = []

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        game = tetris()  # Initialize a Tetris game

        decay_step = 0

        for episode in range(total_episodes):
            print(episode)
            game.reset()
            step = 0

            game.project()
            state = game.field.reshape(state_size)

            while step < max_steps:
                step += 1
                decay_step += 1
                current = game.points

                exp_exp_tradeoff = np.random.rand()
                explore_probability = explore_stop + (explore_start - explore_stop) * np.exp(-decay_rate * decay_step)

                if explore_probability > exp_exp_tradeoff:
                    action = random.choice(possible_actions)

                else:
                    Qs = sess.run(deepqnet1.output, feed_dict={deepqnet1.inputs_: state.reshape((1, *state.shape))})
                    action = np.argmax(Qs)
                    action = possible_actions[int(action)]
                if action[0] == 1:
                    game.wait()
                if action[1] == 1:
                    game.translate_left()
                if action[2] == 1:
                    game.translate_right()
                if action[3] == 1:
                    game.rotate()
                if step % 1 == 0:
                    game.gravitate()



                if game.block == None:
                    done = True
                    total_reward = game.points
                    game = tetris()
                    game.reset()
                    game.project()
                    next_state = game.field.reshape(state_size)
                    step = max_steps
                    """print('Episode: {}'.format(episode),
                          'Total reward: {}'.format(total_reward),
                          'Tr2aining loss: {:.4f}'.format(loss),
                          'Explore P: {:.4f}'.format(explore_probability))"""
                    rewards_list.append((episode, total_reward))
                    memory.add((state, action, reward, next_state, done))

                else:
                    done =False
                    game.project()
                    reward = game.points - current
                    next_state = game.field.reshape(state_size)
                    memory.add((state, action, reward, next_state, done))
                    state = next_state

                # Learning part

                batch = memory.sample(batch_size)
                states = np.array([each[0] for each in batch], ndmin=3)
                actions = np.array([each[1] for each in batch])
                rewards = np.array([each[2] for each in batch])
                next_states = np.array([each[3] for each in batch])
                dones = np.array([each[4] for each in batch])

                target_Qs_batch = []
                target_Qs = sess.run(deepqnet1.output, feed_dict={deepqnet1.inputs_: next_states})

                for i in range(len(batch)):
                    terminal = dones[i]
                    if terminal:
                        target_Qs_batch.append(rewards[i])
                    else:
                        target = rewards[i] + gamma * np.max(target_Qs[i])
                        target_Qs_batch.append(target)
                targets = np.array([each for each in target_Qs_batch])
                loss, _ = sess.run([deepqnet1.loss, deepqnet1.optimizer], feed_dict={deepqnet1.inputs_: states,
                                deepqnet1.target_Q: targets, deepqnet1.actions_: actions})

    saver.save(sess, 'TetrisEuler', global_step=1000)

# Now after training, let the NNet play the game

game_new = tetris()

game_new.reset()
counter=0
moves=2
with tf.Session() as sess:
    saver.restore(sess, "TetrisEuler")
    while game_new.block!=None:
        for i in range(moves):
            game_new.project()
            state = game_new.field.reshape((1,10,20,1))
            output = sess.run(deepqnet1.output, feed_dict={deepqnet1.inputs_: state})
            action = np.argmax(output)
            if action==0:
                game_new.translate_left()
            if action==1:
                game_new.translate_right()
            if action==2:
                game_new.rotate()
            if action==3:
                game_new.wait()
            if game.block==None:
                break
            game_new.project()
            plt.figure(1); plt.clf()
            plt.imshow(game_new.field)
            plt.title('Number ' + str(i+counter))
            plt.pause(0.02)

        counter+=1

        game_new.gravitate()
        if game_new.block == None:
            break
        game_new.project()
        plt.figure(1); plt.clf()
        plt.imshow(game_new.field)
        plt.title('Number ' + str(i+counter))
        plt.pause(0.02)

