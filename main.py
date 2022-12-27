import os
import subprocess
import random
from flask import *

app = Flask(__name__,static_folder="./static")

#コマンドのidとその時に実行する関数を紐づける
#$(spl%)はメタ文字
#[コマンドid]$(spl%)[その時に実行する機能など]$(cmd%)その機能の中で実行する機能
#例
#cmd1$(spl%)os_cmd$(cmd%)start chrome

#id&コマンドは改行で区切られる

id_list_path = "./id_list.csv"

#id_list.csvがなかったら作成
if os.path.isfile(id_list_path) == False:
    f = open(id_list_path,"w")
    f.write("")
    f.close()
    pass


@app.route("/")
def main():
    return "test"


#コマンド登録ページ(仮) http://localhost:5000/static/reg.html

#コマンドを登録(post)
@app.route("/reg/post/", methods=["GET", "POST"])
def make_command():
    cmd_id = str(request.form["id"]) #command id
    cmd_func = str(request.form["func"]) #function
    
    this_id = add_id(cmd_id,cmd_func) #ファイルに追加
    return this_id


#コマンド実行についてのメタ文字
# ^^param_name^^ urlのクエリparam_nameを取得してそこに入れる
#例
#cmd1$(spl%)os_cmd$(cmd%)start ^^p1^^

#/run/cmd1?p1=explorer にアクセスした場合

#os_cmd$(cmd%)start ^^p1^^        から
#os_cmd$(cmd%)start explorer      に変換

#start explorer　が実行される


#コマンド実行
@app.route("/run/<cmd_id>",methods=["GET"])
def run_command(cmd_id):
    f = open(id_list_path,"r")
    list_line = f.readlines() #一行ずつ読む
    f.close()

    ret_msg = ""

    for i in list_line:
        if cmd_id == i.split("$(spl%)")[0]:
            #cmd_idと関連付けされた機能が見つかったら
            

            #関連付けされた機能を実行
            ret_msg = run_function(i.split("$(spl%)")[1],request.args)
            break;
            pass
        pass
    
    return ret_msg


#csvファイルにidと機能の関連付けを追加
#idが重複しているときはやめる return "filename_error"
#idに何も入力されていない場合はランダム
def add_id(cmd_id,cmd_func):
    global id_list_path

    #空白の場合はランダムにidを作成
    if cmd_id == "":
        ab_list = [chr(ord("A")+i) for i in range(26)] #A~Zが並べられたリストを作成

        #10文字のidをA~Zでランダムに作成
        for i in range(10):
            cmd_id += ab_list[random.randint(0,25)]
            pass
        pass
    
    #重複していたらやめる
    f = open(id_list_path,"r")
    list_line = f.readlines() #一行ずつ読む
    f.close()

    ret_msg = ""

    for i in list_line:
        if cmd_id == i.split("$(spl%)")[0]:
            return "filename_error" #ファイル名が重複した場合filename_errorを返す
            break;
            pass
        pass
    
    #追加
    f = open(id_list_path,"a")
    f.write("{0}$(spl%){1}\n".format(cmd_id,cmd_func))
    f.close()

    this_id = "{0}".format(cmd_id)
    
    return this_id #idを返す

#機能を実行
#funcはコマンド, paramはコマンド実行についてのメタ文字を参照

#$(cmd%)でそれぞれを区切る
#command_name$(cmd%)contents$(cmd%)param1$(cmd%)param2
#例
#os_cmd$(cmd%)python main.py
def run_function(func,param):
    print(func)
    print("succeed!")

    #^^param^^　のメタ文字をクエリから取得した文字に変換
    #param.get("クエリの名前","")
    func_meta = func.split("^^")
    func = ""

    print(param)

    for i in range(len(func_meta)):
        if i % 2 == 1: #奇数ならメタ文字
            print(func_meta[i])
            func += param.get(func_meta[i],"")
            pass
        else:
            func += func_meta[i]
        pass
    
    #コマンドを実行する処理

    func_list = func.split("$(cmd%)")

    #コマンド名を判断し、実行
    
    if func_list[0] == "os_cmd": #osコマンド(cmd bashなど)
        subprocess.run(func_list[1],shell=True)
        pass

    ##############
    
    return "function: "+func+" succeed!"

app.run(port=5000)
