import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical



def DataIterator(tunes, tune_lens, maxlen, batch_size, n_classes):
    inds = list(range(len(tunes)))
    prob = tune_lens / sum(tune_lens)
    while True:
        X_seq = []
        y_seq = []
        while len(y_seq) != batch_size:
            tune_ind = np.random.choice(inds, p=prob)
            tune_choice = tunes[tune_ind]
            position = np.random.randint(0, len(tune_choice))
            x = np.array(tune_choice[:position], dtype='intp')
            y = tune_choice[position]
            X_seq.append(x)
            y_seq.append(y)
        yield pad_sequences(X_seq, maxlen, padding='post', truncating='pre'), to_categorical(np.array(y_seq), n_classes+1)
