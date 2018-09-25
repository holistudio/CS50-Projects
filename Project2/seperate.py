def separate(privateChannel):
	#this separates out the two usernames in the private channel
	#it assumes however, that the usernames themselves do not have dashes
	#so Joseph Gordon-Levitt cannot be a username...yet
	#sorry JGL
    newName=0;
    names=['',''];
    for c in str(privateChannel):
        print(c)
        if(c != '-'):
            names[newName] = names[newName]+c;
        else:
            newName=1;
    print(names);
    return names;

separate('Charlie-Zoey');
