import tkinter as tk
from tkinter import messagebox 
import random
from data_structures import UninformedFrontier, CostTrackerArray
from utils import generate_neighbors, trace_and_print_path, calc_manhattan, calc_euclidean

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pathfinding Visualizer")
        self.root.configure(bg="#2c3e50") 
        
        self.dim = 20
        # 0 is free, 1 is wall
        self.grid_state = [[0 for _ in range(self.dim)] for _ in range(self.dim)]
        self.my_gui_boxes = [[None for _ in range(self.dim)] for _ in range(self.dim)]
        
        self.cell_costs = [[random.randint(1, 9) for _ in range(self.dim)] for _ in range(self.dim)]
        
        self.start_coord = (2, 2)
        self.goal_coord = (17, 17)
        
        self.active_algo = tk.StringVar(value="BFS")
        self.mouse_mode = tk.StringVar(value="Wall") 
        self.init_ui()

    def init_ui(self):
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        grid_frame = tk.Frame(main_frame, bg="black", bd=3, relief=tk.SUNKEN)
        grid_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        for r in range(self.dim):
            for c in range(self.dim):
                color = "white"
                if (r, c) == self.start_coord: color = "#27ae60"
                elif (r, c) == self.goal_coord: color = "#e74c3c"
                
                cell_val = self.cell_costs[r][c]
                
                lbl = tk.Label(grid_frame, text=str(cell_val), width=2, height=1, bg=color, bd=0, fg="#34495e", font=("Helvetica", 8))
                lbl.grid(row=r, column=c, padx=1, pady=1)
                lbl.bind("<Button-1>", lambda e, row=r, col=c: self.handle_click(row, col))
                lbl.bind("<B1-Motion>", lambda e, row=r, col=c: self.handle_drag(row, col))
                self.my_gui_boxes[r][c] = lbl

        control_frame = tk.Frame(main_frame, bg="#ecf0f1", bd=2, relief=tk.RAISED, padx=20, pady=20)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(control_frame, text="Control Panel", font=("Helvetica", 16, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=(0, 15))

        mode_lf = tk.LabelFrame(control_frame, text=" 1. Click Mode ", font=("Helvetica", 11, "bold"), bg="#ecf0f1", fg="#2980b9", padx=10, pady=10)
        mode_lf.pack(fill=tk.X, pady=10)
        
        modes = [(" Draw Walls", "Wall"), (" Set Start", "Start"), (" Set Goal", "Goal")]
        for text, val in modes:
            tk.Radiobutton(mode_lf, text=text, variable=self.mouse_mode, value=val, bg="#ecf0f1", font=("Helvetica", 10), cursor="hand2").pack(anchor=tk.W, pady=2)

        algo_lf = tk.LabelFrame(control_frame, text=" 2. Search Algorithm ", font=("Helvetica", 11, "bold"), bg="#ecf0f1", fg="#2980b9", padx=10, pady=10)
        algo_lf.pack(fill=tk.X, pady=10)
        
        algos = [("Breadth-First Search (BFS)", "BFS"), 
                 ("Depth-First Search (DFS)", "DFS"), 
                 ("Uniform Cost Search (UCS)", "UCS"), 
                 ("A* (Manhattan Dist)", "A* Manh"), 
                 ("A* (Euclidean Dist)", "A* Eucl")]
        for text, val in algos:
            tk.Radiobutton(algo_lf, text=text, variable=self.active_algo, value=val, bg="#ecf0f1", font=("Helvetica", 10), cursor="hand2").pack(anchor=tk.W, pady=2)

        tk.Button(control_frame, text=" RUN SEARCH", command=self.trigger_search, bg="#27ae60", fg="white", font=("Helvetica", 12, "bold"), cursor="hand2", pady=8).pack(fill=tk.X, pady=(20, 10))
        tk.Button(control_frame, text=" CLEAR PATHS", command=self.clear_visuals, bg="#f39c12", fg="white", font=("Helvetica", 12, "bold"), cursor="hand2", pady=8).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text=" RESET ENTIRE GRID", command=self.reset_entire_grid, bg="#c0392b", fg="white", font=("Helvetica", 10, "bold"), cursor="hand2", pady=5).pack(fill=tk.X, pady=5)

        self.cost_display = tk.Label(control_frame, text="Total Cost: 0", font=("Helvetica", 15, "bold"), bg="#ecf0f1", fg="#8e44ad")
        self.cost_display.pack(pady=(25, 0))

    def handle_click(self, r, c):
        m_type = self.mouse_mode.get()
        if m_type == "Start":
            if (r, c) == self.goal_coord: return 
            old_r, old_c = self.start_coord
            self.my_gui_boxes[old_r][old_c].config(bg="white")
            self.grid_state[old_r][old_c] = 0
            self.start_coord = (r, c)
            self.my_gui_boxes[r][c].config(bg="#27ae60")
            self.grid_state[r][c] = 0
        elif m_type == "Goal":
            if (r, c) == self.start_coord: return 
            old_r, old_c = self.goal_coord
            self.my_gui_boxes[old_r][old_c].config(bg="white")
            self.grid_state[old_r][old_c] = 0
            self.goal_coord = (r, c)
            self.my_gui_boxes[r][c].config(bg="#e74c3c")
            self.grid_state[r][c] = 0
        elif m_type == "Wall":
            if (r, c) in [self.start_coord, self.goal_coord]: return
            if self.grid_state[r][c] == 0:
                self.grid_state[r][c] = 1
                self.my_gui_boxes[r][c].config(bg="#2c3e50", text="") 
            else:
                self.grid_state[r][c] = 0
                self.my_gui_boxes[r][c].config(bg="white", text=str(self.cell_costs[r][c])) 

    def handle_drag(self, r, c):
        if self.mouse_mode.get() == "Wall" and (r, c) not in [self.start_coord, self.goal_coord]:
            self.grid_state[r][c] = 1
            self.my_gui_boxes[r][c].config(bg="#2c3e50", text="") 

    def clear_visuals(self):
        for r in range(self.dim):
            for c in range(self.dim):
                if (r, c) != self.start_coord and (r, c) != self.goal_coord and self.grid_state[r][c] == 0:
                    self.my_gui_boxes[r][c].config(bg="white")
        self.cost_display.config(text="Total Cost: 0")

    def reset_entire_grid(self):
        for r in range(self.dim):
            for c in range(self.dim):
                if (r, c) not in [self.start_coord, self.goal_coord]:
                    self.grid_state[r][c] = 0
                    self.my_gui_boxes[r][c].config(bg="white", text=str(self.cell_costs[r][c]))
        self.cost_display.config(text="Total Cost: 0")

    def trigger_search(self):
        self.clear_visuals()
        algo = self.active_algo.get()
        
        max_d = 50 
        visited_map = [[False for _ in range(max_d)] for _ in range(max_d)] 
        parents_map = [[None for _ in range(max_d)] for _ in range(max_d)] 
        g_cost_map = [[999999 for _ in range(max_d)] for _ in range(max_d)] 
        closed_map = [[False for _ in range(max_d)] for _ in range(max_d)] 
        
        if algo in ["UCS", "A* Manh", "A* Eucl"]:
            min_heap = CostTrackerArray()
            min_heap.insert_node(0, 0, self.start_coord)
            g_cost_map[self.start_coord[0]][self.start_coord[1]] = 0
            
            found = False
            while not min_heap.is_heap_empty():
                curr = min_heap.pull_lowest_cost_node()
                r, c = curr
                
                if closed_map[r][c]: continue
                closed_map[r][c] = True
                
                if curr == self.goal_coord:
                    found = True
                    break
                    
                if curr != self.start_coord:
                    self.my_gui_boxes[r][c].config(bg="#3498db")
                    self.root.update()
                    self.root.after(10)
                    
                neighbors, count = generate_neighbors(curr, self.dim, self.dim)
                for i in range(count):
                    nr, nc = neighbors[i]
                    if self.grid_state[nr][nc] == 0:
                        
                        if algo == "UCS":
                            step_cost = self.cell_costs[nr][nc] 
                        else:
                            step_cost = 1 
                            
                        new_g = g_cost_map[r][c] + step_cost
                        
                        if new_g < g_cost_map[nr][nc]:
                            g_cost_map[nr][nc] = new_g
                            parents_map[nr][nc] = curr
                            
                            if (nr, nc) != self.start_coord and (nr, nc) != self.goal_coord:
                                self.my_gui_boxes[nr][nc].config(bg="#bdc3c7")

                            if algo == "UCS":
                                min_heap.insert_node(new_g, new_g, (nr, nc))
                            elif algo == "A* Manh":
                                h = calc_manhattan((nr, nc), self.goal_coord)
                                min_heap.insert_node(new_g + h, new_g, (nr, nc))
                            elif algo == "A* Eucl":
                                h = calc_euclidean((nr, nc), self.goal_coord)
                                min_heap.insert_node(new_g + h, new_g, (nr, nc))

            if found:
                final_cost = g_cost_map[self.goal_coord[0]][self.goal_coord[1]]
                self.cost_display.config(text=f"Total Cost: {final_cost}")
                path_arr, p_size = trace_and_print_path(parents_map, self.goal_coord, self.start_coord)
                for i in range(p_size):
                    pr, pc = path_arr[i]
                    if (pr, pc) != self.start_coord and (pr, pc) != self.goal_coord:
                        self.my_gui_boxes[pr][pc].config(bg="#f1c40f")
                        self.root.update()
                
                messagebox.showinfo("Search Complete", f"Path found!\nTotal Cost: {final_cost}")
            else:
                messagebox.showinfo("Result", "No path exists to the goal!")

        else:
            struct = UninformedFrontier()
            
            if algo == "BFS": 
                struct.enqueue_bfs(self.start_coord)
                visited_map[self.start_coord[0]][self.start_coord[1]] = True
            else: 
                struct.push_dfs(self.start_coord)
            
            found = False
            while not (struct.empty_bfs() if algo == "BFS" else struct.empty_dfs()):
                curr = struct.dequeue_bfs() if algo == "BFS" else struct.pop_dfs()
                r, c = curr
                
                if algo == "DFS":
                    if visited_map[r][c]: continue 
                    visited_map[r][c] = True
                    
                if curr == self.goal_coord:
                    found = True
                    break
                
                if curr != self.start_coord:
                    self.my_gui_boxes[r][c].config(bg="#3498db")
                    self.root.update()
                    self.root.after(10)

                neighbors, count = generate_neighbors(curr, self.dim, self.dim)
                for i in range(count):
                    nr, nc = neighbors[i]
                    if self.grid_state[nr][nc] == 0:
                        if algo == "BFS":
                            if not visited_map[nr][nc]:
                                visited_map[nr][nc] = True
                                parents_map[nr][nc] = curr
                                struct.enqueue_bfs((nr, nc))
                        else:
                            if not visited_map[nr][nc]:
                                parents_map[nr][nc] = curr
                                struct.push_dfs((nr, nc))

            if found:
                path_arr, p_size = trace_and_print_path(parents_map, self.goal_coord, self.start_coord)
                self.cost_display.config(text=f"Total Cost: {p_size - 1}")
                for i in range(p_size):
                    pr, pc = path_arr[i]
                    if (pr, pc) != self.start_coord and (pr, pc) != self.goal_coord:
                        self.my_gui_boxes[pr][pc].config(bg="#f1c40f")
                        self.root.update()
                        
                messagebox.showinfo("Search Complete", f"Path found!\nTotal Cost: {p_size - 1}")
            else:
                messagebox.showinfo("Result", "No path exists to the goal!")