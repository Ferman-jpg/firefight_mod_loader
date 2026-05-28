from pathlib import Path
import shutil
import os
import sys
import configparser

#=================INITIALIZE

cm_codename_text =["// List the 4 digit map code for each custom map\n",
"// Write one custom map code per line\n",
"//\n",
"// Each map must have a folder of its 4 digit code name in the Maps folder, required files are (where xxxx is an example 4 digit map code):\n",
"//\n",
"// xxxx.jpg a 4096x4096 background image\n",
"// xxxx-map.jpg a 384x384 shrunken down version of the background image\n",
"// xxxx-contours.png a 1024x1024 image of the hill contours\n",
"// xxxx-scenarios.dat which describes the map name and scenario details\n",
"// xxxx-world.dat which describes the terrain, buildings, trees, hedges etc...\n",
"//\n",
"// for Android use the sixteen 1024x1024 .jpg files instead of the single 4096x4096 jpg file\n",
"\n",
"//XXXX\n"]

#Initialize configparser for the ini file. This is set up so the Mod you're unloading knows what file to return to
mod_loading_success_flag = True
config = configparser.ConfigParser()

# Allows the compiled thing to know the path it lives in. This path is then stored in main_dir
if getattr(sys, 'frozen', False):
    # for exe
    main_dir = Path(sys.executable).parent
else:
    # for py script
    main_dir = Path(__file__).parent

print("Program directory:", main_dir)

#===================CREATE MTL FOLDER AND ferconfig.ini
print("Directory where mtl folder has to be created: ",main_dir) 
print("")

# Create a path type of object named mtl_dir (path to the 'mod_to_load_folder') the fercon_dir(path to the folder where ini file is in)
mtl_dir = Path(main_dir) / "mods_to_load"
fercon_dir = Path(main_dir) / "ferconfig.ini"

print("> Attempting to create a mods_to_load folder and a config file ")
# Check if mtl is already in the main folder
if mtl_dir.is_dir() == False: # If not
    mtl_dir.mkdir(parents = True)  # Create the folder, if folder exist it raises an error
    print("Created mod_to_load")
# If config does not exists in main
if (fercon_dir.is_file() == False):
# Create a config file inside that folder (to store the source file of each mod)
    config["origin_dirs"] = {"current_mod_origin":""}
    config["origin_dirs_map"] = {"current_mod_CM_folder_origin":""}
    config["Custom Maps"] = {"Map List":""}
    with open("ferconfig.ini", "w") as fercon:
        config.write(fercon)
    print("Created config file")

# If config is in but not complete
elif fercon_dir.is_file() == True:
    print("A config file is present but its contents are outdated")
    config.read("ferconfig.ini")
    temp_origin_value = config["origin_dirs"]["current_mod_origin"]
    
    if "origin_dirs" not in config:
        config["origin_dirs"] = {"current_mod_origin":temp_origin_value} # keep the previous stuff
    if "origin_dirs_mod" not in config:
        print("config is missing an origin_dirs_mod section")
        config["origin_dirs_mod"] = {"current_mod_Mod_folder_origin":""}
    if "origin_dirs_map" not in config:
        print("config is missing an origin_dirs_map section")
        config["origin_dirs_map"] = {"current_mod_CM_folder_origin":""}
    if "Custom Maps" not in config:
        print("config is missing a custom maps section")
        config["Custom Maps"] = {"Map List":""}
        
    with open("ferconfig.ini", "w") as fercon:
        config.write(fercon)
    print("Updated the contents")
    print("Created config file")
        
else: # If so
    # Abort this program!!!
    print("> The mod_to_load folder and config file already exists anyway")
    
#===========================LOAD THE MOD

#===========================CHECK IF ROAMING/SEAN OCONNORS GAMES/FIREFIGHT/MOD EXISTS
sean_dir = Path(os.getenv("APPDATA")) / "Sean OConnors Games"
sean_mod_dir = Path(os.getenv("APPDATA")) / "Sean OConnors Games" / "Mod"
roaming_mod_dir = Path(os.getenv("APPDATA")) / "Sean OConnors Games" / "Firefight" / "Mod"

