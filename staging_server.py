"""
Реализация socket клиент-сервер, передача сообщения
с https://www.youtube.com/watch?v=p0NueP55kjs
Сервер
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import cv2
import numpy as np
import os

# Создание промежуточного сервера:
staging_server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

staging_server.bind(

    ("127.0.0.1", 1234) #localhost
)

staging_server.listen() #может принимать некоторое количество сообщений
print("Server is listening")

staging_server2 = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

staging_server2.connect(
    ("127.0.0.1", 1235)
)

#quit = False
while True:
    try:
        client_socket, client_address = staging_server.accept()

        data1 = client_socket.recv(2048)
        sizeOfImage1 = int(data1.decode('utf-16'))
        print("Size of input image:", sizeOfImage1)

        #Принимаю картинку
        file = open('image_staging_server.png', mode="wb")  #открыть для записи принимаемой картинки файл
        data1  = client_socket.recv(2048)

        while data1 :
            file.write(data1 )
            data1  = client_socket.recv(2048)

        file.close()

        #Внесение шума. Взято с https://fooobar.com/questions/493687/how-to-add-noise-gaussiansalt-and-pepper-etc-to-image-in-python-with-opencv
        image = cv2.imread('image_staging_server.png')

        row, col, ch = image.shape
        mean = 0
        var = 100
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        print('Максимальная величина вносимого шума: ', np.max(gauss))
        #gauss = gauss.reshape(row, col, ch)
        noisy = image + gauss

        # save the denoised image
        cv2.imwrite('image_staging_server_output.png', noisy)

        # считывает и отправляет картинку
        file = open('image_staging_server_output.png', mode="rb") #считываем картинку

        imageSize = os.path.getsize('image_staging_server_output.png')
        print("Size of output image:", imageSize)
        staging_server2.send(f"{imageSize}".encode('utf-16'))

        data = file.read(2048)

        while imageSize > 0:
            data = file.read(2048)
            staging_server2.send(data)
            if (imageSize >= 2048):
                imageSize = imageSize - 2048
            else:
                imageSize = imageSize - imageSize

        file.close()
        print("Картинка была отправлена", '\n')
    except:
        print('\n[Сервер остановлен]')
        #quit = True
        break

staging_server.close()