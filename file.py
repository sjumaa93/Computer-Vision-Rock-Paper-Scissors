import cv2
from keras.models import load_model
import numpy as np
import random
import time
model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def compare_options(computer_choice,user_choice):
    if user_choice == 'Rock' and computer_choice == 'Paper':
        message = 'You chose rock, computer chose paper, You Lost!'
    elif user_choice == 'Rock' and computer_choice == 'Scissors':
        message = 'You chose rock, computer chose scissors, You Won!'
    elif user_choice == 'None':
        message = 'You Chose Nothing, You Lost!'
    elif user_choice == 'Paper' and computer_choice == 'Rock':
        message = 'You chose paper, computer chose rock, You Won!'
    elif user_choice == 'Paper' and computer_choice == 'Scissors':
        message = 'You chose paper, computer chose scissors, You Lost!'
    elif user_choice == 'Scissors' and computer_choice == 'Rock':
        message = 'You chose scissors, computer chose rock, You Lost!'
    elif user_choice == 'Scissors!' and computer_choice == 'Paper':
        message = 'You chose scissors, computer chose paper, You Won!'
    else:
        message = 'You both chose the same thing, its a Draw!'
    return message

def get_user_choice(prediction):
    if(prediction[0][1]) > 0.5:
        user_choice = ('Rock')
    elif(prediction[0][2]) > 0.5:
        user_choice = ('Paper')
    elif(prediction[0][3]) > 0.5:
        user_choice = ('Scissors')
    else:
        user_choice = ('None')
    
    return user_choice

started = False
next_round = True
countdown = False
counter = 0
elapsed = 0
show_message = False

user_wins = 0
computer_wins = 0

message = ''


while True: 
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    prediction = model.predict(data)



    if not started:
        message = 'Press s to start'
    if cv2.waitKey(33)  == ord('s'):
        if not started:
            counter = time.time()
            started = True
            countdown = True

    if started:
        elapsed = 5 - (time.time() - counter)
    
        if elapsed <= -4:
            if computer_wins == 3:
                message = f'Your Wins: {user_wins} Computer Wins: {computer_wins}, Game Over You Lose!'
            elif user_wins == 3:
                message = f'Your Wins: {user_wins} Computer Wins: {computer_wins}, Well Done, You Won!'
            else:
                message = f'Your Wins: {user_wins} Computer Wins: {computer_wins}. Press n to continue' 
            if cv2.waitKey(33) == ord('n'):
                started = False
                elapsed = 0
                show_message = False

        elif elapsed <= 0:
            countdown = False
            if show_message == False:
                user_choice = get_user_choice(prediction)
                computer_choice = random.choice(['Rock','Paper','Scissors'])
                message = compare_options(computer_choice, user_choice)
                if 'You Won' in message:
                    user_wins += 1
                elif 'You Lost' in message:
                    computer_wins += 1
                show_message = True

        if countdown:
            message = f'Show your hand in {int(elapsed)} seconds'

 

    
    cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()