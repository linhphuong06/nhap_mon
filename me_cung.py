import heapq
import numpy as np
import random
import time
import psutil
import gc
from colorama import Fore,Back

# Hàm tính khoảng cách Manhattan giữa hai điểm
def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# Hàm tìm đường đi bằng thuật toán A*
def astar(maze, start, end):
    gc.collect()

    open_list = []  # Danh sách mở
    closed_list = []  # Danh sách đóng
    print(len(maze))
    # Mỗi nút trong danh sách mở được biểu diễn bằng (f, g, h, node)
    start_node = (0, 0, manhattan_distance(start, end), start)
    heapq.heappush(open_list, start_node)

    # Lưu trữ cha của mỗi nút để tái tạo đường đi
    came_from = {}

    while open_list:
        _, g, _, current_node = heapq.heappop(open_list)
        for i in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            if (start) == (end[0] + i[0], end[1] + i[1]):
                return [start]
        if current_node == end:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            path.reverse()
            # Thu gom bộ nhớ sau khi thực hiện xong thao tác
            gc.collect()

            # Lấy thông tin về bộ nhớ RAM sau khi thực hiện thao tác
            memory_after = psutil.virtual_memory()
            return path, memory_after

        closed_list.append(current_node)

        for neighbor in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            neighbor_node = (current_node[0] + neighbor[0], current_node[1] + neighbor[1])
            # if neighbor_node[0] == -1 or neighbor_node[1] == -1 or neighbor_node[0] == rows or neighbor_node[1] == rows :
            #     print("hang xom", neighbor_node)
            # else:
            #     print("hang xom", neighbor_node, maze[neighbor_node[0]][neighbor_node[1]])
            # print("duong di", current_node, maze[current_node[0]][current_node[1]])
            if (
                0 <= neighbor_node[0] < len(maze) 
                and 0 <= neighbor_node[1] < len(maze) 
                and maze[neighbor_node[0]][neighbor_node[1]] == 0
                and neighbor_node not in closed_list
            ):
                # print("nhan", neighbor_node)
                # print("end", end, maze[end[0], end[1]])
                tentative_g = g + 1
                if neighbor_node not in [node for (_, _, _, node) in open_list]:
                    heapq.heappush(open_list, (tentative_g + manhattan_distance(neighbor_node, end), tentative_g, manhattan_distance(neighbor_node, end), neighbor_node))
                    came_from[neighbor_node] = current_node
    # Thu gom bộ nhớ sau khi thực hiện xong thao tác

    # Lấy thông tin về bộ nhớ RAM sau khi thực hiện thao tác
    memory_after = psutil.virtual_memory()
    gc.collect()

    # Tính sự khác biệt trong lượng bộ nhớ sử dụng
    return None, memory_after  # Không tìm thấy đường đi
def branch_and_bound(maze, start, end):
    gc.collect()

    cols = len(maze)
    open_list = [(0, start)]  # Hàng đợi ưu tiên với các bộ dữ liệu (f, nút)
    heapq.heapify(open_list)
    closed_list = {}
    came_from = {}
    cost = float('inf')  # Khởi tạo cost là giá trị vô cùng

    while open_list:
        current_cost, current_node = heapq.heappop(open_list)
        if current_node == end:
            # Tạo lại đường dẫn từ điển 'came_from'
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            path.reverse()
            gc.collect()

            # Lấy thông tin về bộ nhớ RAM sau khi thực hiện thao tác
            memory_after = psutil.virtual_memory()

            # Tính sự khác biệt trong lượng bộ nhớ sử dụng
            return path, memory_after

        closed_list[current_node] = current_cost

        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            row, col = current_node
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < cols and 0 <= new_col < cols and maze[new_row][new_col] == 0:
                neighbor_node = (new_row, new_col)

                new_cost = current_cost + 1  # chi phi la 1

                if neighbor_node not in closed_list or new_cost < closed_list[neighbor_node]:
                    heapq.heappush(open_list, (new_cost + manhattan_distance(neighbor_node, end), neighbor_node))
                    came_from[neighbor_node] = current_node

                # Cập nhật cost nếu new_cost nhỏ hơn
                if new_cost < cost:
                    cost = new_cost

    gc.collect()

    # Lấy thông tin về bộ nhớ RAM sau khi thực hiện thao tác
    memory_after = psutil.virtual_memory()

    # Tính sự khác biệt trong lượng bộ nhớ sử dụng
    return None, memory_after
