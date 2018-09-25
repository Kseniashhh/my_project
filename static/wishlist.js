"use strict";





// function addToWishlist(){
//     heart = $("#heart");
//     if (heart.classList.contains("far")){ 
//         heart.classList.replace("far","fas");
//     } else {
//         heart.classList.replace("fas","far")
//     }
// };


//check target


// function addToWishlist(evt){
//     debugger;
//     heart = evt.currentTarget;
//     if (heart.classList.contains("far")){ 
//         heart.classList.replace("far","fas");
//     } else {
//         heart.classList.replace("fas","far")
//     }
// };


function addLike(results){
    console.log(results);
}


function addToWishlist(evt){
    if (this.classList.contains("far")){ 
        this.classList.replace("far","fas");
        console.log(this.classList.contains("far"))
        // console.log(heart, this[0].dataset.movieid)
        $.post("/add_to_wishlist", {movie_py: this.dataset.movieid}, addLike)
        console.log(this.dataset.movieid)
        console.log("post is running")
        // this.classList.replace("far","fas");
    } else {
        this.classList.replace("fas","far")
    }
};



$('.fa-heart').on('click', addToWishlist);


