# Project 2 - Flack

This is a web app imitating the behavior of Slack using Javascript, Flask (hence the name, Flack), and SocketIO.

## Features
### Username
Username is currently changable without password (passwords outside scope of current project). Browser uses local storage to remember the last username.

### Public Channels
Users can send messages on public channels. Using SocketIO, messages are updated in realtime without browser refresh.

### Private Messaging
Users can also send messages to a specific user. Once a private message is sent, the receiver's private channels list will show the sender's name if the receiver hasn't received any messages from the sender before. Private messages are also updated without browser refresh.

## Files

### templates/index.html
Main webpage HTML and Javascript code

### application.py
This is where server code is written.

### static/index.js
Currently an empty file, as it is unclear how Python/Flask global variables can be passed into a separate JS file.

### requirements.txt
Required pip packages to install for deployment.

### use-case-testing-xlsx
An initial attempt to organize how to test the application.