"""
Реализация socket клиент-сервер, передача изображения
с https://www.youtube.com/watch?v=p0NueP55kjs
Сервер
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
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

#quit = False
while True:
    try:
        client_socket, client_address = server.accept()
        data = client_socket.recv(2048)
        sizeOfImage = int(data.decode('utf-16'))
        print("Size of input image:", sizeOfImage)

        #Принимаю картинку
        file = open('image_server.png', mode="wb")  #открыть для записи принимаемой картинки файл

        while data:
            file.write(data)
            data = client_socket.recv(2048)
        """while sizeOfImage > 0:
            data = client_socket.recv(2048)
            file.write(data)
            if (sizeOfImage>=2048):
                sizeOfImage = sizeOfImage - 2048
            else:
                sizeOfImage = sizeOfImage - sizeOfImage
        """
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
        processed_image = cv2.medianBlur(image, 10)

        # save image to disk
        cv2.imwrite('image_server_filter.png', processed_image)
        print("Картинка была принята", '\n')
        # display image
        #cv2.imshow('Median Filter Processing', processed_image)
        # pause the execution of the script until a key on the keyboard is pressed
        #cv2.waitKey(0)
    except:
        print('\n[Сервер остановлен]')
        #quit = True
        break
    #except OSError as err:
    #    print("OS error: {0}".format(err))
    #except ValueError:
    #   print("Could not convert data to an integer.")
    #except:
    #   print("Unexpected error:", sys.exc_info()[0])
    #   raise
server.close()





