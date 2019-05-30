# Import socket module 
import socket                
import pygame
import time
import os
from os.path import isfile, join

from cryptography.fernet import Fernet



def decrypt(cipher,key):
	
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher)
    print(plain_text)
    return plain_text

while True:
    # Create a socket object
    s = socket.socket()          
    # Define the port on which you want to connect 
    port = 12345                
    # connect to the server on local computer 
    s.connect(('192.168.43.22', port)) 
    # receive data from the server
    text = s.recv(1024)
    print(text)
    text = str(text)
    text = text[2:]
    key= text.split(' ')[0]
    cipher = ""
    if(len(text.split(" "))>1):
        cipher = text.split(' ')[1]
    text = decrypt(cipher.encode(),key.encode())
    text = str(text)
    text = text[2:-1]

    s.close()
	
    print('receieved',text)
    text_list = list(text)
    pygame.init()

    modes = pygame.display.list_modes()
    
    pygame.display.set_mode([600,600])

    screen = pygame.display.get_surface()
    pygame.display.set_caption('something')
    pygame.display.toggle_fullscreen()
    clock = pygame.time.Clock()
    crashed = False
    waittime = 1000

    while(not crashed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        try:
            if len(text_list) == 0:
                img = pygame.image.load('./dat/space.png')
                # rescale the image to fit the current display
                img = pygame.transform.scale(img, [600,600])
                screen.blit(img, (0, 0))
                pygame.display.flip()
                time.sleep(1)
                break
            if text_list[0]==' ':
                img = pygame.image.load('./dat/space.png')
            else:
                img = pygame.image.load('./dat/'+text_list[0]+'.jpg')
                        
            text_list.pop(0)
            
            img = img.convert()
            
            # rescale the image to fit the current display
            img = pygame.transform.scale(img, [600,600])
            screen.blit(img, (0, 0))
            pygame.display.flip()
            
            time.sleep(1)

            img = pygame.image.load('./dat/space.png')
            img = pygame.transform.scale(img, [600,600])
            screen.blit(img, (0, 0))
            pygame.display.flip()

            time.sleep(0.1)
            

        except pygame.error as err:                
            crashed = True
            break            
        #break
        #print("TRUE")
    

