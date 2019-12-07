wire1 = []
wire2 = []
with open("3/input.txt","r") as input_file:
    line = input_file.readline()
    wire1 = line.split(",")
    line = input_file.readline()
    wire2 = line.split(",")

class Span:
    def __init__(self, pos, min_span, max_span, total_dist, span_direction):
        self.pos = pos
        self.min_span = min_span
        self.max_span = max_span
        self.total_dist = total_dist
        self.span_direction = span_direction
    def compare_horizontal_span(self, other):
        if other.pos >= self.min_span and other.pos <= self.max_span:
            if self.pos >= other.min_span and self.pos <= other.max_span:
                signal_loss = 0
                if self.span_direction == "U":
                    signal_loss += other.pos - self.min_span
                else:
                    signal_loss += self.max_span - other.pos
                if other.span_direction == "R":
                    signal_loss += self.pos - other.min_span
                else:
                    signal_loss += other.max_span - self.pos
                signal_loss += self.total_dist + other.total_dist
                return (self.pos, other.pos, signal_loss)
        return None

def generate_spans(wire):
    verticals = []
    horizontals = []
    current_pos = (0,0)
    total_dist = 0
    for i in range(0, len(wire)):
        direction = wire[i][0]
        length = int(wire[i][1:])
        new_x = current_pos[0]
        new_y = current_pos[1]
        if direction == "R":
            new_x += length
            horizontals.append(Span(current_pos[1], current_pos[0], new_x, total_dist, direction))
        elif direction == "L":
            new_x -= length
            horizontals.append(Span(current_pos[1], new_x, current_pos[0], total_dist, direction))
        elif direction == "U":
            new_y += length
            verticals.append(Span(current_pos[0], current_pos[1], new_y, total_dist, direction))
        elif direction == "D":
            new_y -= length
            verticals.append(Span(current_pos[0], new_y, current_pos[1], total_dist, direction))
        current_pos = (new_x, new_y)
        total_dist += length
    return (verticals, horizontals)

spans1 = generate_spans(wire1)
spans2 = generate_spans(wire2)

def find_intersections(span1, span2, run_again = True):
    intersections = []
    for v_span in span1[0]:
        for h_span in span2[1]:
            possible_intersection = v_span.compare_horizontal_span(h_span)
            if possible_intersection is not None:
                intersections.append(possible_intersection)
    if run_again:
        intersections += find_intersections(span2, span1, False)
    return intersections

intersections = find_intersections(spans1, spans2)
# part 1
# intersections = [abs(i[0]) + abs(i[1]) for i in intersections]
# print(min(intersections))

# part 2
intersections = [i[2] for i in intersections]
print(min(intersections))
        

