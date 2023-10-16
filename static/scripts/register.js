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
    
  }
debugger
  console.log(user_id,"^^^^^^^^^^^^^^^^^^^^")


  axios({

    method: 'post',
    url: '/'+user_id.toString()+'/skill/',
    data:data ,
    

    
  }).then(res => res) 
 .catch(err => console.log(err)) 

}