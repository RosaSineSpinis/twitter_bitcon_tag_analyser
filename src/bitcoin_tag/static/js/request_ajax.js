// import Moment from 'moment'
// window.Moment = Moment;
var request = new XMLHttpRequest();
request.open('GET', '/bitcoin_tag/data/', true);
var dataStorage = window.sessionStorage
let currentDataset = 0
console.log('request is working')

request.onload = function() {
  if (this.status >= 200 && this.status < 400) {
    // Success!
    var data = JSON.parse(this.response);
    console.log(data)
    data.forEach(function(el, idx){
        let date = new Date(el.tag_date);
        date = date.toLocaleDateString();
        console.log("el.tag_date", date)
        // let time = new Date(el.tag_time)
        let time = moment(el.tag_time, 'HH:mm')
        console.log("Moment time", time)

        let date_time = new Date(el.tag_date + " " + el.tag_time)
        console.log("date_time", date_time)
        date = date_time.toLocaleDateString();   // -> "2/1/2013"
        console.log("date", date)
        time = date_time.toLocaleTimeString();
        console.log("time", time)

    })
    // var data = this.response;
    // console.log(' inside request ', data)
    // console.log(data[0].tag_date)
    // console.log(typeof(data[0].tag_time))
    // console.log(data[0].tag_time)
    // console.log(typeof(data[0].dictionary_tags))
    // console.log(data[0].dictionary_tags)

    create_graphs(data[0])


    let test_dict = {"tag_date": "2021-09-22",
                "tag_time": "01:31:28.991909",
                "dictionary_tags": {
                                    "#bitcoin": 45,
                                    "#epro": 1,
                                    "#mxs": 5
                },
                "checkbox": 1}



    // let obj = new ConvertDict(test_dict, ['order', 'tag_name','number', 'date', 'time', 'checkbox'], ['#', 'Tag Name', 'Number', 'Date', 'Time', 'checkbox'])

    // let dataStorage = window.sessionStorage;
    dataStorage.setItem("data", JSON.stringify(data))

    createInputOption(data)
    let new_data = JSON.parse(dataStorage.getItem("data"))
    // console.log("new_data", new_data)


    // console.log("request test_dict", test_dict)
    let obj = new MakeTable(new_data[currentDataset], ['order', 'tag_name','number', 'date', 'time', 'checkbox'], ['#', 'Tag Name', 'Number', 'Date', 'Time', 'checkbox']);
    // console.log(obj.convertDictData(), obj.list_of_keys, obj.list_of_names);
    obj.createTable(obj.convertDictData(), obj.list_of_keys, obj.list_of_names);



    //newTable = createTable([
    //   {order: 1, tag_name: '#btc', number: 5, date: '01-10-06', time: '11.11'},
    //   {order: 2, tag_name: 'Orange', number: 2, date: '01-10-06', time: '12.12'},
    //   {order: 3, tag_name: 'Apple', number: 6, date: '01-10-06', time: '13.13'}
    // ],
    // ['order', 'tag_name','number', 'date', 'time'], ['#', 'Tag Name', 'Number', 'Date', 'Time']);

  } else {
    // We reached our target server, but it returned an error

  }
};

request.onerror = function() {
  // There was a connection error of some sort
};

request.send();



async function create_graphs(datasets, ) {
                  var ctx = document.getElementById('myChart')
                  tagsChart = setChart(datasets, ctx)
}



// export { dataStorage }