#!/usr/bin/env python
from random import randint
from omxplayer.player import OMXPlayer

from pathlib import Path
import time
import subprocess
import os
import logging
import random
import glob
import RPi.GPIO as GPIO
import scancard3
from pirc522 import RFID


def playmovie(video,directory,player):

	"""plays a video.
	https://python-omxplayer-wrapper.readthedocs.io/en/latest/
	"""

	VIDEO_PATH = Path(directory + video)

	isPlay = isplaying()

	if not isPlay:

		logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + 'playmovie: No videos playing, so play video.')

	else:

		logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+ 'playmovie: Video already playing, so quit current video, then play')
		player.quit()

	try:
		player = OMXPlayer(VIDEO_PATH, 
			dbus_name='org.mpris.MediaPlayer2.omxplayer1')
	except SystemError:
		logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' $Error: Cannot Find Video.')

	except ValueError:
		logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' $Error: Card must be blank.')

	logging.info('playmovie: omxplayer %s' % video)

	time.sleep(2)	#sleeps 2 second after movie starts playing
	logging.info('Post Play Sleep Over')
	return player

def isplaying():

		"""check if omxplayer is running
		if the value returned is a 1 or 0, omxplayer is NOT playing a video
		if the value returned is a 2, omxplayer is playing a video"""

		processname = 'omxplayer'
		tmp = os.popen("ps -Af").read()
		proccount = tmp.count(processname)

		if proccount == 1 or proccount == 0:
			proccount = False
		else:
			proccount = True

		return proccount


def main():

	#program start

	directory = '/home/pi/Videos/'


	logging.basicConfig(level=logging.INFO)


	rdr = RFID()

	logging.info("\n\n\n***** %s Begin Player****\n\n\n" %time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

	current_movie_id = 2
	movie_name = 'none'
	idnum = 2
	playerOB = ""

	gpio_pawpatrol = 13
	gpio_tom = 35
	gpio_coco = 10
	gpio_garbage = 29
	gpio_popeye = 33
	gpio_superman = 26 

	gpio_fastforward = 3
	gpio_rewind = 7
	gpio_pause = 8 
	gpio_quit = 40 


	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(gpio_pawpatrol, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Reset switch
	GPIO.setup(gpio_tom, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Reset switch
	GPIO.setup(gpio_coco, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Reset switch
	GPIO.setup(gpio_garbage, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Reset switch
	GPIO.setup(gpio_popeye, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Reset switch
	GPIO.setup(gpio_superman, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Reset switch

	GPIO.setup(gpio_fastforward, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
	GPIO.setup(gpio_pause, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
	GPIO.setup(gpio_rewind, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
	GPIO.setup(gpio_quit, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 



	try:
		while True: 

			isPlay = isplaying()

			if not isPlay:
				current_movie_id = 2
				idnum = 2

			if (not GPIO.input(gpio_pawpatrol)):
				
				logging.info("PAW PATROL")

				movie_name = 'pawpatrolfolder'
				idnum = 1000

			elif (not GPIO.input(gpio_coco)):
				
				logging.info("COCOMELON")

				movie_name = 'cocomelonfolder'
				idnum = 1001

			elif (not GPIO.input(gpio_tom)):
				
				logging.info("TOM and Jerry")
				movie_name = 'tomandjerryfolder'
				idnum = 1010

			elif (not GPIO.input(gpio_popeye)):
				
				logging.info("POPEYE")
				movie_name = 'popeyefolder'
				idnum = 1011

			elif (not GPIO.input(gpio_garbage)):
				
				logging.info("Garbage Truck Rules!")
				movie_name = 'garbagetruckfolder'
				idnum = 1100


			elif (not GPIO.input(gpio_superman)):
				
				logging.info("This looks like a job for... Superman!")
				movie_name = 'supermanfolder'
				idnum = 1101

			## Controls

			elif (not GPIO.input(gpio_fastforward)):
				
				logging.info(">> Fast Forward")

				try:
					playerOB.seek(30)

				except NameError:

					logging.info("Nothing to forward")

				except IOError:

					logging.info("Nothing to forward anymore")

				except AttributeError:

					logging.info("FF - Attribute Error")


				time.sleep(0.25)

			elif (not GPIO.input(gpio_rewind)):
				
				logging.info("<< Rewind")

				try:
					playerOB.seek(-30)

				except NameError:

					logging.info("Nothing to rewind")

				except IOError:

					logging.info("Nothing to rewind anymore")

				except AttributeError:

					logging.info("RW - Attribute Error")

				time.sleep(0.25)

			elif (not GPIO.input(gpio_pause)):
				
				logging.info("- Pause/ Play -")

				try:
					playerOB.play_pause()

				except NameError:

					logging.info("Nothing is playing yet")

				except IOError:

					logging.info("Nothing is playing right now")

				except AttributeError:

					logging.info("Attribute Error")


				time.sleep(0.25)

			elif (not GPIO.input(gpio_quit)):
				
				logging.info("QUIT!")

				try:
					playerOB.quit()

				except NameError:

					logging.info("Nothing is playing yet")

				except IOError:

					logging.info("Nothing is playing right now")

				except AttributeError:

					logging.info("Attribute Error")


				current_movie_id = 2

				movie_name = 'none'

				idnum = 2

				time.sleep(0.25)

			else:
				logging.debug('..... Waiting')

				try:

					scanned, idnum_temp, text_temp = scancard3.scan_card(rdr)

					if scanned:

						idnum = idnum_temp
						movie_name = text_temp.rstrip()
						logging.debug('Scanned: %s' %movie_name)

				except TypeError:

					logging.warning("SCAN ERROR, Continue")

				time.sleep(0.1)	# checks for button press every 0.1 seconds

			logging.debug("Movie Name: %s" % movie_name)
			logging.debug("current_movie_id: %s" % current_movie_id)
			logging.debug("idnum: %s" % idnum)

			if current_movie_id != idnum:

				logging.info(" - Name: %s" % movie_name)
				#this is a check in place to prevent omxplayer from restarting video if ID is left over the reader.
				#better to use id than movie_name as there can be a problem reading movie_name occasionally

				if movie_name.endswith(('.mp4', '.avi', '.m4v','.mkv')):
					current_movie_id = idnum 	#we set this here instead of above bc it may mess up on first read
					logging.info("PLAYING: omxplayer %s" % movie_name)
			
				elif 'folder' in movie_name:

					movie_directory = movie_name.replace('folder',"") 
					current_movie_id = idnum
				
					try:

						movie_name = random.choice(glob.glob(os.path.join(directory + movie_directory, '*')))
						movie_name = movie_name.replace(directory,"")
					except IndexError:
						movie_name = 'videonotfound.mp4'

				
				logging.info("randomly selected: omxplayer %s" % movie_name)	
				playerOB = playmovie(movie_name,directory,playerOB)
				
			else:

				logging.debug("same movie")



	except KeyboardInterrupt:
		GPIO.cleanup()
		rdr.cleanup()
		print("\nAll Done")


#program start



if __name__ == "__main__":

    main()

