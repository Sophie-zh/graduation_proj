import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

import os
from os import path

# 分布名称映射到scipy.stats中的分布对象
distributions = {
    'Normal': stats.norm,
    'Exponential': stats.expon,
    'Bernoulli': stats.bernoulli,
    'Binomial': stats.binom,
    'Uniform': stats.uniform,
    'Pareto': stats.pareto,
    'T': stats.t,
    'LogNormal': stats.lognorm,
    'Weibull': stats.weibull_min,
    'Gamma': stats.gamma,
    'ChiSquared': stats.chi2
}


def read_data(data_path):
    interval_list = []
    with open(data_path, 'r') as file:
        for line in file:
            interval, frequency = map(int, line.split())
            interval_list.extend([interval] * frequency)
    return np.array(interval_list)


def fit_distributions(intervals):
    results = {}
    for name, dist in distributions.items():
        if name in ['Bernoulli', 'Binomial']:
            continue
        else:
            try:
                params = dist.fit(intervals)
                results[name] = params
            except Exception as e:
                print(f"Failed to fit {name}: {e}")

    p_estimate = np.mean(intervals) / np.max(intervals)
    results['Bernoulli'] = (p_estimate,)
    n_binom = np.max(intervals)
    results['Binomial'] = (n_binom, p_estimate)

    return results


def calculate_cross_entropy(intervals, distribution, params):
    try:
        if distribution in [stats.bernoulli, stats.binom]:
            pmf = distribution.pmf(intervals, *params)
        else:
            pdf = distribution.pdf(intervals, *params)
        values = np.clip(pmf if distribution in [stats.bernoulli, stats.binom] else pdf, 1e-10, 1)
        return -np.sum(np.log(values))
    except Exception as e:
        print(f"Failed to calculate entropy for {distribution.name}: {e}")
        return np.inf


def calculate_section_cdf(data_min, data_max, sec_num, distribution, params):
    sec_len = (data_max - data_min) / sec_num
    cumulated_ans = []
    for i in range(sec_num):
        pos = i * sec_len + data_min
        next_post = pos + sec_len
        proportion = distribution.cdf(next_post, *params) - distribution.cdf(pos, *params)
        cumulated_ans.append((pos, next_post, proportion))

    return cumulated_ans


def plot_best_fit_distribution(intervals, best_fit_name, best_fit_params):
    plt.figure(figsize=(10, 6))
    # Plot histogram of original data
    plt.hist(intervals, bins=30, density=True, alpha=0.6, color='g')

    # Generate points for pdf
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    dist = getattr(stats, distributions[best_fit_name].name)
    if distributions[best_fit_name] in [stats.bernoulli, stats.binom]:
        pmf = dist.pmf(np.round(x), *best_fit_params)
        plt.plot(np.round(x), pmf, 'k', linewidth=2)
    else:
        pdf = dist.pdf(x, *best_fit_params)
        plt.plot(x, pdf, 'k', linewidth=2)

    title = f"Fit results: {best_fit_name}"
    plt.title(title)
    plt.xlabel('Interval')
    plt.ylabel('Density')
    plt.show()
    plt.savefig('./img/' + file + '_' + best_fit_name + '.png')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_data_file>")
        sys.exit(1)

    # 读取该文件夹下的所有.out文件，为所有.out文件生成拟合函数和对应的图片
    file_path = sys.argv[1]

    file_list = os.listdir(file_path)
    for file in file_list:
        data_path = file_path + file
        # print(new_data_path)
        interval_list = read_data(data_path)

        fitted_distributions = fit_distributions(interval_list)

        entropies = {}
        for name, params in fitted_distributions.items():
            dist = distributions[name]
            entropy = calculate_cross_entropy(interval_list, dist, params)
            entropies[name] = entropy

        print(entropies)
        best_fit = min(entropies, key=entropies.get)

        # 将拟合结果写入文件
        with open('./fit_result.txt', 'a') as rst_file:
            rst_file.write(f"{best_fit}:\n")
            rst_file.write(f"The best fitting distribution is {best_fit} with a cross entropy of {entropies[best_fit]:.2f} \n")

        # 将拟合函数生成的分布写入文件
        cumulated_ans = calculate_section_cdf(min(interval_list), max(interval_list), 100, distributions[best_fit], fitted_distributions[best_fit])
        with open('./fit_distribution.txt', 'a') as dis_file:
            dis_file.write(file + '\n')
            for tup in cumulated_ans:
                dis_file.write("{}:{} {}\n".format(tup[0], tup[1], tup[2]))
            dis_file.write("#\n")

        # 将最优拟合画图输出
        plot_best_fit_distribution(interval_list, best_fit, fitted_distributions[best_fit])

