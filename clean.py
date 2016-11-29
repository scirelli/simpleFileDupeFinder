#!/bin/python
import os
from subprocess import call, check_output, CalledProcessError
import shlex

dupeFile = "/tmp/dupes.txt"

def main():
	# Open a file
	basePath = "/Volumes/Public/Media/Games"
	scanTheseFolders = ['Amiga',
					'Atari_2600',
					'Game_Gear',
					'Gameboy',
					'Gameboy_Advance',
					'Gameboy_Color',
					'MAME',
					'NeoGeo_Pocket_Color',
					'Neo_Geo',
					'Nintendo_DS',
					'Nintendo_NES',
					'Sega32x',
					'Sega_CD',
					'Sega_Genesis_(Sega_Mega_Drive)',
					'Sega_Master_System',
					'Super_Nintendo',
					'TurboGrafX16']

	filesInDir = os.listdir(basePath)
	for folder in scanTheseFolders:
		workingPath = basePath + '/' + folder + "/ROMs"
		if(os.path.exists(workingPath)):
			listOfDups = getDedupeMap(workingPath)
			writeToFile(listOfDups)
		else:
			print('Does not exist', folder)

def getDedupeMap(folder):
	'Retruns a map of unique files for this folder.'	
	filesInDir = os.listdir(folder)
	dedupeMap = {}	
	listOfDups = []
	
	if(len(filesInDir)):
		for file in filesInDir:
			fileAndPath = folder + '/' + file
			try:
				md5 = check_output(shlex.split('md5 -q "' + fileAndPath + '"'));
				md5 = md5.decode('utf-8');
				print('"%s": "%s"' % (file, md5.strip()))

				if(md5 not in dedupeMap):
					dedupeMap[md5] = fileAndPath
				else:
					listOfDups.append(fileAndPath);
					print('\n\nFound a dup: ', '"', dedupeMap[md5], '"',  fileAndPath, '\n')
			except CalledProcessError:
				print("subprocess.CalledProcessError stdout output:\n")

		print('\n'.join(listOfDups), '\nDupe count: ' + str(len(listOfDups)))
		print(str(len(listOfDups)), ' out of ', str(len(filesInDir)))
		print(str(len(listOfDups)/len(filesInDir)))
	else:
		print('Nothing to do.', folder)

	return listOfDups

def writeToFile(listOfDups):
	# Open file
	fd = os.open(dupeFile, os.O_RDWR | os.O_CREAT | os.O_APPEND)
	# Writing text
	ret = os.write(fd, ('\n'.join(listOfDups) + '\n').encode('utf-8'))
	# Close opened file
	os.close(fd)

main()
