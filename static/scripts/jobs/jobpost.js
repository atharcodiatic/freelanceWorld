// function jobFormOpen(event){
//     // Get the elements by their ID
//   var popupLink = document.getElementById("popup-link");
//   var popupWindow = document.getElementById("popup-window");
//   var closeButton = document.getElementById("close-button");
//   // Show the pop-up window when the link is clicked
//   popupLink.addEventListener("click", function(event) {
//     event.preventDefault();
//     popupWindow.style.display = "block";
//   });
//   // Hide the pop-up window when the close button is clicked
//   closeButton.addEventListener("click", function() {
//     popupWindow.style.display = "none";
//   });
// }

function jobSkillForm(){
    console.log('runniing')
    formButton = document.getElementsByClassName('jobSkillForm')[0]
    formButton.style.display = 'block';

    let form = document.getElementById('education'); // selecting the form
  
    form.addEventListener('submit', function(event) { // 1
    event.preventDefault()

    data = {}

    // axios.post()
    

})
}