# If there is a roaming mod===================================================
if roaming_mod_dir.is_dir():
    print("""
    > A Mod folder inside AppData/Roaming/Sean OConnors Games/Firefight already exists and is overriding the one in the main directory.
    If you're currently developing a mod using the FF Tank Editor, you might want to temporarily move the folder elsewhere. Otherwise
    Ferloader will move it automatically outside to AppData/Roaming/Sean OConnors Games
    
    """)
    user_decision = False
    # While user tells you not to move the folder of if the folder still exists
    while user_decision == False and roaming_mod_dir.is_dir() == True:
        move_confirm = input("Let the program move the folder?? (yes/no): ")
        
        if move_confirm.lower() == "yes":
            print("User wants to move the program automatically")
            print(f"{sean_mod_dir.is_dir()}")
            
            # If a Mod Folder already exist in Sean OConnors Games
            if sean_mod_dir.is_dir():
                print(f"A mod folder already exist in {sean_dir}")
                counter = 1
                found_folder_name = False
                while found_folder_name == False:
                    new_folder_name =  f"Mod{counter}"
                    
                    # if the name is already taken
                    if (Path(sean_dir) / new_folder_name).is_dir() == True:
                        counter += 1
                        print(f"{new_folder_name} is already taken, trying {roaming_mod_dir.name}{counter}")
                    
                    # if not, rename the folder and move it
                    elif (Path(sean_mod_dir) / new_folder_name).is_dir() == False:
                        print(f"{roaming_mod_dir.name}{counter} is available, renaming folder now...")
                        os.rename(roaming_mod_dir, sean_dir / new_folder_name)  # Essentially moves the folder at the same time
                        print(f"Folder is renamed {roaming_mod_dir}, trying to move to {sean_dir} now")
                        found_folder_name = True
                    else:
                        print("Unknown Error")
                user_decision == True # MOVE DOWN FOR ERROR HANDLING??
                # If mod folder is found in the Sean O Connors Games directory
            
            # If the Sean OConnor Games directory is clear
            elif not sean_mod_dir.is_dir():
                print("Preparing to move")
                shutil.move(roaming_mod_dir, sean_dir)  # move it outside
                found_folder_name = True
                
                            
        elif move_confirm.lower() == "no":
            user_decision == False
        else:
            print("Not a valid answer.")
    
#===============================================================  
    
print("")
# get the target mod, create a path object that leads to the target mod's folder
trg_mod = input("Enter the name of the mod you want to load: ")  #name of the folder of the target mod
mtl_yourmod_path = Path(main_dir) /"mods_to_load"/ trg_mod  # gets the path of mtl/yourmod folder

print(f"Path to mod folder: {str(mtl_yourmod_path)}")

# Directory of the main Mod file (the one that has firefight.exe) thats about to be replaced
main_dir_Mod = Path(main_dir) / "Mod"
mtl_Mod = None # Path to the 'Mod' folder inside the target mod's folder

# Open config file and store the current value to main_dir_Mod_origin. If no loading has happened yet then thats empy
config.read("ferconfig.ini")
main_dir_Mod_origin = config["origin_dirs"]["current_mod_origin"]

