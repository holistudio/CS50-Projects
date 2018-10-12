function privateChannelExists(user1, user2){
    //determine if a private channel already exists between the two users, user1 and user2
    var key1 = `${user1}-${user2}`;
    var key2 = `${user2}-${user1}`;
    return (privateChannels.hasOwnProperty(key1) || privateChannels.hasOwnProperty(key2));
}

function listChannels(channels){
    //clear display list of public channels
    document.querySelector('#channel-list').innerHTML='';

    //list public channels
    for (channel in channels) {
        const label = document.createElement('a');
        label.id=`${channel}`;
        label.classList.add("channel");
        label.innerHTML=`${channel}`;
        label.href="";
        const item = document.createElement('dd');
        item.appendChild(label);
        document.querySelector('#channel-list').append(item);
    }
}

function listPrivateChannels(privateChannels){
    //clear display list of private channels
    document.querySelector('#private-channel-list').innerHTML='';

    //list private channels
    for (channel in privateChannels) {
        // extract out the 'non-user' string in channel keys
        const username = localStorage.getItem('username');
        channel= channel.replace(`${username}`, "").replace("-","");

        //create channel list on webpage
        const label = document.createElement('a');
        label.id=`${channel}`;
        label.classList.add("channel"); 
        label.innerHTML=`${channel}`;
        label.href="";
        const item = document.createElement('dd');
        item.appendChild(label);
        document.querySelector('#private-channel-list').append(item);
    }

}

//add one message to the display given a message JSON object
function addMessageToDisplay(messagePackage){
    const user = document.createElement('dt');
    const message = document.createElement('dd');
    const timestamp = document.createElement('span');
    user.innerHTML = `${messagePackage.user}`;
    message.innerHTML = `${messagePackage.message}`;
    timestamp.innerHTML = ` ${messagePackage.timestamp}`;
    timestamp.setAttribute("class", "text-muted");
    timestamp.style.fontWeight= "normal";
    user.appendChild(timestamp);
    document.querySelector("#messages-list").append(user);
    document.querySelector("#messages-list").append(message);
    return false;
}

function displayMessages(){
    //display for current channel
    let currentChannel = localStorage.getItem('current-channel');

    //clear message display
    document.querySelector('#messages-list').innerHTML='';
    if(currentChannel!=""){
        //determine channel is public or private channel

        //if current channel is a public channel
        if(channels.hasOwnProperty(currentChannel)){
            var channelCategory=channels;
        }
        else{
            //otherwise it's a private channel
            var channelCategory=privateChannels;

            //try the two different combinations of User1-User2 keys
            //set currentChannel to the correct combination
            const username = localStorage.getItem('username');
            if(privateChannels.hasOwnProperty(`${username}-${currentChannel}`)){
                currentChannel=`${username}-${currentChannel}`;
            }
            else if (privateChannels.hasOwnProperty(`${currentChannel}-${username}`)){
                currentChannel=`${currentChannel}-${username}`;
            }
            else{
                //error
            }
        }

        //display messages of that channel
        for (var i = 0; i < channelCategory[currentChannel].length; i++) {
            addMessageToDisplay(channelCategory[currentChannel][i]);
        }
    }
    
}

