/** Input menu is roller menu with when you cn set data for certain dataset **/

function removeInputMenu(){
     let el = document.getElementById('select--input'); //removes the table before creates new one
    // el.parentElement.removeChild(el);
    el.innerHTML = '';
}

function createInputOption(data) {
    // function to generate datasets, time is a visible description
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

function removeTableOfTags(){
    let el = document.getElementById('table--of--tags'); //removes the table before creates new one
    // el.parentElement.removeChild(el);
    el.innerHTML = '';
}

function chooseDataSet(){
    /**
    takes dataset from currentDataset as a key treats date
    removes the table before creates new one
    makes new table
    **/
    currentDataset = this.value
    let data = null;
      try {
      // Parse a JSON
        data = JSON.parse(dataStorage.getItem("data"));
      } catch (e) {
        // You can read e for more info
        data = dataStorage.getItem("data");
      }

    removeTableOfTags()
    //makes new table - first obj of class then creates the table
    let obj = new MakeTable(data[currentDataset], ['order', 'tag_name','number', 'date', 'time', 'checkbox'], ['#', 'Tag Name', 'Number', 'Date', 'Time', 'checkbox']);
    obj.createTable(obj.convertDictData(), obj.list_of_keys, obj.list_of_names);
    // when new table is created initiate rePlotFunction
    rePlotHandler()
}

// when roll menu changes state EventListener starts chooseDataSet
document.getElementById('select--input').addEventListener("change", chooseDataSet);
