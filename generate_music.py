import pickle as pkl
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import numpy as np

start_symbol, end_symbol = '<s>', '</s>'
prt = False

class MusicGenerator:
    def __init__(self, model, max_len = 200):
        with open("char2ind.pkl", 'rb') as f:
            self.char2ind = pkl.load(f)

        with open("ind2char.pkl", 'rb') as f:
            self.ind2char = pkl.load(f)
        self.model = model
        self.max_len = max_len
        self.upTo = 0

    @staticmethod
    def sample(preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)


    def getlist(self, diversity=1.0, maxlen=1000, seed=start_symbol):
        if prt:print('----- diversity:', diversity)

        generated = [seed]
        if prt:print('----- Generating with seed: "' + generated[0] + '"')
        count = 0
        while generated[-1] != end_symbol and count < maxlen:
            x_pred = pad_sequences([[self.char2ind[i] for i in generated]], self.max_len, padding='post', truncating='pre')
            preds = self.model.predict(x_pred, verbose=0)[0]
            next_index = self.sample(preds, diversity)
            try:
                next_char = self.ind2char[next_index]
            except:
                continue

            generated.append(next_char)
            count+=1
        if generated[-1] != end_symbol: generated.append(end_symbol)
        return generated

    @staticmethod
    def parse_generated(generated):
        print('orig: ', ' '.join(generated))
        g = ["X:1\n", "T:synthesized_piece\n"]
        l = len(generated)
        for c, i in enumerate(generated):
            if c == 0 or c == l-1: continue
            if c!=2: g.append(i)
            else: g.append(i[:2] + 'C')
            if c==1 or c == 2: g.append('\n')
            else: g.append(' ')
        return ''.join(g)

    def get(self, diversity=1.0, maxlen=1000, seed=start_symbol):
        g = self.getlist(diversity, maxlen, seed)
        return self.parse_generated(g)

if __name__ == "__main__":
    my_model = load_model(r"saved_models/153-1.5443.h5")

    thingy = MusicGenerator(my_model)
    for i in range(10):
        print(thingy.get(diversity=1))
        print()
