import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import OrderedDict
try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen, HTTPError

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class Hit:
    def __init__(self, batter, pitcher, x, y, hit_type):
        self.batter = batter
        self.pitcher = pitcher
        self.x = x
        self.y = y
        self.hit_type = hit_type

class Out:
    def __init__(self, batter, pitcher, x, y, out_type):
        self.batter = batter
        self.pitcher = pitcher
        self.x = x
        self.y = y
        self.out_type = out_type

base_url = ('http://gd2.mlb.com/components/game/mlb/'
            'year_{0}/month_{1}/day_{2}/')
batter_id = '592450'
inning_url = 'inning/inning_hit.xml'

start_year = '2017'
start_month = '05'
start_day = '01'
end_year = '2017'
end_month = '05'
end_day = '31'

start_date_text = start_year + '-' + start_month + '-' + start_day
end_date_text = end_year + '-' + end_month + '-' + end_day

current_day = datetime.datetime.strptime(start_date_text, '%Y-%m-%d')
end_day = datetime.datetime.strptime(end_date_text, '%Y-%m-%d')
delta = datetime.timedelta(days=1)

hits_list = []
outs_list = []

while current_day <= end_day:
    year = str(current_day.year)
    month = str(current_day.month) if current_day.month >= 10 else '0' + str(current_day.month)
    day = str(current_day.day) if current_day.day >= 10 else '0' + str(current_day.day)
    
    print(base_url.format(year, month, day) + 'batters/' + batter_id  + '_1.xml')

    try:
        response = urlopen(base_url.format(year, month, day) + 'batters/' + batter_id  + '_1.xml')
    except HTTPError:
        current_day += delta
        continue

    tree = ET.parse(response)
    game_id = tree.getroot().attrib.get('game_id')

    #Replace '/' and '-' with '_'
    game_id = game_id.replace('/', '_')
    game_id = game_id.replace('-', '_')

    response = urlopen(base_url.format(year, month, day) + 'gid_' + game_id + '/' + inning_url)

    tree = ET.parse(response)

    for bip in tree.getroot().iter('hip'):
        if bip.attrib.get('batter') != batter_id:
            continue

        pitcher_id = bip.attrib.get('pitcher')
        x = float(bip.attrib.get('x'))
        y = float(bip.attrib.get('y'))
        y = -y
        des = bip.attrib.get('des')

        if x == 0 or y == -0:
            current_day += delta
            continue

        if bip.attrib.get('type') == 'H':
            hit = Hit(batter_id, pitcher_id, x, y, des)
            hits_list.append(hit)
        else:
            out = Out(batter_id, pitcher_id, x, y, des)
            outs_list.append(out)

    current_day += delta

plt.plot([125, 150, 125, 100, 125], [-210, -180, -150, -180, -210], label='_nolegend_', color='black')
plt.axis([0, 250, -250, 0])

for hit in hits_list:
    if hit.hit_type == 'Single':
        plt.plot(hit.x, hit.y, 'b.', label='Single')
    elif hit.hit_type == 'Double':
        plt.plot(hit.x, hit.y, 'y.', label='Double')
    elif hit.hit_type == 'Triple':
        plt.plot(hit.x, hit.y, 'k.', label='Triple')
    else:
        plt.plot(hit.x, hit.y, 'r.', label='Home_run')

handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='best', frameon=False)
plt.show()


#TODO
'''
Need to complete the chart more. Get rid of axes, draw rest of field
'''
















