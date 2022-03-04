class ConvertDict {
  /** class made to convert JSON into data suitable for table
  in this scenario first dict(object) is converted into the **/
  constructor(data, list_of_keys, list_of_names) {
      console.log("ConvertDict constructor");
      this.dict_data = data;
      this.dict_data["dictionary_tags"] = this._sortDictionary(this.dict_data["dictionary_tags"]) // conversion of internal dictionary into ordered by value list of lists
      this.list_of_keys = list_of_keys; // links values in table with keys ['order', 'tag_name', 'date', 'time'];
      this.list_of_names = list_of_names; // names visible to the user ['#', 'Tag Name', 'Number', 'Date', 'Time'];
  }

  _sortDictionary(dictionary){
    //take dictionary return sorted list of lists
    let items = Object.keys(dictionary).map(function(key) {
      return [key, dictionary[key]];
    });
    // Sort the array based on the second element
    items.sort(function(first, second) {
        return second[1] - first[1];
    });
    return items
  }


  convertDictData() {
    console.log("convertDictData: beggining of the function")
    /** creates list of dictionaries (objects)
    data we have
       "tag_date": "2021-09-22",
       "tag_time": "01:31:28.991909",
       "dictionary_tags": {
                           "#bitcoin": 45,
                           "#epro": 1,
                           "#mxs": 1
                           }

    data we need
      {order: 1, tag_name: '#btc', number: 5, date: '01-10-06', time: '11.11'},
      {order: 2, tag_name: '#eth', number: 2, date: '01-10-06', time: '12.12'},
      {order: 3, tag_name: '#dogecoin', number: 6, date: '01-10-06', time: '13.13'}
    **/

    let new_list = []
    let tag_date = this.dict_data["tag_date"]
    let tag_time = this.dict_data["tag_time"]
    let dictionary_tags = this.dict_data["dictionary_tags"]
    let checkbox = this.dict_data["checkbox"]

    dictionary_tags.forEach(function ([key, value], idx) {
      // console.log("order", idx, "tag_name", key, "number", value, "date", tag_date, "time", tag_time);
      let new_dict = {};
      new_dict["order"] = idx + 1;
      new_dict["tag_name"] = key;
      new_dict["number"] = value;
      new_dict["date"] = tag_date;
      new_dict["time"] = tag_time;
      new_dict["checkbox"] = 1;
      new_list.push(new_dict);
    });

    // console.log(new_list)

    return new_list
  }

};


class MakeTable extends ConvertDict{
    /** Class creates table with checkboxes **/
    constructor(data, list_of_keys, list_of_names){
        super(data, list_of_keys, list_of_names)
        console.log("MakeTable contructor");
    };

    createTable(objectArray, fields, fieldTitles) {
        const that = this;

        let body = document.getElementById("table--of--tags"); // element where to put in is chosen
        // document.getElementsByTagName('body')[0];
        let tbl = document.createElement('table'); // whole table is done
        tbl.className = "table table-striped table-sm";
        let thead = document.createElement('thead'); // groups head title in a table
        let thr = document.createElement('tr'); // row is created

        // rows of titles
        fieldTitles.forEach((fieldTitle) => {
            let th = document.createElement('th'); // th defines one header cell in a table
            th.scope = "col";
            if(fieldTitle === "checkbox") { // here we check whether there is a key "checkbox" in dictionary if yes - creates one"
                let chk = th.appendChild(document.createElement('input'));
                // chk.setAttribute('onclick', "MakeTable.prototype.toggle(this)");
                // chk.onclick = function () {that.toggle(this);};
                chk.type = 'checkbox';
                chk.id = "checkbox--master";
                chk.value = "toggle";
                chk.checked = true;
            } else {
                th.appendChild(document.createTextNode(fieldTitle));
                }
            thr.appendChild(th);
            });
        thead.appendChild(thr);
        tbl.appendChild(thead);

        // rest of the table is created
        let tbdy = document.createElement('tbody');
        let tr = document.createElement('tr');
        let idx = 0;
        objectArray.forEach((object) => { // loop over list of dictionaries
            let tr = document.createElement('tr');
            // one full row of data
            fields.forEach((field) => { // loop over one dictionary
                var td = document.createElement('td');
                if(field === "checkbox"){ // here we check whether there is a key "checkbox" in dictionary if yes - creates one"
                    const chk = td.appendChild(document.createElement('input'));
                    tr.appendChild(td);
                    chk.type = 'checkbox';
                    chk.id = "data--to--plot--checkbox";
                    chk.value = object["tag_name"];
                    if(idx < 10) { // created to look nice only first 10 is checked and printed
                        idx += 1;
                        chk.checked = true;
                        console.log("chk.checked = true;")
                    }
                    else{
                        chk.checked = false;
                        console.log("chk.checked = false;")
                    }
                } else {
                    td.appendChild(document.createTextNode(object[field]));
                    tr.appendChild(td);
                    }

            });
            tbdy.appendChild(tr);
            });
        tbl.appendChild(tbdy);
        body.appendChild(tbl)
        console.log("before return", this.dict_data)
        return tbl;
}
};

