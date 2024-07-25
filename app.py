from flask import Flask, Response
import os, requests, time, datetime

app = Flask(__name__)

TARGET = os.environ.get('TARGET', 'Konnichiwa')
PORT = os.environ.get('PORT', 80)
NEXT = os.environ.get('NEXT', "")
PODNAME = os.environ.get('PODNAME', "")
NODENAME = os.environ.get('NODENAME', "")



@app.route("/")
def index():
    if PODNAME or NODENAME:
        response = Response(f"{TARGET} from {PODNAME} in {NODENAME}\n")
    else:
        response = Response(f"{TARGET}\n")
    response.headers["app"] = "shuka"
    return response



@app.route("/sleep/<sleepTime>")
def sleep(sleepTime):
    startTime = datetime.datetime.now()
    time.sleep(int(sleepTime)/1000)
    endTime = datetime.datetime.now()
    return f"Shuka wa {(endTime - startTime).total_seconds()} byougo ni mezameta"



@app.route("/hometag/<tag>")
def home_tag(tag):
    response = Response(f"{TARGET}\n")
    response.headers["tag"] = tag
    response.headers["app"] = "shuka"
    return response



@app.route("/chain/<tag>")
def chain_tag(tag):
    if NEXT:
        next = NEXT
        data = requests.get(f"http://{next}/chain/{tag}", headers={"app": "shuka", "tag": tag}).content
    else:
        next = f"127.0.0.1:{PORT}"
        data = requests.get(f"http://{next}/hometag/{tag}", headers={"app": "shuka", "tag": tag}).content
    response = Response(data)
    response.headers["tag"] = tag
    response.headers["app"] = "shuka"
    return response

@app.route("/chain")
def chain():
    if NEXT:
        next = NEXT
        data = requests.get(f"http://{next}/chain", headers={"app": "shuka"}).content
    else:
        next = f"127.0.0.1:{PORT}"
        data = requests.get(f"http://{next}/", headers={"app": "shuka"}).content
    response = Response(data)
    response.headers["app"] = "shuka"
    return response



if __name__ == "__main__":
    print(PORT)
    app.run(debug=True,host='127.0.0.1',port=int(PORT))
    