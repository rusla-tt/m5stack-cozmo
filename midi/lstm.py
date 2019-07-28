from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import CuDNNLSTM, LSTM, Bidirectional
from keras.layers import Activation
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint, History
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from midi import get_notes

def create_network(network_input, n_vocab):
    """ create the structure of the neural network """
    model = Sequential()
    model.add(CuDNNLSTM(512,input_shape=(network_input.shape[1], network_input.shape[2]),return_sequences=True))
    model.add(Dropout(0.3))
    model.add(Bidirectional(CuDNNLSTM(512, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(CuDNNLSTM(512)))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    return model

def train_network(target):
    """ Train a Neural Network to generate music """
    # Get notes from midi files
    notes = get_notes(target)

    # Get the number of pitch names
    n_vocab = len(set(notes))

    # Convert notes into numerical input
    network_input, network_output = prepare_sequences(notes, n_vocab)

    # Set up the model
    model = create_network(network_input, n_vocab)
    history = History()
    
    # Fit the model
    n_epochs = 100
    model.summary()
    model.fit(network_input, network_output, callbacks=[history], epochs=n_epochs, batch_size=64)
    model.save('{}.h5'.format(target))
    
    # # Use the model to generate a midi
    #prediction_output = generate_notes(model, notes, network_input, len(set(notes)))
    #create_midi(prediction_output, 'pokemon_midi')
    
    # Plot the model losses
    pd.DataFrame(history.history).plot()
    plt.savefig('LSTM_Loss_per_Epoch.png', transparent=True)
    plt.close()

def prepare_sequences(notes, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    sequence_length = 100

    # get all pitch names
    pitchnames = sorted(set(item for item in notes))

     # create a dictionary to map pitches to integers
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

    # reshape the input into a format compatible with LSTM layers
    n_patterns = len(network_input)
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    
    # normalize input between 0 and 1
    network_input = network_input / float(n_vocab)

    network_output = np_utils.to_categorical(network_output)

    return (network_input, network_output)