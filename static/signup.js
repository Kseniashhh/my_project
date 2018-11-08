"use strict";


$("#signup-Pop").on("click", function(evt){
    evt.preventDefault();
    $("#signupPOP").modal('show')
})






function userAdded(results){
    let response = results;
    if (response == 'True'){
        alert("User successfully registered");
        $("#signupPOP").modal('hide')
        location.reload();
    } else {
        alert(response)
        $("#signupPOP").modal('hide')

    }
}



function addUser() {


    let url = "/user_added.json";
    let formData = {
        "email": $("#email").val(),
        "password": $("#password").val(),
        "username": $("#username").val()
    };
    $.post(url, formData, userAdded);
}




function checkError(results) {
    let username = results;
    console.log(username);
    if (username != "None"){
        alert("This username is taken, please choose another one");

    }else {
        addUser();
    }
}

function checkUsername() {
    $.get('/username_check',{username: $('#username').val()}, checkError);
}


function validateSubmit(evt) {
    evt.preventDefault();
    evt.stopImmediatePropagation();
    if ($("#password").val() != $("#confirm").val()){
         alert("Passwords don't match");
         evt.preventDefault();
     } else {
        checkUsername();
     }
    
    return false;


}

$('#signupform').on('submit', validateSubmit);






$(document).ready(function(){

    $("#password").focus();

    $("#pwcheck").click(function(){
        if ($("#pwcheck").is(":checked"))
        {
            $("#password").clone()
            .attr("type", "text").insertAfter("#password")
            .prev().remove();
        }
        else
        {
            $("#password").clone()
            .attr("type","password").insertAfter("#password")
            .prev().remove();
        }
    });
});


$(document).ready(function(){

    $("#confirm").focus();

    $("#confcheck").click(function(){
        if ($("#confcheck").is(":checked"))
        {
            $("#confirm").clone()
            .attr("type", "text").insertAfter("#confirm")
            .prev().remove();
        }
        else
        {
            $("#confirm").clone()
            .attr("type","password").insertAfter("#confirm")
            .prev().remove();
        }
    });
});