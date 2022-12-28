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
            var func_tmp = result[i][1].split("$(cmd%)")
            result_html += "<tr>"
            +"<th>"+result[i][0]+"</th>"
            +"<th>http://"+location.host+"/run/"+result[i][0]+"</th>"
            +"<th>"+func_tmp[0]+"</th>"
            +"<th>"+func_tmp[1]+"</th>"
            +"<th><span class='edit_button'>edit</span></th>"
            +"</tr>"
        }
    }

    document.getElementById("func_list_box").innerHTML = result_html
}
 
getCSV(); //最初に実行される