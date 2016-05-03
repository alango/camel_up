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

def is_desert_tile(track, location):
    if track[location] == -1:
        return True;
    elif track[location] == 1:
        return True
    else:
        return False

def place_desert_tile(track, location, tile_type):
    if track[location] != [] and not is_desert_tile(track,location-1) and  not is_desert_tile(track,location+1):
        print "Tile already occupied, cannot place desert tile here!"
        return
    track[location] = tile_type
    return

def remove_desert_tile(track, location):
    if not is_desert_tile(track, location):
        print "No desert tile at this location"
        return False
    track[location] = []
    return True

def move_camel(track, camel, roll):
    camel_start = -1
    search = 0
    ## Find the starting location of the camel and extract the camel unit.
    while camel_start == -1:
        if not is_desert_tile(track,search):
            if camel in track[search]:
                camel_start = search
                camel_unit_start = track[search].index(camel)
                camel_unit = track[search][camel_unit_start:]
                for camel in camel_unit:
                    track[search].pop()
        search += 1
    new_location = camel_start + roll
    mirage = False
    if is_desert_tile(track,new_location):
        tile_type = track[new_location]
        new_location += tile_type
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
        if not is_desert_tile(track,search):
            for camel in track[search]:
                results.append(camel)
        search += 1
    results.reverse()
    return results
        
def initialise_track(camel_starts, oases, mirages):
    start_track = []
    for i in range(18):
        start_track.append([])
    for (camel,location) in camel_starts:
        start_track[location].append(camel)
    for oasis in oases:
        place_desert_tile(oasis, 1)
    for mirage in mirages:
        place_desert_tile(mirage, -1)
    return start_track


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
    scores = {"blue":[0]*5,"green":[0]*5,"orange":[0]*5,"white":[0]*5,"yellow":[0]*5}
    
    for i in range(n):
        if i % 2500==0: print i
        results = rollout(track, dice)
        for i in range(5):
            scores[results[i]][i-1] += +1
    scores = {camel:map(lambda x:x*100.0/n, score) for camel, score in scores.items()}
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    for score in sorted_scores:
        print score
    return scores

start_track = initialise_track(camel_starts, oases, mirages)   
print start_track     
run_simulations(start_track, remaining_dice, 10000)
