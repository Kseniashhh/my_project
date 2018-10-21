"use strict";


function ShowMoreFood(results){
    console.log(results);
    
    $("#food-container").html(results.data);

}
    


$("#more").on("click",function () {
    
    let formData = {
        "type": $("#type").val(),
        "price": $("#price").val(),
        "term": $("#term").val()
    };
    
    $.get("/more_food.json",formData, ShowMoreFood);

})
