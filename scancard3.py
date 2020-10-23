#!/usr/bin/env python3
from pirc522 import RFID

"""
This script works really well and integrates the use of GPIO buttons. 
The problem with the other scripts is that the RFID reader pauses the script until a scan is done.
This new script uses a different library that allows the script to proceed without waiting for an RFID to be scanned.

sudo pip install pi-rc522
https://github.com/ondryaso/pi-rc522/blob/master/README.md
"""




def scan_card(rdr):
	# this code is complex and handles the rfid tag scanning.
	(error, tag_type) = rdr.request()

	if not error:

		(error, uid) = rdr.anticoll()
		if not error:

			idno = uid_to_num(uid)

			# Select Tag is required before Auth
			if not rdr.select_tag(uid):
				# Auth for block 10 (block 2 of sector 2) using default shipping key A
				if not rdr.card_auth(rdr.auth_a, 10, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
				# This will print something like (False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
					data = []    
					text_read = ''      

					block8 = rdr.read(8)[1]
					block9 = rdr.read(9)[1]
					block10 = rdr.read(10)[1]

					#print("Reading block 8: " + str(block8))
					if block8:

						data += block8

					if block9:

						data += block9

					if block10:

						data += block10

					#print("DATA: " + str(data))

					if data:
						text_read = ''.join(chr(i) for i in data)
						
					# Always stop crypto1 when done working
					rdr.stop_crypto()

					return True, idno, text_read

	else:

		return False, 50, None

def uid_to_num(uid):
	n = 0
	for i in range(0, 5):
		n = n * 256 + uid[i]
	return n


