"use strict";




function addFoodLike(results){
    console.log(results);
}


function addToWishlistFood(evt){
    if (this.classList.contains("far")){ 
        this.classList.replace("far","fas");
        let formData = {
            "food_id": this.dataset.foodid,
            "name": $("#title").val(),
            "price": $("#price").val(),
            "rating": $("#rating").val(),
            "address": $("#food-location").val(),
            "img": $("#food-img").val()
        }
        $.post("/add_to_wishlist_food", formData, addFoodLike)
    } else {
        this.classList.replace("fas","far")
    }
};



$('.fa-heart').on('click', addToWishlistFood);




