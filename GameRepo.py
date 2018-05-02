import os
import pickle
import time
import requests
from bs4 import BeautifulSoup
import fnmatch
import zipfile

# Global Variables

banner = ("=========================\n"
               "= Steam Game Repository =\n"    
               "=========================")

version = "V1.1.2"

# Function Area
def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename

def unzip_file(file_name):
    zip_ref = zipfile.ZipFile(file_name, "r")
    zip_ref.extractall("update")
    zip_ref.close()

def get_next_dir(dir):
    r = []
    subdirs = [x[0] for x in os.walk(dir)]
    for subdir in subdirs:
        files = os.walk(subdir)
        for file in files:
            r.append(file)
    return r[0][1][0]

def edit_settings(master_dir, username, op):
    if op == "write":
        try:
            with open("settings//settings.pickle", "wb") as file:
                settings = {"master_dir": master_dir, "username": username}
                pickle.dump(settings, file)
        except:
            os.system("mkdir settings")
            with open("settings//settings.pickle", "wb") as file:
                settings = {"master_dir": master_dir, "username": username}
                pickle.dump(settings, file)
    elif op == "read":
        try:
            with open("settings//settings.pickle", "rb") as file:
                all_settings = pickle.load(file)
                return all_settings
        except:
            return "SETTINGS NOT FOUND"

def toggle_val():
    with open("settings//settings.pickle", "rb") as file:
        settings = pickle.load(file)
    with open("main_script.txt", "r") as file:
        main_script = file.read()
    try:
        if settings["validate"] == "True":
            settings["validate"] = "False"
            while True:
                if "validate" in main_script:
                    main_script = main_script.replace("validate", "")
                else:
                    break
        elif settings["validate"] == "False":
            settings["validate"] = "True"
            main_script = main_script.splitlines()
            counter = 0
            for line in main_script:
                if "app_update" in line:
                    main_script[counter] = line + "validate"
                counter += 1
            main_script = "\n".join(main_script)
        with open("settings//settings.pickle", "wb") as file:
            pickle.dump(settings, file)
        with open("main_script.txt", "w") as file:
            file.write(main_script)
        return "DONE"
    except:
        val = {"validate": "True"}
        new_dic = {**settings, **val}
        with open("settings//settings.pickle", "wb") as file:
            pickle.dump(new_dic, file)
        return "RUN AGAIN"


def games_add(game_name, game_id, op):
    if op == "write":
        try:
            with open("settings//games.pickle", "rb") as file:
                games = pickle.load(file)
            with open("settings//games.pickle", "wb") as file:
                new_games = {str(game_name): str(game_id)}
                all_games = {**new_games, **games}
                pickle.dump(all_games, file)
        except:
            with open("settings//games.pickle", "wb") as file:
                new_games = {str(game_name): str(game_id)}
                pickle.dump(new_games, file)
    elif op == "read":
        try:
            with open("settings//games.pickle", "rb") as file:
                games = pickle.load(file)
                return games
        except:
            return "NO GAMES"

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def steam_search(game_name, target):
    url_game_name = game_name.replace(" ", "%20")
    url = "http://store.steampowered.com/search/?term={}".format(url_game_name)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    counter = 0
    for link in soup.find_all('a'):
        if "/app/" in str(link):
            counter += 1
            if counter == target:
                link = str(link.get('href'))
                oglink = link
                link = link[33:len(link)]
                id = find_between(link, "/", "/")
                name = find_between(link[2:len(link)], "/", "/")
                name = name.replace("_", " ")
                game = {"game_name": str(name), "game_id": str(id), "game_link": str(oglink)}
                print("\n"
                      " Name: {}\n"
                      " AppID: {}\n"
                      " Game Link: {}".format(name, id, oglink))
                return game

def file_check():
    file_check.stage = {"main_script.txt": 0, "settings.pickle": 0}
    try:
        with open("main_script.txt", "r") as file:
            test_ms = file.read()
        file_check.stage["main_script.txt"] = 1
    except:
        print("main_script.txt not found...")
        time.sleep(.5)
    try:
        with open("settings//settings.pickle", "rb") as file:
            test_set = pickle.load(file)
        file_check.stage["settings.pickle"] = 1
    except:
        print("settings.pickle not found...")
        time.sleep(.5)
    return file_check.stage

