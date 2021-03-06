"""
Реализация socket клиент-сервер, передача сообщения
Клиент
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import socket
# Создание клиента:
client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

client.connect(
    ("127.0.0.1", 1234)
)


# считывает и отправляет картинку
file = open('image.png', mode="rb") #считываем картинку

imageSize = os.path.getsize('image.png')
print("Size of image:", imageSize)
client.send(str(imageSize).encode('utf-16'))

data = file.read(2048)

while data:
    client.send(data)
    data = file.read(2048)

file.close()
client.close()
