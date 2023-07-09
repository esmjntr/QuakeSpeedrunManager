import json
import subprocess
from tkinter import filedialog
from tkinter import *
import os, sys
import time
import shutil
## Fix error when using Eel/PyInstaller with --noconsole (https://github.com/python-eel/Eel/issues/654)
logfile = open('qsm.log', 'wt')
sys.stdout = logfile
sys.stderr = logfile
import eel

qsmversion ="v1.0.1-alpha"


# Set web files folder
eel.init('web')


@eel.expose
def loadproject(projectname):
    global projectdata
    with open(f"projects/{projectname}.json", "rb") as f:
        projectdata = json.load(f)
    render_html = ""
    render_html += f"<h4>Project Name: {projectdata['project_name']}</h4><hr />"
    total_episode_time = 0.00
    total_game_time = 0.00
    for mapname in projectdata['maps']:

        if projectdata['maps'][mapname]['type'] == "episode_start":
            render_html += f"<h4>{projectdata['maps'][mapname]['episode_name']}</h4>"
            total_episode_time = 0
        elif projectdata['maps'][mapname]['type'] == "episode_end":
            render_html += f"<hr />Total Time for {projectdata['maps'][mapname]['episode_name']}: {formattime(total_episode_time)}<hr />"
        elif projectdata['maps'][mapname]['type'] == "map":

            #render_html += f"<h5>{mapname} - {projectdata['maps'][mapname]['map_name']}</h5>"
            render_html += f"<span class=\"h5 mapline\">{mapname} - {projectdata['maps'][mapname]['map_name']} &nbsp;&nbsp;&nbsp;<button onclick=\"eel.startgame('{projectname}', '{mapname}', 'start');\" type=\"button\" class=\"btn btn-outline-light btn-sm smallbtn\">Start Map</button> <button onclick=\"eel.startgame('{projectname}', '{mapname}', 'save')\" type=\"button\" class=\"btn btn-outline-light btn-sm smallbtn\">Save .cfg</button> <button onclick=\"eel.loaddemo('{projectdata['project_id']}','{mapname}');\" type=\"button\" class=\"btn btn-outline-light btn-sm smallbtn\">Load Demo</button></span>"
            if projectdata['maps'][mapname]['demo_time'] != 0:
                total_episode_time += float(projectdata['maps'][mapname]['demo_time'])
                total_game_time += float(projectdata['maps'][mapname]['demo_time'])
                stats = projectdata['maps'][mapname]['end_stats']

                endstats = projectdata['maps'][mapname]['end_stats']

                if "3" in endstats['weapons']:
                    if endstats['weapon'] == 3:
                        slot3 = "<img src=ssg_s.png />"
                    else:
                        slot3 = "<img src=ssg.png />"
                else:
                    slot3 = "<img src=blankweapon.png />"
                if "4" in endstats['weapons']:
                    if endstats['weapon'] == 4:
                        slot4 = "<img src=ng_s.png />"
                    else:
                        slot4 = "<img src=ng.png />"
                else:
                    slot4 = "<img src=blankweapon.png />"
                if "5" in endstats['weapons']:
                    if endstats['weapon'] == 5:
                        slot5 = "<img src=sng_s.png />"
                    else:
                        slot5 = "<img src=sng.png />"
                else:
                    slot5 = "<img src=blankweapon.png />"
                if "6" in endstats['weapons']:
                    if endstats['weapon'] == 6:
                        slot6 = "<img src=gl_s.png />"
                    else:
                        slot6 = "<img src=gl.png />"
                else:
                    slot6 = "<img src=blankweapon.png />"
                if "7" in endstats['weapons']:
                    if endstats['weapon'] == 7:
                        slot7 = "<img src=rl_s.png />"
                    else:
                        slot7 = "<img src=rl.png />"
                else:
                    slot7 = "<img src=blankweapon.png />"
                if "8" in endstats['weapons']:
                    if endstats['weapon'] == 8:
                        slot8 = "<img src=lg_s.png />"
                    else:
                        slot8 = "<img src=lg.png />"
                else:
                    slot8 = "<img src=blankweaponlg.png />"
                if endstats['weapon'] == 2:
                    slot2 = "<img src=sg_s.png />"
                else:
                    slot2 = "<img src=sg.png />"

                if endstats['armor_type'] == 1:
                    armor_icon = "<span><img src=green.png /></span>"
                elif endstats['armor_type'] == 2:
                    armor_icon = "<span><img src=yellow.png /></span>"
                elif endstats['armor_type'] == 2:
                    armor_icon = "<span><img src=red.png /></span>"
                else:
                    armor_icon = "<span><img src=noarmor.png /></span>"

                render_html += f'<table><tr><td class=timeheading>Time:</td><td class=statsheading colspan=11>Demo end stats [<a href="#" onclick="eel.editstats(\'{projectdata["project_id"]}\', \'{mapname}\');">Edit</a>]:</td></tr>'
                render_html += f"<tr class=ammorow><td rowspan=2 class=timecell>{formattime(projectdata['maps'][mapname]['demo_time'])}</td><td class=haiconcell rowspan=2>{armor_icon}</td><td class=hacell rowspan=2>{stats['armor']}</td><td class=haiconcell rowspan=2><img src=face.png /></td><td class=hacell rowspan=2>{stats['health']}</td><td class=ammocell colspan=2>{stats['shells']}<span class=ammoicon><img src=\"shells.png\" /></span>&nbsp;&nbsp;</td><td class=ammocell colspan=2>{stats['nails']} <span><img src=\"nails.png\" /></span>&nbsp;&nbsp;</td><td class=ammocell colspan=2>{stats['rockets']} <span><img src=\"rockets.png\" /></span>&nbsp;&nbsp;</td><td class=ammocell colspan=2>{stats['cells']} <span><img src=\"cells.png\" /></span>&nbsp;&nbsp;</td></tr>"
                render_html += f"       <tr ><td class=weaponcell>{slot2}</td><td class=weaponcell>{slot3}</td><td class=weaponcell>{slot4}</td><td class=weaponcell>{slot5}</td><td class=weaponcell>{slot6}</td><td class=weaponcell>{slot7}</td><td colspan=2 class=weaponcelllg>{slot8}</td></tr></table>"
            else:
                render_html += f"<div>no demo submitted.. </div>"

            render_html += f"<br />"
    render_html += f"<hr />Total Time for Quake: {formattime(total_game_time)}<hr />"

    eel.pageupdate(render_html)

    projectdata['last_modified'] = int(time.time())

    project_file = open(f'projects/{projectdata["project_id"]}.json', "wt")
    project_file.write(json.dumps(projectdata, indent=4, sort_keys=False))
    project_file.close()


