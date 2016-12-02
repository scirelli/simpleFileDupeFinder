#!/bin/python
import os
from subprocess import call, check_output, CalledProcessError
from collections import deque
import shlex

DUPE_FILE = "/tmp/dupes.txt"
STATE_FILE = "/tmp/dupesScanState.txt"
BASE_PATH = "/Volumes/Public/Media/Games"
SCAN_THESE_FOLDERS = ['Amiga',
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

def main():
	restoreStateAndScanFoldersForDupes()

def restoreStateAndScanFoldersForDupes(foldersToScan = SCAN_THESE_FOLDERS):
	scanForDupes(restoreState(foldersToScan, getPersistedState()))

def scanForDupes(foldersToScan):
	for folder in foldersToScan:
		workingPath = BASE_PATH + '/' + folder + "/ROMs"
		if(os.path.exists(workingPath)):
			persistState(folder)
			listOfDups = getDedupeMap(workingPath)
			writeDupeListToFile(listOfDups)
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

def writeDupeListToFile(listOfDups, dupeFile = DUPE_FILE):
	# Open file
	fd = os.open(dupeFile, os.O_RDWR | os.O_CREAT | os.O_APPEND)
	# Writing text
	ret = os.write(fd, ('\n'.join(listOfDups) + '\n').encode('utf-8'))
	# Close opened file
	os.close(fd)

def persistState(currentFolder, stateFile = STATE_FILE):
	if(os.path.exists(stateFile)):
		os.remove(stateFile)

	fd = os.open(stateFile, os.O_WR | os.O_CREAT)
	ret = os.write(fd, (currentFolder).encode('utf-8'))
	os.close(fd)

def getPersistedState(stateFile = STATE_FILE):
	ret = None
	try:
		txt = open(stateFile)
		ret = txt.read()
		txt.close()
	except:
		ret = None

	return ret

def restoreState(originalListOfFolders, lastFolderScanned):
	lastFolderScanned = lastFolderScanned.strip()
	if(lastFolderScanned):
		q = deque(originalListOfFolders)	
		for folder in originalListOfFolders:
			if(lastFolderScanned.lower() != folder.lower()):
				p = q.popleft()
			else:
				break;
		return list(q)

	return originalListOfFolders

main()
