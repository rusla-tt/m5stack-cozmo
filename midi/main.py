
import requests
import shutil
from slack import postMessage
from lstm import prepare_sequences, train_network
from midi import generate_notes, generate_png_midi, get_notes, create_midi
from keras.models import load_model
from cnn import PreProcess, Learning, TestProcess

def download_img(url, file_name):
    r = requests.get(url, stream=True)
    print(r.status_code)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print("error")

def predict_midi():
    midi_class = TestProcess('sample.png')
    generate_png_midi('sample.png', midi_class)
    get_note = get_notes(midi_class)
    n_vocab = len(set(get_note))
    network_input, network_output = prepare_sequences(get_note, n_vocab)
    model = load_model('{}.h5'.format(midi_class), compile=False)
    prediction_output = generate_notes(model, get_note, network_input, len(set(get_note)))
    create_midi(prediction_output, midi_class+"_gen")
    return midi_class+"_gen.midi"

if __name__ == '__main__':
    #print("Start CNN PreProcesser")
    #PreProcess()
    #print("Start CNN Learning")
    #Learning()
    #p = TestProcess('sample.png')
    ClassNames = ["adlut", "bigboss", "classic", "haru", "natu", "aki", "huyu", "pokemon", "wa"]
    for t in ClassNames:
        print("Start {} LSTM Midi Model Learning".format(t))
        train_network(t)
    print("Learning Done")
    #download_img('http://192.168.0.10/capture', 'target.png')
    #midi_name = predict_midi()
    #postMessage(midi_name)