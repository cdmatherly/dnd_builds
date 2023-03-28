// ON PAGE LOAD
bgList = ["bg-1", "bg-2", "bg-3", "bg-4"]
var randomBg = bgList[Math.floor(Math.random() * bgList.length)]

var body = document.querySelector('body')
body.classList.add(randomBg)

//List options
var raceList = ["dragonborn", "dwarf", "elf", 'gnome', 'half-elf', 'half-orc', 'halfling', 'human', 'tiefling'];
var classList = ['barbarian', 'bard', 'cleric', 'druid', 'fighter', 'monk', 'paladin', 'ranger', 'rogue', 'sorcerer', 'warlock', 'wizard'];
var backgroundList = ["acolyte", "con-artist", "scoundrel"];

//Query Selector
var apiContent = document.querySelector("#api-content")
var genBtns = document.querySelector("#genBtns")
var saveButton = document.querySelector("#saveButton")
var warning = document.querySelector("#warning")
var genBtn2 = document.querySelector("#genBtn2")


function getData(raceChoice, classChoice, bgChoice) {
    console.log("Passed through race >> " + raceChoice)
    console.log("Passed through class >> " + classChoice)
    console.log("Passed through bg >> " + bgChoice)
    //Randomize an option from each list on each call
    var rdmRace = raceList[Math.floor(Math.random() * raceList.length)];
    var rdmBg = backgroundList[Math.floor(Math.random() * backgroundList.length)];
    var rdmClass = classList[Math.floor(Math.random() * classList.length)];
    
    if (raceChoice == "null" || raceChoice == undefined){ //makes random choice if there is not one predefined
        raceChoice = rdmRace
        console.log("Overwritten race >> " + raceChoice)
    }
    if (classChoice == "null" || classChoice == undefined){
        classChoice = rdmClass
        console.log("Overwritten class >> " + classChoice)
    }
    if (bgChoice == "null" || bgChoice == undefined){
        bgChoice = rdmBg
        console.log("Overwritten bg >> " + bgChoice)
    }

    raceChoice = raceChoice.toLowerCase();
    classChoice = classChoice.toLowerCase();
    bgChoice = bgChoice.toLowerCase();

    apiContent.innerHTML = `
    <div class="table-responsive mx-auto rounded-4 shadow-lg mb-4 pt-2 bg-light bg-opacity-75">
                                <table class="table table-borderless">
                                    <tbody>
                                        <tr class="">
                                            <td class="h5 col-1 px-5 align-middle fw-bold" scope="row">Race:</td>
                                            <td id="race" class="fw-semibold text-start col-1 fs-2 align-middle eaves"> </td>
                                            <td class="h5 col-1 px-5 pt-4 fw-bold">Proficiencies:</td>
                                            <td id="proficiencies" class="col-2 pt-4 fst-italic" rowspan="3"></td>
                                        </tr>
                                        <tr class="">
                                            <td class="h5 px-5 align-middle fw-bold">Class:</td>
                                            <td id="buildClass" class="fw-semibold text-start align-middle fs-2 eaves"> </td>
                                        </tr>
                                        <tr class="">
                                            <td class="h5 px-5 align-middle fw-bold">Background:</td>
                                            <td id="background" class="fw-semibold text-start align-middle fs-2 eaves"></td>
                                        </tr>
                                        <tr>
                                            <td colspan="4" id="raceDescription" class="pt-5 px-5"></td>
                                        </tr>
                                        <tr>
                                            <td colspan="4"><hr></td>
                                        </tr>
                                        <tr>
                                            <td colspan="4" id="bgDescription" class="pb-5 px-5"></td>
                                        </tr>
                                    </tbody>
                                </table>
                                <input type="hidden" class="form" name="proficiencies" id="proficienciesInput" value = "[">
                            </div>
                            `
    genBtn2.classList.remove("visually-hidden")
    genBtns.classList.remove("flex-column")

    showSave()

    Promise.all([ //chained fetch requests for each option
        fetch(`https://www.dnd5eapi.co/api/races/${raceChoice}`).then(response => response.json()).then(function (race) {
            console.log(race);
            var raceHTML = document.querySelector("#race"); //grab 'race' td from above
            // var imgPath = document.querySelector("#img-path");
            raceHTML.innerHTML = `${race.name}`; //set its innerHTML to our populated race
            apiContent.innerHTML += `<input type="hidden" name="race" value=${race.name}>`; //set a corresponding hidden input to submit to the database
            // imgPath.value = race.name.toLowerCase();
            // console.log(imgPath.value)
        }),
        fetch(`https://www.dnd5eapi.co/api/classes/${classChoice}`).then(response => response.json()).then(function (buildClass) {
            console.log(buildClass);
            var buildClassHTML = document.querySelector("#buildClass");
            // var imgPath = document.querySelector("#img-path");
            buildClassHTML.innerHTML = `${buildClass.name}`;
            apiContent.innerHTML += `<input type="hidden" class="form" name="buildClass" id="" value="${buildClass.name}">`;
            // imgPath.value += `-${buildClass.name.toLowerCase()}`;
            // console.log(imgPath.value)
        }),
        fetch(`https://api.open5e.com/backgrounds/${bgChoice}/?format=json`).then(response => response.json()).then(function (background) {
            console.log(background);
            var backgroundHTML = document.querySelector("#background");
            var bgDescription = document.querySelector("#bgDescription")
            backgroundHTML.innerHTML = `${background.name}`;
            bgDescription.innerHTML = `${background.desc}`;
            apiContent.innerHTML += `<input type="hidden" class="form" name="background" id="" value="${background.name}">`;
            apiContent.innerHTML += `<input type="hidden" class="form" name="bgDescription" id="" value="${background.desc}">`;
        }),
        fetch(`https://www.dnd5eapi.co/api/races/${raceChoice}`).then(response => response.json()).then(function (raceDescription) {
            console.log(raceDescription);
            var raceDescriptionHTML = document.querySelector("#raceDescription");
            raceDescriptionHTML.innerHTML = `${raceDescription.alignment} <br> <br> ${raceDescription.age} <br> <br> ${raceDescription.size_description} <br> <br> ${raceDescription.language_desc}`;
            apiContent.innerHTML += `<input type="hidden" class="form" name="raceDescription" id="" value="${raceDescription.alignment} ${raceDescription.age} ${raceDescription.size_description} ${raceDescription.language_desc}">`;
        }),
        fetch(`https://www.dnd5eapi.co/api/classes/${classChoice}/proficiencies`).then(response => response.json()).then(function (proficiencies) {
            var proficienciesList = proficiencies.results;
            console.log(proficienciesList);
            var proficienciesHTML = document.querySelector("#proficiencies");
            var proficienciesInput = document.querySelector("#proficienciesInput");
            proficienciesHTML.innerHTML = ``
            if (classChoice == "rogue") {
                proficienciesList.pop()
            }
            proficienciesInput.value += `'${proficienciesList[0].name}'`;
            for (var i = 1; i < proficienciesList.length - 1; i++) { // Loop through every proficiency and add it individually
                proficienciesHTML.innerHTML += `${proficienciesList[i].name} <br>`;
                proficienciesInput.value += `, '${proficienciesList[i].name}'`;
            }
            proficienciesInput.value += `, '${proficienciesList[i].name}']`;
        })])
        .catch(err => console.log(err))
}

