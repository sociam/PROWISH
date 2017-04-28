import re, csv,os

alexa = 'top-5k.csv'
apks = 'top5k-apps.csv'

OUTFILE = 'app_to_web.csv'
MISSFILE = 'app_no_matching.csv'

def writefile(OUTFILE):
    newFile = not os.path.isfile(OUTFILE) 
    f = open(OUTFILE,'a')
    writer = csv.writer(f)
    if newFile:
        writer.writerow(['app', 'site'])
    return f,writer


def openfile(infile):
    newFile = not os.path.isfile(infile) 
    f = open(infile,'rb')
    reader = csv.reader(f,delimiter=';')
    return reader


def rewrite(app):
	site = ''
	match = re.findall("([^\.]*)",app)
	if len(match) > 0:
		site = site + match[2] + "." + match[0]
		print "site: " + site
	 
	
	return site

def findsite(appname):
    sites = openfile(alexa)
    match_sites = set()
    for row in sites:
        site = row[1].strip().lower()
        match= re.search(appname,site)
        if match:
        	if site not in match_sites:
        		match_sites.add(site)
    return match_sites


apps = openfile(apks)

for app in apps:
	# print app[0]
	appid = app[0]
	print appid	
	f,writer = writefile('reverse-site.csv')
	writer.writerow([appid,app[2],rewrite(appid)])