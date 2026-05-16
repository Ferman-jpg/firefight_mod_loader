from pathlib import Path
import shutil
import sys
import configparser

#=================INITIALIZE
#Initialize configparser for the ini file. This is set up so the Mod you're unloading knows what file to return to
config = configparser.ConfigParser()

# Allows the compiled thing to know the path it lives in. This path is then stored in main_dir
if getattr(sys, 'frozen', False):
    # for exe
    main_dir = Path(sys.executable).parent
else:
    # for py script
    main_dir = Path(__file__).parent

print("Program directory:", main_dir)

#===================CREATE MTL FOLDER AND FERCON.INI
print("Directory where mtl folder has to be created: ",main_dir) 
print("")

# Create a path type of object named mtl_dir (path to the 'mod_to_load_folder') the fercon_dir(path to the folder where ini file is in)
mtl_dir = Path(main_dir) / "mods_to_load"
fercon_dir = Path(main_dir) / "ferconfig.ini"
# Check if mtl is already in the main folder
if mtl_dir.is_dir() == False: # If not
    print("Creating mod_to_load")
    mtl_dir.mkdir(parents = True)  # Create the folder, if folder exist it raises an error

# If config does not exists in main
if fercon_dir.is_file() == False:
# Create a config file inside that folder (to store the source file of each mod)
    config["origin_dirs"] = {"current_mod_origin" : ""}
    with open("ferconfig.ini", "w") as fercon:
        config.write(fercon)
    
else: # If so
    # Abort this program!!!
    print("The folder mod_to_load already exists anyway")
    
#===========================LOAD THE MOD
print("")
# get the target mod, create a path object that leads to the target mod's folder
trg_mod = input("Enter the name of the mod you want to load: ")  #name of the folder of the target mod
mtl_yourmod_path = Path(main_dir) /"mods_to_load"/ trg_mod  # gets the path of mtl/yourmod folder

# Directory of the main Mod file (the one that has firefight.exe) thats about to be replaced
main_dir_Mod = Path(main_dir) / "Mod"
mtl_Mod = None # Path to the 'Mod' folder inside the target mod's folder

# Open config file and store the current value to main_dir_Mod_origin. If no loading has happened yet then thats empy
config.read("ferconfig.ini")
main_dir_Mod_origin = config["origin_dirs"]["current_mod_origin"]

# Search the folder of the target mod until it hits a 'Mod' folder. Replace the 'Mod' in the main directory with this one
for path in mtl_yourmod_path.rglob("Mod"):  # search recursively in the yourmod path ntil you hit Mod
    if path.is_dir():
        mtl_Mod = Path(path)
        
        # Replace the Mod folder in main with yourmod Mod folder
        if main_dir_Mod_origin != "":  #if the config file is not empty (a previous mod had just been loaded)
            
            # Unloading the current mod
            shutil.move(main_dir_Mod, main_dir_Mod_origin)  # MOve the mainMod folder back to the Mod folder where it came from
            print(f"Moved {main_dir_Mod} back to {main_dir_Mod_origin}")
            
            # Loading yourmod
            # Store original source to config
            config["origin_dirs"]["current_mod_origin"] = str(mtl_yourmod_path)  #stores the path of the current mod being loaded into the config file
            print(f"Successfully stored origin to fercon.ini: {config['origin_dirs']['current_mod_origin']}")           
            with open("ferconfig.ini", "w") as fercon:  #save the edited config file
                config.write(fercon)
                
            # Load the mod. Replace the 'Mod' folder in the main dir with the 'Mod' folder inside the target mod 
            shutil.move(mtl_Mod, main_dir)
            print(f"Loaded {mtl_yourmod_path} to {main_dir}")
            
        elif main_dir_Mod_origin == "": #config file is empty (no loading has ever happened)
            print("No previous loading has ever taken place")
            
            # Scenario where ini file is empty but theres a 'Mod' folder in the main directory. (If an empty Mod folder is there by default)
            if main_dir_Mod.is_dir():
                shutil.move(main_dir_Mod, mtl_dir) 
                
                # Store the original path of the target mod 'Mod' folder to config (so it knows where to return)
                config.read("ferconfig.ini")
                config["origin_dirs"]["current_mod_origin"] = str(mtl_yourmod_path)  #stores the path of the current mod being loaded into the config file
                print(f"Successfully stored origin to fercon.ini: {config['origin_dirs']['current_mod_origin']}")           
                with open("ferconfig.ini", "w") as fercon:  #save the edited config file
                    config.write(fercon)
                    
                shutil.move(mtl_Mod, main_dir)  #Move the target mod to main_dir
                
            else:
                shutil.move(mtl_Mod, main_dir) #If not
                print(f"Loaded {mtl_yourmod_path} to {main_dir}")
        else:
            print("FAILURE dont know why but maybe something about the .ini file or something idk")
        break
        
    else:
        print("Can't find the 'Mod' folder of the mod you want to load")
        break
    
print("Done")
confirm_out = input("Press any key to exit. Please copy the error message if there are any")