document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    //display last username entered
    document.querySelector('#username').innerHTML = localStorage.getItem('username');

    //hide alerts
    document.querySelectorAll('.alert').forEach(div => {
        div.hidden = true;
    });

    //display message input only if username and channel are select
    if(localStorage.getItem('username')=="" || localStorage.getItem('current-channel')==""){
        document.querySelector('#message').hidden = true;
    }
    else{
        document.querySelector('#message').hidden = false;
    }
    
    //list public channels
    listChannels(channels);

    //list private channels
    listPrivateChannels(privateChannels);

    //establish channel click behavior
    document.querySelectorAll('.channel').forEach(channel => {
        channel.onclick = () => {
            localStorage.setItem('current-channel', channel.innerHTML);
        };
    });
    
    //highlight current channel
    if(localStorage.getItem('current-channel')!=""){
        document.getElementById(`${localStorage.getItem('current-channel')}`).classList.add("bg-primary","text-white");
    }

    //display current channel's messages, public or private
    displayMessages();

    //display appropriate display name inputs depending one whether a user is logged in or not
    if (localStorage.getItem('username') != ""){
        //if username is not blank
        //display button for "logging out"
        document.querySelector('#logout').hidden = false;
        //hide the new display name form
        document.querySelector('#new-name').hidden = true;
    }
    else{
        //if username is blank
        //display form for changing display name
        document.querySelector('#new-name').hidden = false;
        //hide button for "logging out"
        document.querySelector('#logout').hidden = true;
        //hide private channel forms, because you can't send private messages with a blank username
        document.querySelector('#new-private-channel').hidden = true;
    }

    socket.on('connect', () => {

        //determine if it's the user's browser's first time since server is up and running
        //to update local storage username to server variable
        if(localStorage.getItem('first-entry')==0){
            socket.emit('update display name', localStorage.getItem('username'));
            localStorage.setItem('first-entry', 1);
        }

        //on "log out" set username to blank
        document.querySelector('#logout').onsubmit = () => {
            localStorage.setItem('username', "");
            socket.emit('update display name', "");
        }

        //change display name when it's submitted
        document.querySelector('#new-name').onsubmit = () => {
            //make sure it's not a public channel name
            if(!(channels.hasOwnProperty(document.querySelector("#username-input").value))){
                //store display name into local storage
                localStorage.setItem('username', document.querySelector("#username-input").value);

                socket.emit('update display name',document.querySelector("#username-input").value);

                //if on private channel, clear messages and reset current channel
                if (!(channels.hasOwnProperty(localStorage.getItem('current-channel')))){
                    document.querySelector('#messages-list').innerHTML='';
                    localStorage.setItem('current-channel',"");
                    //privateChannels list should update after page refresh
                }
                //clear inputs
                document.querySelector("#username-input").value='';
            }
            else{
                //flash username can't be a channel name
                document.querySelector("#invalid-username").innerHTML="Username can't be a public channel name";
                document.querySelector("#invalid-username").hidden=false;
                //prevent page refresh
                return false;
            }

            //if display name change sucessful refresh page
        }

        //button for create a new public channel
        document.querySelector('#new-channel').onsubmit = () => {
            //check if public channel already exists:
            if(channels.hasOwnProperty(document.querySelector("#channel-input").value)){
                //flash public channel already exists
                document.querySelector("#invalid-public-channel").innerHTML="Public channel already exists";
                document.querySelector("#invalid-public-channel").hidden=false;
                document.querySelector("#channel-input").value='';
            }
            else{
                socket.emit('create channel', document.querySelector("#channel-input").value);
            }
            
            //clear inputs
            document.querySelector("#channel-input").value='';

            //prevent page refresh
            return false;
        }

        //send message to public/private channel
        document.querySelector('#message').onsubmit = () => { 
            const currentChannel = localStorage.getItem('current-channel');
            const user = localStorage.getItem('username');
            const message = document.querySelector('#message-input').value;
            const timestamp = new Date().toISOString();

            const messagePackage = {'user': user, 'message': message, 'timestamp':timestamp, 'channel':currentChannel};
            
            //if current channel is a public channel
            if(channels.hasOwnProperty(currentChannel)){
                //add message to the public channel
                socket.emit('add message', messagePackage);
            }
            else{
                //otherwise it's a private channel
                socket.emit('add private message', messagePackage);
                addMessageToDisplay(messagePackage);
            }

            //clear inputs
            document.querySelector('#message-input').value='';
            return false;
        }

        //create a new private channel when submitted
        document.querySelector('#new-private-channel').onsubmit = () => {

            //make sure it's not a public channel name
            if (!channels.hasOwnProperty(document.querySelector("#private-channel-input").value)){
                //make sure it's also not a private channel already on the list
                if (privateChannelExists()){
                    document.querySelector('#invalid-private-channel').innerHTML="Private channel already exists";
                    document.querySelector('#invalid-private-channel').hidden=false;
                    document.querySelector("#channel-input").value='';
                    return false;
                }
                else{
                    //create private channel once all checks are met.
                    socket.emit('create private channel', document.querySelector("#private-channel-input").value);
                    //hide flash message
                    document.querySelector("#invalid-private-channel").innerHTML="";
                    document.querySelector("#invalid-private-channel").hidden=true;
                }
            }
            else{
                //flash private channel can't be a public channel name
                document.querySelector('#invalid-private-channel').innerHTML="Private channel can't be a public channel name";
                document.querySelector('#invalid-private-channel').hidden=false;
                document.querySelector("#channel-input").value='';
                return false;
            }
            //clear inputs
            document.querySelector("#channel-input").value='';

            //page will refresh and updated private channel list will be displayed for the current user
        }
    });

    //send back to server the browser's username when received socket emit from server
    socket.on('check username', () => {
        if(localStorage.getItem('username')!=""){
            console.log('checking username')
            socket.emit('update display name',localStorage.getItem('username'))
        }
        return false;
    });

    //update list of public channels
    socket.on('channel created', channel => {
        const label = document.createElement('a');
        label.id=`${channel}`;
        label.classList.add("channel"); 
        label.innerHTML=`${channel}`;
        label.href="";
        const item = document.createElement('dd');
        item.appendChild(label);
        document.querySelector('#channel-list').append(item);
        //establish channel click behavior
        document.getElementById(`${channel}`).onclick = () => {
            localStorage.setItem('current-channel', channel)
        };

        //hide flash message
        document.querySelector("#invalid-public-channel").innerHTML="";
        document.querySelector("#invalid-public-channel").hidden=true;

        return false;
    });

    //update list of messages on the current public channel, once received emit from server.
    socket.on('message added', messagePackage => {
        if(messagePackage.channel == localStorage.getItem('current-channel')){
            addMessageToDisplay(messagePackage);
        }
        return false;
    });

    //update list of messages on the current private channel, once received emit from server.
    socket.on('private message added', messagePackage => {

        //if message's channel is the same as the username, then a few display elements may need to be updated
        if (localStorage.getItem('username') == messagePackage.channel){

            //check if the message channel doesn't already exist
            if (!(privateChannelExists(messagePackage.user, messagePackage.channel))){

                // if it doesn't, update list of private channels displayed
                const channel = messagePackage.user;
                const label = document.createElement('a');
                label.id=`${channel}`;
                label.classList.add("channel"); 
                label.innerHTML=`${channel}`;
                label.href="";
                const item = document.createElement('dd');
                item.appendChild(label);
                document.querySelector('#private-channel-list').append(item);
                //establish channel click behavior
                document.getElementById(`${channel}`).onclick = () =>{
                    localStorage.setItem('current-channel', channel)
                };
            }

            //if the person is currently viewing that private channel update messages with append
            if(messagePackage.user == localStorage.getItem('current-channel')){
                addMessageToDisplay(messagePackage);
            }
        }
        return false;
    });
});