"use strict";




function addFoodLike(results){
    console.log(results);
}


function addToWishlistFood(evt){
    if (this.classList.contains("far")){ 
        this.classList.replace("far","fas");
        $.post("/add_to_wishlist_food", {food_id: this.dataset.foodid}, addFoodLike);
        console.log(this.dataset.foodid);
    } else {
        this.classList.replace("fas","far")
    }
};



$('.fa-heart').on('click', addToWishlistFood);




