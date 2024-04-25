import signal
import requests
import json
import os
import getpass
import subprocess
import json
import shutil
import sys
from colorama import init, Fore, Back, Style

projets = ["libft","get_next_line","ft_printf", "push_swap", "pipex", "minitalk", "so_long", "FdF", "fract-ol", "philosophers", "minishell","cub3d","minirt","cpp00-04","cpp05-09","ft_irc","webserv","inception"]

tty_fd = os.open('/dev/tty', os.O_RDWR)

sys.stdin = open(tty_fd, 'r')
sys.stdout = open(tty_fd, 'w')

def print_centered(text):
    terminal_width = shutil.get_terminal_size().columns
    padding = (terminal_width - len(text)) // 2
    print(" " * padding + text)

def check_password(input_string):
    curl_command = [
        'curl',
        '-X', 'POST',
        '-d', 'input_string={}'.format(input_string),
        'http://51.77.151.35:8000/check_string/'
    ]
    process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    if process.returncode == 0:
        output, error = process.communicate()
        response_json = json.loads(output.decode('utf-8'))
        result = response_json['result']
        if result != 1:
            exit()
    if process.returncode == -1:
        exit()

def get_token(input_string):
    curl_command = [
    'curl',
    '-X', 'POST',
    '-d', 'input_string={}'.format(input_string),
    'http://51.77.151.35:8000/get_token/'
    ]

    process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        response_json = json.loads(output.decode('utf-8'))
        result = response_json['result']
        if result == 0:
            exit()
        return (result)
    if process.returncode == -1:
        exit()

def show_choice(projets):
    i = 0
    for item in projets:
        string = "(" + str(i) + ") " + item
        print_centered(string)
        i = i + 1

def git_clone_with_token(repo_url, destination_dir, token):
    try:
        command = ['git', 'clone', repo_url, destination_dir]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print("Erreur lors du clonage :", e)

def print_ascii_art(text):
    try:
        # Obtenir la largeur du terminal
        terminal_width, _ = shutil.get_terminal_size()
        
        # Générer le texte ASCII art
        ascii_art = text
        # Adapter la largeur du texte ASCII art à la largeur du terminal
        lines = ascii_art.split('\n')
        scaled_ascii_art = '\n'.join(line.center(terminal_width) for line in lines)
        
        # Afficher le texte ASCII art
        print(Fore.RED + scaled_ascii_art + Style.RESET_ALL)
    except Exception as e:
        print("Une erreur s'est produite :", e)

def execute_script(path):
    for file in os.listdir(path):
        path_file = os.path.join(path, file)
        if os.path.isfile(path_file) and os.access(path_file, os.X_OK):
            try:
                subprocess.run([path_file],shell=True, stdin=sys.stdin, stdout=sys.stdout)  
            except Exception as e:
                print("Une erreur s'est produite lors de l'exécution du script bash :", e)

def handler(sig, frame):
    if sig == signal.SIGINT:
        print("",end='')
    elif sig == signal.SIGQUIT:
        print("",end='')

def delete_directory(directory):
    try:
        subprocess.run(["rm", "-rf", directory])
    except Exception as e:
        print("Une erreur s'est produite lors de la suppression du répertoire :", e)

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGQUIT, handler)
command = ['clear']
subprocess.run(command)
print_ascii_art(":=.\n:+%@@@%+:\n-*@%%#####%@@*-.\n----.             .----.\n:==-                       -==.\n:==:                             -==:\n-*=.                                   :*+:\n-*@@:                -%*..%=%@=            .@@@*-\n.-+%@@@@*              .+%*:   .+%=.             -@@@@@#+-\n:*%@@@@@+              %@@@@@@:@@:=-             :@@@@@@%+.\n:+%@@%                  :@@.::::.             *@@@#=.\n.=%#                  ::                  :@*-.\n.===.                               .==:\n--==:                       .---.\n:+*=.                -==.\n.=**+=--::::-==++=\n.-*@@@@@@@+:\n:*#+:")
try:
    input_string = getpass.getpass("Password:")
except EOFError:
    exit()
check_password(input_string)
github_token = get_token(input_string)
command = ['clear']
subprocess.run(command)
print_ascii_art("  ____           _            _     _   _____ \n / ___|   ___   | |_    ___  (_)   / | |___ / \n| |  _   / _ \  | __|  / _ \ | |   | |   |_ \ \n| |_| | | (_) | | |_  |  __/ | |   | |  ___) |\n \____|  \___/   \__|  \___| |_|   |_| |____/\n\n")
repo_owner = "repo-gotei13"
show_choice(projets)
print("")
try:
    choice = getpass.getpass("")
except EOFError:
    exit()
try:
    choice = int(choice)
except ValueError:
    print("Value not valid")
    exit()
if choice > 17 or choice < 0:
    exit()
repo_name = projets[choice]
repository_url = "https://" + github_token + "@github.com/repo-gotei13/" + repo_name
git_clone_with_token(repository_url,repo_name,github_token)
command = ['clear']
subprocess.run(command)
execute_script("./"+ repo_name)
delete_directory(repo_name)
