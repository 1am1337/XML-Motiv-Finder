import motivFinder as mF
import os
import music21 as m21
import pandas as pd
import matplotlib.pyplot as plt



BachMotivNotes = [ 
					[m21.note.Note("B-4"),m21.note.Note("A4"),m21.note.Note("C5"),m21.note.Note("B4")],			#Prime / Retrograde-Inversion (same intervals)
					[m21.note.Note("B4"), m21.note.Note("C5"), m21.note.Note("A4"), m21.note.Note("B-4")]		#Retrograde / Inversion (same intervals)
				  ]

BachMotivNotes = mF.generateMotiveIntervals(BachMotivNotes)

Directory = "KdF/"
MXLFiles = []
for file in os.listdir(Directory):
	if file.endswith(".mxl"):
		MXLFiles.append(file)

bachCorpus = m21.corpus.search('bach', 'composer')


totalFound = []


sumTotal = 0

for file in sorted(MXLFiles):
	tupleFoundMotives = mF.findMotivFromMXL(f"{Directory}{file}", BachMotivNotes)
	sumFoundMotives = sum(tupleFoundMotives)
	if sumFoundMotives == 0:
		pass
		print(f"0 times in {file}")
	else:
		print(f"{sumFoundMotives} times in {file}")
		totalFound.append([file, tupleFoundMotives[0], tupleFoundMotives[1]])
		sumTotal += sumFoundMotives

print("\nswitched to corpus search... \n")

for i in range(len(bachCorpus)):
	tupleFoundMotives = mF.findMotivFromMXL(bachCorpus[i], BachMotivNotes)
	sumFoundMotives = sum(tupleFoundMotives)
	print(f"{i+1}/{len(bachCorpus)}")
	if sumFoundMotives == 0:
		pass
		# print("nothing found")
	else:
		# print(f"{sumFoundMotives} times in {bachCorpus[i].metadata.bestTitle}")
		totalFound.append([bachCorpus[i].metadata.bestTitle, tupleFoundMotives[0], tupleFoundMotives[1]])
		sumTotal += sumFoundMotives


print(f"\namount of pieces containing B-A-C-H: {len(totalFound)}\ntotal times B-A-C-H appears: {sumTotal}")

data = pd.DataFrame(totalFound, columns=["Name", "P/RI", "R/I"])
data.to_csv("totalMotivesFound.csv")
print("\nExported to totalMotivesFound.csv\n")

data.plot.bar(x = "Name")
plt.xticks(rotation=-45)
plt.show()