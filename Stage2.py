import tkinter, re
from tkinter import filedialog

rootWindow = tkinter.Tk()
rootWindow.withdraw()

inputPath = filedialog.askopenfilename()
outputPath = filedialog.askdirectory()

outputPath1 = outputPath + "/Output1.txt"
outputPath2 = outputPath + "/Output2.txt"
outputPath3 = outputPath + "/Output3.txt"

exceptionList1 = ['RESULT: Da','ANNUAL CO2','SHARE OF R','ANNUAL FUE','ANNUAL COS']
exceptionList2 = ['EnergyPLAN','RESULT: Da','Technical ','Critical E']
exceptionList3 = ['Coal ','Oil ','N.Gas ','Biomass ','Renewable ','H2 Etc. ','Biofuel ','Nucl/Ccs ','Total ','So2 ','Pm2.5 ','Nox ','Ch4 ','N2O ','Detailed Emi']

out1 = ''
out2 = ''

opf = open(outputPath1, 'w')

with open(inputPath) as ipf:
    for i, line in enumerate(ipf):

        if line[:10] == 'TOTAL FOR ':
            lineAnnual = i
            next

        elif line[:10] == 'MONTHLY AV':
            lineMonthly = i
            next

        elif line[:10] == 'HOURLY VAL':
            lineHourly = i
            break

with open(inputPath) as ipf:
    for i, line in enumerate(ipf):

        if i < lineAnnual-4:

            if line[:17].isspace():
                next

            elif line[:20].title().find('Warning') != -1:
                line = line.encode('ascii',errors='ignore').decode()
                opf.write(line.replace('\t',' ').replace('WARNING:','\n' + 'Warning').strip() + '\n')
                next

            elif line[:20].title().find('Result') != -1:
                opf.write('InputStudy ' + line[line.rfind('/') + 1 : line.rfind('.txt') + 4].strip().replace('\t',' ') + '\n')
                next

            elif line[:10] in exceptionList1:
                next

            else:
                opf.write(line[:91].replace('\t',' ').strip().title() + '\n')
                next

with open(inputPath) as ipf:
    for i, line in enumerate(ipf):

        if i < lineAnnual-4:

            if line[:95].isspace():
                next

            elif line[:20].title().find('Warning') != -1:
                next

            elif line[:10] in exceptionList2:
                next

            else:
                opf.write(line[91:151].replace('\t',' ').strip().title() + '\n')
                next

opf.close()

opf = open(outputPath2, 'w')

with open(inputPath) as ipf:
    for i, line in enumerate(ipf):

        if i < lineAnnual-4:

            if line[:20].title().find('Warning') != -1:
                next

            elif line[:10] in exceptionList2:
                next
            
            else:
                opf.write(line[151:].replace('\t',' ').strip().title() + '\n')
                next

opf.close()

opf = open(outputPath1, 'a')

with open(outputPath2) as ipf:
    for i, line in enumerate(ipf):

        if line[:10].isspace():
            next

        elif line[:2].replace('\t',' ').strip().isalpha():

            if any((match := x) in line.title() for x in exceptionList3):
                out1 = out1 + (line[:line.find(match)].replace('\t',' ').strip().title() + '   ')
                out2 = out2 + (line[line.find(match):].replace('\t',' ').strip().title() + '\n')

            else:
                out1 = out1 + (line.replace('\t',' ').strip().title() + '   ')

        elif line[:2].replace('\t',' ').strip().isdigit():

            if any((match := x) in line.title() for x in exceptionList3):
                out1 = out1 + (line[:line.find(match)].replace('\t',' ').strip().title() + '\n')
                out2 = out2 + (line[line.find(match):].replace('\t',' ').strip().title() + '\n')

            else:
                out1 = out1 + (line.replace('\t',' ').strip().title() + '\n')

opf.write(out1)
opf.write(out2)

opf.close()

opf = open(outputPath2, 'w')

with open(outputPath1) as ipf:
    for i, line in enumerate(ipf):
        
        if line[:5].strip().isdigit():
            next

        else:
            opf.write(re.sub(r'\s+',r'',re.sub(r'\s+(?=\d|-\d)', r',', re.sub(r'(?!\w)\s(?=\d|-\d)',r'',line))) + '\n')

opf.close()

opf = open(outputPath3, 'w')

with open(inputPath) as ipf:
    for i, line in enumerate(ipf):

        if i > lineAnnual and i <= lineHourly:

            if line.isspace():
                next

            elif i == lineMonthly or i == lineHourly:
                next

            else:
                opf.write(re.sub(r'\s+',r'',re.sub(r'\s+(?=\d|-\d|-\s|Percent)', r',', line)) + '\n')

        elif i > lineHourly:
            opf.write(re.sub(r'\s+(?=\d)', r'h', line[:14]) + ',' + re.sub(r'\s+',r'',line[:14]) + (',' * 21) + re.sub(r'\s+(?=\d|-\d)', r',', line[14:].strip()) + '\n')

opf.close()

opf = open(outputPath1, 'w')

with open(outputPath2) as ipf:
    for i, line in enumerate(ipf):

        if line[:17] == 'DetailedEmissions':
            next

        elif len(re.findall(',',line)) <= 3:
            opf.write(re.sub(r'(?!\w):',r'',line.replace('InputStudy','InputStudy,').replace('planModel','planModel,').replace('RegulationNo.','RegulationNo.,').replace('Percent','').replace('Twh/Year','').replace('Warning',('Warning' + str(i) + ','))))

        elif 18 >= len(re.findall(',',line)) > 3:
            opf.write(line.replace(',', ',,,,', 1))

opf.close()

opf = open(outputPath1, 'a')

with open(outputPath3) as ipf:
    for i, line in enumerate(ipf):
        if line[:1] != 'h':
            opf.write(re.sub(r'(?!\w):',r'',line.replace(',', (',' * 22), 1).replace('Percent','').replace(',-,',',,')))
        else:
            opf.write(line)

opf.close()

rootWindow.destroy()