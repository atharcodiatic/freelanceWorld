
window.onload = function(){

    let form = document.getElementById("job_skillform"); // selecting the form
    form.addEventListener('submit', function(event) { // 1runnibg
    event.preventDefault()

    skill= document.getElementById('id_name').value
    console.log(skill,'***********************')
    data = {
        "skill" : skill,
    }
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    axios({
        method: 'post',
        url: '/skillcreate/',
        data:data ,
        
      })
      .then(res => {
          if( res.data.status == "success"){
              console.log('##############33',res.data)
            id = res.data.id
            let add_skill = document.getElementById('id_skill_required')

            let skillDiv = document.createElement('div')
            let label = document.createElement('label');

            label.setAttribute('for',"id_skill_required_"+id.toString());
            label.textContent = skill


            checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.name = 'skill_required'
            console.log(typeof id)
            checkbox.value = id.toString()
            checkbox.id = "id_skill_required_"+id.toString()
            checkbox.checked = true
            label.appendChild(checkbox)
            skillDiv.appendChild(label)
            add_skill.appendChild(skillDiv)
            form.reset();
            formButton.style.display = 'none';
        }
    
    })
    

})

}
function formJobSkillAdd(){
    formButton = document.getElementsByClassName('jobSkillForm')[0]
    formButton.style.display = 'block';
    debugger
    
}