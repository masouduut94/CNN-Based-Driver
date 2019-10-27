import numpy as np
from models import inception_v3 as googlenet
from random import shuffle

FILE_I_END = 1

WIDTH = 480
HEIGHT = 270
LR = 1e-3
EPOCHS = 30

MODEL_NAME = 'model_1.model'
PREV_MODEL = 'pre_models/'
LOAD_MODEL = True

model = googlenet(WIDTH, HEIGHT, 3, LR, output=9, model_name=MODEL_NAME)

if LOAD_MODEL:
    model.load(PREV_MODEL)
    print('We have loaded a previous model!!!!')

# iterates through the training files
for e in range(EPOCHS):
    # data_order = [i for i in range(1,FILE_I_END+1)]
    data_order = [i for i in range(1, FILE_I_END + 1)]
    shuffle(data_order)
    for count, i in enumerate(data_order):
        try:
            file_name = 'C:/Users/masoud/Desktop/PycharmProjects/CNN-Based-Driver/data/training_data-{0}.npy'.format(i)
            # full file info
            train_data = np.load(file_name, allow_pickle=True)
            print('training_data-{0}.npy'.format(i), len(train_data))

            train = train_data[:-50]
            test = train_data[-50:]

            X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 3)
            Y = [i[1] for i in train]

            test_x = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 3)
            test_y = [i[1] for i in test]

            model.fit({'input': X}, {'targets': Y}, n_epoch=1,
                      validation_set=({'input': test_x}, {'targets': test_y}),
                      snapshot_step=2500, show_metric=True, run_id=MODEL_NAME)

            if count % 10 == 0:
                print('SAVING MODEL!')
                model.save(MODEL_NAME)

        except Exception as e:
            print(e)

# tensorboard --logdir=log/E8JBLM --host localhost --port 8080