function showSave() {
    console.log(warning)
    console.log(saveButton)
    if (saveButton != null) {
        saveButton.classList.remove("visually-hidden")
    }
    if (warning != null) {
        warning.classList.remove("visually-hidden")
    }
}

function hideSave(){
    console.log(warning)
    console.log(saveButton)
    if (saveButton != null) {
        saveButton.classList.add("visually-hidden")
    }
    if (warning != null) {
        warning.classList.add("visually-hidden")
    }
}


function showInputs(){
    hideSave()
    genBtn2.classList.add("visually-hidden")
    apiContent.innerHTML = ` <div class="options d-flex flex-column justify-content-center align-items-center rounded-4 shadow-lg mb-4 p-5 pb-4 bg-light bg-opacity-75">
    <div class="mb-3">
        <p class="fs-4">Choose options from below or leave blank to keep random!</p>
    </div>
    <div class="mb-3 col-6">
        <label for="" class="form-label h5 fw-bold">Race</label>
        <select class="form-select form-select-lg" name="race" id="raceSelect">
            <option selected value="null">Select one</option>
            <!--New options added here-->
        </select>
    </div>
    <div class="mb-3 col-6">
        <label for="" class="form-label h5 fw-bold">Class</label>
        <select class="form-select form-select-lg" name="buildClass" id="classSelect">
            <option selected value="null">Select one</option>
            <!--New options added here-->
        </select>
    </div>
    <div class="mb-5 col-6">
        <label for="" class="form-label h5 fw-bold">Background</label>
        <select class="form-select form-select-lg" name="background" id="bgSelect">
            <option selected value="null">Select one</option>
            <!--New options added here-->
        </select>
    </div>
    <button type="button" class="btn btn-success" onclick="getNewData()">Generate</button>
</div>`

var raceSelect = document.querySelector("#raceSelect")
var classSelect = document.querySelector("#classSelect")
var bgSelect = document.querySelector("#bgSelect")

for (var i of raceList){
    i = i.charAt(0).toUpperCase() + i.slice(1) //capitalizes the first letter
    raceSelect.innerHTML += `<option value="${i}">${i}</option>` //inserts select option from race list
}
for (var i of classList){
    i = i.charAt(0).toUpperCase() + i.slice(1) //capitalizes the first letter
    classSelect.innerHTML += `<option value="${i}">${i}</option>` //inserts select option from race list
}
for (var i of backgroundList){
    i = i.charAt(0).toUpperCase() + i.slice(1) //capitalizes the first letter
    bgSelect.innerHTML += `<option value="${i}">${i}</option>` //inserts select option from race list
}
}

function getNewData(){
    var newRaceChoice = document.querySelector("#raceSelect").value
    var newClassChoice = document.querySelector("#classSelect").value
    var newBgChoice = document.querySelector("#bgSelect").value
    getData(newRaceChoice, newClassChoice, newBgChoice)
}