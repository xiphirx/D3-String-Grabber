from D3StringGrabber import stlFile

D3Affixes = stlFile()
D3Affixes.init('Affixes.stl')
"""
for desc in D3Affixes.desc:
	print '\nDesc'
	for record in desc:
		print str(record)
"""
for string in D3Affixes.stringList:
	print string
