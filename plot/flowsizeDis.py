import math
import matplotlib.pyplot as plt
import colorExample.colorStyle as cst

file_names = ["/camp_its", "/camp_mail", "/camp_vpn", 
              "/ip58", "/ip129",
              "/time_01", "/time_15", "/time_18"]
test_names = ["/camp_its"]
file_names = ["/bilibili_output", "/pku_disk_output", "/liveoutput", "/videooutput"]
for file_name in file_names:

    # Read data from the file
    file_path = "./campus_other"+file_name+"/fiveTupleInfo.out"
    flow_size = []

    with open(file_path, "r") as file:
        for line in file:
            _, size, _  = line.split()
            if int(size) != 0 and int(size) >= 100000:
                log_size = math.log(int(size), 10)
                flow_size.append(log_size)

    # Create a histogram
    interval = (max(flow_size) - 5) / 50
    
    # print("interval: ", interval)

    size_counts = [0] * 51
    for sz in flow_size:
        size_counts[int((sz-5)//interval)] += 1
    proportions = [count / len(flow_size) for count in size_counts]

    xtick_labels = ['' for _ in range(51)]
    for i in range(5,int(max(flow_size))):
        xtick_labels[int((i-5)//interval)] = i

    plt.bar(range(51), proportions, tick_label=xtick_labels, color = cst.style15.color3)

    # ax.hist(flow_size, bins=50, color=cst.style15.color3, weights=[1./len(flow_size)]*len(flow_size))
    # ax.set_xticks(range(5, int(max(flow_size)), 1))
    # # Set axis labels and title
    # ax.set_xlabel('Flow Size (Byte, log10 scale)')
    # ax.set_ylabel('Frequency')
    # # ax.set_title('Histogram of Flow Duration (log10 scale)')

    
    plt.xlabel("Flow Size (Byte, log10 scale)")
    plt.ylabel("Frequency")
    # plt.title("Packet Count Distribution")

    # Hide x-axis ticks
    plt.tick_params(axis='x', which='both', length=0)
    plt.savefig("./campus_figs/flowsizeDis"+file_name+".svg", format="svg")
    plt.clf()


    # # Display the plot
    # plt.show()