

var query_add = document.getElementById("query_add")

var add_window = document.getElementById("add_window")

query_add.addEventListener("click",function(){
    if(add_window.style.display == "none"){
        add_window.style.display = "block"
    }else{
        add_window.style.display = "none"
    }
})


var add_param = document.getElementById("add_param")


add_param.addEventListener("click",function(){
    var param_text = document.getElementById("param_text")

    var cmd_textarea = document.getElementById("cmd")

    cmd_textarea.value += "^^"+param_text.value+"^^"
})