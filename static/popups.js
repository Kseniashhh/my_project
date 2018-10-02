"use strict";

// $(".login-pop").click(function() {
// $("#contactdiv").css("display", "block");
// });

// $('#login').on('show.bs.modal', function (evt) {
//   var button = $(event.relatedTarget) // Button that triggered the modal
//   var recipient = button.data('whatever') // Extract info from data-* attributes
//   // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
//   // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
//   var modal = $(this)
//   modal.find('.modal-title').text('New message to ' + recipient)
//   modal.find('.modal-body input').val(recipient)
// })

$("#login-Pop").on("click", function(evt){
    evt.preventDefault();
    $("#loginPOP").modal('show')
})


function checkUser(results) {
    let user = results;
    console.log(user)
    if (user == 'True'){
        alert("User was successfuly logged in");
        $("#loginPOP").modal('hide')

    }else {
        alert("This user doesn't exist. Please register")
    }
    console.log("Finished checking username"); // after this form will be submitted
}





// $("#loginform").on("submit", function(evt){
//     $.get('/login-user',{email: $('#email').val(), password: $('#password').val()}, checkUser);
// })

$("#loginform").on("submit",function (evt) {
    evt.preventDefault();


    let url = "/login_user.json";
    let formData = {
        "email": $("#email").val(),
        "password": $("#password").val()
    };
    console.log("sending ajax");
    $.post(url, formData, checkUser);
})