#!/usr/bin/env

import tensorflow as tf

# use InteractiveSession
sess = tf.InteractiveSession()

x = tf.Variable([1.0, 2.0])
a = tf.constant([3.0, 3.0])

# init variable 'x', initializer is an operation
x.initializer.run()

# sub is a `tensor`
sub = tf.sub(x, a)
print sub.eval()
