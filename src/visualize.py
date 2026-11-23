#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK KR','Noto Sans CJK JP','NanumGothic','Malgun Gothic','DejaVu Sans']

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# top 10 by value, then sorted low to high
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)[:10]
items = items[::-1]
keys = [k for k,v in items]
values = [v for k,v in items]

# label the axes based on which kind of file this is
kind = 'Country' if args.input_path.endswith('.country') else 'Language'
ylabel = 'Fraction of all tweets in that ' + kind.lower() if args.percent else 'Number of tweets'

# plot
fig, ax = plt.subplots(figsize=(10,6))
ax.bar(keys, values)
ax.set_xlabel(kind)
ax.set_ylabel(ylabel)
title_key = args.key if args.key.isascii() else 'the Korean coronavirus hashtag'
ax.set_title(f'Usage of {title_key} by {kind.lower()} (2020, top 10)')
fig.tight_layout()

# save the png
os.makedirs('img', exist_ok=True)
name = os.path.basename(args.input_path) + '_' + args.key.lstrip('#') + ('_percent' if args.percent else '') + '.png'
output_path = os.path.join('img', name)
fig.savefig(output_path, dpi=150)
print('saved', output_path)
