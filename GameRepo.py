import os
import pickle
import time
import requests
from bs4 import BeautifulSoup

# Function Area
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
                name = find_between(link[1:len(link)], "/", "/")
                name = name.replace("_", " ")
                game = {"game_name": str(name), "game_id": str(id), "game_link": str(oglink)}
                print("\n"
                      " Name: {}\n"
                      " AppID: {}\n"
                      " Game Link: {}".format(name, id, oglink))
                return game

banner = ("=========================\n"
               "= Steam Game Repository =\n"
               "=========================")

# First time setup section
try:
    with open("main_script.txt", "r") as file:
        test_main_script = file.read()
    with open("settings//settings.pickle", "rb") as file:
        settings = pickle.load(file)
        stage = 1
except:
    try:
        with open("settings//games.pickle", "rb") as file:
            games = pickle.load(file)
        print("1 or more important file cannot be found!\n"
              "However, your game data may be able to be recovered!\n"
              "In order to recover your game data, you will need to\n"
              "go through part of the initial setup process!\n"
              "You will need to know the following:\n"
              "1. Where your games (if any) are installed! This would've been your ROOT PATH!\n"
              "2. Steam username!\n"
              "Would you like to attempt a restore on your game data?")
        gr = input("Y/N: ")
        if gr.upper() == "Y":
            stage2 = 1
        elif gr.upper() == "N":
            stage2 = 0
        else:
            print("That wasn't a Y or N so I'm assuming you want to attempt a restore.")
            stage2 = 1
            input(" ")
        stage = 0
    except:
        print(banner)
        print("1 or more critical files not found...\n"
              "Starting first time setup...")
        time.sleep(1)
        print(".")
        time.sleep(1)
        print(".")
        time.sleep(1)
        stage = 0
        stage2 = 0
        os.system("cls")

if stage == 0:
    x = "N"
    while x.upper() == "N":
        os.system("cls")
        print(banner)
        print("!!BEFORE PROCEEDING!!\n"
              "PLEASE START STEAM CMD AND PERFORM THE FOLLOWNG COMMANDS!\n"
              "================\n"
              "login (YOUR STEAM USERNAME)\n"
              "     (IT WILL THEN ASK FOR YOUR PASSWORD & 2FA IF APPLICABLE)\n"
              "quit\n"
              "================\n"
              "THIS IS TO ENSURE PROPER FUNCTIONALITY!")
        input("PRESS ENTER WHEN THE ABOVE IS COMPLETE: ")
        os.system("cls")
        print(banner)
        print("Where would you like the ROOT of the Game Repository to be?\n"
                           "Example: 'G:\Steam'\n"
                           "The above example will cause indivisual game folders to be \n"
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
            if stage2 == 0:
                edit_settings(master_dir, username, "write")
                os.system("cls")
                print(banner)
                input("Initial setup is complete...\n"
                      "Restarting Steam Game Repository for your changes to take effect!")
                os.system("python GameRepo.py")
                quit()
            else:
                edit_settings(master_dir, username, "write")
                os.system("cls")
                print(banner)
                input("Game data recovery is complete...\n"
                      "Restarting Steam Game Repository for your changes to take effect!")
                input("MAKE SURE YOU PERFORM THE FOLLOWING STEPS AFTER RESTART!!!\n"
                      "1. Go to Settings(5)!\n"
                      "2. Recover your Main Script(3)!\n"
                      "Once you perform the above steps, your Steam Game Repository should be back to normal!")
                os.system("python GameRepo.py")
                quit()


# Main Menu
elif stage == 1:
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
                    print("\nIs the game listed above? It is recommended to take a sec and verify\nthat the correct game"
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
                                                          'app_update {} validate\n'.format(game_name, master_dir, game_name, game_id), "")
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
                  "3. Recover Main Script")
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