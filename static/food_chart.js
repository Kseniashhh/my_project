"use strict";


  const f_options = {
      responsive: true,
      defaultFontFamily: 'Helvetica'
    };

    // Make Donut Chart of percent of different types of Melons
    let ctx_donut_f = $("#foodChart").get(0).getContext("2d");

    $.get("/food_chart.json", function (data) {
      if (data["datasets"][0]["data"].length != 0 ){
        let myDonutChart = new Chart(ctx_donut_f, {
                                              type: 'pie',
                                              data: data,
                                              f_options: options
                                            });
      // $('#donutLegend').html(myDonutChart.generateLegend());
    }
    else {
      $("#fooChart").hide();
    }
    });