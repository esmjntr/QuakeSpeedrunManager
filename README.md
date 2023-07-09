# QuakeSpeedrunManager
A small tool for managing segmented runs of the game Quake.

![Quake Speedrun Manager project page](docs/qsm.png?raw=true)

## Getting Started
- Download from the [releases](https://github.com/esmjntr/QuakeSpeedrunManager/releases) section and extract the .zip file.
- Download demtool from https://speeddemosarchive.com/quake/downloads.html and put demtool.exe in the same directory as qsm.exe
- Start qsm.exe and goto settings
  - JoeQuake Path: put the location to joequake-gl.exe here
  - Command line parameters: At minimum this should load the qdqstats mod with -game qdqstats
  - QdQStats path: put the location of your qdqstats directory (Where config file and demos are stored)
 - Start a new project and click Start Map to record the first demo
 - Upload the demo which will load the demo time and the ending stats for the level
 - Click Start Map on the next map to record the next demo starting with the correct stats
  
## What does this do?
When you click Start Map it will create a config file calls sqmstats.cfg with the requested setting in the qsqstats folder and start Quake running that config file
 
The contents of the config file will depend on the settings

**Set Skill**\
If this is enabled it will write skill X into the config (0 for easy or 3 for nightmare)

**Start Map**\
If this will add a key binding to restart the run. It can either use the record command with a file name and the map or it can just use the map command if you wish to use autorecord. You can also choose to not bind a key at all.

the config will also include commmands to start the map and set the initial starting stats based of the previous level. 

When you load a demo is copies the demo file into the qsm directory with the name temp.dem and runs demtool.exe -s to get the time and ending stats from the demo and puts these in to the project file. It then moves temp.dem to the project folder for safe keeping.

## Help my maps always start with non-default stats now
you can add the following commands to your regular config which will reset it to default

registered 1\
sys_ticrate 0\
temp1 0





  
  
