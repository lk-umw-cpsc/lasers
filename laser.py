import math

class rect(object):
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    
    def __repr__(self):
        return f'Rect: ({self.x1}, {self.y1}), ({self.x2}, {self.y2})'
    
    def range_from_point(self, x):
        tx1 = self.x1 - x
        tx2 = self.x2 - x
        if x < self.x1: # laser to the left
            ty1 = self.y2
            ty2 = self.y1
        elif x > self.x2: # laser to the right
            ty1 = self.y1
            ty2 = self.y2
        elif self.y1 == 0: # laser directly below, bottom resting on x axis
            if tx1 == 0:
                return (0, math.pi/2) # laser on box left side
            if tx2 == 0:
                return (math.pi/2, math.pi) # laser on box right side
            return (0, math.pi)
        else: # laser directly below, box above laser
            ty1 = self.y1
            ty2 = self.y1
        # calculate theta using inverse tangent
        range_max = math.atan2(ty1, tx1)
        range_min = math.atan2(ty2, tx2)
        return (range_min, range_max)

def recurs_pick2(ranges: list, len: int, cur: int):
    start = cur + 1
    low = ranges[cur][0]
    high = ranges[cur][1]
    hits = set()
    for i in range(start, len):
        low_max = max(low, ranges[i][0])
        high_min = min(high, ranges[i][1])
        if low_max < high_min:
            hits.add((low_max, high_min))
    if start < len:
        hits.union(recurs_pick2(ranges, len, start))
        return hits
    return set()

def range_hit_count(rnge: tuple[float], ranges: list[tuple[float]]) -> int:
    best_min, best_max = rnge
    hit_count = 0
    for range_min, range_max in ranges:
        low_max = max(best_min, range_min)
        high_min = min(best_max, range_max)
        if low_max < high_min:
            hit_count += 1
    return hit_count

def find_best_overlap(ranges: list):
    current = ranges
    current_length = len(current)
    previous = []
    while current_length > 1:
        current = recurs_pick2(current, current_length, 0)
        current = list(current)
        current_length = len(current)
        if current_length == 0:
            if previous:
                return range_hit_count(previous[0], ranges)
            return 1
        previous = current
    return range_hit_count(current[0], ranges)


def grab_int() -> int:
    return int(input())

def grab_ints() -> list[int]:
    strs = input().split()
    return [int(s) for s in strs]

if __name__ == '__main__':
    num_boxes = grab_int()
    rects = []
    for i in range(num_boxes):
        rects.append(rect(*grab_ints()))
    best = 0
    for i in range(0, 101):
        round_best = find_best_overlap([r.range_from_point(i) for r in rects])
        if round_best > best:
            best = round_best
    print(best)