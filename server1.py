import socket as s
from random import randint

HOST = '192.168.70.114'
PORT = 33000
BUFFER = 1024

random = randint(0, 3185486)
tab = []

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

while True:
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established.")

    with open("slowa.txt", encoding='UTF-8') as file:
        for line in file:
            line.lower()
            tab.append(line)
    word = tab[random]
    print(word)

    coded = ''
    for i in range(0, len(word)):
        for letter in word[i]:
            if letter in 'aceimnorsuvwxz':
                coded += '1'
            if letter in 'ąęgjpqy':
                coded += '2'
            if letter in 'bćdfhklłńóśtżź':
                coded += '3'
    print(coded)
    code = coded.encode('utf8')
    client_socket.send(code)
    break

counter = 0
length = len(coded)
print(length)
repetition = []
while True:
    letter = client_socket.recv(BUFFER).decode('utf8')
    if letter in repetition:
        client_socket.send("The letter has been provided. Please choose another one: ".encode('utf8'))
        continue
    else:
        repetition.append(letter)
    if letter == '':
        server_socket.close()
        break

    for i in range(0, len(coded)):
        if letter in word[i]:
            coded_list = list(coded)
            coded_list[i] = letter
            coded = "".join(coded_list)
            length = length - 1
        if i == (len(coded) - 1) and letter not in word:
            counter += 1
            if counter == 10:
                msg = f"This is your {counter} mistake.\nYOU LOST!\n The correct answer is : {word}" \
                      f"\nIf you want to finish, please press enter :)"
                client_socket.send(msg.encode('utf8'))
                server_socket.close()
                break
            else:
                msg1 = f"This is your {counter} mistake.\n{coded}"
                client_socket.send(msg1.encode('utf8'))
        if i == (len(coded) - 1) and letter in word and length != 0:
            client_socket.send(coded.encode('utf8'))
        if i == (len(coded) - 1) and letter in word and length == 0:
            msg2 = f"{coded}\n YOU WON!\nIf you want to finish, please press enter :)"
            client_socket.send(msg2.encode('utf8'))

    print(coded)
