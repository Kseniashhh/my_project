"use strict";



$("#login-Pop").on("click", function(evt){
    evt.preventDefault();
    $("#loginPOP").modal('show')
})


function checkUser(results) {
    console.log("in check user fun")

    let user = results;
    console.log(user)
    if (user.ERROR){
        alert("Wrong password");
    }else if (user != null){
        alert("User was successfuly logged in");
        $("#loginPOP").modal('hide');
        location.reload();
    }else {
        alert("This user doesn't exist. Please register")
    console.log("Finished checking user"); // after this form will be submitted
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
    console.log(formData)
    console.log("sending ajax");
    $.post(url, formData, checkUser);
    return false;
})