def dis(path, random_matrix, start, end):
    if path:
        count = 1
        for row in range(len(random_matrix)):
            for col in range(len(random_matrix[0])):
                if (row, col) == start:
                    print(Back.RED+"S|"+Back.RESET, end="")
                elif (row, col) == end:
                    print(Back.RED+"E|"+Back.RESET, end="")
                elif (row, col) in path:
                    print(Back.RED+"_|" +Back.RESET, end="")
                    count += 1
                elif random_matrix[row][col] == 0:
                    print(Back.WHITE+"_|"+Back.RESET, end="")
                else:
                    print(Back.BLACK+"_|"+Back.RESET, end="")
            print()
        if (start == end): 
            print("Số bước đi ngắn nhất: 0")
        else:
            print("Số bước đi ngắn nhất: ", count)
    else:
        for row in range(len(random_matrix)):
            for col in range(len(random_matrix[0])):
                if (row, col) == start:
                    print(Back.RED+"S|"+Back.RESET, end="")
                elif (row, col) == end:
                    print(Back.RED+"E|"+Back.RESET, end="")
                elif random_matrix[row, col] == 1:
                    print(Back.BLACK+"_|"+Back.RESET, end="")
                else:
                    print(Back.WHITE+"_|"+Back.RESET, end="")
            print() 
        print("Không tìm thấy đường đi.")
    

def create_maze(rows, cols):
    # Tạo một ma trận maze ban đầu với tất cả các ô là tường
    maze = np.zeros((rows, cols), dtype=int)

    # Tạo đường đi ngang ngẫu nhiên
    for i in range(rows):
        random.seed(time.time())
        a = random.randint(0,rows-2)
        random.seed(time.time())
        b = random.randint(0,int((rows - a)/2))
        if (b<5):
            random.seed(time.time())
            a = random.randint(0,rows-3)
            random.seed(time.time())
            b = random.randint(3,15)
            maze[a:(a+b),i] = 1
        else:
            maze[i,a:(a+b)] = 1

    # Tạo các đường dọc ngẫu nhiên
    maze[:,0] = 1
    maze[0,:] = 1
    maze[rows-1,:] = 1
    maze[:,cols-1] = 1

    # for i in range(1, rows, 2):
    #     for j in range(2, cols, 2):
    #         if np.random.randint(2):
    #             maze[i, j] = 0

    return maze

def main():
    request = input("Nhập yêu cầu (start/ end): ")
    while (request == "start"):
        # Bắt đầu đo thời gian

        # Tạo mê cung và tìm đường đi
        num = random.randint(20,50)
        # random_matrix = np.random.choice([0, 1], size=(num, num), p=[0.7, 0.3])

        random_matrix = create_maze(num,num)

        start = ((random.randint(1, num-2)), (random.randint(1, num-2)))
        end = ((random.randint(1, num-2)), (random.randint(1, num-2)))
        random_matrix[end[0]][end[1]] = 0
        random_matrix[start[0]][start[1]] = 0
        
        print("Mê cung:",num)
        for row in range(len(random_matrix)):
            for col in range(len(random_matrix[0])):
                if (row,col) == start:
                    print("S", end = " ")
                elif (row, col) == end:
                    print("E", end=" ")
                else:
                    print(random_matrix[row,col], end = " ")
            print()
        start_time = time.time()
        path, memory_usage = astar(random_matrix, start, end)
        end_time = time.time()
        elapsed_time = end_time - start_time

        print("\nA*:")
        dis(path, random_matrix, start, end)
        print("Thời gian thực thi:", elapsed_time, "giây")
        print("Bộ nhớ sử dụng:", memory_usage, "KB")

        gc.collect()


        start_time = time.time()
        path, memory_usage = branch_and_bound(random_matrix, start, end)
        end_time = time.time()
        elapsed_time = end_time - start_time
                
        print("\nNhanh cận:")
        dis(path, random_matrix, start, end)
        print("Thời gian thực thi:", elapsed_time, "giây")
        print("Bộ nhớ sử dụng:", memory_usage, "KB")

        print("------------------------------------------------------------")
        request = input("Nhập yêu cầu (start/ end): ")

if __name__ == "__main__":
    main()