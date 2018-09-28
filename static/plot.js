"use strict";

// function ShowPlot(){
//     $("invisible").classList.replace("invisible","visible");
// }




$("#image").hover(
    function {
        $("d-none").classList.replace("d-none","d-block");
    }, 
    function {
        $("d-block").classList.replace("d-block","d-none");
    })