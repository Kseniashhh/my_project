"use strict";



function ValidatePsw(evt){
    if ($("#password").val() != $("#confirm").val()){
        alert("Passwords don't match");
        evt.preventDefault();
    }
}


function checkError(results) {
    let username = results;
    if (username != None){
        alert("This username exists");
    }
    console.log("Finished checking username");
}

function checkUsername() {
    $.get('/username_check',{username: $('#username').val()}, checkError);
    console.log($('#username').val());
    console.log("Finished sending AJAX");
}


function validateSubmit() {
    checkUsername();
    ValidatePsw();
}

$('#signup').on('submit', validateSubmit);
