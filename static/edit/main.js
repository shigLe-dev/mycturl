
window.onload = function(){
    var query_list = getUrlQueries()

    document.getElementById("id").value = query_list["id"]

    //valueが取得したfunctionと同じfunc_boxを選択
    var func_sel = document.getElementById("func_box")

    var opt = func_sel.getElementsByTagName("option")
    for(var i = 0;i < opt.length;i++){
      if(opt[i].value.includes(query_list["func"])){
        opt[i].selected = true;
      }  
    }


    document.getElementById("cmd").value = query_list["cmd"].replaceAll("$(n%)","\n") //$(n%)と\nを変換
}


//urlクエリを取得
function getUrlQueries() {
    var queryStr = window.location.search.slice(1);  // 文頭?を除外
        queries = {};
  
    // クエリがない場合は空のオブジェクトを返す
    if (!queryStr) {
      return queries;
    }
  
    // クエリ文字列を & で分割して処理
    queryStr.split('&').forEach(function(queryStr) {
      // = で分割してkey,valueをオブジェクトに格納
      var queryArr = queryStr.split('=');
      queries[queryArr[0]] = decodeURI(queryArr[1]);
    });
  
    return queries;
  }