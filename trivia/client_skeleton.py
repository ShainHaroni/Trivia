import ast
import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****
import json
import random


class bcolors:
    HEADDER = '\033[95m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    BLUE = '\033[34m'

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    # Implement Code
    msg = chatlib.build_message(code, data)
    conn.send(msg.encode())


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """

    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)

    return cmd, data


def connect():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", 5678))
    return my_socket


def error_and_exit(error_msg):
    error_msg.quit()


def login(conn):

    while True:
        username = input("Please enter username: \n")
        password = input("Please enter your password: \n")
        data = username + chatlib.DATA_DELIMITER + password

        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)
        answer = recv_message_and_parse(conn)
        if answer[0] == "LOGIN_OK":
            print("Logged in!")
            return username
        elif answer[0] == "ERROR":
            print(answer[1])


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print(bcolors.RED, "Good Bye!", bcolors.ENDC)


def build_send_recv_parse(conn, msg_code, data):
    build_and_send_message(conn, msg_code, data)
    temp = recv_message_and_parse(conn)
    return temp


def get_score(conn, username):
    score = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_score"], username)

    if score == (None, None):
        print(bcolors.FAIL,"Error !", bcolors.ENDC)
    else:
        print(bcolors.BOLD, bcolors.BLUE,f"Your score is: {int(score[1])} ", bcolors.ENDC)


def get_highscore(conn):
    high_score = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_high_score"], "")
    result = high_score[1]
    x = list(ast.literal_eval(result))

    for i in x:
        print(bcolors.BOLD, bcolors.BLUE, i[0], ':', i[1], bcolors.ENDC)


def print_ans(answers):
    for i, ans in enumerate(answers):
        print(i + 1, ": ", ans,bcolors.ENDC)
    print(bcolors.RED, '\nTo quit press ''9''',bcolors.ENDC)


def play_question(conn, username):
    response = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_question"], "")
    questions_dict = eval(response[1])
    questions_list = list(questions_dict.values())

    while True:
        if len(questions_list) == 0:
            print(bcolors.RED,"Sorry, No more question for you genius!",bcolors.ENDC)
            break

        current_question = random.choice(questions_list)
        print(bcolors.BLUE,current_question['question'], bcolors.ENDC)
        print_ans(current_question['answers'])
        user_ans = int(input(("Choose your answer [1-4] ")))


        if user_ans == 9:
             break

        if user_ans == int(current_question['correct']):
            print(bcolors.BOLD,"Yes! another question..\n",bcolors.ENDC)
            questions_list.remove(current_question)
            build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_update_score"], username)
        else:
            print(bcolors.FAIL,f"Wrong! the answer is: {current_question['correct']}", bcolors.ENDC)


def get_logged_users(conn):

    users = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_users"], "")[1]
    result = list(ast.literal_eval(users))

    for i in result:
        print(bcolors.BOLD,bcolors.BLUE, f'Connected users are: {i}', bcolors.ENDC)


def main():

    my_socket = connect()
    username = login(my_socket)
    arr = ["Play a trivia question", "Get my score", "Get high Score", "Get logged users", "Quit"]

    while True:
        print(bcolors.BLUE, "\nMAIN MENU:\n", bcolors.ENDC)
        for i, item in enumerate(arr):
            print(bcolors.BOLD, str(i+1) + "." + "         " + item, bcolors.ENDC)
        print(" ")
        select = int(input("Please enter your choice:  "))
        if select == 1:
            play_question(my_socket,username)
        if select == 2:
            get_score(my_socket, username)
        elif select == 3:
            get_highscore(my_socket)
        elif select == 4:
            get_logged_users(my_socket)
        elif select == 5:
            logout(my_socket)
            break


if __name__ == '__main__':
    main()
