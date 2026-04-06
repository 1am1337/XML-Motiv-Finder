import music21 as m21


def generateMotiveIntervals(motivNotes):
	BachMotivIntervals = []
	for i in range(len(motivNotes)):
		BachMotivIntervals.append([])
		for note in motivNotes[i]:
			firstMidiVal = motivNotes[i][0].pitch.midi
			BachMotivIntervals[i].append(note.pitch.midi - firstMidiVal)
	return BachMotivIntervals


def generateFlatScore(fullScore):
	flatScoreBach = []
	for i in range(len(fullScore.getElementsByClass('Part'))):
		currentVoice = []
		for item in fullScore.parts[i].flatten().getElementsByClass(m21.note.GeneralNote):
			if item.isNote:
				currentVoice.append((item.pitch, item.offset))
			elif item.isRest:
				currentVoice.append((m21.note.Note(0).pitch, item.offset))
		flatScoreBach.append(currentVoice)
	return flatScoreBach


def convertToIntervals(NoteSelection):
	lenNoteSelection = len(NoteSelection)
	intervalList = []
	firstMidiVal = NoteSelection[0][0].midi
	for i in range(lenNoteSelection):
		currentInterval = NoteSelection[i][0].midi - firstMidiVal
		intervalList.append(currentInterval)
	return intervalList


def findMotiv(flatScore, motiv):
	AmountOfParts = len(flatScore)
	lenMotiv = len(motiv[0])
	foundMotives = [[],[]]
	for i in range(AmountOfParts):
		lenPart = len(flatScore[i])
		for j in range(lenPart):
			currentInterval = convertToIntervals(flatScore[i][j:j+lenMotiv])	
			if currentInterval == motiv[0]:
				foundMotives[0].append((i,(flatScore[i][j][1]+1)))
				# print(f"found p / r-i @ {currentInterval, i, j+1}")
			elif currentInterval == motiv[1]:
				foundMotives[1].append((i,(flatScore[i][j][1]+1)))
				# print(f"found r / p-i @ {currentInterval, i, j+1}")
			else:
				pass
	return (len(foundMotives[0]), len(foundMotives[1]))


def findMotivFromMXL(fileName, motiv):
	motiv = generateMotiveIntervals(motiv)
	fullScore = m21.converter.parse(fileName)
	flatScore = generateFlatScore(fullScore)
	listFoundMotives = findMotiv(flatScore, motiv)

	return listFoundMotives



