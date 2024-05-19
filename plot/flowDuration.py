import math
import matplotlib.pyplot as plt
import colorExample.colorStyle as cst

file_names = ["/camp_its", "/camp_mail", "/camp_vpn",
              "/ip58", "/ip129",
              "/time_01", "/time_15", "/time_18",
              "/VR_4K", "/VR_8K", "/VR_output", "/VR_shotGame", "/VR_worldGame"]
test_names = ["/time_01", "/time_15", "/time_18"]

iter=0
colors=[cst.style15.color3, cst.style15.color4, cst.style15.color5]
interval = 0
minimal, maximal = 0, 0
for file_name in test_names:
    # Read data from the file
    file_path = "./campus_result"+file_name+"/heavyFlowDuration.out"
    flow_durations = []

    with open(file_path, "r") as file:
        for line in file:
            duration = line.strip()
            if int(duration) != 0:
                log_duration = math.log(int(duration), 10)
                flow_durations.append(log_duration)

    # Create a histogram
    if iter == 0:
        interval = (max(flow_durations) - min(flow_durations)) / 50
        minimal = min(flow_durations)
        maximal = max(flow_durations)

    counts = [0] * 51
    for du in flow_durations:
        counts[int((du-minimal)//interval)] += 1
    proportions = [count / len(flow_durations) for count in counts]

    xtick_labels = ['' for _ in range(51)]
    for i in range(int(minimal)+1,int(maximal)):
        xtick_labels[int((i-minimal)//interval)] = i

    plt.bar([i+iter*0.33 for i in range(51)], proportions, width = 0.33,
            tick_label=xtick_labels, color = colors[iter], label=file_name)
    iter+=1


# fig, ax = plt.subplots(figsize=(10, 6))
# ax.hist(flow_durations, bins=50, edgecolor='black', color=cst.style15.color3, weights=[1./len(flow_durations)]*len(flow_durations))

plt.xlabel("Flow Duration (us, log10 scale)")
plt.ylabel("Frequency")

# Hide x-axis ticks
plt.tick_params(axis='x', which='both', length=0)
plt.legend()
# # Set axis labels and title
# ax.set_xlabel('Flow Duration (us, log10 scale)')
# ax.set_ylabel('Frequency')
# # ax.set_title('Histogram of Flow Duration (log10 scale)')


# plt.savefig("./campus_figs/flowDuration"+file_name+".png")
# plt.clf()

# Display the plot
plt.show()