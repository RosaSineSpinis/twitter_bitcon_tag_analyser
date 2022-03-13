
//setup

function setChartPie(data, ctx){
    console.log("setChartPie: beginning of the function")
    let _data = data
    console.log(_data)
    let _data_keys = []
     let _data_values = []
     _data_keys =  Object.keys(_data);
     _data_values = Object.values(_data);
     // console.log("_data_keys", _data_keys);
     // console.log("_data_values", _data_values);


    // var myChart =  new Chart(ctx, {
  const xyz =  new Chart(ctx, {
        type: 'pie',
        data: {
          labels: [
            'Neutral',
            'Positive',
            'Negative'
          ],
          datasets: [{
            label: 'My First Dataset',
            data: _data_values,
            backgroundColor: [
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)'
            ],
            // hoverOffset: 0
          }]
        },
        options: {
            responsive: true,
            radius: 150,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Tweet\'s attitude',
                    font: {
                        size: 20
                    },
                    padding: {
                        top: 30,
                        bottom: 30
                    }
                }
            }
            // scales: {
            //     yAxes: [{
            //         ticks: {
            //             beginAtZero: true
            //         }
            //     }]
            //  }
        }
    });
    return xyz
}


// function setChartPie(data, ctx){
//     console.log("setChartPie: beginning of the function")
//     let _data = data
//
//      let _data_keys = []
//      let _data_values = []
//      // _data_keys =  Object.keys(_data.dictionary_tags);
//      // _data_values = Object.values(_data.dictionary_tags);
//      // console.log("_data.tag_date", data.tag_date);
//      // console.log("_data.tag_time", data.tag_time);
//     // let _date_time = moment(_data.tag_date + " " + _data.tag_time);
//     //  console.log("_date_time", _date_time);
//     // console.log("createInputOption", date_time.format("Do, MM, YYYY, h:mm"))
//     // _date_time = _date_time.format("Do, MM, YYYY, h:mm");
//
//
//
//     const data_to_plot = {
//       labels: ['Red', 'Orange', 'Yellow', 'Green', 'Blue'],
//       datasets: [
//         {
//           label: 'Dataset 1',
//           data: [300, 50, 100, 10, 120],
//           backgroundColor: [
//               'rgb(255, 99, 132)',
//               'rgb(54, 162, 235)',
//               'rgb(255, 205, 86)',
//               'rgb(255, 10, 86)',
//               'rgb(10, 205, 86)'
//             ],
//         }
//       ]
//     };
//     // config
//      const config = {
//       type: 'pie',
//       data: {
//       labels: ['Red', 'Orange', 'Yellow', 'Green', 'Blue'],
//       datasets: [
//         {
//           label: 'Dataset 1',
//           data: [300, 50, 100, 10, 120],
//           backgroundColor: [
//               'rgb(255, 99, 132)',
//               'rgb(54, 162, 235)',
//               'rgb(255, 205, 86)',
//               'rgb(255, 10, 86)',
//               'rgb(10, 205, 86)'
//             ],
//         }
//       ]
//       },
//       options: {
//         responsive: true,
//         plugins: {
//           legend: {
//             position: 'top',
//           },
//           title: {
//             display: true,
//             text: 'Chart.js Pie Chart'
//           }
//         }
//       },
//     };
//
//     // var myChart =  new Chart(ctx, {
//      xyz =  new Chart(ctx, {
//         config: config
//     });
//     return xyz
// }


