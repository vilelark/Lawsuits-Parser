import urllib2
import urllib
from bs4 import BeautifulSoup


ls_startdate = ['2014-1-1','2014-2-1','2014-3-1','2014-4-1','2014-5-1','2014-6-1','2014-7-1','2014-8-1','2014-9-1','2014-10-1','2014-11-1','2014-12-1']
ls_enddate = ['2014-1-31','2014-2-28','2014-3-31','2014-4-30','2014-5-31','2014-6-30','2014-7-31','2014-8-31','2014-9-30','2014-10-31','2014-11-30','2014-12-31']


ls_date =[ls_startdate,ls_enddate]


for d in range(len(ls_startdate)):

	openlink = urllib2.urlopen('https://www.patexia.com/ip-research/lawsuits?type%5B0%5D=1&showDateField=filingDate&showCharts=1&startFilingDateRange='+ls_date[0][d]+'&endFilingDateRange='+ls_date[1][d]+'&page=1')
	x = openlink.read()

	soup = BeautifulSoup(x)
	totalPageNum = soup.body.find('span',attrs={'class':'totalPages'}).string
	Result = soup.body.find('table',attrs={'class':'adminTable'})

	import math
	totalPageNum = totalPageNum.replace(',','')

	'''print totalPageNum'''

	totalPageNum = int(totalPageNum)/20.0
	totalPageNum = math.ceil(totalPageNum)

	seq = 1

	for page in range(1,int(totalPageNum)+1):
		openlink = urllib2.urlopen('https://www.patexia.com/ip-research/lawsuits?type%5B0%5D=1&showDateField=filingDate&showCharts=1&startFilingDateRange='+ls_date[0][d]+'&endFilingDateRange='+ls_date[1][d]+'&page='+str(page))
		x = openlink.read()

		soup = BeautifulSoup(x)
		Result = soup.body.find('table',attrs={'class':'adminTable'})
		
		for link in Result.find_all('a'):
			
			openlink = urllib.urlopen('https://www.patexia.com'+link.get('href'))
			k = openlink.read()
			soup2 = BeautifulSoup(k)

			LawsuitsResult = soup2.body.find('div',attrs={'class':'lawsuitDocuments clearfix'})
			DefendantResult = soup2.body.find('div',attrs={'id':'middleCol'})

			try:			
				LawsuitsTitle = DefendantResult.h1.text.strip('> Summary')

				CourtCastNumber = LawsuitsResult.p.text.strip('Court Cast Number')
				FillingDate = LawsuitsResult.p.next_sibling.next_sibling.text.strip('Filling Date')
							
				print seq,'|',
				print CourtCastNumber,'|',
				print FillingDate,'|',
				print LawsuitsTitle,'|',

				pass
			except(TypeError):
				break
			except Exception, e:
				break		
			else:
				pass
			finally:
				pass
			

			try:	
				Plaintiff = LawsuitsResult.div.next_sibling.next_sibling
				Plaintiff = Plaintiff.p.text.strip()
				print Plaintiff,'|',

			except Exception, e:
				print '|',
				pass
			else:
				pass
			finally:
				pass


			try:
				'''Defendant'''
				defendant = DefendantResult.div.next_sibling.next_sibling
				sum_defendant = defendant.find('div',attrs={'class':'patentsSummaryTxt clearfix'})
				sub_defendant = defendant.find('div',attrs={'class':'patentsSummarySubTxt clearfix'})

				sum_defendant = sum_defendant.text.strip()
				print sum_defendant,';',

				sub_defendants = sub_defendant.text.lstrip()
				sub_defendants = sub_defendants.rstrip()
				sub_defendants = sub_defendants.replace('\n',';')

				print sub_defendants,'|',
				pass
			except Exception, e:
				print '|',
				pass
			else:
				pass
			finally:
				pass

			

			try:
				docNum = soup2.body.find('table',attrs={'class':'adminTable'})

				for link in docNum.find_all('a'):
					strHref = link.get('href')
					EachDocNum = strHref.strip(r'/us-patents/')

					print EachDocNum,';',
				pass
			except Exception, e:
				pass
			else: 
				pass
			finally:
				pass

			seq = seq + 1
			print ''

	


