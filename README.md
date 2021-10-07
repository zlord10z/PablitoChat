# PablitoChat
!!!WARNING!!! 
I'm still working on crypthography, but the version on Git sends MSGs UNENCRYPTED, so any sniffer in your LAN can EASILY EAVESDROPS YOR CONVERSATION!

Instant messaging python app. With this app you can create your own chat room or join to room created by somebody else.
App is working only in LAN, but you can still use hamachi or some other VPN app. 
This app have few emoticons (mainly lenny faces) which can be choosen from emoticon window (just click ":-(" button in chat window).
It's possible to send and open URL (you can paste link like example.com or www.example.com). To open URL just click on MSG with it. The page will open on your default browser.

Names Server, Host and Room as well as Client and Guest will be used synonymously.
This app use client-server architecture. With this app its possible to either create room (server role and this server client role simultaneously) or join other room (client role)
App is using two ports: 50008 (for multicast) and 50007. Multicast is used to broadcast an ip address and server name to other clients in same LAN. It's allows to display Room in "availble servers (LAN)" window in clients app. Beside multicast, it's still possible to join room by direct connect (enter room ip address manualy).


To do:
-RSA and AES crypto
-language text files which could be easily translated by anyone (and translate app to english)
-pictures sending
-standalone server






