import matplotlib.pyplot as plt
import colorExample.colorStyle as cst

file_names = ["/camp_its", "/camp_mail", "/camp_vpn",
              "/ip58", "/ip129",
              "/time_01", "/time_15", "/time_18"]
file_names = ["/bilibili_output", "/pku_disk_output", "/liveoutput", "/videooutput"]
for file_name in file_names:
    # 读取数据
    file_path = "./campus_other"+file_name+"/pktInterArrivalTime.out"
    inter_arrival_times = []
    packet_counts = []

    with open(file_path, 'r') as f:
        for line in f.readlines():
            time, count = map(int, line.strip().split())
            if time <= 30:
                inter_arrival_times.append(time)
                packet_counts.append(count)

    # 计算占比
    total_packets = sum(packet_counts)
    proportions = [count / total_packets for count in packet_counts]

    # 绘制图形
    plt.bar(inter_arrival_times, proportions, color=cst.style15.color3)
    plt.xlabel('Packet Inter-Arrival Time (μs)')
    plt.ylabel('Proportion')
    # plt.title('Packet Inter-Arrival Time Distribution')
    # plt.show()

    plt.savefig("./campus_figs/pktInterArrival"+file_name+".svg", format="svg")
    plt.clf()