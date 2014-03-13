#Name: Extrusion to relative Ormerod RepRapPro
#Info: Converts extrution values to relative Ormerod RepRapPro
#Depend: GCode
#Type: postprocess
#Param: zretraction(float:1.0) Retraction at layer change (mm)
#Param: subsequentlayertemp(int:0) Extruder temp after 1st layer (C)
#Param: subsequentlayerbedtemp(int:0) Bed temp  after 1st layer (C)

__copyright__ = "Copyright (C) 2014 Frank Brandner - Released under terms of the AGPLv3 License"
import re

def convert(m):
	global elast
	try:
		e = float(m.group(2))
		e = e - elast
		elast = float(m.group(2))
		return m.group(1) + "{:.5f}".format(e)
	except:
		return m.group(0)

with open(filename, "r") as f:
	lines = f.readlines()

elast = 0.
e = 0.

with open(filename, "w") as f:
	for line in lines:
		line2 = list(line.partition(";"))
		if "G0" in line2[0]:
			line2[0] = line2[0].replace("G0","G1")
		if "Z" in line2[0] and "X" in line2[0] and "Y" in line2[0]:
			part1 = line2[0].split('Z')[0]
			part2 = "G1 Z" + line2[0].split('Z')[1]
			line2[0] = part2 + part1 + "\n"
		if "G92 E0" in line2[0]:
			elast = 0
		if "G1 " in line2[0]:
			line2[0] = re.sub("([E])([+-]?[0-9]+\.?[0-9]*)", convert, line2[0])
			if "Z" in line2[0] and "X" in line2[0] and "Y" in line2[0]:
				line2[0] = "G1 F1800.000 E-" + str(round(zretraction,5)) + "\n" + line2[0] + "G1 F1800.000 E" + str(round(zretraction,5)) + "\n"
		if "CURA_PROFILE_STRING" in line2[2] or "#" in line2[2]:
			line = ""
		else:
			line = "" + line2[0] + line2[1] + line2[2]
			f.write(line)
		if line2[2] == 'LAYER:1\n':
			if int(subsequentlayerbedtemp) > 0:
				f.write("M140 S" + str(subsequentlayerbedtemp) + " ; Set bed temp\n")
			if int(subsequentlayertemp) > 0:
				f.write("M104 S" + str(subsequentlayertemp) + " ; Set extruder temp\n")