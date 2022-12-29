
window.onload = function(){
    var query_list = getUrlQueries()

    document.getElementById("id").value = query_list["id"]

    document.getElementById("func").value = query_list["func"]

    document.getElementById("cmd").value = query_list["cmd"]
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