import matplotlib.pyplot as plt
import colorExample.colorStyle as cst

labelFontStyle = {'family':'Arial', 'size':10, 'weight':'black'}

file_names = ["/camp_its", "/camp_mail", "/camp_vpn",
              "/ip58", "/ip129",
              "/time_01", "/time_15", "/time_18",
              "/VR_4K", "/VR_8K", "/VR_output", "/VR_shotGame", "/VR_worldGame"]
test_names = ["/camp_vpn"]
file_names = ["/bilibili_output", "/pku_disk_output", "/liveoutput", "/videooutput"]
for file_name in file_names:
    # Read data from the file
    data_mb = []
    s_limit = 1800
    i = 0
    with open("./campus_other"+file_name+"/throughput.out", "r") as f:
        for line in f:
            # Convert bytes to MB
            throughput_mb = int(line.strip())*8 / (1024 * 1024)
            data_mb.append(throughput_mb)
            i += 1
            if i >= s_limit:
                break
    del data_mb[:5]
    del data_mb[-5:]


    # Create the x-axis (time in seconds)
    time = list(range(len(data_mb)))

    # Plot the data
    plt.plot(time, data_mb, label="Throughput", color=cst.style15.color3)

    # Fill the area under the curve with color
    # plt.fill_between(time, data_mb, color=cst.style15.color3)

    # Set labels and title
    plt.xlabel("Time (s)", font=labelFontStyle)
    plt.ylabel("Throughput (Mbps)", font=labelFontStyle)
    # plt.title("Throughput vs Time")

    plt.savefig("./campus_figs/throughput" + file_name + ".png")
    plt.savefig("./campus_figs/throughput" + file_name + ".svg", format='svg')
    plt.clf()
    # # Display the graph
    # plt.show()