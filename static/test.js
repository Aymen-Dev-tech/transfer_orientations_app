const API="https://reqres.in/api"

window.onload= async()=>{
    await fetch(`${API}/users`)
        .then(res=>res.json())
        .then(data=>display(data))
        .catch(err=>console.error(err))
} 
const display=(data)=>{
    document.querySelector(".table td[9]").innerHTML = data.data[0].email
}


fetch("database.db")
    .then(function(res){
        return res.json()
    })
    .then(function(data){
        let placeholder = document.querySelector("#table.content")
        let out = "";
        for(let item of data){
            out+=`
                <tr>
                    <td><a href=#>``</a></td>
                </tr>
            
            `;
        }
        placeholder.innerHTML=out;
    })


