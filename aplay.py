#!/usr/bin/env python
from random import randint

import time
import subprocess
import os
import logging
import random
import glob
import RPi.GPIO as GPIO


def playmovie(video):

	"""plays a video."""

	global myprocess
	global directory

	isPlay = isplaying()

	if not isPlay:

		logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + 'playmovie: No videos playing, so play video.')

	else:

		logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+ 'playmovie: Video already playing, so quit current video, then play')
		myprocess.communicate(b"q")

	myprocess = subprocess.Popen(['omxplayer',directory + video],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
	
	logging.info('playmovie: omxplayer %s' % video)

	time.sleep(2)	#sleeps 2 second after movie starts playing

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

	logging.basicConfig(level=logging.INFO)
	logging.info("Begin Player")

	global directory

	current_movie_id = 'none'
	movie_name = 'none'

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


			if (not GPIO.input(gpio_pawpatrol)):
				
				logging.info("PAW PATROL")

				movie_name = 'pawpatrolfolder'

			elif (not GPIO.input(gpio_coco)):
				
				logging.info("COCOMELON")

				movie_name = 'cocomelonfolder'

			elif (not GPIO.input(gpio_tom)):
				
				logging.info("TOM and Jerry")
				movie_name = 'tomandjerryfolder'

			elif (not GPIO.input(gpio_popeye)):
				
				logging.info("POPEYE")
				movie_name = 'popeyefolder'

			elif (not GPIO.input(gpio_garbage)):
				
				logging.info("Garbage Truck Rules!")
				movie_name = 'garbagetruckfolder'

			elif (not GPIO.input(gpio_superman)):
				
				logging.info("This looks like a job for... Superman!")
				movie_name = 'supermanfolder'

			## Controls

			elif (not GPIO.input(gpio_fastforward)):
				
				logging.info(">> Fast Forward")

				try:
					myprocess.stdin.write("^[[C")

				except NameError:

					logging.info("Nothing to forward")

				except IOError:

					logging.info("Nothing to forward anymore")

				time.sleep(0.25)

			elif (not GPIO.input(gpio_rewind)):
				
				logging.info("<< Rewind")

				try:
					myprocess.stdin.write("^[[D")

				except NameError:

					logging.info("Nothing to rewind")

				except IOError:

					logging.info("Nothing to rewind anymore")

				time.sleep(0.25)

			elif (not GPIO.input(gpio_pause)):
				
				logging.info("- Pause/ Play -")

				try:
					myprocess.stdin.write("p")

				except NameError:

					logging.info("Nothing is playing yet")

				except IOError:

					logging.info("Nothing is playing right now")

				time.sleep(0.25)

			elif (not GPIO.input(gpio_quit)):
				
				logging.info("QUIT!")


				try:

					myprocess.communicate(b"q")

				except ValueError:

					logging.info("File already closed.")

				except NameError:

					logging.info("Nothing is playing yet")
 
				except IOError:

					logging.info("Nothing is playing right now")

				current_movie_id = 'none'

				movie_name = 'none'

				time.sleep(0.25)

			else:
				logging.debug('..... Waiting')
				time.sleep(0.1)	# checks for button press every 0.1 seconds

			if current_movie_id != movie_name:

				logging.info(" - Name: %s" % movie_name)
				#this is a check in place to prevent omxplayer from restarting video if ID is left over the reader.
				#better to use id than movie_name as there can be a problem reading movie_name occasionally
				
				movie_directory = movie_name.replace('folder',"") 
				
				try:

					movie_name = random.choice(glob.glob(os.path.join(directory + movie_directory, '*')))
					movie_name = movie_name.replace(directory,"")
				except IndexError:
					movie_name = 'videonotfound.mp4'

				logging.info("randomly selected: omxplayer %s" % movie_name)
				current_movie_id = movie_name
				playmovie(movie_name)

			else:

				logging.debug("same movie")



	except KeyboardInterrupt:
		print("\nAll Done")


#program start

directory = '/home/pi/Videos/'

if __name__ == "__main__":

    main()

