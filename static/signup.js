"use strict";



function ValidatePsw(evt){
    if ($("#password").val() != $("#confirm").val()){
        alert("Passwords don't match");
        evt.preventDefault();
    }
}


function checkError(results) {
    let username = results;
    if (username != "None"){
        alert("This username exists");
    }
    console.log("Finished checking username"); // after this form will be submitted
}

function checkUsername() {
    $.get('/username_check',{username: $('#username').val()}, checkError);
    console.log("Finished sending AJAX");
}


function validateSubmit(evt) {
    evt.preventDefault();
    checkUsername();
    ValidatePsw(evt);
}

$('#signup').on('submit', validateSubmit);



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