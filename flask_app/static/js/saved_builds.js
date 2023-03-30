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
    .then( function(sources){
        // console.log(sources)
        sources = sources.split(',')
        // console.log(sources)
        var arr = []
        for (each_source of sources){
            each_source = each_source.split('-- ')
            each_source[0] = each_source[0].replace('-', " ")
            each_source[0] = each_source[0].replace('-', " ")
            arr.push(each_source)
            // modalContent.innerHTML += `<p>${each_source}</p>`
        }
        obj = Object.fromEntries(arr)
        for (each_entry in obj){
            modalContent.innerHTML += `<p">${each_entry}: <a href='${obj[each_entry]}'>Source</a></p>`
        }
    })