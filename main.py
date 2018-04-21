import requests
import bs4
import sys
import re
import mechanize
import urllib2
import cookielib
import string
import os
from time import sleep

#path = '/workspace/addUniBadaass'
path = '../../../../../media/futurenode/My Passport/UniBackup3'

def pdf_download(full_page_url, host):
	notFinished = True

	print "Looking at " + full_page_url
	while notFinished:
		try:
			res = requests.get(full_page_url)
			notFinished = False
			if res.status_code != 404:
				print res.status_code
				res.raise_for_status()
				soup = bs4.BeautifulSoup(res.text)
				print 'full_page_url: ' + full_page_url
				print full_page_url.split('/')
				htmlName = full_page_url.split('/')[-1]
				print type(htmlName)
				if 'html' not in htmlName:
					htmlName = full_page_url.split('/')[-2] + '.html'
				f = open(path+'/files/' + course + '/' + htmlName, 'w')
				allText = res.text
				allText = allText.encode('utf-8')
				f.write(allText)
				f.close()
				print type(htmlName)

				file_list = []
				for link in soup.find_all('a'):
					file_loc = link.get('href')
					if file_loc is not None:
						if file_loc.endswith('pdf'):
							if '' in file_loc:
								print("ORG: " + file_loc)
								file_list.append(file_loc)
						elif file_loc.endswith('.html') and 'index-2011-2012.html' not in file_loc and 'plagiarism' not in file_loc and 'webmaster' not in file_loc and 'contact' not in file_loc and 'cookies' not in file_loc and 'www.inf.ed.ac.uk' in file_loc:
							#				print "Warp speed to " + file_loc
							pdf_download(file_loc, host)

				for file in file_list:

					# relative or absolute path?
					if file.startswith('http'):
						url = file
					else:
						url = '{}/{}'.format(host[:-14], file)

					print("URL: " + url)
					print "file: " + file

					filename = url.split('/')[-1]
					print(filename)

					if 'rejkjkjstrict' in url:
						br = mechanize.Browser()

						br.open(url)

						br.select_form(name="factors")
						br.form['login'] = 's1143039'
						br.form['password'] = 'DICExkcdps120191'
						resp = br.submit()

						f = open(path+'/files/' + course + '/' + filename, 'w')
						f.write(resp.read())
						f.close()
					#elif 'aied' not in url and '':
					elif 'assets' in url:
						download = requests.get(url)
						if res.status_code == 200:
							print("OH YES")
							download.raise_for_status()
							local_file = open(
								'{}/files/{}/{}'.format(path,course, filename), 'wb')
							for chunk in download.iter_content(100000):
								local_file.write(chunk)
							print("DWL'D")

							local_file.close()

						elif res.status_code == 403:
							print("Ummm ... yes")
							br = mechanize.Browser()
							br.addheaders = [
								('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3')]

							new_url = string.replace(url, 'http', 'https')
							new_url = string.replace(new_url, '//.', '')
							br.open(new_url)

				#			f = open('files2/'+filename+'test1.html','w')
				#			f.write(br.response().read())
				#			f.close()

							br.select_form(name="factors")
							br.form['login'] = 's1143039'
							br.form['password'] = 'DICExkcdps120191'
							resp = br.submit()

				#			print br.response().read()
							f = open(path+'/files/' + course + '/' +
																filename + '.html', 'w')
							f.write(br.response().read())
							f.close()

		except requests.exceptions.ConnectionError as exc:
			print('There was a problem: {}'.format(exc))
			global sleepyTimeCount
			#if 'retries' in exc:
			if sleepyTimeCount <= 4:
				sleepyTime = sleepyTimeCount * 5 * 60 + 1
				sleepyTimeCount = sleepyTimeCount + 1
				print("Connection refused by the server..")
				print("Let me sleep for " + str(sleepyTime / 60.0) + " minutes")
				print("ZZzzzz...")
				sleep(sleepyTime)
				print("Had a nice sleep, now let me continue...")
				continue
			else:
				notFinished = False
	
		except Exception as exc:
			print('There was a problem: {}'.format(exc))
			global sleepyTimeCount
			#if 'retries' in exc:
			if sleepyTimeCount <= 0:
				sleepyTime = sleepyTimeCount * 5 * 60 + 1
				sleepyTimeCount = sleepyTimeCount + 1
				print("Random error..")
				print("Let me sleep for " + str(sleepyTime / 60.0) + " minutes")
				print("ZZzzzz...")
				sleep(sleepyTime)
				print("Had a nice sleep, now let me continue...")
				continue
			else:
				notFinished = False


#courses = ['fnlp','anlp','tnlp','ttds','stn','rss','rc','rl','pmr','nlu','nip','nc','mi','mlp','mlpr','ivr','bio1','bio2','dme','hci','bdl','ar','dmr','ale1']
#courses = [u'fnlp/lectures', u'PROJ', u'HCI', u'IVC',
#           u'IPP', u'IRR', u'IAR', u'IoTSSC', u'IJP', u'IJP-DL', u'IMC', u'IQC', u'IRDS', u'ITCS', u'IVR', u'IVR-DL', u'IAML', u'IAML-DL', u'MIP1', u'MIP2', u'DISS', u'RTDS', u'RTDS+', u'RTPP', u'MLPR', u'MLP', u'MT', u'MDI', u'MI', u'NLU', u'NC', u'NIP', u'OS', u'PA', u'PPLS', u'PM', u'PERP', u'PDIoT', u'PMR', u'PI', u'RC', u'RL', u'RLSC', u'RASRT', u'RSS', u'SP', u'STN', u'SAPM', u'SELP', u'ST', u'SDP', u'TTDS', u'THF', u'TNLP', u'TSPL', u'ALE1', u'ASR', u'AR', u'AILP', u'ANLP', u'ADBS', u'ATFD', u'AV', u'AV-DL', u'AGTA', u'ADS', u'BIO1', u'BIO2', u'BDL', u'CDI1', u'CDI2', u'CQI', u'COPT', u'CT', u'CCN', u'CCS', u'CMC', u'CA', u'CAV', u'CAR', u'COMN', u'CD', u'CG', u'CN', u'CP', u'CSLP', u'CS', u'DME', u'DBS', u'DMR', u'DMMR', u'DS', u'EPL', u'EXC', u'FV', u'INF2C-SE', u'INF2D',
#           u'INF1-CG', u'INF1-CL', u'INF1-DA', u'INF1-FP', u'INF1-OP', u'INF2A', u'INF2B', u'INF2C-CS']
name = 'nlu/syllabus.html'

courses = [ name ]

for each in courses:

	course = each.lower()

	os.makedirs(path+'/files/' + course)

	url = 'http://www.inf.ed.ac.uk/teaching/courses/' + course 

	full_page_url = url
	host = url

	sleepyTimeCount = 1

	pdf_download(full_page_url, host)
