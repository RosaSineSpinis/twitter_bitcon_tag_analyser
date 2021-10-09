

function createInputOption(data) {
    // function to generate datasets, time is as visible description
    let select = document.getElementById('select--input');
    data.forEach(function(element, idx){
        let opt = document.createElement('option');
        console.log(element)
        opt.value = idx;
        let date_time = moment(element.tag_date + " " + element.tag_time)
        // console.log("createInputOption", date_time.format("Do, MM, YYYY, h:mm"))
        opt.innerHTML = date_time.format("Do, MM, YYYY, h:mm");
        select.appendChild(opt);
    })
    // for (var i = min; i <= max; i++) {

}

function chooseDataSet(){
    console.log("this.value should be 0123", this.value)
    currentDataset = this.value
    let data = JSON.parse(dataStorage.getItem("data"));

    let el = document.getElementById('table--of--tags');
    // el.parentElement.removeChild(el);
    el.innerHTML = '';

    let obj = new MakeTable(data[currentDataset], ['order', 'tag_name','number', 'date', 'time', 'checkbox'], ['#', 'Tag Name', 'Number', 'Date', 'Time', 'checkbox']);
    obj.createTable(obj.convertDictData(), obj.list_of_keys, obj.list_of_names);
    rePlotHandler()
}

document.getElementById('select--input').addEventListener("change", chooseDataSet);
