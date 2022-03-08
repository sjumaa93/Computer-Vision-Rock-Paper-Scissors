import cv2
from keras.models import load_model
import numpy as np
model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

while True: 
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    prediction = model.predict(data)
    cv2.imshow('frame', frame)
    # Press q to close the window

    input('Press Enter to Start')
    import random

    if(prediction[0][3]) > 0.8:
        user_choice = ('None')
    elif(prediction[0][1]) > 0.8:
        user_choice = ('Paper')
    elif(prediction[0][2]) > 0.8:
        user_choice = ('Scissors')
    else:
        user_choice = ('Rock')
    
    print(f'You chose {user_choice}')

    computer_choice = random.choice(['Rock','Paper','Scissors'])
    
    print(f'Computer chose {computer_choice}')


    if user_choice == 'Rock' and computer_choice == 'Paper':
        print('Computer Won')
    elif user_choice == 'Rock' and computer_choice == 'Scissors':
        print('You Won')
    elif user_choice == 'None':
        print('You Chose Nothing, You Lost')
    elif user_choice == 'Paper' and computer_choice == 'Rock':
        print('You Won')
    elif user_choice == 'Paper' and computer_choice == 'Scissors':
        print('You Lost')

    elif user_choice == 'Scissors' and computer_choice == 'Rock':
        print('You Lost')
    elif user_choice == 'Scissors' and computer_choice == 'Paper':
        print('You Won')
    
    else:
        print('Draw')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
            
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
