"""
Wikicopy is a program to download the articles of a dokuwiki and save them in a zip file.


==Commands==
===Help===
The -h option, the -help option, will print the help, which is this document. The example follows:
python account.py -h

===Input===
Default is http://devtome.com

The -input option sets the input file name. The example follows:
python wikicopy.py -input http://devtome.com


==Install==
For wikicopy to run, you need Python 2.x, wikicopy will probably not run with python 3.x. To check if it is on your machine, in a terminal type:
python

If python 2.x is not on your machine, download the latest python 2.x, which is available from:
http://www.python.org/download/
"""

import almoner
import devtome
import os
import shutil
import sys
import time


__license__ = 'MIT'


def getTitles(wikiAddress):
	'Write zip file.'
	indexDepth = 0
	popularPageAddress = wikiAddress + '/doku.php?id=start&idx=wiki%3Auser'
	lines = almoner.getTextLines(almoner.getInternetText(popularPageAddress))
	prefix = '?id='
	prefixLength = len(prefix)
	titles = []
	for line in lines:
		if line.startswith('</ul>'):
			if indexDepth > 0:
				indexDepth -= 1
		if indexDepth > 0 and 'class="wikilink1"' in line:
			prefixIndex = line.find(prefix) + prefixLength
			title = line[prefixIndex :]
			quoteIndex = title.find('"')
			if len(title) > 0:
				titles.append(title[: quoteIndex])
		if line == '<ul class="idx">':
			indexDepth += 1
	return titles

def writeOutput(arguments):
	'Write output.'
	if '-h' in arguments or '-help' in arguments:
		print(__doc__)
		return
	wikiAddress = almoner.getParameter(arguments, 'http://devtome.com', 'wiki')
	fileNameRoot = wikiAddress
	if 'http://' in fileNameRoot:
		fileNameRoot = fileNameRoot[len('http://') :]
	if '.' in fileNameRoot:
		fileNameRoot = fileNameRoot[: fileNameRoot.find('.')]
	fileNameRoot = almoner.getParameter(arguments, fileNameRoot, 'output')
	writeZipFile(fileNameRoot, wikiAddress)

def writeZipFile(fileNameRoot, wikiAddress):
	'Write zip file.'
	print('Copying:')
	print(wikiAddress)
	print('')
	if os.path.isdir(fileNameRoot):
		shutil.rmtree(fileNameRoot)
	os.makedirs(fileNameRoot)
	previousLetter = '0'
	titles = getTitles(wikiAddress)
#	titles = titles[:2]
	for title in titles:
		letter = title[0]
		if letter != previousLetter:
			previousLetter = letter
			print('Copying articles starting with %s.' % letter.upper())
		sourceText = devtome.getSourceText(wikiAddress + '/doku.php?id=%s&do=edit' % title)
		time.sleep(2)
		fileName = os.path.join(fileNameRoot, title)
		almoner.writeFileText(fileName, sourceText)
	print('There were %s files in the wiki.\n' % len(titles))
	almoner.writeZipFileByFolder(fileNameRoot)


def main():
	'Write output.'
	writeOutput(sys.argv)

if __name__ == '__main__':
	main()
