#!/usr/bin/env python

import tensorflow as tf

#####
# 1. Make map
# Tensors(variable) declare and operation declare
#####
state = tf.Variable(0, name = 'counter')

one = tf.constant(1)
new_value = tf.add(state, one)
update = tf.assign(state, new_value)

# variables need to be init
init_op = tf.initialize_all_variables()

#####
# 2. Start Map
# Run operations
#####
with tf.Session() as sess:
    sess.run(init_op)

    # fetch the value of the tensor 'state', use list for multiple tensors.
    print sess.run(state)
    print sess.run([state, new_value])

    for _ in range(3):
        # 
        sess.run(update)
        print sess.run(state)
        print sess.run([state, new_value])
