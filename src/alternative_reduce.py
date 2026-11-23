#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags',nargs='+',required=True)
parser.add_argument('--input_folder',default='outputs')
parser.add_argument('--output_path',default='img/alternative_reduce.png')
args = parser.parse_args()

# imports
import os
import re
import glob
import json
import datetime
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# scan the outputs folder and build {hashtag: {day_of_year: count}}
daily = defaultdict(lambda: defaultdict(int))
for path in sorted(glob.glob(os.path.join(args.input_folder,'*.lang'))):
    m = re.search(r'geoTwitter(\d\d)-(\d\d)-(\d\d)', os.path.basename(path))
    date = datetime.date(2000+int(m.group(1)), int(m.group(2)), int(m.group(3)))
    day = date.timetuple().tm_yday
    with open(path) as f:
        counts = json.load(f)
    for hashtag in args.hashtags:
        daily[hashtag][day] = sum(counts.get(hashtag, {}).values())

# plot one line per hashtag
fig, ax = plt.subplots(figsize=(12,6))
for hashtag in args.hashtags:
    days = sorted(daily[hashtag])
    ax.plot(days, [daily[hashtag][d] for d in days], label=hashtag)

# label the x-axis with months instead of day numbers
month_starts = [datetime.date(2020,m,1).timetuple().tm_yday for m in range(1,13)]
ax.set_xticks(month_starts)
ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
ax.set_xlabel('Day of the year (2020)')
ax.set_ylabel('Number of tweets per day')
ax.set_title('Daily tweets using each hashtag in 2020')
ax.legend()
fig.tight_layout()

os.makedirs(os.path.dirname(args.output_path) or '.', exist_ok=True)
fig.savefig(args.output_path, dpi=150)
print('saved', args.output_path)
