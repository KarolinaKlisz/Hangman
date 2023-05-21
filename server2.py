import socket as s
from random import randint

HOST = '192.168.70.114'
PORT = 33000
BUFFER = 1024

random = randint(0, 3185486)
tab = []

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)  # tworzymy obiekt socket
server_socket.bind((HOST, PORT))
server_socket.listen(2)  # ilu użytkowników

while True:
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established.")
    client_socket1, address1 = server_socket.accept()
    print(f"Connection from {address1} has been established.")

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
    code1 = coded
    code2 = coded
    client_socket.send(code)
    client_socket1.send(code)
    break

counter1 = 0
counter2 = 0
length1 = len(code1)
length2 = len(code2)

repetition1 = []
repetition2 = []
while True:
    letter1 = client_socket.recv(BUFFER).decode('utf8')
    if letter1 in repetition1:
        client_socket.send("The letter has been provided, please choose another one: ".encode('utf8'))
        continue
    else:
        repetition1.append(letter1)

    if letter1 == '':
        break

    for i in range(0, len(code1)):
        if letter1 in word[i]:
            coded1_list = list(code1)
            coded1_list[i] = letter1
            code1 = "".join(coded1_list)
            length1 = length1 - 1
        if i == (len(code1) - 1) and letter1 not in word:
            counter1 += 1
            if counter1 == 10:
                msg = f"This is your {counter1} mistake.\nYOU LOST\nThe correct answer is: {word}" \
                      f"\nIf you want to finish, please press enter :)"
                client_socket.send(msg.encode('utf8'))
                client_socket1.send(
                    f"Your opponent lost, you won. Congratulations!\n The correct answer is: {word}" \
                    f"\nIf you want to finish, please press enter :)".encode('utf8'))
                server_socket.close()
                break
            else:
                msg1 = f"This is your {counter1} mistake.\n{code1}"
                client_socket.send(msg1.encode('utf8'))
        if i == (len(code1) - 1) and letter1 in word and length1 != 0:
            client_socket.send(code1.encode('utf8'))
        if i == (len(code1) - 1) and letter1 in word and length1 == 0:
            msg2 = f"{code1}\n YOU WON!\nIf you want to finish, please press enter :)"
            client_socket.send(msg2.encode('utf8'))
            client_socket1.send(
                f"You lost. Your opponent won. The correct answet is: {word}" \
                f"\nIf you want to finish, please press enter :)".encode('utf8'))
            server_socket.close()
    print(coded)
    letter2 = client_socket1.recv(BUFFER).decode('utf8')
    if letter2 in repetition2:
        client_socket1.send("The letter has been provided, please choose another one: ".encode('utf8'))
        continue
    else:
        repetition2.append(letter2)

    if letter2 == '':
        break
    for j in range(0, len(code2)):
        if letter2 in word[j]:
            coded2_list = list(code2)
            coded2_list[j] = letter2
            code2 = "".join(coded2_list)
            length2 = length2 - 1
        if j == (len(code2) - 1) and letter2 not in word:
            counter2 += 1
            if counter2 == 10:
                msg = f"This is your {counter2} mistake.\nYOU LOST\nThe correct answer is: {word}" \
                      f"\nIf you want to finish, please press enter :)"
                client_socket1.send(msg.encode('utf8'))
                client_socket.send(
                    f"Your opponent lost, you won. Congratulations!\n The correct answer is: {word}" \
                    f"\nIf you want to finish, please press enter :)".encode('utf8'))
                server_socket.close()
                break
            else:
                msg1 = f"This is your {counter2} mistake.\n{code2}"
                client_socket1.send(msg1.encode('utf8'))
        if j == (len(code2) - 1) and letter2 in word and length2 != 0:
            client_socket1.send(code2.encode('utf8'))
        if j == (len(code2) - 1) and letter2 in word and length2 == 0:
            msg2 = f"{code2}\n YOU WON!\nIf you want to finish, please press enter:)"
            client_socket1.send(msg2.encode('utf8'))
            client_socket.send(
                f"You lost. Your opponent won. The correct answer is: {word}" \
                f"\nIf you want to finish, please press enter :)".encode('utf8'))
            server_socket.close()




