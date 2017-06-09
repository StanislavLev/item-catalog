
function setDefaultTextOnblur(id, defaultVal) {
    if (document.getElementById(id).value == ""){
        document.getElementById(id).value = defaultVal
        document.getElementById(id).style.color = "grey"
    }; 
}

function clearDefaultTextOnfocus(id, defaultVal) {
    if (document.getElementById(id).value == defaultVal){
        document.getElementById(id).value = ""
        document.getElementById(id).style.color = "black"
    }; 
}

function timedText() {
    var x = document.getElementById("flashtxt");
    setTimeout(function(){ x.innerHTML=""}, 3000);
}