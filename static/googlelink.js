'use strict';




$(document).ready(function () {
    //Convert address tags to google map links 
    $('address').each(function () {
        let link = "<a class='font' href='http://maps.google.com/maps?q=" + encodeURIComponent( $(this).text() ) + "' target='_blank'>" + $(this).text() + "</a>";
        $(this).html(link);
    });
});