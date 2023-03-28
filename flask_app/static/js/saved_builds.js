console.log('linked')


//List options
var raceList = ["dragonborn", "dwarf", "elf", 'gnome', 'half-elf', 'half-orc', 'halfling', 'human', 'tiefling'];
var classList = ['barbarian', 'bard', 'cleric', 'druid', 'fighter', 'monk', 'paladin', 'ranger', 'rogue', 'sorcerer', 'warlock', 'wizard'];
var backgroundList = ["acolyte", "con-artist", "scoundrel"];

showOptions()

// Get the modal
var modal = document.getElementById("sourcesModal");

// Get the button that opens the modal
var btn = document.getElementById("modalBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function () {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function showOptions(){
    var raceSelect = document.querySelector("#raceSelect")
    var classSelect = document.querySelector("#classSelect")
    var bgSelect = document.querySelector("#bgSelect")

    for (var i of raceList){
        i = i.charAt(0).toUpperCase() + i.slice(1) //capitalizes the first letter
        if (i != raceSelect.value){ //checks to make sure selected race is not repeated
        raceSelect.innerHTML += `<option value="${i}">${i}</option>` //inserts select option from race list
        }
    }
    for (var i of classList){
        i = i.charAt(0).toUpperCase() + i.slice(1) //capitalizes the first letter
        if (i != classSelect.value){
        classSelect.innerHTML += `<option value="${i}">${i}</option>` //inserts select option from race list
        }
    }
    backgroundList = ["Acolyte", "Con Artist", "Scoundrel"]; //redefining list due to "con-artist" discrepency
    for (var i of backgroundList){
        if (i != bgSelect.value){
        bgSelect.innerHTML += `<option value="${i}">${i}</option>` //inserts select option from race list
        }
    }
}