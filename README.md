# firefight_mod_loader
Simple script that allows you to load mods instantly regardless of size.

# NOTE: IF YOU USED THE FF TANK EDITOR BEFORE:
  THE MOD FOLDER IN THE MAIN DIRECTORY WILL BE OVERRIDEN BY THE MOD FOLDER IN APPDATA/ROAMING/SEAN O CONNOR/FIREFIGHT/MOD
  REMOVE THAT FOLDER OR MOVE IT ELSEWHERE TEMPORARILY IF YOU WANT THIS TO WORK  

# Instructions
1). Install the loader and move it to the same directory where firefight.exe is located (usually- \Firefight\Firefight.vx.x.x\game) <br>
2). Open the loader, it will create a "mods_to_load" folder, extract all of your mods there. It will also generate a config file. This is how the loader knows where to put back the files of the mod that has to be unloaded <br>
3). If you want to load a mod, just enter the exact name of the folder that contains the modded content. Note that for it to work correctly, the data, image and sound files must be inside a 'Mod' folder. <br>

# How it works (for now)
  All it does is replace the 'Mod' folder in the main directory (where firefight.exe is located) with the 'Mod' folder from the modded content. <br>
  
  When you load a mod, it will first read the .ini file to know where the 'Mod' folder in the main directory came from. If it cannot read a path/.ini file is empty(meaning its your first time loading a content), it will simply move that folder inside the mods_to_load folder. <br>
  However, if a path is read, it will move that folder back to where it came from depending on whats written on the .ini. <br>
  
  The next step is it will recursively search the directory of the mod you wanted to load, then if it detects a 'Mod' folder, it will move that to the main directory. <br>

# Limitations (for now)
1). Can only load ONE mod at a time, cannot merge <br>
2). Only for pc (idk if an android version is feasible) <br>

# Issues
If problem occurs, just remove the config file and move the 'Mod' folder back to where it came from 