@eel.expose
def projectpage():


    render_html = ""
    render_html += f"<h4>Create new project</h4>"

    templates = {}
    templatessort = {}
    try:
        for filename in os.listdir('templates'):
            if filename.endswith(".json"):
                with open(f"templates/{filename}", "rb") as f:
                    try:
                        templatedata = json.load(f)
                    except json.decoder.JSONDecodeError:
                        templatedata = {}


                try:
                    templatessort[filename[:-5]] = templatedata['last_modified']
                    templates[filename[:-5]] = {"name": templatedata['project_name']}
                except KeyError:
                    pass


        templatessort = dict(sorted(templatessort.items(), key=lambda x: x[1]))

        render_html += f'<div class="form-group"><label for="projectname">Project Name</label><input type="text" class="form-control form-control-sm w-50" id="projectname" placeholder="My Quake Speedrun">'
        render_html += f'<label for="projecttemplate">Project Template</label><select class="form-select form-select-sm w-50" id="projecttemplate">'

        for template in templatessort:
            render_html += f'<option value="{template}">{templates[template]["name"]}</option>'



        render_html += f'</select><br /><button onclick="startprojectjs();" class="btn btn-outline-light">Create Project</button></div>'

    except FileNotFoundError:
        render_html += "Error: templates folder could not be found."


    render_html += f"<br /><br /><h4>Load project</h4>"


    projects = {}
    projectssort = {}
    try:
        for filename in os.listdir('projects'):

            if filename.endswith(".json"):
                with open(f"projects/{filename}", "rb") as f:
                    try:
                        projectdata = json.load(f)
                    except json.decoder.JSONDecodeError:
                        projectdata = {}

                try:
                    if "last_modified" in projectdata:
                        projectssort[filename[:-5]] = projectdata['last_modified']
                    else:
                        projectssort[filename[:-5]] = 0
                    projects[filename[:-5]] = {"project_name": projectdata['project_name']}
                except KeyError:
                    pass

        projectssort = dict(sorted(projectssort.items(), key=lambda x: x[1], reverse=True))

        render_html += "<ul>"
        for project in projectssort:
            render_html += f'<li><a href="#" class="h5 projectlink" onclick="eel.loadproject(\'{project}\');">{projects[project]["project_name"]}</a> <span class=prjid>(Project ID: {project})</a></li>'

        render_html += "</ul>"

    except FileNotFoundError:
        render_html += "Error: templates folder could not be found."

    render_html += f'<br /><br />Quake Speedrun Manager {qsmversion}<br /><a href="https://github.com/esmjntr/qsm">https://github.com/esmjntr/qsm</a>'

    eel.pageupdate(render_html)