function toggle() {
    /**
    set checked/unchecked all checkboxes below in table
    first checkbox in the table controls checkboxes in this function
    * */
    let checkboxes = document.querySelectorAll("#data--to--plot--checkbox");
    for (let i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i] !== this.checked)
          checkboxes[i].checked = this.checked;
    }

};

function collectCheckboxes() {
    /**
    function checks status of the all checkboxes
    returns list of tags?
    * */

    let tags_to_plot = []
    console.log("rePlot works");
    let checkboxes = document.querySelectorAll("#data--to--plot--checkbox");
    console.log("checkboxes", checkboxes);
    for (let i = 0; i < checkboxes.length; i++) {
      // if (checkboxes[i] != source)
      if (checkboxes[i].checked) {
        // checkboxes[i].checked = source.checked;
        console.log("i", i);
        console.log(checkboxes[i].value);
        tags_to_plot.push(checkboxes[i].value);
      }
    }
    return tags_to_plot;
  }

function rePlotHandler() {
    /**
    when graphs is supposed to change, the function takes
    variable of the graph and change its parameters then update canvas
    * */
    console.log("rePlot is working")
    // let data = JSON.parse(dataStorage.getItem("data"));
    let data = null;
    try {
      // Parse a JSON
      data = JSON.parse(dataStorage.getItem("data"));
      } catch (e) {
      // You can read e for more info
      data = dataStorage.getItem("data");
      }

    data = data[currentDataset] // change it later
    console.log("data", data)
    let tags_to_plot = collectCheckboxes();
    console.log('data["dictionary_tags"][tag_name]', data["dictionary_tags"]["#bitcoin"])
    let temp_dict = {};
    tags_to_plot.forEach((tag_name) => {
        console.log(tag_name);
      console.log('dict_data["dictionary_tags"]', data["dictionary_tags"][tag_name]);
      temp_dict[tag_name] = data["dictionary_tags"][tag_name];
    })
    data["dictionary_tags"] = temp_dict;
      console.log("temp_dict ",temp_dict);

    console.log(data)

    //title of dataset
    let date_time = moment(data.tag_date + " " + data.tag_time)
    // console.log("createInputOption", date_time.format("Do, MM, YYYY, h:mm"))
    date_time = date_time.format("Do, MM, YYYY, h:mm");

    // config graph
    tagsChart.data.datasets[0].label = date_time
    tagsChart.data.datasets[0].data = Object.values(data["dictionary_tags"])
    tagsChart.data.labels = Object.keys(data["dictionary_tags"])
    tagsChart.update()

};

 document.addEventListener('click',function (e){
     /** if master checkbox changes its state the function change state of the rest **/
    let master_checkbox = document.getElementById('checkbox--master')
    if(e.target && e.target.id === 'checkbox--master'){
        let checkboxes = document.querySelectorAll("#data--to--plot--checkbox");
        for (let i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i] !== master_checkbox.checked)
                checkboxes[i].checked = master_checkbox.checked;
        }

     }
 });

window.onload=function(){
    /** when whole document is loaded then the addEventListener to the button is created **/
    document.getElementById('button--rePlot').addEventListener("click", rePlotHandler);

}


// let data = JSON.parse(dataStorage.getItem("data"))
// console.log("in table_of_tags", data)