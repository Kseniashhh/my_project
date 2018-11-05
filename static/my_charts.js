"use strict";





 const options = {
      responsive: true,
      defaultFontFamily: 'Helvetica'
    };

    // Make Donut Chart of percent of different types of Melons
    let ctx_donut = $("#donutChart").get(0).getContext("2d");

    $.get("/mov_chart.json", function (data) {
      if (data["datasets"][0]["data"].length != 0 ){
        let myDonutChart = new Chart(ctx_donut, {
                                              type: 'pie',
                                              data: data,
                                              options: options
                                            });

      // $('#donutLegend').html(myDonutChart.generateLegend())
    }
    else {
      $("#movChart").hide();
    }
    });