@eel.expose
def startprojectpy(prjname, prjtemplate):
    with open(f"templates/{prjtemplate}.json", "rb") as f:
        projectdata = json.load(f)

    projectdata['project_name'] = prjname

    existing_projects = []
    try:
        for filename in os.listdir('projects'):
            if filename.endswith(".json"):
                existing_projects.append(filename[:-5])
    except FileNotFoundError:
        os.mkdir("projects")

    pid = 'aa'
    break_out_flag = False
    for n in range(97, 123):
        for nn in range(97, 123):
            pid = chr(n) + chr(nn)
            if pid not in existing_projects:
                break_out_flag = True
                break
        if break_out_flag == True:
            break
    print(f"New Project Code: {pid}")

    projectdata['project_id'] = pid
    projectdata['last_modified'] = int(time.time())

    project_file = open(f"projects/{pid}.json", "wt")
    project_file.write(json.dumps(projectdata, indent=4, sort_keys=False))
    project_file.close()

    loadproject(pid)



@eel.expose
def loaddemo(projectid, mapname):
    for i in [1]:
        try:
            try:
                with open(f"settings.json", "rb") as f:
                    settingsdata = json.load(f)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                eel.showerrormodal("Could not settings file")
                break

            root = Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            filename = filedialog.askopenfilename(initialdir=settingsdata['qdqdir'], title="Select file",
                                                  filetypes=(("Demo files", "*.dem"), ("all files", "*.*")))
            root.update()  # to make dialog close on MacOS

            shutil.copyfile(filename, "temp.dem")
        except:
            eel.showerrormodal("Could not load demo")
            break

        try:
            demostats = subprocess.run(['demtool.exe', '-s', 'temp.dem'], capture_output=True, text=True)
            print(repr(demostats.stdout))
        except:
            eel.showerrormodal("Could not run demtool.exe<br />Please ensure demtool.exe is in QSM directory")
            break

        ## move temp file to project folder
        try:
            shutil.copyfile("temp.dem", f"projects/{projectid}/{mapname}.dem")
        except FileNotFoundError:
            os.mkdir(f"projects/{projectid}")
            shutil.copyfile("temp.dem", f"projects/{projectid}/{mapname}.dem")



        ver_search = re.search(
            r'Start stats:\\n Health:(\d\d?\d?) Armor:(\d\d?\d?)(.*?)\\n Sh:(\d\d?\d?) Nl:(\d\d?\d?) Rk:(\d\d?\d?) Ce:(\d\d?\d?)\\n(.*?)\\n(.*?)\\nEnd: {2}\((.*)\)\\n Health:(\d\d?\d?) Armor:(\d\d?\d?)(.*?)\\n Sh:(\d\d?\d?) Nl:(\d\d?\d?) Rk:(\d\d?\d?) Ce:(\d\d?\d?)\\n(.*?)\\n(.*?)\\n', repr(demostats.stdout), re.M)
        if ver_search:
            print("regex yes")
            health = ver_search.group(1)
            armor = ver_search.group(2)
            armortype = ver_search.group(3)
            shells = ver_search.group(4)
            nails = ver_search.group(5)
            rockets = ver_search.group(6)
            cells = ver_search.group(7)
            weapons = ver_search.group(8)
            weapon = ver_search.group(9)
            etime = ver_search.group(10)
            ehealth = ver_search.group(11)
            earmor = ver_search.group(12)
            earmortype = ver_search.group(13)
            eshells = ver_search.group(14)
            enails = ver_search.group(15)
            erockets = ver_search.group(16)
            ecells = ver_search.group(17)
            eweapons = ver_search.group(18)
            eweapon = eweapons[ver_search.group(19).find('*')]


            if earmortype == " Green":
                earmor_type = 1
            elif earmortype == " Yellow":
                earmor_type = 2
            elif earmortype == " Red":
                earmor_type = 3
            else:
                earmor_type = 0

            try:
                with open(f"projects/{projectid}.json", "rb") as f:
                    projectdata = json.load(f)

                projectdata['maps'][mapname]['demo_time'] = etime

                projectdata['maps'][mapname]['end_stats'] = {
                        "health": int(ehealth),
                        "armor": int(earmor),
                        "armor_type": int(earmor_type),
                        "shells": int(eshells),
                        "nails": int(enails),
                        "rockets": int(erockets),
                        "cells": int(ecells),
                        "weapons": eweapons,
                        "weapon": int(eweapon)
                }

                projectdata['last_modified'] = int(time.time())
            except FileNotFoundError:
                eel.showerrormodal("Could not load project file")
            except NameError:
                eel.showerrormodal("Could not update project file")


            project_file = open(f"projects/{projectdata['project_id']}.json", "wt")
            project_file.write(json.dumps(projectdata, indent=4, sort_keys=False))
            project_file.close()

            loadproject(projectdata['project_id'])
        else:
            eel.showerrormodal("Could not get demo stats")


