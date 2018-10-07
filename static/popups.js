"use strict";



$("#login-Pop").on("click", function(evt){
    evt.preventDefault();
    $("#loginPOP").modal('show')
})


function checkUser(results) {

    let user = results;
    if (user.ERROR){
        alert("Wrong password");
    }else if (user != null){
        alert("User was successfuly logged in");
        $("#loginPOP").modal('hide');
        location.reload();
    }else {
        alert("This user doesn't exist. Please register")
}
}




$("#loginform").on("submit",function (evt) {
    evt.preventDefault();
    evt.stopImmediatePropagation();

    let url = "/login_user.json";
    let formData = {
        "email": $("#logemail").val(),
        "password": $("#logpassword").val()
    };
    $.post(url, formData, checkUser);
    return false;
})