import socket as s

HOST = '192.168.70.114'
PORT = 33000
BUFFER = 1024

client_socket1 = s.socket(s.AF_INET, s.SOCK_STREAM)
client_socket1.connect((HOST, PORT))

code = client_socket1.recv(BUFFER).decode('utf8')
print(code)

while True:
    letter = input("Podaj literkę ")
    if not letter:
        break
    letter1 = letter.encode('utf8')
    client_socket1.send(letter1)
    attempt = client_socket1.recv(BUFFER).decode('utf8')
    print(attempt)
client_socket1.close()
