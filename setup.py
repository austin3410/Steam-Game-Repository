import os

try:
    import pickle
    import requests
    from bs4 import BeautifulSoup
    print("Good to go\n"
          "Starting GameRepo.py")
    os.system("python GameRepo.py")
except:
    os.system("get-pip.py")
    os.system("pip install requests")
    os.system("pip install bs4")
    os.system("pip install requests")
    print("Dependencies installed...\n"
          "Running setup.py again to be sure.")
    os.system("python setup.py")
quit()