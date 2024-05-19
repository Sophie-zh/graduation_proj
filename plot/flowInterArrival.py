import matplotlib.pyplot as plt
import colorExample.colorStyle as cst

labelFontStyle = {'family':'Arial', 'size':10, 'weight':'black'}

file_names = ["/camp_its", "/camp_mail", "/camp_vpn",
              "/ip58", "/ip129",
              "/time_01", "/time_15", "/time_18",
              "/VR_4K", "/VR_8K", "/VR_output", "/VR_shotGame", "/VR_worldGame"]
file_names = ["/pku_disk_output"]
for file_name in file_names:
    # 读取数据
    file_path = "./campus_other"+file_name+"/flowInterArrivalTime.out"
    inter_arrival_times = []
    packet_counts = []

    with open(file_path, 'r') as f:
        for line in f.readlines():
            time, count = map(int, line.strip().split())
            if time <= 200:
                inter_arrival_times.append(time)
                packet_counts.append(count)
    inter_arrival_times.append(40)
    packet_counts.append(0)
    # 计算占比
    total_packets = sum(packet_counts)
    proportions = [count / total_packets for count in packet_counts]

    # 绘制图形
    plt.bar(inter_arrival_times, proportions, color=cst.style15.color3)
    plt.xlabel('Flow Inter-Arrival Time (us)', font=labelFontStyle)
    plt.ylabel('Proportion', font=labelFontStyle)
    # plt.title('Flow Inter-Arrival Time Distribution')
    # plt.show()
    plt.savefig("./campus_figs/flowInterArrival"+file_name+".svg", format='svg')
    plt.clf()