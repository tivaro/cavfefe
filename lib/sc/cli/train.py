from __future__ import print_function
import tensorflow as tf
import numpy as np
from lib.ds import Vocabulary
from lib.sc import SentenceClassifier, SentenceReader
import lib.etc as etc
import sys

def sc_train():
    max_length     = 30
    num_classes    = 200
    embedding_size = len(Vocabulary().restore("data/ds/vocabulary.csv"))

    reader = SentenceReader("data/sc/training.csv",
                            num_classes, embedding_size = embedding_size)

    batch_size = 128
    epochs     = 2000

    # Network Parameters
    num_hidden = 512 # hidden layer num of features

    model = SentenceClassifier(max_length, embedding_size,
                               num_hidden, num_classes)

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)

        for step, pi in etc.range(epochs):
            # Get a batch of training instances.
            batch_x, batch_y, batch_len = reader.read(lines = batch_size)

            # Run optimization op (backprop)
            model.train(batch_x, batch_y, batch_len, sess)

            # Calculate batch accuracy and loss
            acc, loss = model.evaluate(batch_x, batch_y, batch_len, sess)

            print("Iter " + str(1 + step) + " / " + str(epochs) + \
                  ", Minibatch Loss= " + \
                  "{:.6f}".format(loss) + ", Training Accuracy= " + \
                  "{:.5f}".format(acc) + ", Time Remaining= " + \
                  etc.format_seconds(pi.time_remaining()), file = sys.stderr)

            if (1 + step) % 10 == 0:
                model.save(sess, 1 + step)

        print("Optimization Finished!", file = sys.stderr)
