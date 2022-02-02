import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []

questions = [
     " What is the Italian word for PIE? \n a.Pasty\n b.Patty\n c.Pizza",
     " Water boils at 212 Units at which scale? \n a.Fahrenheit\n b.Celsius\n c.Kelvin",
     " Which sea creature has three hearts? \n a.Dolphin\n b.Octopus\n c.Walrus",
     " Hg stands for? \n a.Mercury\n b.Hulgerium\n c.Halfnium",
     " Which planet is closest to the sun? \n a.Mercury\n b.Pluto\n c.Venus"
]

answers = ['c', 'a', 'b', 'a', 'a']

print("This server has started")

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn, nickname):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer will only be a, b, c or d".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    print(answer)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.split(" ")[-1].lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
                print(answer)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message = "{} joined!".format(nickname)
    print(message)
    new_thread = Thread(target= clientthread,args=(conn, nickname))
    new_thread.start()