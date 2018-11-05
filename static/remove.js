"use strict";




// function removeItem(results){
//     alert(results + "Movie was removed from wishlist")
//     location.reload();





// $("#mremove").on("click", function(evt){
//     let formData = {
//         "movie": this.dataset.movid,
//         "type" : "movie"
//     }
//     $.post("/remove_item",formData, removeItem)
//     console.log(this.dataset.movid)
// });

///////////////////////////////////////////////////////////////


function removeItem(results){
    // alert(results + "Item was removed from wishlist")
    location.reload();
}




$(".remove").on("click", function(evt){
    // let formData = {
    //     "content": this.dataset.movid,
    //     "type" : $('input[name="type"]').val()
    // }
    $.post("/remove_item",{content: this.dataset.movid}, removeItem)
    console.log(this.dataset.movid)
});


