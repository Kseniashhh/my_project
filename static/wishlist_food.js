"use strict";




function addFoodLike(results){
    console.log(results);
}


function addToWishlistFood(evt){
    if (this.classList.contains("far")){ 
        this.classList.replace("far","fas");
        console.log(this.dataset.foodid);
        // let formData = {
        //     "food_id": this.dataset.foodid,
        //     "name": $("#title").val(),
        //     "price": $("#price").val(),
        //     // "rating": $("#rating").val(),
        //     "address": $("#location").val(),
        //     "img": $("#food-img").val()
        // }
        // console.log(formData);
        $.post("/add_to_wishlist_food", {food_id: this.dataset.foodid}, addFoodLike)
    } else {
        this.classList.replace("fas","far")
    }
};



$('.fa-heart').on('click', addToWishlistFood);




