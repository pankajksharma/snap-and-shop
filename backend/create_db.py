import re
i=1
while True:
	try:
		line = raw_input()
	except:
		break
	if not line:
		break
	line = line.split(',')
	line1, line2 = ','.join(line[:-1]), line[-1]
	line2 = ', '.join(line2.split())
	line = line1+', '+line2
	line = 'insert into android values('+str(i)+', "flipkart", '+line+');'
	print line
	i += 1
