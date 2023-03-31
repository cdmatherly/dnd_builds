console.log('linked')



// Get the modal
var modal = document.getElementById("sourcesModal");
var modalContent = document.querySelector(".modal-text")
// Get the button that opens the modal
var btn = document.getElementById("modalBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
// var span = document.getElementById("close");

// var modalText = document.getElementById("modal-text");

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

var sourcesUrl = '/static/img/combo_imgs/sources.txt'
fetch(sourcesUrl)
    .then( r => r.text())
    .then( function(sources){ //grabs the text file's content
        // console.log(sources)
        sources = sources.split(',') //makes a list from each line separated by a comma
        // console.log(sources)
        var arr = []
        for (each_source of sources){
            each_source = each_source.split('-- ') //makes a new list separating at "-- " and just lists the name/source pairs
            console.log(each_source[0])
            arr.push(each_source) //pushes each name/source pair array into larger array
            // modalContent.innerHTML += `<p>${each_source}</p>`
        }
        sourcesObj = Object.fromEntries(arr) //makes new object from each individual name/source array within the bigger array
        for (each_entry in sourcesObj){
            modalContent.innerHTML += `<p">${each_entry.replace('-',' ').replace('-',' ')}: <a href='${sourcesObj[each_entry]}'>Source</a></p>` 
            // * '.replace' gets rid of all hyphens (do it twice for instances like half-orc or half-elf where there are hyphens twice)
        }
    })