@eel.expose
def settingspage():
    try:
        with open(f"settings.json", "rb") as f:
            settingsdata = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        eel.showerrormodal('Settings could not be loaded, restoring to default.')
        settingsdata = {
            "joequakeexe": "D:\\JoeQuake\\joequake-gl.exe",
            "joequakeparams": "-game qdqstats",
            "qdqdir": "D:\\JoeQuake\\qdqstats\\",
            "setskill": "yes",
            "recordsetting": "record",
            "restartrunkey": "b"
        }

    render_html = ""
    render_html += f'<h4>Settings</h4>'
    render_html += f'<h5>JoeQuake</h5>'

    render_html += f'<div class="form-group"><label for="jqpath">JoeQuake path</label><input type="text" class="form-control form-control-sm w-50" id="jqpath" placeholder="" value="{settingsdata["joequakeexe"]}">'
    render_html += f'<div class="form-group"><label for="cmdparams">Command line parameters</label><input type="text" class="form-control form-control-sm w-50" id="cmdparams" placeholder="" value="{settingsdata["joequakeparams"]}">'
    render_html += f'<div class="form-group"><label for="qdqdir">QdQStats Directory</label><input type="text" class="form-control form-control-sm w-50" id="qdqdir" placeholder="" value="{settingsdata["qdqdir"]}"><br />'

    render_html += f'<h5>Config output</h5>'
    render_html += f'<label for="setskill">Set Skill</label><select class="form-select form-select-sm w-50" id="setskill">'
    if settingsdata["setskill"] == "yes":
        render_html += '<option value="yes" selected>Yes, set skill in startup config</option>'
        render_html += '<option value="no">No, don\'t set skill in startup config</option>'
    else:
        render_html += '<option value="no" selected>No, don\'t set skill in startup config</option>'
        render_html += '<option value="yes">Yes, set skill in startup config</option>'
    render_html += '</select>'

    render_html += f'<label for="recordsetting">Start Map</label><select class="form-select form-select-sm w-50" id="recordsetting">'
    if settingsdata["recordsetting"] == "record":
        render_html += '<option value="record" selected>bind {key} record {projectid}{mapname} {mapname}</option>'
        render_html += '<option value="map">bind {key} map {mapname}</option>'
        render_html += '<option value="none">Dont include any map/record bind in config</option>'
    elif settingsdata["recordsetting"] == "map":
        render_html += '<option value="record">bind {key} record {projectid}{mapname} {mapname}</option>'
        render_html += '<option value="map" selected>bind {key} map {mapname}</option>'
        render_html += '<option value="none">Dont include any map/record bind in config</option>'
    else:
        render_html += '<option value="record">bind {key} record {projectid}{mapname} {mapname}</option>'
        render_html += '<option value="map">bind {key} map {mapname}</option>'
        render_html += '<option value="none" selected>Dont include any map/record bind in config</option>'
    render_html += '</select>'

    render_html += f'<div class="form-group"><label for="restartrunkey">Restart Run Key</label><input type="text" class="form-control form-control-sm w-50" id="restartrunkey" placeholder="" value="{settingsdata["restartrunkey"]}">'

    render_html += f'<br /><button onclick="savesettingsjs();" class="btn btn-outline-light">Save Settings</button> <button onclick="eel.projectpage();" class="btn btn-outline-light">Cancel</button></div>'




    eel.pageupdate(render_html)



