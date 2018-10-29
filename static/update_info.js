"use strict";

// function userAdded(results){
//     let response = results;
//     if (response == 'True'){
//         alert("User successfully registered");
//         $("#signupPOP").modal('hide')
//         location.reload();
//     } else {
//         alert(response)
//         $("#signupPOP").modal('hide')

//     }
// }



// function UpdateUser() {


//     let url = "/user_update.json";
//     let formData = {
//         "email": $("#email").val(),
//         "password": $("#password").val(),
//         "username": $("#username").val()
//     };
//     $.post(url, formData, userAdded);
// }




function checkPass(results) {
    let username = results;
    console.log(username);
    if (username == 'Success'){
        alert("User's info was successfully updated!")
        location.reload();
    } else if (username == "This email is already registered") {
        alert(username)
    } else if (username == "This username is already taken") {
        alert(username)
    } else if (username == "This username and email already registered"){
        alert(username)
    }
//     if (username != "None"){
//         alert("This username is taken, please choose another one");

//     }else {
//         UpdateUser();
//     }
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
            alert("Incorrect current password!")
        }
    })
}



function updatePswrd() {

    $.post("/psw_update", {psw: $("#newPassword").val()}, function (results) {
        let res = results
        alert("Your password was successfully updated!");
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
