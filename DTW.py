import numpy as np


def gen_throughput(file_path):
    last_interval = 0
    interval = 1000     # 1000us, 1ms
    init_time = -1
    throughput = []
    with open(file_path, 'r') as file:
        for line in file:
            _, _, _, _, _, pktlen, timestamp = map(int, line.split())
            if init_time == -1:
                init_time = timestamp
            cur_interval = (timestamp - init_time) // interval
            # 更新区间
            if cur_interval != last_interval:
                for i in range(last_interval, cur_interval):
                    throughput.append(0)
            last_interval = cur_interval
            # 更新包
            if len(throughput) == 0:
                throughput.append(0)
            throughput[-1] += pktlen

    return throughput


def dtw_distance(series1, series2):
    # Calculate the distance matrix
    distance_matrix = np.zeros((len(series1), len(series2)))
    for i in range(len(series1)):
        for j in range(len(series2)):
            distance_matrix[i, j] = abs(series1[i] - series2[j])

    # Initialize the accumulated cost matrix
    accumulated_cost = np.zeros((len(series1), len(series2)))
    accumulated_cost[0, 0] = distance_matrix[0, 0]

    # Initialize the first row
    for i in range(1, len(series1)):
        accumulated_cost[i, 0] = accumulated_cost[i-1, 0] + distance_matrix[i, 0]

    # Initialize the first column
    for j in range(1, len(series2)):
        accumulated_cost[0, j] = accumulated_cost[0, j-1] + distance_matrix[0, j]

    # Fill in the rest of the matrix
    for i in range(1, len(series1)):
        for j in range(1, len(series2)):
            accumulated_cost[i, j] = min(accumulated_cost[i-1, j], accumulated_cost[i, j-1], accumulated_cost[i-1, j-1]) + distance_matrix[i, j]

    # Return the DTW distance
    return accumulated_cost[-1, -1]


def find_match(series1, series2):
    # !! 注意是 series1 比 series2 短
    len1 = len(series1)
    len2 = len(series2)
    n = (len2 // len1)
    min_dist = -1
    min_pos = 0
    for i in range(n):
        pos = i * len1
        new_series2 = series2[pos: pos+len1]
        dist = dtw_distance(series1, new_series2)
        if dist < min_dist or min_dist == -1:
            min_dist = dist
            min_pos = pos

    return (min_dist, min_pos)


# Example usage:
series1 = [1, 3, 4, 9, 8]
series2 = [1, 4, 2, 7, 10, 1, 3, 0, 9, 8, 2, 8, 9, 1, 0, 3, 3, 4, 9, 8]
distance, pos = find_match(series1, series2)
sim_rate = 1 - (distance / sum(series2[pos:pos+len(series1)]))
print("DTW sim rate between series1 and series2:", sim_rate, pos)
