# Steam-Game-Repository
Steam Game Repository SGR is a Python based tool that helps people maintain a repository or archive of their Steam games. I imagine that this tool would help households that have low bandwidth and multiple gamers. Or just a lot of gamers in general.


Steam Game Repository (SGR) README

Setting up:

	Setting up SGR is pretty easy. Everything you need should be in the downloaded .zip file:
		Pip Install Script (get-pip.py)
		SteamCMD (steamcmd.exe)
		Steam Game Repository (GameRepo.py)
		Setup (setup.py)
		Settings Folder (settings)
	
	Extract the following into one folder that can be named anything you want and placed anywhere you want.
		GameRepo.py
		get-pip.py
		steamcmd.exe
		setup.py
		settings (folder with the following contents)
		   |----default_script.txt
		   |----README.txt
	
	After that run steamcmd.exe and login using your actual Steam credentials.
	(This will allow SGR to use the cached credentials to download games that you own)
	Next run setup.py to make sure all of the correct dependencies are installed in order to run GameRepo.py.
	Once setup.py has finished installing all missing dependencies (if any exist) it will automatically start
	GameRepo.py. REMEMBER: You only need to run setup.py once. After the first run you can just start GameRepo.py.

Things to know:
	
	To get the best experience with SGR make sure you do the following:
		For the best AppID search results, type in the games name the same way that it appears in the Steam Store.
			SGR will attempt to search for your game up to 3 times.
			After that it will give you a link to go to in a web browser and manually find 
			the AppID from there.

		Setup Task Scheduler to auto sync your repository.
			To do this, create a task in Task Scheduler and schedule it to run every X days at a specific time.
			Then tell it to launch "steamcmd.exe" with the following launch options:
				"+runscript main_script.txt"
			You can test the task to make sure it correctly launches.
			Example of fully built task:
				Name: Steam Game Repository 24 Hour Sync
				Run every: 1 day, at 5:00 AM
				Start Program: "PATH\TO\steamcmd.exe"
				Launch Options: "+runscript main_script.txt"

	Current Bugs/Issues:
	    1. This isn't really in issue with SGR, more so with Steam. In testing I found that some Steam games
	        won't actually show up in the Steam Store search (which is what SGR uses to obtain the AppID for games)
	        In order to find the AppID of these specific games you have to visit either the link that SGR give you
	        after the 3rd failed lookup or the games store page or community workshop page in a web browser to find
	        their AppID.
	        List of known affected games:
	            The Elder Scrolls V: Skyrim (original edition) : 72850
