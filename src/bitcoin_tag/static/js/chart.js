 function setChart(data, ctx){
    console.log("setChart: beginning of the function")
    let _data = data

     let _data_keys = []
     let _data_values = []
     _data_keys =  Object.keys(_data.dictionary_tags);
     _data_values = Object.values(_data.dictionary_tags);
     console.log("_data.tag_date", data.tag_date);
     console.log("_data.tag_time", data.tag_time);
    let _date_time = moment(_data.tag_date + " " + _data.tag_time);
     console.log("_date_time", _date_time);
    // console.log("createInputOption", date_time.format("Do, MM, YYYY, h:mm"))
    _date_time = _date_time.format("Do, MM, YYYY, h:mm");

    // var myChart =  new Chart(ctx, {
    tagsChart =  new Chart(ctx, {
        type: 'bar',
        data: {
            labels: _data_keys,  //labels
            datasets: [{
                label: _date_time,
                data: _data_values,
                backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(255, 159, 64, 0.2)',
                  'rgba(255, 205, 86, 0.2)'
                ],
                borderColor: [
                  'rgb(255, 99, 132)',
                  'rgb(255, 159, 64)',
                  'rgb(255, 205, 86)'
                ],
                borderWidth: 1
                }] //data come in [ ]
        },
        options: {
            responsive: true,
            // maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
             }
        }
    });
    return tagsChart
}