@eel.expose
def savesettings(jqpath, cmdparams, qdqdir, setskill, recordsetting, restartrunkey):
    newsettings = {
        "joequakeexe": jqpath,
        "joequakeparams": cmdparams,
        "qdqdir": qdqdir,
        "setskill": setskill,
        "recordsetting": recordsetting,
        "restartrunkey": restartrunkey
    }

    project_file = open("settings.json", "wt")
    project_file.write(json.dumps(newsettings, indent=4, sort_keys=False))
    project_file.close()

    projectpage()

@eel.expose
def startgame(projectid, mapname, action):
    ## Generate qsm_setstats.cfg
    try:
        with open(f"settings.json", "rb") as f:
            settingsdata = json.load(f)

        with open(f"projects/{projectid}.json", "rb") as f:
            projectdata = json.load(f)

        if projectdata['maps'][mapname]['inherit_stats_from'] == "default":
            reg = 1
            ticr = 0
            temp1 = 0
        else:
            endstats = projectdata['maps'][projectdata['maps'][mapname]['inherit_stats_from']]['end_stats']


            ## Set force starting stats to acceptable values
            acceptable_start_stats = {
                    "health": [50, 100],
                    "armor": [0, 200],
                    "armor_type": [0, 4],
                    "shells": [25, 100],
                    "nails": [0, 200],
                    "rockets": [0, 100],
                    "cells": [0, 100],
                    "weapon": [1, 8]
            }

            if endstats['armor'] < 1:
                endstats['armor_type'] = 0
            elif endstats['armor'] > 150:
                endstats['armor_type'] = 3
            elif endstats['armor'] > 100:
                endstats['armor_type'] = 2
            elif endstats['armor'] > 0:
                endstats['armor_type'] = 1

            for stat in acceptable_start_stats:
                if endstats[stat] < acceptable_start_stats[stat][0]:
                    endstats[stat] = acceptable_start_stats[stat][0]
                elif endstats[stat] > acceptable_start_stats[stat][1]:
                    endstats[stat] = acceptable_start_stats[stat][1]


            ## Calulate held weapons and current weapon
            items = 0

            if "3" in endstats['weapons']:
                items += 1
            if "4" in endstats['weapons']:
                items += 2
            if "5" in endstats['weapons']:
                items += 4
            if "6" in endstats['weapons']:
                items += 8
            if "7" in endstats['weapons']:
                items += 16
            if "8" in endstats['weapons']:
                items += 32


            if endstats['weapon'] < 2:
                endstats['weapon'] = 9 ## Axe
            items += 656064 * (endstats['weapon'] - 2)

            print(items)
            reg = 1 + items + 64 * (100 - endstats['health']) + 3264 * endstats['armor']
            ticr = endstats['shells'] - 25 + 76 * endstats['nails'] + 15276 * endstats['rockets']
            temp1 = endstats['cells'] + 101 * endstats['armor_type']


        configcontents = f"// Settings for QSRM\nregistered {reg}\nsys_ticrate {ticr}\ntemp1 {temp1}\n"



        if settingsdata['setskill'] == "yes":
            configcontents += f"skill {projectdata['skill']}\n"

        if settingsdata['recordsetting'] == "record":
            configcontents += f'bind {settingsdata["restartrunkey"]} "record {projectdata["project_id"]}{mapname} {mapname}"\nrecord {projectdata["project_id"]}{mapname} {mapname}\n'
        elif settingsdata['recordsetting'] == "map":
            configcontents += f'bind {settingsdata["restartrunkey"]} "map {mapname}"\nmap {mapname}\n'


        # Write settings file
        if settingsdata['qdqdir'][-1] != "\\":
            settingsdata['qdqdir'] += "\\"

        project_file = open(f"{settingsdata['qdqdir']}qsmstats.cfg", "wt")
        project_file.write(configcontents)
        project_file.close()

        if action == "start":
            workingdir = settingsdata['joequakeexe'].rsplit("\\", 1)[0] + "\\"
            subprocess.Popen(f"{settingsdata['joequakeexe']} {settingsdata['joequakeparams']} +exec qsmstats.cfg", cwd=workingdir)
        else:
            eel.showsavedmodal()
    except:
        eel.showerrormodal('Could not save config or launch Quake. Please check all settings are valid.')


