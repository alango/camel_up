import random
import copy
import operator

start_track = []
for i in range(18):
    start_track.append([])

camel_starts = [('blue',1), ('green',1), ('orange',1), ('white',1), ('yellow',1)]

oases = []
mirages = []

remaining_dice = ['white','green','yellow','orange','blue']

def place_desert_tile(track, location, tile_type):
    if track[location] != [] and track[location-1] != [] and track[location+1] != []:
        print "Tile already occupied, cannot place desert tile here!"
        return
    track[location] = tile_type
    return

def remove_desert_tile(track, location):
    if type(track[location]) == list:
        print "No desert tile at this location"
        return
    track[location] = []
    return

def move_camel(track, camel, roll):
    camel_start = -1
    search = 0
    ## Find the starting location of the camel and extract the camel unit.
    while camel_start == -1:
        if type(track[search]) == list:
            if camel in track[search]:
                camel_start = search
                camel_unit_start = track[search].index(camel)
                camel_unit = track[search][camel_unit_start:]
                for camel in camel_unit:
                    track[search].pop()
        search += 1
    new_location = camel_start + roll
    mirage = False
    tile_type = track[new_location]
    if type(tile_type) != list:
        new_location += track[new_location]
        if tile_type == -1:
            mirage = True
    if mirage == False:
        track[new_location] = track[new_location] + camel_unit
    else:
        track[new_location] = camel_unit + track[new_location]
    return

def results(track):
    results = []
    search = 0
    while len(results) < 5:
        if type(track[search]) == list:
            for camel in track[search]:
                results.append(camel)
        search += 1
    results.reverse()
    return results
        

for (camel,location) in camel_starts:
    start_track[location].append(camel)

for oasis in oases:
    place_desert_tile(oasis, 1)

for mirage in mirages:
    place_desert_tile(mirage, -1)


def rollout(start_track, remaining_dice):
    track = copy.deepcopy(start_track)
    dice = remaining_dice[:]
    while len(dice) != 0:
        die = random.randint(0, len(dice)-1)
        camel = dice[die]
        del dice[die]
        roll = random.randint(1,3)
        move_camel(track,camel,roll)
    return results(track)

def run_simulations(track, dice, n):
    scores = {'blue':0,'green':0,'orange':0,'white':0,'yellow':0}
    for i in range(n):
        if i % 2500==0: print i
        results = rollout(track, dice)
        for i in range(5):
            scores[results[i]] += i+1
    sorted_results = sorted(scores.items(), key=operator.itemgetter(1))
    return sorted_results

    
print start_track     
print run_simulations(start_track, remaining_dice, 10000)
