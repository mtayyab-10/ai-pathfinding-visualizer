def generate_neighbors(loc, r_limit, c_limit):
    r, c = loc
    valid_spots = [None] * 4
    found_count = 0
    
    # up, down, left, right (no diagonals allowed)
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < r_limit and 0 <= nc < c_limit:
            valid_spots[found_count] = (nr, nc)
            found_count += 1
            
    return valid_spots, found_count

def trace_and_print_path(parents_map, goal, start):
    raw_path = [None] * 2500
    path_len = 0
    curr = goal

    for _ in range(2500):
        if curr is None: break
        raw_path[path_len] = curr
        path_len += 1
        if curr == start: break
        r, c = curr
        curr = parents_map[r][c]
        
    # reverse path array manually 
    half_steps = path_len // 2
    for i in range(half_steps):
        opp_idx = path_len - 1 - i
        temp = raw_path[i]
        raw_path[i] = raw_path[opp_idx]
        raw_path[opp_idx] = temp

    print("\n--- Final Path ---")
    for i in range(path_len):
        pr, pc = raw_path[i]
        print(f"{pr} {pc}")
        
    return raw_path, path_len

def calc_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def calc_euclidean(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5