@eel.expose
def editstats(projectname, mapname):
    global projectdata
    with open(f"projects/{projectname}.json", "rb") as f:
        projectdata = json.load(f)

    render_html = ""
    render_html += f"<h4>Project Name: {projectdata['project_name']}</h4><hr />"

    render_html += f"<span class=\"h5 mapline\">Edit ending stats for: {mapname} - {projectdata['maps'][mapname]['map_name']}</span>"


    endstats = projectdata['maps'][mapname]['end_stats']

    if "3" in endstats['weapons']:

        if endstats['weapon'] == 3:
            slot3 = "<img id=wep3 onclick=\"selectweapon(3)\" src=ssg_s.png />"
        else:
            slot3 = "<img id=wep3 onclick=\"selectweapon(3)\" src=ssg.png />"
    else:
        slot3 = "<img id=wep3 onclick=\"selectweapon(3)\" src=blankweapon.png />"
    if "4" in endstats['weapons']:

        if endstats['weapon'] == 4:
            slot4 = "<img id=wep4 onclick=\"selectweapon(4)\" src=ng_s.png />"
        else:
            slot4 = "<img id=wep4 onclick=\"selectweapon(4)\" src=ng.png />"
    else:
        slot4 = "<img id=wep4 onclick=\"selectweapon(4)\" src=blankweapon.png />"
    if "5" in endstats['weapons']:

        if endstats['weapon'] == 5:
            slot5 = "<img id=wep5 onclick=\"selectweapon(5)\" src=sng_s.png />"
        else:
            slot5 = "<img id=wep5 onclick=\"selectweapon(5)\" src=sng.png />"
    else:
        slot5 = "<img id=wep5 onclick=\"selectweapon(5)\" src=blankweapon.png />"
    if "6" in endstats['weapons']:

        if endstats['weapon'] == 6:
            slot6 = "<img id=wep6 onclick=\"selectweapon(6)\" src=gl_s.png />"
        else:
            slot6 = "<img id=wep6 onclick=\"selectweapon(6)\" src=gl.png />"
    else:
        slot6 = "<img id=wep6 onclick=\"selectweapon(6)\" src=blankweapon.png />"
    if "7" in endstats['weapons']:

        if endstats['weapon'] == 7:
            slot7 = "<img id=wep7 onclick=\"selectweapon(7)\" src=rl_s.png />"
        else:
            slot7 = "<img id=wep7 onclick=\"selectweapon(7)\" src=rl.png />"
    else:
        slot7 = "<img id=wep7 onclick=\"selectweapon(7)\" src=blankweapon.png />"
    if "8" in endstats['weapons']:

        if endstats['weapon'] == 8:
            slot8 = "<img id=wep8 onclick=\"selectweapon(8)\" src=lg_s.png />"
        else:
            slot8 = "<imgid=wep8 onclick=\"selectweapon(8)\" src=lg.png />"
    else:
        slot8 = "<img id=wep8 onclick=\"selectweapon(8)\" src=blankweaponlg.png />"
    if endstats['weapon'] == 2:
        slot2 = "<img id=wep2 onclick=\"selectweapon(2)\" src=sg_s.png />"
    else:
        slot2 = "<img id=wep2 onclick=\"selectweapon(2)\" src=sg.png />"

    sslot2 = "<a href=\"#\" class=weaponselect id=sel2 onclick=\"selectweapon(2)\">*****</a>"
    sslot3 = "<a href=\"#\" class=weaponselect id=sel3 onclick=\"selectweapon(3)\">*****</a>"
    sslot4 = "<a href=\"#\" class=weaponselect id=sel4 onclick=\"selectweapon(4)\">*****</a>"
    sslot5 = "<a href=\"#\" class=weaponselect id=sel5 onclick=\"selectweapon(5)\">*****</a>"
    sslot6 = "<a href=\"#\" class=weaponselect id=sel6 onclick=\"selectweapon(6)\">*****</a>"
    sslot7 = "<a href=\"#\" class=weaponselect id=sel7 onclick=\"selectweapon(7)\">*****</a>"
    sslot8 = "<a href=\"#\" class=weaponselect id=sel8 onclick=\"selectweapon(8)\">*****</a>"



    if endstats['armor_type'] == 1:
        armor_icon = "<span><img id=newarmortype onclick=\"changearmor();\" src=green.png /></span>"
    elif endstats['armor_type'] == 2:
        armor_icon = "<span><img id=newarmortype onclick=\"changearmor();\" src=yellow.png /></span>"
    elif endstats['armor_type'] == 2:
        armor_icon = "<span><img id=newarmortype onclick=\"changearmor();\" src=red.png /></span>"
    else:
        armor_icon = "<span><img id=newarmortype onclick=\"changearmor();\" src=noarmor.png /></span>"

    #### Render edit stats dialog
    render_html += f'<table><tr><td class=statsheading colspan=11>Demo end stats:</tr>'
    render_html += f"<tr><td class=haiconcell rowspan=2>{armor_icon}</td><td class=hacell rowspan=2><input type=number id=newarmor class=hain value={endstats['armor']}></td><td class=haiconcell rowspan=2><img src=face.png /></td><td class=hacell rowspan=2><input type=number id=newhealth class=hain value={endstats['health']}></td><td class=ammocell colspan=2><input type=number id=newshells class=ammoin value={endstats['shells']}> <span class=ammoicon><img src=\"shells.png\" /></span>&nbsp;&nbsp;</td><td class=ammocell colspan=2><input type=number id=newnails class=ammoin value={endstats['nails']}> <span><img src=\"nails.png\" /></span>&nbsp;&nbsp;</td><td class=ammocell colspan=2><input type=number id=newrockets class=ammoin value={endstats['rockets']}> <span><img src=\"rockets.png\" /></span>&nbsp;&nbsp;</td><td class=ammocell colspan=2><input type=number id=newcells class=ammoin value={endstats['cells']}> <span><img src=\"cells.png\" /></span>&nbsp;&nbsp;</td></tr>"
    render_html += f"       <tr ><td class=weaponcell>{slot2}</td><td class=weaponcell>{slot3}</td><td class=weaponcell>{slot4}</td><td class=weaponcell>{slot5}</td><td class=weaponcell>{slot6}</td><td class=weaponcell>{slot7}</td><td colspan=2 class=weaponcelllg>{slot8}</td></tr>"
    render_html += f"       <tr ><td class=weaponcell><a href=\"#\" class=weaponselect onclick=\"changearmor();\">*****</a></td><td class=toggleselectedcell colspan=3>&nbsp;</td><td class=weaponcell>{sslot2}</td><td class=weaponcell>{sslot3}</td><td class=weaponcell>{sslot4}</td><td class=weaponcell>{sslot5}</td><td class=weaponcell>{sslot6}</td><td class=weaponcell>{sslot7}</td><td colspan=2 class=weaponcelllg>{sslot8}</td></tr></table>"
    render_html += f"<input type=hidden id=currentselectedweapon value={endstats['weapon']}> <input type=hidden id=currentprojectid value={projectdata['project_id']}> <input type=hidden id=currentmap value={mapname}>"

    render_html += f'<br /><button onclick="savestatsjs();" class="btn btn-outline-light">Save Stats</button> <button onclick="eel.loadproject(\'{projectdata["project_id"]}\');" class="btn btn-outline-light">Cancel</button></div>'


    eel.pageupdate(render_html)


