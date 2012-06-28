MakerBarManager
===============

This is a Django app that handles several functional or really cool applications for the Hoboken MakerBar.

presence app:
Currently its an integration of bertHartm's presence detection(https://github.com/MakerBar/Presence-Detector) which SSH's into your router and pulls MAC addresses.
I've pulled the MAC->name resolution out of the pickle and integrated it into a MySQL database.

How to use:

Assuming you're not going to be checking our router, you'll need to replace the ssh host fingerprint and hostname in presence.py.
You'll need an ssh key to connect (I highly recommend restricting it to command="wl assoclist" in your authorized_keys file), or add a password parameter to the .connect() function (not recommended).

The settings.py file contains the hostname, port and ssh key for the router. 

NOTE:
if no users are found, the server returns HTTP code 204 (No Content). This often leaves browsers confused, but is great from an API perspective.

SupplyRequest app:
Preliminary checkin not functional.

