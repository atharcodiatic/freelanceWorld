axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
function hideOpen(event){
    let data = { 
    "showFeed":null,
    "allJob":null,
    }
    if (event.target.value == "feed"){
        data["showFeed"] = true;
        data["allJob"] = false;
    }
    else{
        data["allJob"] = true;
        data["showFeed"] =false;
    }
    
    axios({

        method: 'post',
        url: '/freelancerfeed/',
        data:data ,
    
      })
      .then(res => console.log(res.data.status)) 
     .catch(err => console.log(err)) 
}