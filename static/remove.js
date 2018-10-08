"use strict";




function removeItem(results){
    alert(results + "Movie was removed from wishlist")
    location.reload();
}






$(".remove").on("click", function(evt){
    $.post("/remove_item",{movie: this.dataset.movid}, removeItem)
    console.log(this.dataset.movid)
});