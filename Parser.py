import urllib2
from bs4 import BeautifulSoup

'''ls_year = '2010'''

ls_year = raw_input('please input a year... ')

if int(ls_year) % 400 == 0:
	ls_startdate = ['-1-1','-2-1','-3-1','-4-1','-5-1','-6-1','-7-1','-8-1','-9-1','-10-1','-11-1','-12-1']
	ls_enddate = ['-1-31','-2-29','-3-31','-4-30','-5-31','-6-30','-7-31','-8-31','-9-30','-10-31','-11-30','-12-31']
else:
	ls_startdate = ['-1-1','-2-1','-3-1','-4-1','-5-1','-6-1','-7-1','-8-1','-9-1','-10-1','-11-1','-12-1']
	ls_enddate = ['-1-31','-2-28','-3-31','-4-30','-5-31','-6-30','-7-31','-8-31','-9-30','-10-31','-11-30','-12-31']

ls_date =[ls_startdate,ls_enddate]

with open(ls_year+'_lawsuits.txt','w') as f:
	for d in range(len(ls_startdate)):

		openlink = urllib2.urlopen('https://www.patexia.com/ip-research/lawsuits?type%5B0%5D=1&showDateField=filingDate&showCharts=1&startFilingDateRange='+ls_year+ls_date[0][d]+'&endFilingDateRange='+ls_year+ls_date[1][d]+'&page=1')
		x = openlink.read()

		soup = BeautifulSoup(x)
		totalPageNum = soup.body.find('span',attrs={'class':'totalPages'}).string
		Result = soup.body.find('table',attrs={'class':'adminTable'})

		import math
		totalPageNum = totalPageNum.replace(',','')

		totalPageNum = int(totalPageNum)/20.0
		totalPageNum = math.ceil(totalPageNum)

		seq = 1

		for page in range(1,int(totalPageNum)+1):
		
			openlink = urllib2.urlopen('https://www.patexia.com/ip-research/lawsuits?type%5B0%5D=1&showDateField=filingDate&showCharts=1&startFilingDateRange='+ls_year+ls_date[0][d]+'&endFilingDateRange='+ls_year+ls_date[1][d]+'&page='+str(page))
			x = openlink.read()

			soup = BeautifulSoup(x)
			Result = soup.body.find('table',attrs={'class':'adminTable'})
			
			for link in Result.find_all('a'):
				
				openlink = urllib2.urlopen('https://www.patexia.com'+link.get('href'))
				k = openlink.read()
				soup2 = BeautifulSoup(k)

				LawsuitsResult = soup2.body.find('div',attrs={'class':'lawsuitDocuments clearfix'})
				DefendantResult = soup2.body.find('div',attrs={'id':'middleCol'})

				try:
					'''Lawsuits Info'''		
					LawsuitsTitle = DefendantResult.h1.text.strip('> Summary')

					CourtCastNumber = LawsuitsResult.p.text.strip('Court Cast Number')
					FillingDate = LawsuitsResult.p.next_sibling.next_sibling.text.strip('Filling Date')
								
					print seq,'|',
					print CourtCastNumber,'|',
					print FillingDate,'|',
					print LawsuitsTitle,'|',

					f.write('%s|'%seq)
					f.write('%s|'%CourtCastNumber)
					f.write('%s|'%FillingDate)
					f.write('%s|'%LawsuitsTitle)
					pass
				except Exception, e:
					break		
				
				try:
					'''Plaintiff'''
					PlaintiffResult = LawsuitsResult.find('div',attrs={'class':'patentsSummaryBox clearfix'})

					PlaintiffResult = PlaintiffResult.next_sibling.next_sibling

					sum_plaintiff = PlaintiffResult.find('div',attrs={'class':'patentsSummaryTxt clearfix'})
					sub_plaintiff = PlaintiffResult.find('div',attrs={'class':'patentsSummarySubTxt clearfix'})

					sum_plaintiff = sum_plaintiff.text.strip()
					
					print sum_plaintiff,';',
					f.write('%s;'%sum_plaintiff)

					sub_plaintiff = sub_plaintiff.text.lstrip()
					sub_plaintiff = sub_plaintiff.rstrip()
					sub_plaintiff = sub_plaintiff.replace('\n',';')

					print sub_plaintiff,'|',
					f.write('%s|'%sub_plaintiff)

				except Exception, e:
					print '|',
					f.write('|')
					pass
				
				try:
					'''Defendant'''
					defendant = DefendantResult.div.next_sibling.next_sibling
					sum_defendant = defendant.find('div',attrs={'class':'patentsSummaryTxt clearfix'})
					sub_defendant = defendant.find('div',attrs={'class':'patentsSummarySubTxt clearfix'})

					sum_defendant = sum_defendant.text.strip()
					
					print sum_defendant,';',
					f.write('%s;'%sum_defendant)

					sub_defendants = sub_defendant.text.lstrip()
					sub_defendants = sub_defendants.rstrip()
					sub_defendants = sub_defendants.replace('\n',';')

					print sub_defendants,'|',
					f.write('%s|'%sub_defendants)

					pass
				except Exception, e:
					print '|',
					f.write('|')
					pass
				
				try:
					'''docNum'''
					docNum = soup2.body.find('table',attrs={'class':'adminTable'})

					for link in docNum.find_all('a'):
						strHref = link.get('href')
						EachDocNum = strHref.strip(r'/us-patents/')

						print EachDocNum,';',
						f.write('%s;'%EachDocNum)
					pass
				except Exception, e:
					pass
				
				seq = seq + 1
				print ''
				f.write('\n')

f.close()