# First time setup section
# Crit File Check
stage = file_check()
if stage["main_script.txt"] == 0 and stage["settings.pickle"] == 0:
    os.system("cls")
    print(banner)
    print("Starting first time setup...")
    time.sleep(1)
    os.system("cls")
    print(banner)
    print("!!BEFORE PROCEEDING!!\n"
          "PLEASE START STEAM CMD AND PERFORM THE FOLLOWING COMMANDS!\n"
          "================\n"
          "login (YOUR STEAM USERNAME)\n"
          "     (IT WILL THEN ASK FOR YOUR PASSWORD & 2FA IF APPLICABLE)\n"
          "quit\n"
          "================\n"
          "THIS IS TO ENSURE PROPER FUNCTIONALITY!")
    input("PRESS ENTER WHEN THE ABOVE IS COMPLETE: ")
    x = "N"
    while x.upper() == "N":
        os.system("cls")
        print(banner)
        print("Where would you like the ROOT of the Game Repository to be?\n"
              "Example: 'G:\Steam'\n"
              "The above example will cause individual game folders to be \n"
              "generated inside the Steam folder.")
        master_dir = input("Path without 's: ")
        try:
            temp_master_dir = master_dir.replace("\\", "//")
            with open("{}//test.txt".format(temp_master_dir), "w") as file:
                test = "test"
                file.write(test)
            os.system("del /Q {}\\test.txt".format(master_dir))
        except:
            print("This path doesn't currently exist.\n"
                  "I will go ahead and create it for you...")
            os.system("mkdir {}".format(master_dir))
            input("Path has been created!")
        os.system("cls")
        print(banner)
        print("Ok, now what is your Steam username? This is the name you use to login to Steam.")
        username = input("Username: ")
        os.system("cls")
        print(banner)
        print("Please verify that both the path and username are correct.\n"
              "Path: {}\n"
              "Username: {}".format(master_dir, username))
        y = input("Y/N: ")
        if y.upper() == "N":
            x = "N"
        elif y.upper() == "Y":
            with open("settings//default_script.txt", "r") as file:
                default_script = file.read()
                main_script = default_script.replace("anonymous", username)
            with open("main_script.txt", "w") as file:
                file.write(main_script)
            edit_settings(master_dir, username, "write")
            os.system("cls")
            print(banner)
            print("Initial setup is complete...\n"
                  "Restarting Steam Game Repository for your changes to take effect!")
            time.sleep(2)
            os.system("python GameRepo.py")
            quit()

elif stage["main_script.txt"] == 0 and stage["settings.pickle"] == 1:
    os.system("cls")
    print(banner)
    print("Your main_script.txt file is missing or unreadable...\n"
          "SGR will now attempt and automatic recovery.\n")
    input("CONTINUE AFTER YOU'VE READ THE ABOVE!!")
    os.system("cls")
    print(banner)
    print("MAIN SCRIPT REBUILD IN PROGRESS...")
    settings = edit_settings(None, None, "read")
    with open("settings//default_script.txt", "r") as file:
        default_script = file.read()
    main_script = default_script.replace("anonymous", settings["username"])
    try:
        with open("settings//games.pickle", "rb") as file:
            games = pickle.load(file)
        games = games_add(None, None, "read")
        for game in games:
            main_script = main_script.replace("//END", '\n'
                                                       '\n'
                                                       '//{}\n'
                                                       'force_install_dir "{}\{}"\n'
                                                       'app_update {} validate\n'
                                                       '//END'.format(game, settings["master_dir"], game, games[game]))
    except:
        pass
    with open("main_script.txt", "w") as file:
        file.write(main_script)
    print("REBUILD COMPLETE!")
    time.sleep(1)
    os.system("cls")
    print(banner)
    print("Restarting Steam Game Repository for your changes to take effect!")
    time.sleep(2)
    os.system("python GameRepo.py")
    quit()

elif stage["main_script.txt"] == 1 and stage["settings.pickle"] == 0:
    os.system("cls")
    print(banner)
    print("Your settings.pickle file is missing or unreadable...\n"
          "You will have to go through part of the initial setup\n"
          "once again in order to fix the problem.\n")
    input("CONTINUE AFTER YOU'VE READ THE ABOVE!!")
    x = "N"
    while x.upper() == "N":
        os.system("cls")
        print(banner)
        print("Where is the ROOT of your Game Repository?\n"
              "Example: 'G:\Steam'\n"
              "The above example will cause individual game folders to be \n"
              "generated inside the Steam folder.")
        master_dir = input("Path without 's: ")
        try:
            temp_master_dir = master_dir.replace("\\", "//")
            with open("{}//test.txt".format(temp_master_dir), "w") as file:
                test = "test"
                file.write(test)
            os.system("del /Q {}\\test.txt".format(master_dir))
        except:
            print("This path doesn't currently exist.\n"
                  "I will go ahead and create it for you...")
            os.system("mkdir {}".format(master_dir))
            input("Path has been created!")
        os.system("cls")
        print(banner)
        print("Ok, now what is your Steam username? This is the name you use to login to Steam.")
        username = input("Username: ")
        os.system("cls")
        print(banner)
        print("Please verify that both the path and username are correct.\n"
              "Path: {}\n"
              "Username: {}".format(master_dir, username))
        y = input("Y/N: ")
        if y.upper() == "N":
            x = "N"
        elif y.upper() == "Y":
            with open("settings//default_script.txt", "r") as file:
                default_script = file.read()
                main_script = default_script.replace("anonymous", username)
            edit_settings(master_dir, username, "write")
            os.system("cls")
            print(banner)
            print("Settings recovery is complete...\n"
                  "Restarting Steam Game Repository for your changes to take effect!")
            time.sleep(2)
            os.system("python GameRepo.py")
            quit()

