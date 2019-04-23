import random
import math
import sys
import os

from collections import defaultdict


directions = {
    'up': lambda i, j: (i-1, j),
    'right': lambda i, j: (i, j+1),
    'down': lambda i, j: (i+1, j),
    'left': lambda i, j: (i, j-1),
}



class Maze:
    def __init__(self):
        self.maze = []
        self.entry = ()
        self.exit = ()
        self.empty_len = 0
        self.size = 0
        self.current_state = []
        self.t = 100000
        self.k = 0.8
        self.found = False
        self.max_iterations = 15000
        self.visited = {}
        
    def read_file(self, filepath):
        with open(os.path.join(f'files/{filepath}'), 'r') as f:
            f.readline()
            for i, l in enumerate(f.readlines()):
                self.maze.append([])
                for j, c in enumerate(l.strip().split(' ')):
                    self.maze[i].append(c)
                    if c == "E":
                        self.entry = (i, j)
                    elif c == "0":
                        self.empty_len += 1
                    elif c == "S":
                        self.exit = (i, j)
            self.size = len(self.maze)
            self.max_iterations = self.size * 1500
            self.current_state = [random.choice(list(directions.keys())) for _ in range(self.empty_len)]
            
        return self

    
    def print_p(self, i, j, visited):
        if (i, j) in visited:
            return 'S' if self.maze[i][j] == 'S' else 'E' if self.maze[i][j] == 'E' else 'x' if self.is_valid(i, j) else 'B'
        if self.maze[i][j] == '0':
            return '-'
        return self.maze[i][j]
            
    def print_state(self, visited):
        print('\n'.join([' '.join([self.print_p(i, j, visited) for j,x, in enumerate(sf)]) for i,sf in enumerate(self.maze)]), '\n')
        return self

    def is_valid(self, i, j):
        if 0 <= i < self.size and 0 <= j < self.size:
            p = self.maze[i][j]
            if self.maze[i][j] != '1': return True
        return False

    def aptitude(self, path):
        score = 0
        x, y = self.entry[0], self.entry[1]
        for i, p in enumerate(path):
            if 0 <= x < self.size and 0 <= y < self.size:
                position = self.maze[x][y]
                if position == '1':
                    break
                elif position == 'S':
                    self.found = True
                    score += 20
                    self.visited[x, y] = 1
                    print("Tempera simulada encontrou: ", x, ',', y, ' - Tamanho: ', i)
                    self.print_state(self.visited.keys())
                    break

                if (x, y) in self.visited:
                    score -= self.visited[x, y]*3
                    self.visited[x, y] += 1
                else:
                    self.visited[x, y] = 1
                    score += 3
            else:
                break
            x, y = directions[p](x, y)
        return score

    def generate_path(self, path):
        new_path = path.copy()
        for i in range(3):
            index = random.randint(0, len(path) - 1)
            new_path[index] = random.choice([k for k in directions.keys() if k != new_path[index]])
        return new_path
        
    def run(self):
        i, previous_path, previous_aptitude = 0, self.current_state, self.aptitude(self.current_state)
        best_visited = {}
        while i < self. max_iterations and not self.found and round(self.t, 10) != 0:
            if i%(self.max_iterations//200) == 0:
                self.t = round(self.t * self.k, 10)
            self.visited = {}
            new_path = self.generate_path(previous_path)
            new_aptitude = self.aptitude(new_path)

            if new_aptitude > previous_aptitude or (self.t > 0 and random.uniform(0, 1) < math.exp(-((previous_aptitude-new_aptitude)/self.t))):
                previous_path = new_path.copy()
                previous_aptitude = new_aptitude
                best_visited = self.visited.copy()

            i+= 1
        if not self.found:
            self.print_state(self.visited.keys())

    def reconstruct_path(self, came_from, current):
        total_path = [current]

        current = came_from[current]
        while current != self.entry:
            total_path.append(current)
            current = came_from[current]
            
        print("A* encontrou: ", current[0], ',', current[1], ' - Tamanho: ', len(total_path))
        self.print_state(total_path)




    def heuristic(self, start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
        

    def a_star(self):
        closed_set = set()
        open_set = set([self.entry])

        came_from = {}
        g_score = defaultdict(lambda: math.inf)
        g_score[self.entry] = 0

        f_score = defaultdict(lambda: math.inf)
        f_score[self.entry] = self.heuristic(self.entry, self.exit)

        while len(open_set) > 0:
            current = min(open_set, key=lambda x: f_score[x])
            if current == self.exit:
                return self.reconstruct_path(came_from, current)
            open_set.remove(current)
            closed_set.add(current)

            for k in directions.keys():
                neighbor = directions[k](*current)
                if not self.is_valid(*neighbor) or neighbor in closed_set:
                    continue
                
                tentative_gscore = g_score[current] + 1

                if neighbor not in open_set:
                    open_set.add(neighbor)
                elif tentative_gscore >= g_score[neighbor]:
                    continue
                
                came_from[neighbor] = current
                g_score[neighbor] = tentative_gscore
                f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, self.exit)


def main():
    m = Maze().read_file(sys.argv[1] if len(sys.argv) > 1 else 'labirinto1_10.txt')
    while not m.found:
        m.run()
    
    m.a_star()

if __name__ == '__main__':
    main()