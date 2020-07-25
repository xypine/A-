import os
from flask import Flask, redirect
from flask import request
from flask import jsonify
import hashlib

app = Flask(__name__)

c = 0
clients = []
chat = []

version = 5

additive = 0
def getIp():
    return "we'll see about that"
def getUID(ip):
    return hashlib.sha256(str(ip).encode("utf8")).hexdigest()
def addChat(toAdd, limit = True):
    global chat, additive
    if limit:
        additive = additive + 1
    print("new chat: " + toAdd)
    toAdd = toAdd.replace("<script>", "").replace("</script>", "")
    if(additive > 50):
        chat.pop(0)
    chat.append(toAdd)

def addClient(uID):
    if uID not in clients:
        clients.append(uID)
        addChat("--- " + uID + " Joined the Chat ---")
        print("connection from " + str(request.remote_addr))
def removeClient(uID):
    if uID in clients:
        clients.remove(uID)
        addChat("--- " + uID + " Left the Chat ---")
@app.route('/')
def hello():
    global chat, version
    uIp = request.access_route[0]
    uID = getUID(uIp)
    addClient(uID)
    view = "<title>A+</title>"
    global c
    c = c + 1
    view = view + "Connected as: " + uID + " (" + uIp + ")<br \\>"
    view = view + "Refresh the page to access the latest messages."
    view = view + "<br \\>-----------------------------------------------------------------------<br \\>"
    for i in chat:
        view = view + i.replace("<", "").replace(">", "") + "<br \\>"
    view = view + "<br \\>-----------------------------------------------------------------------<br \\>"
    view = view + "note that only the latest 50 messages are stored and displayed. <br \\><br \\>"
    view = view + "<form action=\" " + "/post" + "\" method=\"post\">"
    view = view + "<input type=\"text\" name=\"msg\">"
    view = view + "<input type=\"submit\">"
    view = view + "</form>"
    view = view + "<br \\><hr \\>"
    view = view + "A+ v. " + str(version) + " | <a href=\"https://raw.githubusercontent.com/jonnelafin/A-/master/LICENSE\">LICENSE</a>"
    return(view)
@app.route('/post', methods=['POST'])
def handle_data():
    uIp = request.access_route[0]
    uID = getUID(uIp)
    msg = request.form['msg']
    addChat(uID + ": " + msg)
    return redirect("/", code=302)
@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.access_route[0], 'viewcount' : c}), 200
@app.route("/announce", methods=["GET"])
def announceThem():
    global chat
    uIp = request.access_route[0]
    uID = getUID(uIp)
    addClient(uID)
    return jsonify({'you': uID}), 200
@app.route("/unannounce", methods=["GET"])
def unannounceThem():
    global chat
    uIp = request.access_route[0]
    uID = getUID(uIp)
    removeClient(uID)
    return jsonify({'you': uID}), 200
@app.route("/list", methods=["GET"])
def listAnnounced():
    return jsonify({'clients': clients}), 200
@app.route("/history", methods=["GET"])
def returnHistory():
    return jsonify({'chat-history': chat}), 200
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
