import os
import requests

from flask import Flask, session, render_template
from flask_socketio import SocketIO, emit
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app, manage_session=False)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


channels = {};
# channels = {'main': [{'user': 'Josh', 'message': 'hi', 'timestamp':'YYYY-MM-DDTHH:mm:ss.sssZ'}]};

privateChannels = {};
# privateChannels = {'Charlie-Zoey': [{'user': 'Charlie', 'message': 'hi', 'timestamp':'YYYY-MM-DDTHH:mm:ss.sssZ', 'channel':'Zoey'}]};



def separate(privateChannel):
	#this separates out the two usernames in the private channel
	#it assumes however, that the usernames themselves do not have dashes
	#so Joseph Gordon-Levitt cannot be a username...yet
	#sorry JGL
	newName=0;
	names=['',''];
	for c in str(privateChannel):
		if(c != '-'):
			names[newName] = names[newName]+c;
		else:
			newName=1;
	return names;

def findPrivateChannels ():
	global privateChannels
	userPrivateChannels = {};
	if(session['username'] != ''):
		#only send private channels for the current session's user
		for key in privateChannels.keys():
			if (session['username'] in key):
				usernames = separate(key);
				if (session['username'] == usernames[0] or session['username'] == usernames[1]):
					userPrivateChannels[key] = privateChannels[key];
	
	return userPrivateChannels;



@app.route("/")
def index():
	if not('username' in session):
		session['username'] = '';
	userPrivateChannels = findPrivateChannels();
	return render_template("index.html", channels = channels, privatechannels= userPrivateChannels)

@socketio.on("update display name")
def sessionUser(displayName):
	#change session username
	session['username'] = str(displayName);
	print(session['username'])

@socketio.on("create channel")
def newchannel(channelName):
	global channels
	channels[str(channelName)] = [];
	emit("channel created", channelName, broadcast=True)

@socketio.on("add message")
def addmessage(messagePackage):
	global channels

	currentChannel = messagePackage['channel'];
	channels[currentChannel]=channels[currentChannel]+[{'user': messagePackage['user'], 'message': messagePackage['message'], 'timestamp':messagePackage['timestamp']}];

	if (len(channels[currentChannel])>100):
		channels[currentChannel].pop(0);
	emit("message added", messagePackage, broadcast=True);

@socketio.on("create private channel")
def newPrivateChannel(channelName):

	privateChannels[(f"{session['username']}-{channelName}")] = [];


@socketio.on("add private message")
def addPrivateMessage(privateMessagePackage):
	global privateChannels

	#create a key with 'User1-User2' and 'User2-User1'
	key1 = (f"{session['username']}-{privateMessagePackage['channel']}");
	key2 = (f"{privateMessagePackage['channel']}-{session['username']}");
	if(key1 in privateChannels or key2 in privateChannels):
		#determine currentChannel in privateChannels
		if key1 in privateChannels:
			currentChannel = key1;
		elif key2 in privateChannels:
			currentChannel = key2;
		#add message to existing channel
		privateChannels[currentChannel]=privateChannels[currentChannel]+[privateMessagePackage];
		if (len(privateChannels[currentChannel])>100):
			privateChannels[currentChannel].pop(0);
		emit("private message added", privateMessagePackage, broadcast=True);
	

	
if __name__ == '__main__':
    app.run(debug=True)