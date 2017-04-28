import json
import re
import csv
import os
from collections import defaultdict

outfile_app_children = open('app_children_naive.csv', 'a')
outfile_app_parents = open('app_parents_naive.csv', 'a')
outfile_app_children_prom = open('app_children_prom.csv', 'a')
outfile_app_parents_prom = open('app_parents_prom.csv', 'a')

with open('5k_static_2.0.json') as data_file:    
    data = json.load(data_file)

companyinfo = open('../curated/company_details.json', 'rb')
companyinfo = json.load(companyinfo)

# get the app downloads data to estimate rank

with open('top5k-apps-estimated-ranks.csv') as f:
	reader = csv.reader(f)
	rows = list(reader)
app_ranks = {}
for row in rows:
	app_ranks[row[0]] = row[3]

child_counts = defaultdict(int)
parent_counts = defaultdict(int)
child_counts_prom = defaultdict(int)
parent_counts_prom = defaultdict(int)

def getParent(co):
	if co in companyinfo:
		co_inf = companyinfo[co]['parent']
		if not co_inf:
			return co
		else:
			return co_inf

# children, unweighted
for apk in data:
	trackers = data[apk]
	print trackers
	for tracker in trackers:
		child_counts[tracker] += 1
	print trackers

print child_counts

# children, weighted
for apk in data:
	if apk in app_ranks:
		rank = float(app_ranks[apk])
	else:
		# if rank is unknown, assign mid-point rank
		rank = 2500
	prominence_weight = 1 * 1/rank
	trackers = data[apk]
	for tracker in trackers:
		child_counts_prom[tracker] += prominence_weight

print child_counts_prom

# parents, unweighted
for apk in data:
	trackers = data[apk]
	tracker_parents = []
	for tracker in trackers:
		parent = getParent(tracker)
		tracker_parents.append(parent)
	tracker_parents = set(tracker_parents)
	for tracker_parent in tracker_parents:
		parent_counts[tracker_parent] += 1

print parent_counts

# parents, weighted
for apk in data:
	if apk in app_ranks:
		rank = float(app_ranks[apk])
	else:
		# if rank is unknown, assign mid-point rank
		rank = 2500
	prominence_weight = 1 * 1/rank
	trackers = data[apk]
	tracker_parents = []
	for tracker in trackers:
		parent = getParent(tracker)
		tracker_parents.append(parent)
	tracker_parents = set(tracker_parents)
	for tracker_parent in tracker_parents:
		parent_counts_prom[tracker_parent] += prominence_weight

print parent_counts_prom


for key, value in child_counts.items():
	row = '%s,%s\n' % (key, value)
	outfile_app_children.write(row)

for key, value in parent_counts.items():
	row = '%s,%s\n' % (key, value)
	outfile_app_parents.write(row)

for key, value in child_counts_prom.items():
	row = '%s,%s\n' % (key, value)
	outfile_app_children_prom.write(row)

for key, value in parent_counts_prom.items():
	row = '%s,%s\n' % (key, value)
	outfile_app_parents_prom.write(row)

print app_ranks