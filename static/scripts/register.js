let user_id = localStorage.getItem('user_id')
console.log(user_id,'%%%%%%%%%%%%%')

function formPopup() {

    let formshow = document.getElementsByClassName("education")[0].style.display='block';
    
    let form = document.getElementById('education'); // selecting the form
  
    form.addEventListener('submit', function(event) { // 1
    event.preventDefault()
    
    const token = document.querySelectorAll('input[name=csrfmiddlewaretoken]')[0].value
    
    start_date_month = document.getElementById('id_start_date_month').value
    start_date_day  =  document.getElementById('id_start_date_day').value
    start_date_year = document.getElementById('id_start_date_year').value
    
    let start_date = [start_date_year, start_date_month, start_date_day]

    end_date_month = document.getElementById('id_end_date_month').value
    end_date_year = document.getElementById('id_end_date_year').value
    end_date_day  = document.getElementById('id_end_date_day').value

    let end_date = [end_date_year, end_date_month, end_date_day]

    let data = new FormData(); 
    data.append("type", document.getElementById('id_type').value)  
    data.append("degree", document.getElementById('id_degree_name').value)
    data.append("course", document.getElementById('id_course').value)
    data.append("college_name", document.getElementById('id_college_name').value)
    data.append("start_date", start_date)
    data.append("end_date", end_date)
    
    data.append("csrfmiddlewaretoken", token) 
    console.log(data)

    
    formshow = document.getElementsByClassName("education")[0].style.display='none';
    form.reset();
    axios({
        method: 'post',
        url: '/'+user_id.toString()+'/education/',
        data:data,
        
      }).then(res => freelancer_edu()) 
     .catch(err => console.log(err)) 

})


}


let freelancer_edu = async()=>{
  let response = await axios.get('/'+user_id.toString()+'/education/')
  response_data = response.data 
  response_data.forEach(element => {

  let education_tag = document.getElementById('education_section');

  let span_tag = document.createElement('span')
  span_tag.innerText = element.fields.type +' : '+ element.fields.course + " , "
  education_tag.appendChild(span_tag)


    console.log(element.fields)
    console.log(element.fields.type , element.fields.course)
    
  });
  
  
  return response.data
}

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

function addSkill(){

  let skill_to_add = addSkill.caller.arguments[0].target.id;

  data = {
    'skill' : skill_to_add,
    'level' :'EXP' ,
  }

  console.log(user_id,"^^^^^^^^^^^^^^^^^^^^")

  axios({

    method: 'post',
    url: '/'+user_id.toString()+'/skill/',
    data:JSON.stringify(data) ,

  })
  .then(res => freelancer_skill()) 
 .catch(err => console.log(err)) 


}

// this function fetch freelancer skills and update them without refreshing the page
let freelancer_skill = async()=>{

  let response = await axios.get('/'+user_id.toString()+'/skill/')
  response_data = response.data 


  let skills_tag = document.getElementById('skills');
  skills_tag.innerHTML = '';

  console.log(skills_tag,'$$$$$$$')
  response_data.forEach(element => {
    let each_skill = document.createElement('div')

    each_skill.setAttribute('id',element.fields.skill_name)
    each_skill.innerText= "Name : "+ element.fields.skill_name + ", Level : "+ element.fields.level

      

      //Create array of options to be added
      let array = ["BEG","INT","EXP",];

      //Create and append select list
      let  selectList = document.createElement("select");
      selectList.id = element.fields.skill_name;
      selectList.addEventListener("change",selectedLevel);
      each_skill.appendChild(selectList);

      //Create and append the options
      for (var i = 0; i < array.length; i++) {
          var option = document.createElement("option");
          option.value = array[i];
          option.text = array[i];
          selectList.appendChild(option);
      }

    let deleteButton = document.createElement('button')
    deleteButton.setAttribute('id','id_'+element.fields.skill_name)
    deleteButton.innerText ='delete'
    deleteButton.style.height = '15px';
    deleteButton.style.width = '40px';

    deleteButton.addEventListener("click", deleteSkill);
  
    each_skill.append(deleteButton)

    
    skills_tag.append(each_skill)
    

    //edit functionality will be added later remaining 
    skills_tag.style.backgroundColor = 'wheat';
    skills_tag.style.border = 'black';

    // console.log(element.fields,"*******")
    // console.log(element.fields.level , element.fields.skill_name)
    
  });
}


function selectedLevel(event){
  
  let skill = event.target.id
  let level = event.target.value
  
  data = {
    "skill" : skill,
    'level': level,
  }

  axios({

    method: 'patch',
    url: '/'+user_id.toString()+'/skill/',
    data:data ,

  }).then(res => freelancer_skill())
 .catch(err => console.log(err)) 

}

function deleteSkill(event){

  
  let id = event.target.id
  skill_name = id.substring(3, id.length)
  
  data = {
    "skill" : skill_name,

  }
  axios({

    method: 'delete',
    url: '/'+user_id.toString()+'/skill/',
    data:data ,

  }).then(res => freelancer_skill())
 .catch(err => console.log(err)) 
  
}

function addFormPop(){

  let formDisplay = document.getElementsByClassName("addSkillForm")[0]
  formDisplay.style.display ='block';

  let form = document.getElementById('add_skillform'); 
  
    form.addEventListener('submit', function(event) { 
    event.preventDefault()

    
    skill= document.getElementById('id_skill_name').value  
    level =  document.getElementById('id_level').value

    data = {
      "skill" : skill,
      "level" : level,
    }
    
    axios({

      method: 'post',
      url: '/'+user_id.toString()+'/skill/',
      data:data ,
      
    })
    .then(res => {
      console.log('##############33',res.data)
      if (res.data.status =="failed"){
        let errorMessage = document.getElementById("formError")
        errorMessage.innerText = res.data.message
  
      }
      else{
        formDisplay.style.display = 'none';
        form.reset()
      

      return freelancer_skill()}
    }) 
   .catch(err => console.log(err))   
    }
    )
 }
