"use strict";


function ShowMore(results){
    console.log(results);
    // let movies = results;
    // debugger;
    
    // $("#movie-container").remove();
    console.log("HELLP!!!!!")
    $("#movie-container").html(results.data);
    // $("#movie-container").append(results.data);

}
    


$("#more").on("click",function () {
    // evt.preventDefault();
    // evt.stopImmediatePropagation();

    
    // $.get("/more_movies.json",{"type": $("#type").val(), "decade": $("#decade").val(),"genre": $("#genre").val()}, ShowMore);
    $.get("/more_movies.json",{"type": $("#type").val()}, ShowMore);

    console.log("ajax sent");
    console.log($("#type").val());
})

