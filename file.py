import cv2
from keras.models import load_model
import numpy as np
import random
import time
model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

t_0 = time.time()
while True: 
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    prediction = model.predict(data)


    if(prediction[0][3]) > 0.5:
        user_choice = ('None')
    elif(prediction[0][1]) > 0.5:
        user_choice = ('Paper')
    elif(prediction[0][2]) > 0.5:
        user_choice = ('Scissors')
    else:
        user_choice = ('Rock')

    print(f'You chose {user_choice}')
 
    time.sleep(3)
 
    computer_choice = random.choice(['Rock','Paper','Scissors'])
   
    print(f'Computer chose {computer_choice}')
   
    time.sleep(3)
    if user_choice == 'Rock' and computer_choice == 'Paper':
        message = 'Computer Won!'
    elif user_choice == 'Rock' and computer_choice == 'Scissors':
        message = 'You Won!'
    elif user_choice == 'None':
        message = 'You Chose Nothing, You Lost!'
    elif user_choice == 'Paper' and computer_choice == 'Rock':
        message = 'You Won!'
    elif user_choice == 'Paper' and computer_choice == 'Scissors':
        message = 'You Lost!'
    elif user_choice == 'Scissors' and computer_choice == 'Rock':
        message = 'You Lost!'
    elif user_choice == 'Scissors!' and computer_choice == 'Paper':
        message = 'You Won!'
    else:
        message = 'Draw'
    
    time.sleep(3)
    cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()