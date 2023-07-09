
eel.expose(pageupdate);
function pageupdate(msg) {
  document.getElementById("maincontent").innerHTML = msg;
}

function startprojectjs() {
  prjname = document.getElementById("projectname").value;
  prjtemplate = document.getElementById("projecttemplate").value;
  eel.startprojectpy(prjname, prjtemplate);
}

function savesettingsjs() {
  jqpath = document.getElementById("jqpath").value;
  cmdparams = document.getElementById("cmdparams").value;
  qdqdir = document.getElementById("qdqdir").value;
  setskill = document.getElementById("setskill").value;
  recordsetting = document.getElementById("recordsetting").value;
  restartrunkey = document.getElementById("restartrunkey").value;
  eel.savesettings(jqpath, cmdparams, qdqdir, setskill, recordsetting, restartrunkey);
}



eel.expose(showsavedmodal);
function showsavedmodal() {
  $('#SavedModal').modal('show');

}

eel.expose(showerrormodal);
function showerrormodal(msg) {
    document.getElementById("errormodeltext").innerHTML = msg;
    $('#ErrorModal').modal('show');

}




function changearmor() {
  let currentarmor = document.getElementById("newarmortype").src;
  if (currentarmor.includes("green.png")) {
    document.getElementById("newarmortype").src = "yellow.png";
  } else if (currentarmor.includes("yellow.png")) {
    document.getElementById("newarmortype").src = "red.png";
  } else if (currentarmor.includes("red.png")) {
    document.getElementById("newarmortype").src = "noarmor.png";
  } else {
    document.getElementById("newarmortype").src = "green.png";
  }
}

function selectweapon(wep) {

      let wepblankimg = "blankweapon.png";
      let wepname;
      if (wep == 2) { wepname = "sg"; wepblankimg = "sg.png";}
      else if (wep == 3) { wepname = "ssg"; }
      else if (wep == 4) { wepname = "ng"; }
      else if (wep == 5) { wepname = "sng"; }
      else if (wep == 6) { wepname = "gl"; }
      else if (wep == 7) { wepname = "rl"; }
      else if (wep == 8) { wepname = "lg"; wepblankimg = "blankweaponlg.png"; }

      let cwep = document.getElementById("currentselectedweapon").value;

      let cwepname;
      if (cwep == 2) { cwepname = "sg"; }
      else if (cwep == 3) { cwepname = "ssg"; }
      else if (cwep == 4) { cwepname = "ng"; }
      else if (cwep == 5) { cwepname = "sng"; }
      else if (cwep == 6) { cwepname = "gl"; }
      else if (cwep == 7) { cwepname = "rl"; }
      else if (cwep == 8) { cwepname = "lg"; }

      let currentweaponstate = document.getElementById("wep" + wep).src;

      if (currentweaponstate.includes("blankweapon")) {
        document.getElementById("wep" + wep).src = wepname + ".png";

      } else if (cwep == wep) {
        document.getElementById("currentselectedweapon").value = 1;
        document.getElementById("wep" + wep).src = wepblankimg;
      } else {
        document.getElementById("wep" + wep).src = wepname + "_s.png";
        if (cwep != 1) {

          document.getElementById("wep" + cwep).src = cwepname + ".png";
        }
        document.getElementById("currentselectedweapon").value = wep;
      }
}

function savestatsjs() {
  let newhealth = document.getElementById("newhealth").value;
  let newarmor = document.getElementById("newarmor").value;
  let selectedweapon = document.getElementById("currentselectedweapon").value;
  let shells = document.getElementById("newshells").value;
  let nails = document.getElementById("newnails").value;
  let rockets = document.getElementById("newrockets").value;
  let cells = document.getElementById("newcells").value;


  let wepstr = " 2";
  for (let wep = 3; wep < 9; wep++) {
    let currentweaponstate = document.getElementById("wep" + wep).src;
    if (!currentweaponstate.includes("blankweapon")) {
      wepstr = wepstr + " " + wep;
    }
  }

  let newarmortype;
  let currentarmor = document.getElementById("newarmortype").src;
  if (currentarmor.includes("green.png")) {
    newarmortype = 1
  } else if (currentarmor.includes("yellow.png")) {
    newarmortype = 2
  } else if (currentarmor.includes("red.png")) {
    newarmortype = 3
  } else {
    newarmortype = 0
  }

  let mapname = document.getElementById("currentmap").value;
  let prjid = document.getElementById("currentprojectid").value;

  alert("A:" + newarmor + "\nH:" + newhealth + "\n" + wepstr + "\nW:" + selectedweapon + "\nAT:" + newarmortype + "\nSh:" + shells + "\nNi:" + nails + "\nRk:" + rockets + "\nCe:" + cells);

  eel.savestatspy(prjid, mapname, newhealth, newarmor, newarmortype, shells, nails, rockets, cells, wepstr, selectedweapon)

}