print(f"> Attempting to search for the Mod folder in {trg_mod}...")
# Search the folder of the target mod until it hits a 'Mod' folder. Replace the 'Mod' in the main directory with this one
for path in mtl_yourmod_path.rglob("Mod"):  # search recursively in the yourmod path ntil you hit Mod
    if path.is_dir():
        print(f"Mod folder from {trg_mod} exist")
        mtl_Mod = Path(path)
        
        print("> Attempting to replace the 'Mod' folder in the main directory with the 'Mod' subfolder from your chosen mod...")
        # Replace the Mod folder in main with yourmod Mod folder
        if main_dir_Mod_origin != "":  #if the config file is not empty (a previous mod had just been loaded)
            print("Config file is not empty, it seems a mod has just been loaded here")
            print("Attempting to unload the old mod first")
            # Unloading the current mod
            shutil.move(main_dir_Mod, main_dir_Mod_origin)  # MOve the mainMod folder back to the Mod folder where it came from
            print(f"Moved {main_dir_Mod} back to {main_dir_Mod_origin}")
            
            # Loading yourmod
            print("> Attempting to load your mod...")
            # Store original source to config
            config["origin_dirs"]["current_mod_origin"] = str(mtl_yourmod_path)  #stores the path of the current mod being loaded into the config file
            print(f"Successfully stored origin path to ferconfig.ini: {config['origin_dirs']['current_mod_origin']}")           
            with open("ferconfig.ini", "w") as fercon:  #save the edited config file
                config.write(fercon)
            print(f"Wrote down the return path: {str(mtl_yourmod_path)} to the config file ")
            # Load the mod. Replace the 'Mod' folder in the main dir with the 'Mod' folder inside the target mod 
            shutil.move(mtl_Mod, main_dir)
            print(f"Loaded {mtl_yourmod_path} to {main_dir}")
            
        elif main_dir_Mod_origin == "": #config file is empty (no loading has ever happened)
            print("Config file is empty, it seems NO previous mod have just been loaded")
            
            # Scenario where ini file is empty but theres a 'Mod' folder in the main directory. (If an empty Mod folder is there by default)
            if main_dir_Mod.is_dir():
                
                # Rename the Mod file and move it to mtl_dir, if Mod folder duplicate is in there append a suffix at the end
                print("Mod folder exist in the main directory but no loading has ever happened, attempting to move the rogue Mod folder to mtl...")
                if (mtl_dir / "Mod").is_dir():
                    counter = 1
                    rename_successful = False
                    while rename_successful == False:
                        main_dir_mod_rename = f"Mod{counter}"
                        if (Path(mtl_dir) / main_dir_mod_rename).is_dir():
                            counter += 1
                            print(f"{main_dir_mod_rename} is taken, trying Mod{counter}")
                        elif (Path(mtl_dir) / main_dir_mod_rename).is_dir() == False:
                            os.rename(main_dir_Mod, mtl_dir / main_dir_mod_rename)  # rename and move
                            rename_successful = True
                            print(f"Moved successfuly to mtl")
                            
                # No rogue Mod in mtl, meaning no need to append a suffix     
                elif (mtl_dir / "Mod").is_dir() == False:
                    os.rename(main_dir_Mod, mtl_dir / "Mod")  # rename and move
                    rename_successful = True
                    print(f"Moved successfuly to mtl")
               
                
                # Store the original path of the target mod 'Mod' folder to config (so it knows where to return)
                config.read("ferconfig.ini")
                config["origin_dirs"]["current_mod_origin"] = str(mtl_yourmod_path)  #stores the path of the current mod being loaded into the config file
                print(f"Successfully stored origin to ferconfig.ini: {config['origin_dirs']['current_mod_origin']}")
                
                #save the edited config file
                with open("ferconfig.ini", "w") as fercon:  
                    config.write(fercon)
                print("Wrote down the return path: {mtl_yourmod_path} to the config file ")
                
                shutil.move(mtl_Mod, main_dir)  #Move the target mod to main_dir
                print(f"Loaded {mtl_yourmod_path} / Mod to {main_dir}")
            else:
                print("> There is no rogue Mod folder in the main directory, loading your mod...")
                 # Store the original path of the target mod 'Mod' folder to config (so it knows where to return)
                config.read("ferconfig.ini")
                config["origin_dirs"]["current_mod_origin"] = str(mtl_yourmod_path)  #stores the path of the current mod being loaded into the config file
                print(f"Successfully stored origin to ferconfig.ini: {config['origin_dirs']['current_mod_origin']}")
                
                #save the edited config file
                with open("ferconfig.ini", "w") as fercon:  
                    config.write(fercon)
                print("Wrote down the return path: {mtl_yourmod_path} to the config file ")
                
                shutil.move(mtl_Mod, main_dir) #If not
                print(f"Loaded {mtl_yourmod_path} to {main_dir}")
        else:
            print("FAILURE dont know why but maybe something about the .ini file or something idk")
            mod_loading_success_flag = False
        break
        
    else:
        print("Can't find the 'Mod' folder of the mod you want to load")
        mod_loading_success_flag = False
        break
else: 
    print("Error in loading the mod. Check if its already loaded, otherwise check if the data, img and sound folders are inside of a 'Mod' folder")
    mod_loading_success_flag = False

