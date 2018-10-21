"use strict";


function ShowMoreFood(results){
    console.log(results);
    
    $("#food-container").html(results.data);

}
    


$("#more").on("click",function () {
    
    let formData = {
        "type": $("#type").val(),
        "term": $("#cuisine").val(),
        "price": $("#price").val()
    };
    console.log(formData)
    $.get("/more_food.json",formData, ShowMoreFood);

})
