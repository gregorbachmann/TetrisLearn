import tensorflow as tf
from collections import deque
import numpy as np


# Implement Convolutional Neural Network without Pooling Layer as a class using TensorFlow
class DeepQNet:
    def __init__(self, state_size, action_size, learning_rate, name="DeepQnet"):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate

        with tf.variable_scope(name):
            # Introduce the inputs and actions as placeholders
            self.inputs_ = tf.placeholder(tf.float32, [None, *state_size], name="Inputs")
            self.actions_ = tf.placeholder(tf.float32, [None,4], name="Actions")
            self.target_Q = tf.placeholder(tf.float32, [None], name="Target")

            # First layer consisting of convolution, batch normalization and ELu-Activation
            # Input is of shape [20,10,1]
            self.conv1 = tf.layers.conv2d(inputs=self.inputs_, filters=32, kernel_size=[4,4], strides=[1,1],
                                          padding="VALID", kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d(),
                                          name="ConvLayer1")

            self.conv1_batchnorm = tf.layers.batch_normalization(self.conv1, training=True, epsilon=1e-5,
                                                                 name="BatchNorm1")

            self.conv1_out = tf.nn.elu(self.conv1_batchnorm, name="ConvLayer_Output1")

            # Second layer consisting of convolution, batch normalization and ELu-Activation
            # Input is of shape ??
            self.conv2 = tf.layers.conv2d(inputs=self.conv1_out, filters=64, kernel_size=[4, 4], strides=[2, 2],
                                          padding="VALID",
                                          kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d(),
                                          name="ConvLayer2")

            self.conv2_batchnorm = tf.layers.batch_normalization(self.conv2, training=True, epsilon=1e-5,
                                                                 name="BatchNorm2")

            self.conv2_out = tf.nn.elu(self.conv2_batchnorm, name="ConvLayer_Output2")

            # Flatten last output to one vector [??]
            self.flatten_layer = tf.contrib.layers.flatten(self.conv2_out)

            # Add the dense layer with 300 neurons
            self.dense_layer = tf.layers.dense(inputs=self.flatten_layer, units=300, activation=tf.nn.elu,
                                              kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                              name="DenseLayer")

            # Finally we obtain the output layer consisting of 4 units for our 4 actions in Tetris
            self.output = tf.layers.dense(inputs=self.dense_layer, units=4,
                                          kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                          activation=None)

            # Calculate the resulting Q-values for each action
            self.Qval = tf.reduce_sum(tf.multiply(self.output, self.actions_), axis=1)

            # Take MSE Loss for Backpropagation
            self.loss = tf.reduce_mean(tf.square(self.Qval-self.target_Q))

            # Train the model
            self.optimizer = tf.train.RMSPropOptimizer(self.learning_rate).minimize(self.loss)


# Implement the class memory that will store past experiences of our DeepQNet to "remind" it of its past
# by training it again with these past samples and to break high correlation between consecutive samples

class Memory:
    def __init__(self, max_size):
        self.buffer = deque(maxlen=max_size)

    # Add a new experience to the queue
    def add(self, experience):
        self.buffer.append(experience)

    # Sample batch_size experiences from our queue randomly
    def sample(self, batch_size):
        buffer_size = len(self.buffer)
        index = np.random.choice(np.arange(buffer_size), size=batch_size, replace=False)

        return [self.buffer[i] for i in index]