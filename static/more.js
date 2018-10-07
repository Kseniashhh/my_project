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
    // let length = movies.length;
    // let i=0;

    // while (i < length){
    //     // console.log(movies[i]);
    //     // console.log(movies[i]["title"])
    //     // console.log(movies[i]["year"])
    //     // console.log(movies[i]["poster"])
    //     // console.log(movies[i]["plot"])
    //     // $("#title").html(movies[i]["title"]);
    //     // $("#year").html(movies[i]["year"]);
    //     // $("#mov-img").html(movies[i]["poster"]);
    //     // $("#mov-plot").html(movies[i]["plot"]);
    //     // i +=1;

    



    // for (let mov in movies){
    //     console.log(mov);

    //     $("#title").html(mov.title);
    //     $("#year").html(mov.year);
    //     $("#mov-img").html(mov.poster);
    //     $("#mov-plot").html(mov.plot);

    // }







$("#more").on("click",function () {
    // evt.preventDefault();
    // evt.stopImmediatePropagation();

    
    $.get("/more_movies.json",{"type": $("#type").val()}, ShowMore);
    console.log("ajax sent");
    console.log($("#type").val());
})

// $("#more").on("click", function() { alert("works")})
