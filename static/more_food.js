"use strict";


function ShowMoreFood(results){
    console.log(results);
    
    $("#food-container").html(results.data);

}
    


$("#more").on("click",function () {
    
    let formData = {
        "type": $("#type").val(),
        "price": $("#hidden-price").val(),
        "term": $("#cuisine").val()
        
    };
    console.log(formData)
    $.get("/more_food.json",formData, ShowMoreFood);

})
