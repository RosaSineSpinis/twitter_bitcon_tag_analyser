let tagsChart
let charts_list = []
let dataStorage = window.sessionStorage
let currentDataset = 0
document.body.addEventListener('click', function (event) {
    if (event.target.className === 'form-check-input') {
        console.log("add event listener works")
        const form = event.target.form;
        const data_form = new FormData(form);

        const request = new XMLHttpRequest();
        request.responseType = 'json';

        request.open(form.method, form.action, true);

        request.send(data_form);
        console.log("data_form: ", data_form)
        // var dataStorage = window.sessionStorage
        // let currentDataset = 0

        request.addEventListener("load", function () {
            if (this.readyState === 4 && this.status === 200) {
                // Success!
                let data = null
                try {
                    // Parse a JSON
                    data = JSON.parse(this.response);
                } catch (e) {
                    // You can read e for more info
                    data = this.response;
                }


                console.log(data)
                data.forEach(function (el, idx) {
                    let time = moment(el.tag_time, 'HH:mm')
                    let date_time = new Date(el.tag_date + " " + el.tag_time)
                    let date = date_time.toLocaleDateString();   // -> "2/1/2013"
                    time = date_time.toLocaleTimeString();

                })

                process_drawing_tasks(data)

                //newTable = createTable([
                //   {order: 1, tag_name: '#btc', number: 5, date: '01-10-06', time: '11.11'},
                //   {order: 2, tag_name: 'Orange', number: 2, date: '01-10-06', time: '12.12'},
                //   {order: 3, tag_name: 'Apple', number: 6, date: '01-10-06', time: '13.13'}
                // ],
                // ['order', 'tag_name','number', 'date', 'time'], ['#', 'Tag Name', 'Number', 'Date', 'Time']);

            } else {
                // We reached our target server, but it returned an error

            }
        });
        request.onerror = function() {
          // There was a connection error of some sort
            console.log("request.onerror")
        };

    }
});


async function create_graphs(datasets) {
                  var ctx = document.getElementById('myChart')
                  let myChart = setChart(datasets, ctx)
                  charts_list.push(myChart)
                  console.log("async function create_graphs works")
}

// export { dataStorage }

var hatEvalData = document.getElementById("radioButton--hour");
hatEvalData.click();

function createSemanticChartPie(data){
    console.log("createSemanticChartPie data", data)
    // data = {"0":2, "1":5, "-1":5}
    var ctx = document.getElementById('semantic_analysis_Chart')
    let myChart = setChartPie(data, ctx)
    charts_list.push(myChart)
    // charts_list.push(myChart)

}


function process_drawing_tasks(data) {

        // let dataStorage = window.sessionStorage;
    dataStorage.setItem("data", JSON.stringify(data))
    let new_data = JSON.parse(dataStorage.getItem("data")) //

        for (let i = 0; i < charts_list.length; i++) {
        charts_list[i].destroy()
        console.log("process_drawing_tasks: destroying")
    }
    charts_list = []


    createSemanticChartPie(new_data[currentDataset]["semantic_analysis"])
    createSemanticIndicator(new_data[currentDataset]["semantic_analysis"])

    removeInputMenu()  // remove InputMenu when new dataset is send from backend
    createInputOption(data) // creates new InputMenu


    removeTableOfTags()  //remove table if table exists
    let obj = new MakeTable(new_data[currentDataset], ['order', 'tag_name', 'number', 'date', 'time', 'checkbox'], ['#', 'Tag Name', 'Number', 'Date', 'Time', 'checkbox']);
    obj.createTable(obj.convertDictData(), obj.list_of_keys, obj.list_of_names);
    console.log("process_drawing_tasks: end of function")

    create_graphs(data[data.length - 1]) // the last in the list // here it is immediately replotted as only 10 graphs are plotted

    rePlotHandler()

    //old version of the graph
    // check if graph is already created if no destroy

    // for (let i = 0; i < charts_list.length; i++) {
    //     charts_list[i].destroy()
    //     console.log("process_drawing_tasks: destroying")
    // }
    // charts_list = []
    // create_graphs(data[data.length - 1]) // the last in the list
    //
    // // let dataStorage = window.sessionStorage;
    // dataStorage.setItem("data", JSON.stringify(data))
    // let new_data = JSON.parse(dataStorage.getItem("data")) //
    //
    // removeInputMenu()  // remove InputMenu when new dataset is send from backend
    // createInputOption(data) // creates new InputMenu
    //
    // removeTableOfTags()  //remove table if table exists
    // let obj = new MakeTable(new_data[currentDataset], ['order', 'tag_name', 'number', 'date', 'time', 'checkbox'], ['#', 'Tag Name', 'Number', 'Date', 'Time', 'checkbox']);
    // obj.createTable(obj.convertDictData(), obj.list_of_keys, obj.list_of_names);
    // console.log("process_drawing_tasks: end of function")
}