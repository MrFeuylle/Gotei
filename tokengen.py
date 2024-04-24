import requests
import json
import os
import getpass
import subprocess
import json
import pyfiglet
import shutil
from colorama import init, Fore, Back, Style

projets = ["libft","get_next_line","ft_printf", "push_swap", "pipex", "minitalk", "so_long", "FdF", "fract-ol", "philosophers", "minishell","cub3d","minirt","cpp00-04","cpp05-09","ft_irc","webserv","inception"]

def print_centered(text):
    terminal_width = shutil.get_terminal_size().columns
    padding = (terminal_width - len(text)) // 2
    print(" " * padding + text)

def check_password(intput_string):
    curl_command = [
        'curl',
        '-X', 'POST',
        '-d', 'input_string={}'.format(input_string),
        'http://51.77.151.35:8000/check_string/'
    ]

    process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        response_json = json.loads(output.decode('utf-8'))
        result = response_json['result']
    if result != 1:
        exit()

def get_token(intput_string):
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
        return (result)

def add_deploy_key(repo_owner, repo_name, ssh_key, title, token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/keys"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": title,
        "key": ssh_key,
        "read_only": True  # Set to False if you want write access
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        print("Deploy key added successfully.")
    else:
        print("Failed to add deploy key:")
        print(response.text)

def delete_deploy_key(repo_owner, repo_name, key_id, token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/keys/{key_id}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        print("Deploy key deleted successfully.")
    else:
        print("Failed to delete deploy key:")
        print(response.text)

def get_deploy_key_id(repo_owner, repo_name, title, token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/keys"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        keys = response.json()
        for key in keys:
            if key['title'] == title:
                return key['id']
        return None
    else:
        print("Failed to get deploy keys:")
        print(response.text)
        return None

def read_file_content(file_path):
    try:
        expanded_path = os.path.expanduser(file_path)
        with open(expanded_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Le fichier '{file_path}' n'existe pas.")
        return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier : {e}")
        return None

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
        print("Clonage réussi !")
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

# Utilisation de la fonction pour imprimer "Gotei13" en ASCII art
print_ascii_art(":=.\n:+%@@@%+:\n-*@%%#####%@@*-.\n----.             .----.\n:==-                       -==.\n:==:                             -==:\n-*=.                                   :*+:\n-*@@:                -%*..%=%@=            .@@@*-\n.-+%@@@@*              .+%*:   .+%=.             -@@@@@#+-\n:*%@@@@@+              %@@@@@@:@@:=-             :@@@@@@%+.\n:+%@@%                  :@@.::::.             *@@@#=.\n.=%#                  ::                  :@*-.\n.===.                               .==:\n--==:                       .---.\n:+*=.                -==.\n.=**+=--::::-==++=\n.-*@@@@@@@+:\n:*#+:")


input_string = getpass.getpass("Password:")
check_password(input_string)
command = ['clear']
subprocess.run(command)
print_ascii_art("  ____           _            _     _   _____ \n / ___|   ___   | |_    ___  (_)   / | |___ / \n| |  _   / _ \  | __|  / _ \ | |   | |   |_ \ \n| |_| | | (_) | | |_  |  __/ | |   | |  ___) |\n \____|  \___/   \__|  \___| |_|   |_| |____/\n\n")
repo_owner = "repo-gotei13"
ssh_key = read_file_content("~/.ssh/id_rsa.pub")
title = "Gotei Deploy key"
github_token = get_token(input_string)
show_choice(projets)
choice = getpass.getpass()
choice = int(choice)
repo_name = projets[choice]
print("Projet =", repo_name)
repository_url = "https://" + github_token + "@github.com/repo-gotei13/" + repo_name
git_clone_with_token(repository_url,repo_name,github_token)
