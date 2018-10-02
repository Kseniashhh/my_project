"use strict";


$("#signup-Pop").on("click", function(evt){
    evt.preventDefault();
    $("#signupPOP").modal('show')
})



function ValidatePsw(evt){
    if ($("#password").val() != $("#confirm").val()){
        alert("Passwords don't match");
        evt.preventDefault();
    }
}



function userAdded(results){
    let response = results;
    if (response != 'True'){
        alert("User successfully registered");
    } else {
        alert("This user is registered, please log in")
    }
}



function addUser() {
    evt.preventDefault();


    let url = "/user_added.json";
    let formData = {
        "email": $("#email").val(),
        "password": $("#password").val(),
        "username": $("#username").val()
    };
    console.log("sending ajax signup");
    $.post(url, formData, userAdded);
}




// function checkError(results) {
//     let username = results;
//     if (username != "None"){
//         alert("This username exists, please log in");

//     }else {
//         let form_data = $("#signupform").serialize();
//         window.location = '/user_added?' + form_data;
//     }
//     console.log("Finished checking username"); // after this form will be submitted
// }

function checkError(results) {
    let username = results;
    if (username != "None"){
        alert("This username is taken, please choose another one");

    }else {
        addUser();
    }
    console.log("Finished checking username"); // after this form will be submitted
}

function checkUsername() {
    $.get('/username_check',{username: $('#username').val()}, checkError);
    console.log($('#username').val());
    console.log("Finished sending AJAX");
}


function validateSubmit(evt) {
    evt.preventDefault();
    ValidatePsw(evt);
    checkUsername();

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