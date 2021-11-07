import json
import barlow

def prepForDump(ratios):
    intervals = dict((v,k) for k,v in ratios.items())

    sum = 0
    for ratio in intervals:
        harm = intervals[ratio]
        harm = abs(harm)
        if(harm >= 1.0): harm = 0.0
        sum += harm
        intervals[ratio] = harm
    
    for ratio in intervals:
        intervals[ratio] = intervals[ratio]/sum
    
    newRatios = dict()
    for ratio in intervals:
        newRatios[str(ratio[1]) + "/" + str(ratio[0])] = intervals[ratio]
    
    return newRatios

master_interval_dict = dict()
for h in range(0, 8):
    minHarmonicity = 0.1 - float(h)*0.01
    master_interval_dict["{:.2f}".format(minHarmonicity)] = prepForDump(barlow.calcAllIntervals(minHarmonicity, True))
json_object = json.dumps(master_interval_dict, indent = 1)
print(json_object)
with open('intervals.json', 'w') as f:
    f.write(json_object)