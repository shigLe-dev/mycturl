import os
import subprocess
import random
from flask import *

app = Flask(__name__,static_folder="./static")

#コマンドのidとその時に実行する関数を紐づける
#$(spl%)はメタ文字
#[コマンドid]$(spl%)[その時に実行する機能など]$(cmd%)その機能の中で実行する機能
#command_id$(spl%)function(cmd%)content/command
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
    return redirect("/static/main/index.html")

#id_list.csvを返す
@app.route("/id_list")
def id_list_csv():
    f = open("./id_list.csv","r")
    f_content = str(f.read())
    f.close()
    response = make_response(f_content)
    response.headers["Content-Type"] = "text/plain"
    return response


#コマンド登録ページ(仮) http://localhost:5000/static/register/index.html
#メインページ          http://localhost:5000/static/main/index.html

#コマンドを登録(post)
@app.route("/reg/post/", methods=["GET", "POST"])
def make_command():
    cmd_id = str(request.form["id"]) #command id
    cmd_func = str(request.form["func"]) #function
    cmd_content = str(request.form["cmd"]).replace("\n","$(n%)").replace("\r","") #command #改行を$(n%)に変換
    
    this_id = add_id(cmd_id,cmd_func+"$(cmd%)"+cmd_content) #ファイルに追加
    return redirect("/static/main/index.html")

#コマンドを編集(post)
#そのコマンドを一旦削除→
#新規作成を行う
@app.route("/edit/post/", methods=["GET", "POST"])
def edit_command():
    cmd_id = str(request.form["id"]) #command id
    cmd_func = str(request.form["func"]) #function
    cmd_content = str(request.form["cmd"]).replace("\n","$(n%)").replace("\r","") #command

    del_id(cmd_id)
    
    this_id = add_id(cmd_id,cmd_func+"$(cmd%)"+cmd_content) #ファイルに追加
    return redirect("/static/main/index.html")

#コマンドを消す
@app.route("/del/post/<cmd_id>")
def delete_command(cmd_id):
    del_id(cmd_id)
    return "succeed!"



#コマンド実行についてのメタ文字
# ^^param_name^^ urlのクエリparam_nameを取得してそこに入れる
#例
#cmd1$(spl%)os_cmd$(cmd%)start ^^p1^^

#/run/cmd1?p1=explorer にアクセスした場合

#os_cmd$(cmd%)start ^^p1^^        から
#os_cmd$(cmd%)start explorer      に変換

#start explorer　が実行される


#/run/[command_id]
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


#commandを消す
#消したいcommand id
def del_id(cmd_id):
    global id_list_path
    
    #重複していたら削除
    f = open(id_list_path,"r")
    list_line = f.readlines() #一行ずつ読む
    f.close()

    for i in range(len(list_line)):
        if cmd_id == list_line[i].split("$(spl%)")[0]:
            list_line.pop(i)
            break;
            pass
        pass

    write_file = ""

    for i in list_line:
        write_file += i+"\n"
        pass

    
    f = open(id_list_path,"w")
    f.write(write_file)
    f.close()
    
    pass

#csvファイルにidと機能の関連付けを追加
#idが重複しているときはやめる return "filename_error"
#idに何も入力されていない場合はランダム
def add_id(cmd_id,cmd_func):
    global id_list_path

    #空白の場合はランダムにidを作成
    if cmd_id == "":
        ab_list = [chr(ord("A")+i) for i in range(26)] #A~Zが並べられたリストを作成
        for i in range(26):
            ab_list.append(chr(ord("a")+1))
            pass
        

        #20文字のidをA~Zでランダムに作成
        for i in range(20):
            cmd_id += ab_list[random.randint(0,54)]
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

    return_text = ""

    #コマンド名を判断し、実行
    
    if func_list[0].find("os_cmd") != -1: #osコマンド(cmd bashなど)
        run_text = func_list[1].split("$(n%)") #改行で区切って実行
        for run_cmd in run_text: #一行ずつコマンド実行
            return_text = subprocess.run(run_cmd,shell=True,check=True,stdout=subprocess.PIPE).stdout.decode('utf-8')
            pass
        pass
    elif func_list[0].find("open") != -1: #open application
        subprocess.Popen(["start", func_list[1]], shell=True)
        pass
    
    elif func_list[0].find("write_file") != -1:#write file
        run_text = func_list[1].split("$(n%)") #$(n%)　は改行なので区切る

        file_text = ""
        
        for i in range(len(run_text)-1): #2行目以降はファイルの内容
            file_text += run_text[i+1]+"\n"
            pass
        
        f = open(run_text[0],"w") #1行目はfile path
        f.write(file_text)
        f.close()
        pass

    ##############

    print("function: "+func+" succeed!")

    response = make_response(return_text)
    response.headers["Content-Type"] = "text/plain"
    
    return response

app.run(port=5000)
