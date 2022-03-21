function createSemanticIndicator(dataset){ //make new page
    console.log("createSemanticIndicator function")
    let _data_keys = []
    let _data_values = []
    _data_keys =  Object.keys(dataset);
    _data_values = Object.values(dataset);
    console.log("dataset[0]", dataset[0]);
    console.log("dataset[1]", dataset[1]);
    console.log("dataset[-1]", dataset[-1]);
    let mood = 0
    if (dataset[-1] > dataset[1] && dataset[-1] > dataset[0]){
        console.log("Mood is negative")
        mood = -1
    }
    else if (dataset[1] > dataset[0] && dataset[1] > dataset[-1]){
        console.log("Mood is positive")
        mood = 1
    }
    else{
        console.log("Mood is neutral")
        mood = 0
    }
    setSemanticIcon(mood)
}

function setSemanticIcon(mood){

    let select_id = document.getElementById('mood-icon');
    let attr_val = ""
    // select_id.parentNode.removeChild(select_id);
    //
    // select_id = document.getElementById('mood-icon');
    console.log("select_id", select_id)
    if (mood === -1){
        attr_val = "frown";
    }
    else if (mood === 1){
        attr_val = "smile";
    }
    else if (mood === 0){
        attr_val = "meh"
    }
    else
        console.log("setSemanticIcon can't be set")

    select_id.setAttribute("data-feather", attr_val);
    feather.replace()
}