#===============================More carbonara code
#===================================================================CUSTOM MAP
if mod_loading_success_flag == True:
    print(">>> LOADING THE CUSTOM MAPS ====================== <<<")
    print("> Checking if a Custom Maps exist in the main directory with a CustomMapCodeNames.txt inside")
    cm_main_dir = Path(main_dir) / "Custom Maps"
    cm_main_txt = Path(cm_main_dir) / "CustomMapCodeNames.txt"  # path to the code name file
    if cm_main_dir.is_dir() == False:
        cm_main_dir.mkdir(parents = True)
        print("Found no Custom Maps file so one is created")
    if cm_main_txt.is_file() == False:
        cm_main_txt.touch()
        # Write the stuff down
        with open(str(cm_main_txt),"w") as cm_txt:
            cm_txt.writelines(cm_codename_text)
        print("Found no CustomMapCodeNames.txt so one is generated")

    cm_mod_dir = Path(config["origin_dirs_map"]["current_mod_CM_folder_origin"])  # directory of the Map folder of the mod ot be loaded
    current_cm_dir = Path(config["origin_dirs"]["current_mod_origin"])  # directory of the current mod that has to be unloaded

    map_to_unload = []
    map_to_load = []
    # Outer for loop just searches for the path of the modded custom maps folder
    for path in mtl_yourmod_path.rglob("Custom Maps"):
        if path.is_dir():
            # Get all the map folders and move it to the custom maps in main dir
            print(f"Custom Map folder exists in {trg_mod} folder")
            config.read("ferconfig.ini")
            cm_config_name_list = config["Custom Maps"]["Map List"]
            
            # UNLOADING
            # 1). Retrieve the string value from the "map_list" key and store it to a list
            # 2). Using that list as a reference, move each map from the main_dir custom map folder to the mod folder where it came from
            # 3). Clear the config file
            print("> Attempting to move the files...")
            if cm_config_name_list != "":  # Map list is NOT empty (a mod is loaded in there)
                print("Config file says that A map pack has been loaded")
                map_to_unload = cm_config_name_list.split(",")  # Unpack the map list
                print(f"> Unloading these maps first: {map_to_unload} before proceeding...")
            
                for map_name in map_to_unload:
                    shutil.move(cm_main_dir / map_name, cm_mod_dir) # this fucking thing
                    print(f"Moved {cm_main_dir}/{map_name} back to {mtl_yourmod_path}/Custom Maps")
                    
                # Erase the map list
                config.read("ferconfig.ini")
                config["Custom Maps"]["Map List"] = ""
                with open("ferconfig.ini", "w") as fercon:
                    config.write(fercon)
                    print("No more previous maps to unload")
                          
            else:
                print("Config file says that NO maps have been loaded since the currently loaded maps list is empty")
           
            # LOADING
            # Checks the inside of the modded custom maps folder and transfers it to the main_dir custom maps folder
            # 1). Move each maps from the "yourmod custom mod" directory to the "main dir custom mod" directory
            # 2). For each map that you moved, store the name of the folder to a list
            # 3). Wrap that list as a string and write it to the config file
            print("> Attempting to load the maps now...")
            for maps in path.iterdir():  # path.iterdir() holds the paths of the items inside the mod_custom maps folder
                if maps.is_dir():  # if the item is a folder
                    if (Path(cm_main_dir) / (maps.name)).is_dir() == False: # if that mod map folder already exist in the destination
                        shutil.move(maps, cm_main_dir)  # maps is a path
                        map_to_load.append(maps.name)
                        print(f"Moved {maps} to {cm_main_dir}")
                    else:
                        print(f"The map {maps.name} already exist in {cm_main_dir}")
            print("Finished moving the maps")

            # Write map names to map list
            config["Custom Maps"]["Map List"] = ",".join(map_to_load)
            config["origin_dirs_map"]["current_mod_CM_folder_origin"] = str(path)  # Record the path to the custom_map folder
            print(f"Recorded {path} to config file as the return directory of the Custom Maps folder for the mod you want to load")
            with open("ferconfig.ini", "w") as fercon:
                config.write(fercon)
                print(f"Recorded the current loaded maps to the config: {map_to_load}")
            print(f"> Loaded the maps: {map_to_load} to {cm_main_dir}")
            
            # >>> Adding the name of the added map folders to the CustomMapsCodeName.txt ==========================
            # =====================================================================================================
            
            # This replaces the stuff written in the custom map.txt with the stuff from the mods
            cm_folder_main = cm_main_dir
            fresh_cm = []

            # Erase the previous custom map names
            # Copy the entire text until a //@ identifier is mentioned
            print("> Attempting to edit CustomMapCodeNames.txt to include all the names of the maps")
            with open(cm_main_txt,"r") as cm_codename:  
                cm_lines = cm_codename.readlines()
                for line in cm_lines:
                    if "//@" in line:  # Once the identifier is detected, stop copying
                        break
                    else:
                        fresh_cm.append(line)

            # Paste the copied text without the stuff after the identifier
            with open(cm_main_txt,"w") as cm_codename:  
                cm_codename.writelines(fresh_cm)
                print("Erased the previous codename entries")
            
            # Add the custom map names of the loaded mod
            with open(cm_main_txt,"a") as cm_codename:
                
                # If newline is not detected at the end of the text, add one. Solves the weird problem i get
                if "\n" not in fresh_cm[-1]:
                    cm_codename.write("\n")
                    print(fresh_cm[-1])
                    print("Added new line at the end of the text file, it solves some weird shit")
                
                cm_codename.write(f"//@")  # dont add a newline before the identifier
                # Append the names
                for path in cm_folder_main.iterdir():
                    if path.is_dir():
                        cm_codename.write(f"\n{path.name}")
                        print(f"Wrote the codenames for map: {path.name}") 
                else:
                    print("No more codenames written")
            
        else:  # Custom map is missing
            print(f"Can't find custom maps folder from {mtl_yourmod_path}")
else:
    print("Loading the Mod folder failed, Custom Map will not be loaded")

#error handling if two custom maps are of the same name
# Record mod Mod folder path in config
# same for map folder, and return them to the complete path no?
#should be able to work when there is an existing config file but the stuff inside is different?
confirm_out = input("Program is done, press any key to exit. Please copy the error message if there are any and send it to the discord")





