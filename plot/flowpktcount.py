import math
import matplotlib.pyplot as plt
import colorExample.colorStyle as cst

labelFontStyle = {'family':'Arial', 'size':10, 'weight':'black'}

file_names = ["/camp_its", "/camp_mail", "/camp_vpn", 
              "/ip58", "/ip129",
              "/time_01", "/time_15", "/time_18"]
# file_names = ["/bilibili_output", "/pku_disk_output"]
file_names = ["/bilibili_output", "/pku_disk_output", "/liveoutput", "/videooutput"]
for file_name in file_names:

    # Read data from the file
    file_path = "./campus_other"+file_name+"/fiveTupleInfo.out"
    pkt_count = []

    with open(file_path, "r") as file:
        for line in file:
            pktcount, size, _  = line.split()
            if int(size) != 0 and int(size) >= 100000:
                pkt_count.append(int(pktcount))

    # Determine the number of intervals and width of each interval
    interval_count = 50
    max_count = 20000
    interval_width = (max_count - 0) // interval_count
    
    # Initialize a list to store the packet counts for each interval
    packet_counts = [0] * interval_count
    outrange_count = 0

    # Assign packets to the corresponding intervals based on their size, and accumulate the counts
    for size in pkt_count:
        index = size // interval_width
        if index >= interval_count:
            outrange_count += 1
            continue
        packet_counts[index] += 1
    
    # Calculate the total number of packets
    total_packets = len(pkt_count)

    # Calculate the proportion of packets in each interval
    packet_proportions = [count/total_packets for count in packet_counts]

    # Generate the x-axis labels, showing a label every 300 units
    xtick_labels = [i * interval_width if i * interval_width % 2000 == 0 else '' for i in range(interval_count)]

    # Plot the bar chart
    plt.bar(range(interval_count), packet_proportions, tick_label=xtick_labels, color = cst.style15.color3)
    plt.bar(range(interval_count), [0]*(interval_count-1)+[outrange_count/total_packets], bottom=packet_proportions, tick_label=xtick_labels, color = cst.style15.color5)

    # Set the axis labels and title
    plt.xlabel("Flow Packet Count", font=labelFontStyle)
    plt.ylabel("Frequency", font=labelFontStyle)
    # plt.title("Packet Count Distribution")

    # Rotate the x-axis tick labels for better clarity
    plt.xticks(rotation=30, ha="right", fontsize=7)

    # Hide x-axis ticks
    plt.tick_params(axis='x', which='both', length=0)

    # plt.savefig("./campus_figs/flowpktNew"+file_name+".png")
    plt.savefig("./campus_figs/flowpktNew" + file_name + ".svg", format="svg")
    plt.clf()

    # # Display the plot
    # plt.show()