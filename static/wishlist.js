"use strict";





// function addToWishlist(){
//     heart = $("#heart");
//     if (heart.classList.contains("far")){ 
//         heart.classList.replace("far","fas");
//     } else {
//         heart.classList.replace("fas","far")
//     }
// };


//check target


function addToWishlist(evt){
    debugger;
    heart = evt.currentTarget;
    if (heart.classList.contains("far")){ 
        heart.classList.replace("far","fas");
    } else {
        heart.classList.replace("fas","far")
    }
};



$('.fa-heart').on('click', addToWishlist);