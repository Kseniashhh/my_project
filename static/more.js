"use strict";


function ShowMore(results){
    
    $("#movie-container").html(results.data);

}
    


$("#more").on("click",function (evt) {
    
    let formData = {
        "type": $("#type").val(),
        "genre": $("#genre").val(),
        "decade": $("#decade").val()
    };
    $.get("/more_movies.json",formData, ShowMore);

})

