class UninformedFrontier:
    def __init__(self):
        # max grid is 50x50 so 2500 is the limit
        self.nodes = [None] * 2500 
        self.head = 0  
        self.tail = 0   
        self.stack_top = -1   

    def enqueue_bfs(self, cell):
        self.nodes[self.tail] = cell
        self.tail += 1

    def dequeue_bfs(self):
        cell = self.nodes[self.head]
        self.head += 1
        return cell

    def push_dfs(self, cell):
        self.stack_top += 1
        self.nodes[self.stack_top] = cell

    def pop_dfs(self):
        cell = self.nodes[self.stack_top]
        self.stack_top -= 1
        return cell

    def empty_bfs(self):
        return self.head == self.tail

    def empty_dfs(self):
        return self.stack_top == -1


# for UCS & A*
# It is a manual Min-Heap (Priority Queue)
class CostTrackerArray:
    def __init__(self):
        # manual min-heap array
        self.heap_data = [None] * 2500
        self.active_elements = 0

    def insert_node(self, f_val, g_val, cell): # f_val : priority val
        self.heap_data[self.active_elements] = (f_val, g_val, cell) 
        self.bubble_node_up(self.active_elements) # Insert at end, then move up to maintain min-heap
        self.active_elements += 1

    def bubble_node_up(self, start_idx): # Moves node upward if smaller cost
        curr_idx = start_idx
        for _ in range(2500):
            if curr_idx == 0:
                break
            parent_idx = (curr_idx - 1) // 2
            curr_f, curr_g, _ = self.heap_data[curr_idx]
            parent_f, parent_g, _ = self.heap_data[parent_idx]

            swap_needed = False
            if curr_f < parent_f:
                swap_needed = True
            elif curr_f == parent_f and curr_g < parent_g:
                swap_needed = True
            # Moves node upward until heap property is satisfied
            if swap_needed:
                temp = self.heap_data[curr_idx]
                self.heap_data[curr_idx] = self.heap_data[parent_idx]
                self.heap_data[parent_idx] = temp
                curr_idx = parent_idx
            else:
                break

    def pull_lowest_cost_node(self):
        if self.active_elements == 0: 
            return None
        best_cell = self.heap_data[0][2] # Always take root (smallest)
        self.active_elements -= 1
        
        self.heap_data[0] = self.heap_data[self.active_elements]
        self.heap_data[self.active_elements] = None
        self.sink_node_down(0)
        return best_cell

    def sink_node_down(self, start_idx):
        curr_idx = start_idx
        for _ in range(2500):
            left_child = 2 * curr_idx + 1
            right_child = 2 * curr_idx + 2
            smallest_idx = curr_idx

            if left_child < self.active_elements:# then pick 'left'
                curr_f, curr_g, _ = self.heap_data[smallest_idx]
                l_f, l_g, _ = self.heap_data[left_child]
                if l_f < curr_f or (l_f == curr_f and l_g < curr_g):
                    smallest_idx = left_child

            if right_child < self.active_elements:
                curr_f, curr_g, _ = self.heap_data[smallest_idx]
                r_f, r_g, _ = self.heap_data[right_child]
                if r_f < curr_f or (r_f == curr_f and r_g < curr_g):
                    smallest_idx = right_child

            if smallest_idx != curr_idx: # swap
                temp = self.heap_data[curr_idx]
                self.heap_data[curr_idx] = self.heap_data[smallest_idx]
                self.heap_data[smallest_idx] = temp
                curr_idx = smallest_idx
            else:
                break

    def is_heap_empty(self):
        return self.active_elements == 0