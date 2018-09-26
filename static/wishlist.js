"use strict";




function addLike(results){
    console.log(results);
}


function addToWishlist(evt){
    if (this.classList.contains("far")){ 
        this.classList.replace("far","fas");
        console.log(this.classList.contains("far"))
        // console.log(heart, this[0].dataset.movieid)
        $.post("/add_to_wishlist", {movie_id: this.dataset.movieid}, addLike)
        console.log(this.dataset.movieid)
        console.log("post is running")
        // this.classList.replace("far","fas");
    } else {
        this.classList.replace("fas","far")
    }
};



$('.fa-heart').on('click', addToWishlist);