@eel.expose
def savestatspy(prjid, mapname, newhealth, newarmor, newarmortype, shells, nails, rockets, cells, wepstr, selectedweapon):
    global projectdata
    with open(f"projects/{prjid}.json", "rb") as f:
        projectdata = json.load(f)
    projectdata['maps'][mapname]['end_stats'] = {
                "health": int(newhealth),
                "armor": int(newarmor),
                "armor_type": int(newarmortype),
                "shells": int(shells),
                "nails": int(nails),
                "rockets": int(rockets),
                "cells": int(cells),
                "weapons": wepstr,
                "weapon": int(selectedweapon)
        }

    projectdata['last_modified'] = int(time.time())

    project_file = open(f"projects/{projectdata['project_id']}.json", "wt")
    project_file.write(json.dumps(projectdata, indent=4, sort_keys=False))
    project_file.close()

    loadproject(projectdata['project_id'])


def formattime(demotime):
    ssms = str(demotime).split(".")
    secs = int(ssms[0]) % 60
    mins = (int(ssms[0]) - int(secs)) / 60
    if len(ssms) < 2:
        ssms.append(0)
    return f"{int(mins)}:{secs:02}.{str(ssms[1])[:3]}"


eel.start('main.html', size=(1300, 800))  # Start

try:
    eel.start('main.html', size=(790, 850), disable_cache=True)
except EnvironmentError:
    # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
    if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
        eel.start('main.html', size=(790, 850), disable_cache=True, mode='edge')
    else:
        raise