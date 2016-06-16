from flask import Flask, Response, send_file
import subprocess
import time

app = Flask("__main__", static_folder='')

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/render')
def render():
    txt = lerArquivo("main.py")
    txtTam = 0
    for a in open("main.py", 'r').readlines():
        txtTam+=1
    txtTam = str(txtTam*18+25)
    return """<script type="text/javascript">
                  window.onload = function(){
                      var el = document.getElementsByTagName("textarea")[0];
                      var text = el.innerHTML;
                      var tam = (""" + txtTam + """) + 'px';
                     parent.document.getElementById("render").style.height = tam;
                 }
                </script>
                <textarea style='width:100%; height:100%; border:0;' readonly>""" + txt + "</textarea>"

@app.route('/jquery.js')
def jquery():
    return send_file('jquery.js')

@app.route('/baixar/main.py')
def baixar():
    return send_file('main.py')

@app.route('/grafico')
def grafico():
    return lerArquivo("Grafico.json")

@app.route('/executar')
def executar():
    cmd=r"python main.py teste.svg teste2.svg"
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    output = ""
    for a in out.splitlines():
        output += str(a).replace("b", "").replace("''", "<br>").replace("\"", "").replace("\\xf3", "ó").replace("\\xe9", "é").replace("\\xa", "º")
    return '<div style="color:#FFFFFF; font-style:italic;">' + output + '</div>'

def lerArquivo(arq):
    f = open(arq, 'r')
    arq = f.read()
    return arq

app.run(host='0.0.0.0', port=80)
