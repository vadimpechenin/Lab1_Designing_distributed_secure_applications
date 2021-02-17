"""
Реализация socket клиент-сервер, передача изображения
с https://www.youtube.com/watch?v=p0NueP55kjs
Сервер
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
# Прежде всего нам необходимо создать сокет:
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

server.bind(
    ("127.0.0.1", 1235) #localhost
)

server.listen() #может принимать некоторое количество сообщений
print("Server is listening")
client_socket, client_address = server.accept()


#Принимаю картинку
file = open('image_server.png', mode="wb")  #открыть для записи принимаемой картинки файл
data = client_socket.recv(2048)

while data:
    file.write(data)
    data = client_socket.recv(2048)

file.close()

#Применение медианного фильтра
# взято c https://coderlessons.com/articles/programmirovanie/filtratsiia-izobrazhenii-v-python
#import argparse
import cv2

# create the argument parser and parse the arguments
"""
#Полезный код для указания пути к картинке
ap = argparse.ArgumentParser()
ap.add_argument('-i', '—image', required = True, help = 'Path to the input image')
args = vars(ap.parse_args())
"""
# read the image
#image = cv2.imread(args['image'])
image = cv2.imread('image_server.png')
# apply the 50×50 median filter on the image
processed_image = cv2.medianBlur(image, 50)
# display image
cv2.imshow('Median Filter Processing', processed_image)
# save image to disk
cv2.imwrite('image_server_filter.png', processed_image)
# pause the execution of the script until a key on the keyboard is pressed
cv2.waitKey(0)




