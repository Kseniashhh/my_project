"use strict";




function addLike(results){
    console.log(results);
}


function addToWishlist(evt){
    if (this.classList.contains("far")){ 
        this.classList.replace("far","fas");
        $.post("/add_to_wishlist", {movie_id: this.dataset.movieid}, addLike)
    } else {
        this.classList.replace("fas","far")
    }
};



$('.fa-heart').on('click', addToWishlist);