# Main Menu
if stage["main_script.txt"] == 1 and stage["settings.pickle"] == 1:
    all_settings = edit_settings(master_dir=None, username=None, op="read")
    master_dir = all_settings["master_dir"]
    x = "1"
    while x.upper() != "Q":
        os.system("cls")
        print(banner)
        settings = edit_settings(None, None, "read")
        games = games_add(None, None, "read")
        if games == "NO GAMES":
            counter = 0
        else:
            counter = 0
            for game in games:
                counter += 1
        print("Steam Username:  {}\n"
              "ROOT PATH:       {}\n"
              "Number of Games: {}\n"
              "~~~~~~~~~~~~~~~~".format(settings["username"], settings["master_dir"], counter))
        print("What would you like to do?\n"
              "1. Add Game\n"
              "2. Start Manual Sync\n"
              "3. Remove Game\n"
              "4. List Games\n"
              "5. Settings\n"
              "~~~~~~~~~~~~~~~~\n"
              "Q: Quit\n"
              "R: ReadMe")
        x = input(": ")
        if x == "1":
            os.system("cls")
            print(banner)
            print("What is the games name?")
            game_name = input(": ")
            a = "N"
            counter = 4
            while a.upper() == "N":
                if counter == 7:
                    game_url = "https://steamdb.info/search/?a=app&q=" + game_name.replace(" ", "%20")
                    os.system("cls")
                    print(banner)
                    print("Go to:\n"
                          "{}\n"
                          "to find the games App ID.\n".format(game_url))
                    print("What is the games App ID?")
                    game_id = input(": ")
                    games_add(game_name, game_id, "write")
                    with open("main_script.txt", "r") as file:
                        script = file.read()
                        script = script.replace("//END", '\n'
                                                         '\n'
                                                         '//{}\n'
                                                         'force_install_dir "{}\{}"\n'
                                                         'app_update {} validate\n'
                                                         '//END'.format(game_name, master_dir, game_name, game_id))
                    with open("main_script.txt", "w") as file:
                        file.write(script)
                    a = "Y"
                else:
                    os.system("cls")
                    print(banner)
                    print("The following game was found:")
                    rgame = steam_search(game_name, counter)
                    print("\nIs the game listed above? It is recommended to take a sec and verify\nthat the correct "
                          "game"
                          " was found by visiting the link above.")
                    counter += 1
                    a = input("Y/N: ")
            if a.upper() == "Y":
                os.system("cls")
                print(banner)
                game_id = rgame["game_id"]
                game_name = rgame["game_name"]
                game_link = rgame["game_link"]
                games_add(game_name, game_id, "write")
                with open("main_script.txt", "r") as file:
                    script = file.read()
                    script = script.replace("//END", '\n'
                                                     '\n'
                                                     '//{}\n'
                                                     'force_install_dir "{}\{}"\n'
                                                     'app_update {} validate\n'
                                                     '//END'.format(game_name, master_dir, game_name, game_id))
                with open("main_script.txt", "w") as file:
                    file.write(script)
                print("{} has been added to your Repository!".format(game_name))
                input(" ")
        elif x == "2":
            os.system("cls")
            print(banner)
            print("running main_script.txt...")
            os.system("steamcmd.exe +runscript main_script.txt")
            print("DONE!!!")
            input(" ")
        elif x == "3":
            os.system("cls")
            print(banner)
            games = games_add(None, None, "read")
            game_list = []
            if games == "NO GAMES":
                counter = 0
                print("No games have been found!")
            else:
                counter = 0
                print("Which game would you like to remove?")
                print("~~~~~~~~~~~~~~~~")
                for game in games:
                    print(" {}. {} : {}".format(counter, game, games[game]))
                    game_list.append(str(game))
                    counter += 1
            if counter == 0:
                os.system("cls")
                print(banner)
                print("No games have been found!")
                input(" ")
            else:
                print("~~~~~~~~~~~~~~~~")
                number = input(": ")
                if number.isalpha():
                    print("Please enter the number that's to the left of the game's name.")
                elif int(number) <= (counter - 1):
                    os.system("cls")
                    print(banner)
                    print("Are you sure you want to delete:\n {}".format(game_list[int(number)]))
                    a = input("Y/N: ")
                    if a.upper() == "Y":
                        game_id = games[game_list[int(number)]]
                        game_name = game_list[int(number)]
                        del games[game_name]
                        with open("settings//games.pickle", "wb") as file:
                            pickle.dump(games, file)
                        with open("main_script.txt", "r") as file:
                            main_script = file.read()
                        main_script = main_script.replace('\n'
                                                          '\n'
                                                          '//{}\n'
                                                          'force_install_dir "{}\{}"\n'
                                                          'app_update {} validate\n'.format(game_name, master_dir,
                                                                                            game_name, game_id), "")
                        with open("main_script.txt", "w") as file:
                            file.write(main_script)
                        os.system("cls")
                        print(banner)
                        print("{} removed from Repository!".format(game_name))
                        print("Would you like to erase the local game files as well?")
                        z = input("Y/N: ")
                        if z.upper() == "Y":
                            os.system("cls")
                            print(banner)
                            print("DELETING FOLDER {}\{}".format(master_dir, game_name))
                            os.system('rmdir /S /Q "{}\{}"'.format(master_dir, game_name))
                            print("\n"
                                  "\n"
                                  "DONE!!!")
                            print("{} removed from file system!".format(game_name))
                        elif z.upper() == "N":
                            os.system("cls")
                            print(banner)
                            print("{}'s local files will be saved!".format(game_name))
                        else:
                            print("That wasn't a Y or a N so I'm assuming you want to keep the files.")
                    elif a.upper() == "N":
                        os.system("cls")
                        print(banner)
                        game_name = game_list[int(number)]
                        print("Ok, {} won't be uninstalled or removed from your repository.".format(game_name))
                    else:
                        os.system("cls")
                        print(banner)
                        print("That wasn't a Y or a N so I'm assuming you don't want to remove the game.")
                        pass
                else:
                    print("Game Not Found!\n"
                          "Make sure you are spelling the game correctly and\n"
                          "that the game is in the games list!")
                input(" ")
        elif x == "4":
            os.system("cls")
            print(banner)
            games = games_add(None, None, "read")
            print(" Game Name : Steam App ID\n"
                  "~~~~~~~~~~~~~~~~~~~~~~~~~~")
            if games == "NO GAMES":
                counter = 0
            else:
                counter = 0
                for game in games:
                    print(" {} : {}".format(game, games[game]))
                    counter += 1
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("{} games found in total!".format(str(counter)))
            input(" ")
        elif x.upper() == "R":
            os.system("cls")
            print(banner)
            os.system("settings\README.txt")
        elif x.upper() == "5":
            os.system("cls")
            print(banner)
            print("Settings:\n"
                  "NOTE: Changes to these settings\n"
                  "will require a restart of\n"
                  "Steam Game Repository!!\n"
                  "~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                  "1. Change Steam Games ROOT PATH\n"
                  "2. Change Steam Username\n"
                  "3. Recover Main Script\n"
                  "4. Toggle Game Validation\n"
                  "5. About SGR")
            z = input(": ")
            if z == "1":
                os.system("cls")
                print(banner)
                settings = edit_settings(None, None, "read")
                print("Current ROOT PATH: {}".format(settings["master_dir"]))
                print("Enter new ROOT PATH:")
                new_master_dir = input(": ")
                edit_settings(master_dir=new_master_dir, username=settings["username"], op="write")
                try:
                    with open("main_script.txt", "r") as file:
                        main_script = file.read()
                    main_script = main_script.replace(settings["master_dir"], new_master_dir)
                    with open("main_script.txt", "w") as file:
                        file.write(main_script)
                    print("ROOT PATH has been changed!\n"
                          "Now restarting Steam Game Repository!")
                except:
                    print("main_script.txt not found!")
                input(" ")
                os.system("python GameRepo.py")
                quit()
            elif z == "2":
                os.system("cls")
                print(banner)
                settings = edit_settings(None, None, "read")
                print("Current Steam Username: {}".format(settings["username"]))
                print("Enter new Steam Username:")
                new_username = input(": ")
                edit_settings(master_dir=settings["master_dir"], username=new_username, op="write")
                try:
                    with open("main_script.txt", "r") as file:
                        main_script = file.read()
                    main_script = main_script.replace(settings["username"], new_username)
                    with open("main_script.txt", "w") as file:
                        file.write(main_script)
                    print("Steam Username has been changed!\n"
                          "Now restarting Steam Game Repository!")
                except:
                    print("main_script.txt file not found!")
                input(" ")
                os.system("python GameRepo.py")
                quit()
            elif z == "3":
                os.system("cls")
                print(banner)
                print("If your main_script.txt gets lost or\n"
                      "is corrupted and no longer works.\n"
                      "You can try to make Steam Game Repository\n"
                      "recover your main_script.txt file by\n"
                      "rebuilding it with the data it already has.")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("Would you like to rebuild\n"
                      "your main_script.txt file?")
                a = input("Y/N: ")
                if a.upper() == "Y":
                    os.system("cls")
                    print(banner)
                    print("MAIN SCRIPT REBUILD IN PROGRESS...")
                    settings = edit_settings(None, None, "read")
                    with open("settings//default_script.txt", "r") as file:
                        default_script = file.read()
                    main_script = default_script.replace("anonymous", settings["username"])
                    games = games_add(None, None, "read")
                    for game in games:
                        main_script = main_script.replace("//END", '\n'
                                                         '\n'
                                                         '//{}\n'
                                                         'force_install_dir "{}\{}"\n'
                                                         'app_update {} validate\n'
                                                         '//END'.format(game, settings["master_dir"], game, games[game]))
                    with open("main_script.txt", "w") as file:
                        file.write(main_script)
                    print("REBUILD COMPLETE!")
                    input(" ")
                elif a.upper() == "N":
                    pass
            elif z == "5":
                os.system("cls")
                print(banner)
                print("Thanks for using Steam Game Repository!\n"
                      "Created by austin3410\n"
                      "Current Version: {}\n"
                      "\n"
                      "1. Check for new version:\n".format(version))
                x = input(": ")
                if x == "1":
                    os.system("cls")
                    print(banner)
                    url = "https://github.com/austin3410/Steam-Game-Repository/releases/latest"
                    r = requests.get(url)
                    data = r.text
                    soup = BeautifulSoup(data, "html.parser")
                    span = soup.find_all("span", {"class": "css-truncate-target"})
                    for thing in span:
                        filtered = fnmatch.filter(thing, "V?.?.?")
                        new_version = filtered[0]
                        if version == new_version:
                            print("You have the most up to date version!")
                        else:
                            print("There is a newer version available!\n"
                                  "Your Version: {}\n"
                                  "Current Version: {}\n"
                                  "Would you like to download and install it?\n".format(version, new_version))
                            u = input("Y/N: ")
                            if u.upper() == "Y":
                                os.system("cls")
                                print(banner)
                                try:
                                    durl = "https://github.com/austin3410/Steam-Game-Repository/archive/{}.zip".format(new_version)
                                    file_name = download_file(durl)
                                    unzip_file(file_name)
                                    next_dir = get_next_dir("update")
                                    with open("update//{}//settings//instructions.txt".format(next_dir), "r") as file:
                                        ins = file.read()
                                        ins = ins.splitlines()
                                    for i in ins:
                                        os.system("{}".format(i))
                                    os.system("rm {}.zip".format(new_version))
                                    os.system("rmdir /Q /S update")
                                    print("Update complete! SGR will now restart!")
                                    input(" ")
                                    os.system("python GameRepo.py")
                                    quit()
                                except:
                                    print("Something went wrong!")
                            else:
                                pass

                input(" ")
            elif z == "4":
                os.system("cls")
                print(banner)
                with open("settings//settings.pickle", "rb") as file:
                    settings = pickle.load(file)
                print("Disabling Game Validation will drastically decrease update times.\n"
                      "However, doing this will also prevent games from performing\n"
                      "integrity checks.\n")
                try:
                    print("CURRENT VALIDATION SETTING: {}\n".format(settings["validate"]))
                except:
                    print("CURRENT VALIDATION SETTING: True\n")
                x = input("Are you sure: Y/N: ")
                if x.upper() == "Y":
                    tog = toggle_val()
                    os.system("cls")
                    print(banner)
                    if tog == "RUN AGAIN":
                        print("Please run this command again!\n"
                              "You should only have to do this once!")
                    elif tog == "DONE":
                        print("Validation toggled!")
                    input("")
                else:
                    pass
