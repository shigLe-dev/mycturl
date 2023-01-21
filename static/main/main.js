//CSVファイルを読み込む関数getCSV()の定義
function getCSV(){
    var req = new XMLHttpRequest(); // HTTPでファイルを読み込むためのXMLHttpRrequestオブジェクトを生成
    req.open("get", "/id_list", true); // アクセスするファイルを指定
    req.send(null); // HTTPリクエストの発行
	
    // レスポンスが返ってきたらconvertCSVtoArray()を呼ぶ	
    req.onload = function(){
	convertCSVtoArray(req.responseText); // 渡されるのは読み込んだCSVデータ
    }
}

get_ip(); //ipを取得
getCSV(); //最初に実行される


 
// 読み込んだCSVデータを二次元配列に変換する関数convertCSVtoArray()の定義
function convertCSVtoArray(str){ // 読み込んだCSVデータが文字列として渡される
    var result = []; // 最終的な二次元配列を入れるための配列
    var tmp = str.split("\n"); // 改行を区切り文字として行を要素とした配列を生成
 
    // 各行ごとに$(spl%)で区切った文字列を要素とした二次元配列を生成
    for(var i=0;i<tmp.length;++i){
        result[i] = tmp[i].split("$(spl%)");
    }

    console.log(result)

    result_html = ""

    for(var i = 0;i < result.length;i++){
        if(result[i][1] != undefined){
            console.log(result[i][1])
            //id: result[i][0] func:func_tmp[0] cmd:func_tmp[1]
            var func_tmp = result[i][1].split("$(cmd%)")
            result_html += "<tr>"
            +"<th>"+result[i][0]+"</th>"
            +"<th>http://"+host_ip+":"+location.port+"/run/"+result[i][0]+"</th>" //host_ip: ローカルホストのip
            +"<th>"+func_tmp[0]+"</th>"
            +"<th>"+func_tmp[1]+"</th>"
            +"<th><span onclick='id_del(event)' style='color:#ff0000;'>delete</span></th>"
            +"<th><a href='../edit/index.html?id="+encodeURI(result[i][0])+"&func="+encodeURI(func_tmp[0])+"&cmd="+encodeURI(func_tmp[1])+"' class='edit_button'>edit</a></th>"
            +"</tr>"
        }
    }

    document.getElementById("func_list_box").innerHTML = result_html
}

//削除ボタンが押されたらコマンド削除
function id_del(e){
    id_name = e.target.parentElement.parentElement.getElementsByTagName("th")[0].textContent 

    var req = new XMLHttpRequest(); // HTTPでファイルを読み込むためのXMLHttpRrequestオブジェクトを生成
    req.open("get", "/del/post/"+id_name, true); // アクセスするファイルを指定
    req.send(null); // HTTPリクエストの発行

    e.target.parentElement.parentElement.remove()
}

var host_ip;

function get_ip(){
    /*
    var req = new XMLHttpRequest(); // HTTPでファイルを読み込むためのXMLHttpRrequestオブジェクトを生成
    req.open("get", "/get_ip", true); // アクセスするファイルを指定
    req.send(null); // HTTPリクエストの発行

    req.onload = function(){
	    host_ip = req.responseText
    }*/

    host_ip = location.hostname
}