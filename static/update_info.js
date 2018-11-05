"use strict";


function checkPass(results) {
    let username = results;
    console.log(username);
    if (username == 'Success'){
        location.reload();
    } else if (username == "This email is already registered") {
        $(".alert-danger strong").html("This email is already registered");
        $(".alert-danger").attr("hidden", false)
    } else if (username == "This username is already taken") {
        $(".alert-danger strong").html("This username is already registered");
        $(".alert-danger").attr("hidden", false)
    } else if (username == "This username and email already registered"){
        $(".alert-danger strong").html("This username and email already registered");
        $(".alert-danger").attr("hidden", false)
    }

 }

function checkInfoExist() {

    let formData = {
        "username": $("#update-username").val(),
        "email": $("#update-email").val()
    }

    $.get('/info_check',formData, checkPass);
}


function validateUpdate(evt) {
    evt.preventDefault();
    evt.stopImmediatePropagation();
    checkInfoExist();
    return false;



}

$('#updateForm').on('submit', validateUpdate);

/////////////////////////////////////////////////////////////////////


function ValidatePsws(evt){
    if ($("#newPassword").val() != $("#confPassword").val()){
        alert("Passwords don't match");
        evt.preventDefault();

    } else {
        checkPSW();
    }
}


function checkPSW() {

    $.post("/psw_check", {psw: $("#current-pswd").val()}, function (results) {
        let res = results;
        if (res == "Success") {
            updatePswrd();
        }
        else {
            $(".alert-danger strong").html("Incorrect current password!");
            $(".alert-danger").attr("hidden", false)
        }
    })
}



function updatePswrd() {

    $.post("/psw_update", {psw: $("#newPassword").val()}, function (results) {
        let res = results
        // alert("Your password was successfully updated!");

        location.reload();
        console.log(results);

    });
}







function updatePSW(evt) {
    evt.preventDefault();
    evt.stopImmediatePropagation();
    ValidatePsws(evt);
    return false;


}




$('#psw-update').on('submit', updatePSW)
