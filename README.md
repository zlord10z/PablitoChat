# PablitoChat
!!!WARNING!!! 
I'm still working on crypthography, but the version on Git sends MSGs UNENCRYPTED, so any sniffer in your LAN can EASILY EAVESDROPS YOR CONVERSATION!

Instant messaging python app. With this app you can create your own chat room or join to room created by somebody else.
App is working only in LAN, but you can still use hamachi or some other VPN app. 

Names Server, Host and Room as well as Client and Guest will be used synonymously.
This app use client-server architecture. With this app its possible to either create room (server role and this server client role simultaneously) or join other room (client role)
App is using two ports: 50008 (for multicast) and 50007. Multicast is used to broadcast ip and server name to other clients in same LAN. It's allows to display Room in "availble servers (LAN)" window in clients app.

To do:
-RSA and AES crypto
-language text files which could be easily translated by anyone to other language (and build-in english translation)
-pictures sending
-standalone server






