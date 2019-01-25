#!/usr/bin/env python

# python modules
import os
import re
import math
import time
import numpy as np
from scipy import stats as stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns


# Get a list of keys from dictionary which has the given value
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys


# Re-order a list's element under a specific rule
def reorderList(lst, rule, values=None):
    new_list, new_values = [], []
    for r in rule:
        if r in lst:
            idx = lst.index(r)
            new_list.append(lst[idx])
            new_values.append(values[idx])
    return new_list, new_values


# Define a function for a plot
def plot(x, y, directory, x_label=None, y_label=None, title=None, x_lim_min=None, x_lim_max=None, y_lim_min=None, y_lim_max=None, x_tick_labels=None):
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o', linestyle='None')
    # number of index to markers
    i = 0
    for x_i, y_i in zip(x, y):
        ax.text(x_i, y_i, str(i), fontsize=8)
        i = i+1
    if x_label:
        ax.set_xlabel(x_label, fontsize=8)
    if y_label:
        ax.set_ylabel(y_label, fontsize=8)
    if x_tick_labels:
        ax.set_xticklabels(x_tick_labels, fontsize=8)
    if title:
        ax.set_title(title, fontsize=10)
    if x_lim_min and x_lim_max:
        plt.xlim(x_lim_min, x_lim_max)
    if y_lim_min and y_lim_max:
        plt.ylim(y_lim_min, y_lim_max)
    plt.savefig(directory+title+".png")
    plt.close(fig)


# Define a function for multiple plots
def multiplot(x, y_data, directory, y_names=None, x_label=None, y_label=None, title=None, x_lim_min=None, x_lim_max=None, y_lim_min=None, y_lim_max=None, x_tick_labels=None):
    if y_names:
        fig, (ax, lax) = plt.subplots(ncols=2, gridspec_kw={"width_ratios":[5,1]})
        for i in range(len(y_data)):
            ax.plot(x, y_data[i], label=y_names[i], linestyle='None', marker='o')
            # number of index to markers
            j = 0
            for x_j, y_j in zip(x, y_data[i]):
                ax.text(x_j, y_j, str(j), fontsize=8)
                j = j+1
    else:
        fig, ax = plt.subplots()
        for y in y_data:
            ax.plot(x, y, linestyle='--', marker='o')
            # number of index to markers
            i = 0
            for x_i, y_i in zip(x, y):
                ax.text(x_i, y_i, str(i), fontsize=8)
                i = i+1
    if x_label:
        ax.set_xlabel(x_label, fontsize=8)
    if y_label:
        ax.set_ylabel(y_label, fontsize=8)
    if x_tick_labels:
        ax.set_xticklabels(x_tick_labels, fontsize=8)
    if title:
        ax.set_title(title, fontsize=10)
    if y_names:
        h,l = ax.get_legend_handles_labels()
        lax.legend(h, l, borderaxespad=0, prop={'size': 8})
        lax.axis("off")
        plt.tight_layout()
    if x_lim_min and x_lim_max:
        plt.xlim(x_lim_min, x_lim_max)
    if y_lim_min and y_lim_max:
        plt.ylim(y_lim_min, y_lim_max)
    plt.savefig(directory+title+".png")
    plt.close(fig)


# Define a function for a 3D scatterplot
def scatterplot3D(x, y, z, directory, x_label=None, y_label=None, z_label=None, title=None, x_lim_min=None, x_lim_max=None, y_lim_min=None, y_lim_max=None, z_lim_min=None, z_lim_max=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='r', marker='o')
    # number of index to markers
    i = 0
    for x_i, y_i, z_i in zip(np.array(x)[~np.isnan(np.array(x))], np.array(y)[~np.isnan(np.array(y))], np.array(z)[~np.isnan(np.array(z))]):
        ax.text(x_i, y_i, z_i, str(i), fontsize=8)
        i = i+1
    if x_label:
        ax.set_xlabel(x_label, fontsize=8)
    if y_label:
        ax.set_ylabel(y_label, fontsize=8)
    if z_label:
        ax.set_zlabel(z_label, fontsize=8)
    if title:
        ax.set_title(title, fontsize=10)
    if x_lim_min and x_lim_max and y_lim_min and y_lim_max and z_lim_min and z_lim_max:
        if x_lim_min != x_lim_max:
            ax.set_xlim3d(x_lim_min, x_lim_max)
        if y_lim_min != y_lim_max:
            ax.set_ylim3d(y_lim_min, y_lim_max)
        if z_lim_min != z_lim_max:
            ax.set_zlim3d(z_lim_min, z_lim_max)
    plt.savefig(directory+title+".png")
    plt.close(fig)


# Define a function for a 2D multi-scatterplot
def multiscatterplot2D(data, directory, names=None, x_label=None, y_label=None, title=None, x_lim_min=None, x_lim_max=None, y_lim_min=None, y_lim_max=None, border_idx=None):
    colors = ['red', 'green', 'silver', 'rosybrown', 'firebrick',
            'grey', 'darksalmon', 'sienna', 'sandybrown', 'darkkhaki',
            'palegreen', 'lightseagreen', 'darkcyan', 'paleturquoise', 'deepskyblue',
            'royalblue', 'navy', 'lightcoral', 'brown', 'y',
            'limegreen', 'teal', 'steelblue', 'darkmagenta', 'peru']
    # print len(data)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if border_idx:
        if names:
            b, j = 0, 0
            for d, name in zip(data, names):
                x, y, _ = d
                if b <= border_idx:
                    ax.scatter(x, y, marker='o', label=name, c=colors[j])
                    j = j + 1
                else:
                    ax.plot(x, y, marker='o', label=name)
                b = b + 1

        else:
            b = 0
            for d in data:
                x, y, _ = d
                if b <= border_idx:
                    ax.scatter(x, y, marker='o')
                else:
                    ax.plot(x, y, marker='o')
                b = b + 1
    else:
        if names:
            j = 0
            for d, name in zip(data, names):
                x, y, _ = d
                ax.scatter(x, y, marker='o', label=name, c=colors[j])
                j = j + 1
        else:
            for d in data:
                x, y, _ = d
                ax.scatter(x, y, marker='o')
    if x_label:
        ax.set_xlabel(x_label, fontsize=8)
    if y_label:
        ax.set_ylabel(y_label, fontsize=8)
    if title:
        ax.set_title(title, fontsize=10)
    if names:
        chartBox = ax.get_position()
        ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.85, chartBox.height])
        ax.legend(loc='center', bbox_to_anchor=(1.15, 0.5), shadow=True, ncol=1, borderaxespad=0, prop={'size':6})
    if x_lim_min and x_lim_max and y_lim_min and y_lim_max:
        plt.xlim(x_lim_min, x_lim_max)
        plt.ylim(y_lim_min, y_lim_max)
    plt.savefig(directory+title+".png")
    plt.close(fig)


# Define a function for a 3D multi-scatterplot
def multiscatterplot3D(data, directory, names=None, x_label=None, y_label=None, z_label=None, title=None, x_lim_min=None, x_lim_max=None, y_lim_min=None, y_lim_max=None, z_lim_min=None, z_lim_max=None, border_idx=None):
    colors = ['red', 'green', 'silver', 'rosybrown', 'firebrick',
            'grey', 'darksalmon', 'sienna', 'sandybrown', 'darkkhaki',
            'palegreen', 'lightseagreen', 'darkcyan', 'paleturquoise', 'deepskyblue',
            'royalblue', 'navy', 'lightcoral', 'brown', 'y',
            'limegreen', 'teal', 'steelblue', 'darkmagenta', 'peru']
    # print len(data)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax = fig.gca(projection='3d')
    if border_idx:
        if names:
            b, j = 0, 0
            for d, name in zip(data, names):
                x, y, z = d
                if b <= border_idx:
                    ax.scatter(x, y, z, marker='o', label=name, c=colors[j])
                    j = j + 1
                else:
                    ax.plot(x, y, z, marker='o', label=name)
                b = b + 1

        else:
            b = 0
            for d in data:
                x, y, z = d
                if b <= border_idx:
                    ax.scatter(x, y, z, marker='o')
                else:
                    ax.plot(x, y, z, marker='o')
                b = b + 1
    else:
        if names:
            j = 0
            for d, name in zip(data, names):
                x, y, z = d
                ax.scatter(x, y, z, marker='o', label=name, c=colors[j])
                j = j + 1
        else:
            for d in data:
                x, y, z = d
                ax.scatter(x, y, z, marker='o')
    if x_label:
        ax.set_xlabel(x_label, fontsize=8)
    if y_label:
        ax.set_ylabel(y_label, fontsize=8)
    if z_label:
        ax.set_zlabel(z_label, fontsize=8)
    if title:
        ax.set_title(title, fontsize=10)
    if names:
        chartBox = ax.get_position()
        ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.85, chartBox.height])
        ax.legend(loc='center', bbox_to_anchor=(1.15, 0.5), shadow=True, ncol=1, borderaxespad=0, prop={'size':6})
    if x_lim_min and x_lim_max and y_lim_min and y_lim_max and z_lim_min and z_lim_max:
        if x_lim_min != x_lim_max:
            ax.set_xlim3d(x_lim_min, x_lim_max)
        if y_lim_min != y_lim_max:
            ax.set_ylim3d(y_lim_min, y_lim_max)
        if z_lim_min != z_lim_max:
            ax.set_zlim3d(z_lim_min, z_lim_max)
    plt.savefig(directory+title+".png")
    if len(data) > 2:
        plt.show(fig)
    plt.close(fig)


# Define a function for a histogram
def histogram(data, directory, x_label=None, y_label=None, title=None):
    fig, ax = plt.subplots()
    ax.hist(np.array(data)[~np.isnan(np.array(data))], color = '#539caf')
    if x_label:
        ax.set_xlabel(x_label, fontsize=8)
    if y_label:
        ax.set_ylabel(y_label, fontsize=8)
    if title:
        ax.set_title(title, fontsize=10)
    plt.savefig(directory+title+".png")
    plt.close(fig)


# Define a function for a boxplot
def boxplot(data, directory, data_label=None, y_label=None, title=None, x_tick_labels=None):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.boxplot(data)
    if data_label:
        ax.set_xlabel(data_label, fontsize=8)
    if y_label:
        ax.set_ylabel(y_label, fontsize=8)
    if x_tick_labels:
        ax.set_xticklabels(x_tick_labels, rotation=45, ha="right", fontsize=8)
    if title:
        ax.set_title(title, fontsize=10)
    plt.savefig(directory+title+".png")
    plt.close(fig)


# MAIN FUNCTION


if __name__ == "__main__":
    # expand the color palette for the plots, once and for all
    sns.set_palette(sns.color_palette("hls", 25))

    # Body 25 human pose model specific variables
    body_25_body_parts_dict = dict([ (0,  "Nose"), (1,  "Neck"), (2,  "RShoulder"), (3,  "RElbow"), (4,  "RWrist"),
                                     (5,  "LShoulder"), (6,  "LElbow"), (7,  "LWrist"), (8,  "MidHip"), (9,  "RHip"),
                                     (10, "RKnee"), (11, "RAnkle"), (12, "LHip"), (13, "LKnee"), (14, "LAnkle"),
                                     (15, "REye"), (16, "LEye"), (17, "REar"), (18, "LEar"), (19, "LBigToe"),
                                     (20, "LSmallToe"), (21, "LHeel"), (22, "RBigToe"), (23, "RSmallToe"), (24, "RHeel"),
                                     (25, "Background")
                                    ])
    body_25_body_part_pairs = [ [1, 8], [1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7],
                                [8, 9], [9, 10], [10, 11], [8, 12], [12, 13], [13, 14], [1, 0],
                                [0, 15], [15, 17], [0, 16], [16, 18], [14, 19],
                                [19, 20], [14, 21], [11, 22], [22, 23], [11, 24]
                            ]
    body_25_body_parts_LR_order_of_appearance = [ '4', '23', '3', '22', '11', '2', '10', '9', '24', '17', '15', '8', '1', '0', '16', '18', '21', '12', '13', '14', '19', '5', '6', '20', '7' ]

    # OpenPose specific variables
    element_dict = dict([ (0, "x"), (1, "y"), (2, "z"), (3, "certainty") ])

    # File I/O specific variables
    output_path = "/home/gkamaras/catkin_ws/src/openpose_ros/openpose_ros_receiver/output/"
    # output_subfolder = "take1/"
    # raw_output_file_prefix = "raw Tue Jan 15 14:21:2"   # to go from 14:21:20 to 14:21:29 (10 files -- 10 log frames)
    # tfed_output_file_prefix = "tfed Tue Jan 15 14:21:"
    # output_subfolder = "take6/"
    # raw_output_file_prefix = "raw Thu Jan 24 12:10:"   # to go from 12:10:00 to 11:10:39 (40 files -- 40 log frames)
    # tfed_output_file_prefix = "tfed Thu Jan 24 12:10:"
    # output_subfolder = "take7/"
    # raw_output_file_prefix = "raw Thu Jan 24 12:47:4"   # to go from 12:47:40 to 12:47:49 (10 files -- 10 log frames)
    # tfed_output_file_prefix = "tfed Thu Jan 24 12:47:"
    # output_subfolder = "take8/"
    # raw_output_file_prefix = "raw Thu Jan 24 13:06:"   # to go from 13:06:00 to 13:06:59 (60 files -- 60 log frames)
    # tfed_output_file_prefix = "tfed Thu Jan 24 13:06:"
    # output_folder_path = output_path + output_subfolder
    output_subfolder = "take9/"
    op_output_file_prefix = "OP Fri Jan 25 12:41:"
    raw_output_file_prefix = "raw Fri Jan 25 12:41:"   # to go from 13:06:00 to 13:06:59 (60 files -- 60 log frames)
    tfed_output_file_prefix = "tfed Fri Jan 25 12:41:"
    output_folder_path = output_path + output_subfolder
    csv_folder_path = output_folder_path + "csv/"
    plots_folder_path = output_folder_path + "plots/"
    statistics_folder_path = output_folder_path + "statistics/"
    # label_postfix = "pix"
    label_postfix = "cam"
    # label_postfix = "rob"

    # create CSVs directory
    if not os.path.exists(csv_folder_path):
        os.makedirs(csv_folder_path)

    # create plots directory
    if not os.path.exists(plots_folder_path):
        os.makedirs(plots_folder_path)
    
    # create statistics directory
    if not os.path.exists(statistics_folder_path):
        os.makedirs(statistics_folder_path)

    # create CSVs
    for key, value in body_25_body_parts_dict.items():
        fp = open(csv_folder_path + value + "CoordsAndProb" + ".csv", 'w')
        fp.close()
    for key, value in body_25_body_parts_dict.items():
        fp = open(csv_folder_path + value + ".csv", 'w')
        fp.close()
    
    # create statistics file(s)
    fp = open(statistics_folder_path + "Statistics.txt", 'w')
    fp.close()
    fp = open(statistics_folder_path + "z_table.txt", 'w')
    fp.close()
    
    # create our 3d report matrix for 10 log frames: [BodyPart][x/y/z/prob][t0,...,t9,mean,nobs,min,max,variance,skewness,kurtosis,std_dev] --> 25 * 4 * 18
    part, elem, val = 25, 4, 18
    max_files = 10
    stat_analysis_idx, mean_idx, nobs_idx, min_idx, max_idx, variance_idx, skewness_idx, kurtosis_idx, std_dev_idx = 10, 10, 11, 12, 13, 14, 15, 16, 17
    report_matrix = [ [ [ np.nan for k in range(val) ] for j in range(elem) ] for i in range(part) ]
    # # create our 3d report matrix for 40 log frames: [BodyPart][x/y/z/prob][t0,...,t39,mean,variance,skewness,kurtosis,std_dev] --> 25 * 4 * 48
    # part, elem, val = 25, 4, 48
    # max_files = 40
    # stat_analysis_idx, nobs_idx, min_idx, max_idx, mean_idx, variance_idx, skewness_idx, kurtosis_idx, std_dev_idx = 40, 40, 41, 42, 43, 44, 45, 46, 47
    # report_matrix = [ [ [ np.nan for k in range(val) ] for j in range(elem) ] for i in range(part) ]
    # # create our 3d report matrix for 60 log frames: [BodyPart][x/y/z/prob][t0,...,t59,mean,variance,skewness,kurtosis,std_dev] --> 25 * 4 * 68
    # part, elem, val = 25, 4, 68
    # max_files = 60
    # stat_analysis_idx, nobs_idx, min_idx, max_idx, mean_idx, variance_idx, skewness_idx, kurtosis_idx, std_dev_idx = 60, 60, 61, 62, 63, 64, 65, 66, 67
    # report_matrix = [ [ [ np.nan for k in range(val) ] for j in range(elem) ] for i in range(part) ]

    # access the files of the output directory
    file_counter = 0
    for file in os.listdir(output_folder_path):

        try:

            if os.path.isfile(os.path.join(output_folder_path, file)) and raw_output_file_prefix in file:

                # read from file
                with open( os.path.join(output_folder_path, file), 'r' ) as fp:

                    for cnt, line in enumerate(fp):
                        if "Body" not in line and line.strip():     # ignore header lines and empty lines
                            body_part = re.search('kp (.*):', line).group(1)
                            coords_and_prob = re.findall(r'\d+\.\d+', line)

                            # write in the appropriate CSV
                            with open(csv_folder_path + body_part + "CoordsAndProb" + ".csv", 'a') as fp:
                                string = ""
                                coord_or_prob_idx = 0
                                for i in coords_and_prob:
                                    if string.strip():
                                        string = string + ","
                                    string = string + str(i)

                                    # fill report matrix
                                    report_matrix[ getKeysByValue(body_25_body_parts_dict, body_part)[0] ][coord_or_prob_idx][file_counter] = float(i)

                                    coord_or_prob_idx = coord_or_prob_idx + 1

                                string = string + "\n"
                                fp.write(string)
            
                file_counter = file_counter + 1

                if file_counter == max_files:
                    break
            
        except Exception as e:
            raise e


    # do statistical analysis
    occurences_accross_frames = [ 0 for i in range(part) ]
    certainty_accross_frames = [ [ 0.0 for j in range(stat_analysis_idx) ] for i in range(part) ]
    z_table = [ [ [ np.nan for k in range(stat_analysis_idx) ] for j in range(elem) ] for i in range(part) ]

    for i in range(part):

        for j in range(elem):
            # count the non-nan values
            non_nans = (~np.isnan(report_matrix[i][j][0:stat_analysis_idx])).sum(0)
            if not non_nans:
                continue

            # source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.describe.html
            description = stats.describe(np.array(report_matrix[i][j][0:stat_analysis_idx])[~np.isnan(report_matrix[i][j][0:stat_analysis_idx])])
            report_matrix[i][j][nobs_idx] = description.nobs
            report_matrix[i][j][min_idx] = np.nanmin(report_matrix[i][j][0:stat_analysis_idx], axis=0)
            report_matrix[i][j][max_idx] = np.nanmax(report_matrix[i][j][0:stat_analysis_idx], axis=0)
            report_matrix[i][j][mean_idx] = description.mean
            report_matrix[i][j][variance_idx] = description.variance
            report_matrix[i][j][skewness_idx] = description.skewness
            report_matrix[i][j][kurtosis_idx] = description.kurtosis
            report_matrix[i][j][std_dev_idx] = np.std(np.array(report_matrix[i][j][0:stat_analysis_idx])[~np.isnan(report_matrix[i][j][0:stat_analysis_idx])])

            # fill z-table
            for k in range(stat_analysis_idx):
                if not np.isnan(report_matrix[i][j][k]) and not np.isnan(report_matrix[i][j][mean_idx]) and not np.isnan(report_matrix[i][j][std_dev_idx]) and report_matrix[i][j][std_dev_idx] != 0:
                    z_table[i][j][k] = (report_matrix[i][j][k] - report_matrix[i][j][mean_idx]) / report_matrix[i][j][std_dev_idx]
                else:
                    z_table[i][j][k] = np.nan
        

        # Do a scatterplot of a certain body part's keypoints detected in space
        if (~np.isnan(report_matrix[i][0][0:stat_analysis_idx])).sum(0) and (~np.isnan(report_matrix[i][1][0:stat_analysis_idx])).sum(0) and (~np.isnan(report_matrix[i][2][0:stat_analysis_idx])).sum(0):
            scatterplot3D(    x=report_matrix[i][0][0:stat_analysis_idx], y=report_matrix[i][1][0:stat_analysis_idx], z=report_matrix[i][2][0:stat_analysis_idx],
                            x_label='X'+label_postfix, y_label='Y'+label_postfix, z_label='Z'+label_postfix,
                            title="Scatterplot of X"+label_postfix+", Y"+label_postfix+", Z"+label_postfix+" at "+body_25_body_parts_dict.get(i),
                            directory=plots_folder_path,
                            x_lim_min=np.nanmin(report_matrix[i][0][0:stat_analysis_idx]), x_lim_max=np.nanmax(report_matrix[i][0][0:stat_analysis_idx]),
                            y_lim_min=np.nanmin(report_matrix[i][1][0:stat_analysis_idx]), y_lim_max=np.nanmax(report_matrix[i][1][0:stat_analysis_idx]),
                            z_lim_min=np.nanmin(report_matrix[i][2][0:stat_analysis_idx]), z_lim_max=np.nanmax(report_matrix[i][2][0:stat_analysis_idx])
                        )

        # Do a boxplot for a certain body part's keypoints elements
        # first, sanitize data
        x = np.array(report_matrix[i][0][0:stat_analysis_idx])[~np.isnan(np.array(report_matrix[i][0][0:stat_analysis_idx]))]
        y = np.array(report_matrix[i][1][0:stat_analysis_idx])[~np.isnan(np.array(report_matrix[i][1][0:stat_analysis_idx]))]
        z = np.array(report_matrix[i][2][0:stat_analysis_idx])[~np.isnan(np.array(report_matrix[i][2][0:stat_analysis_idx]))]
        # second, plot them
        boxplot(    data=[x, y, z],
                    data_label=body_25_body_parts_dict.get(i),
                    title="Boxplot of X"+label_postfix+", Y"+label_postfix+", Z"+label_postfix+" at "+body_25_body_parts_dict.get(i),
                    directory=plots_folder_path,
                    x_tick_labels=["X"+label_postfix, "Y"+label_postfix, "Z"+label_postfix]
                )

        # Count occurences accross log frames
        occurences_accross_frames[i] = (~np.isnan(report_matrix[i][ getKeysByValue(element_dict, "certainty")[0] ][0:stat_analysis_idx])).sum(0)

        # Log certainty accross frames
        for k in range(stat_analysis_idx):
            if ~np.isnan(report_matrix[i][ getKeysByValue(element_dict, "certainty")[0] ][k]):
                certainty_accross_frames[i][k] = report_matrix[i][ getKeysByValue(element_dict, "certainty")[0] ][k]


    # Collect the elements of each body part
    x_col, y_col, z_col, certainty_col = [], [], [], []
    for i in range(part):
        x_col.append(report_matrix[i][ getKeysByValue(element_dict, "x")[0] ][0:stat_analysis_idx])
        y_col.append(report_matrix[i][ getKeysByValue(element_dict, "y")[0] ][0:stat_analysis_idx])
        z_col.append(report_matrix[i][ getKeysByValue(element_dict, "z")[0] ][0:stat_analysis_idx])
        certainty_col.append(report_matrix[i][ getKeysByValue(element_dict, "certainty")[0] ][0:stat_analysis_idx])

    # Sanitize collected data
    for i in range(len(x_col)):
        x_col[i] = np.array(x_col[i])[~np.isnan(x_col[i])]
        y_col[i] = np.array(y_col[i])[~np.isnan(y_col[i])]
        z_col[i] = np.array(z_col[i])[~np.isnan(z_col[i])]
        certainty_col[i] = np.array(certainty_col[i])[~np.isnan(certainty_col[i])]
    
    # Trim data to what is not empty
    x_data = [ x_c for x_c in x_col if len(x_c) ]
    x_x_tick_labels = [ str(i) for i in body_25_body_parts_dict if i < len(x_col) and len(x_col[i]) ]
    y_data = [ y_c for y_c in y_col if len(y_c) ]
    y_x_tick_labels = [ str(i) for i in body_25_body_parts_dict if i < len(y_col) and len(y_col[i]) ]
    z_data = [ z_c for z_c in z_col if len(z_c) ]
    z_x_tick_labels = [ str(i) for i in body_25_body_parts_dict if i < len(z_col) and len(z_col[i]) ]
    certainty_data = [ certainty_c for certainty_c in certainty_col if len(certainty_c) ]
    certainty_x_tick_labels = [ str(i) for i in body_25_body_parts_dict if i < len(certainty_col) and len(certainty_col[i]) ]

    # Re-order data in order of appearance
    x_x_tick_labels_LR, x_data_LR = reorderList(x_x_tick_labels, body_25_body_parts_LR_order_of_appearance, x_data)
    y_x_tick_labels_LR, y_data_LR = reorderList(y_x_tick_labels, body_25_body_parts_LR_order_of_appearance, y_data)
    z_x_tick_labels_LR, z_data_LR = reorderList(z_x_tick_labels, body_25_body_parts_LR_order_of_appearance, z_data)
    certainty_x_tick_labels_LR, certainty_data_LR = reorderList(certainty_x_tick_labels, body_25_body_parts_LR_order_of_appearance, certainty_data)

    # Do a boxplot for each body parts' element
    boxplot(    data=x_data_LR,
                data_label="BODY_25 human pose model body parts",
                title="Boxplot of x values for all BODY_25 human pose model body parts",
                directory=plots_folder_path,
                x_tick_labels=[ body_25_body_parts_dict.get(int(i)) for i in x_x_tick_labels_LR ]
            )
    boxplot(    data=y_data_LR,
                data_label="BODY_25 human pose model body parts",
                title="Boxplot of y value for all BODY_25 human pose model body parts",
                directory=plots_folder_path,
                x_tick_labels=[ body_25_body_parts_dict.get(int(i)) for i in y_x_tick_labels_LR ]
            )
    boxplot(    data=z_data_LR,
                data_label="BODY_25 human pose model body parts",
                title="Boxplot of z value for all BODY_25 human pose model body parts",
                directory=plots_folder_path,
                x_tick_labels=[ body_25_body_parts_dict.get(int(i)) for i in z_x_tick_labels_LR ]
            )
    boxplot(    data=certainty_data_LR,
                data_label="BODY_25 human pose model body parts",
                title="Boxplot of certainty value for all BODY_25 human pose model body parts",
                directory=plots_folder_path,
                x_tick_labels=[ body_25_body_parts_dict.get(int(i)) for i in certainty_x_tick_labels_LR ]
            )

    # Repeat, with median normalization
    # Collect the elements of each body part
    x_col, y_col, z_col, certainty_col = [], [], [], []
    for i in range(part):
        x_col.append(report_matrix[i][ getKeysByValue(element_dict, "x")[0] ][0:stat_analysis_idx])
        y_col.append(report_matrix[i][ getKeysByValue(element_dict, "y")[0] ][0:stat_analysis_idx])
        z_col.append(report_matrix[i][ getKeysByValue(element_dict, "z")[0] ][0:stat_analysis_idx])
        certainty_col.append(report_matrix[i][ getKeysByValue(element_dict, "certainty")[0] ][0:stat_analysis_idx])

    # Perform median normalization to the collected data
    for i in range(len(x_col)):
        for j in range(len(x_col[i])):
            if not np.isnan(x_col[i][j]):
                x_col[i][j] = x_col[i][j] - report_matrix[i][ getKeysByValue(element_dict, "x")[0] ][mean_idx]
            if not np.isnan(y_col[i][j]):
                y_col[i][j] = y_col[i][j] - report_matrix[i][ getKeysByValue(element_dict, "y")[0] ][mean_idx]
            if not np.isnan(z_col[i][j]):
                z_col[i][j] = z_col[i][j] - report_matrix[i][ getKeysByValue(element_dict, "z")[0] ][mean_idx]
            if not np.isnan(certainty_col[i][j]):
                certainty_col[i][j] = certainty_col[i][j] - report_matrix[i][ getKeysByValue(element_dict, "certainty")[0] ][mean_idx]

    # Sanitize collected data
    for i in range(len(x_col)):
        x_col[i] = np.array(x_col[i])[~np.isnan(x_col[i])]
        y_col[i] = np.array(y_col[i])[~np.isnan(y_col[i])]
        z_col[i] = np.array(z_col[i])[~np.isnan(z_col[i])]
        certainty_col[i] = np.array(certainty_col[i])[~np.isnan(certainty_col[i])]
    
    # Trim data to what is not empty
    x_data = [ x_c for x_c in x_col if len(x_c) ]
    x_x_tick_labels = [ str(i) for i in body_25_body_parts_dict if i < len(x_col) and len(x_col[i]) ]
    y_data = [ y_c for y_c in y_col if len(y_c) ]
    y_x_tick_labels = [ str(i) for i in body_25_body_parts_dict if i < len(y_col) and len(y_col[i]) ]
    z_data = [ z_c for z_c in z_col if len(z_c) ]
    z_x_tick_labels = [ str(i) for i in body_25_body_parts_dict if i < len(z_col) and len(z_col[i]) ]
    certainty_data = [ certainty_c for certainty_c in certainty_col if len(certainty_c) ]
    certainty_x_tick_labels = [ str(i) for i in body_25_body_parts_dict if i < len(certainty_col) and len(certainty_col[i]) ]

    # Re-order data in order of appearance
    x_x_tick_labels_LR, x_data_LR = reorderList(x_x_tick_labels, body_25_body_parts_LR_order_of_appearance, x_data)
    y_x_tick_labels_LR, y_data_LR = reorderList(y_x_tick_labels, body_25_body_parts_LR_order_of_appearance, y_data)
    z_x_tick_labels_LR, z_data_LR = reorderList(z_x_tick_labels, body_25_body_parts_LR_order_of_appearance, z_data)
    certainty_x_tick_labels_LR, certainty_data_LR = reorderList(certainty_x_tick_labels, body_25_body_parts_LR_order_of_appearance, certainty_data)

    # Do a boxplot for each body parts' element
    boxplot(    data=x_data_LR,
                data_label="BODY_25 human pose model body parts",
                title="Boxplot of x values for all BODY_25 human pose model body parts after median normalization",
                directory=plots_folder_path,
                x_tick_labels=[ body_25_body_parts_dict.get(int(i)) for i in x_x_tick_labels_LR ]
            )
    boxplot(    data=y_data_LR,
                data_label="BODY_25 human pose model body parts",
                title="Boxplot of y value for all BODY_25 human pose model body parts after median normalization",
                directory=plots_folder_path,
                x_tick_labels=[ body_25_body_parts_dict.get(int(i)) for i in y_x_tick_labels_LR ]
            )
    boxplot(    data=z_data_LR,
                data_label="BODY_25 human pose model body parts",
                title="Boxplot of z value for all BODY_25 human pose model body parts after median normalization",
                directory=plots_folder_path,
                x_tick_labels=[ body_25_body_parts_dict.get(int(i)) for i in z_x_tick_labels_LR ]
            )
    boxplot(    data=certainty_data_LR,
                data_label="BODY_25 human pose model body parts",
                title="Boxplot of certainty value for all BODY_25 human pose model body parts after median normalization",
                directory=plots_folder_path,
                x_tick_labels=[ body_25_body_parts_dict.get(int(i)) for i in certainty_x_tick_labels_LR ]
            )


    # Plot certainty accross frames
    # first, for each body part individually
    for i in range(part):
        plot(   x=[ j for j in range(stat_analysis_idx) ],
                y=certainty_accross_frames[i],
                x_label="Frame",
                y_label=body_25_body_parts_dict.get(i) + " certainty",
                title="Plot of " + body_25_body_parts_dict.get(i) + " certainty accross frames",
                directory=plots_folder_path,
                x_tick_labels=[str(j) for j in range(stat_analysis_idx)]
            )
    # second, for all body part pairs
    for pair in body_25_body_part_pairs:
        plot(   x=certainty_accross_frames[pair[0]],
                y=certainty_accross_frames[pair[1]],
                x_label=body_25_body_parts_dict.get(pair[0]) + " certainty",
                y_label=body_25_body_parts_dict.get(pair[1]) + " certainty",
                title="Plot of " + body_25_body_parts_dict.get(pair[0]) + " and " + body_25_body_parts_dict.get(pair[1]) + " certainty accross frames",
                directory=plots_folder_path
            )
    # third, for all body parts collectivelly
    multiplot(  x=[ i for i in range(stat_analysis_idx) ],
                y_data=certainty_accross_frames,
                y_names=[ body_25_body_parts_dict.get(i) for i in range(part) ],
                y_lim_min=0.0,
                y_lim_max=1.0,
                x_label="Frame",
                y_label="Body parts certainty",
                title="Plot of body parts certainty accross frames",
                directory=plots_folder_path,
                x_tick_labels=[str(j) for j in range(stat_analysis_idx)]
            )


    # Do a scatterplot for all body part pairs detected in space
    for pair in body_25_body_part_pairs:
        if (~np.isnan(report_matrix[ pair[0] ][0][0:stat_analysis_idx])).sum(0) and (~np.isnan(report_matrix[ pair[0] ][1][0:stat_analysis_idx])).sum(0) and (~np.isnan(report_matrix[ pair[0] ][2][0:stat_analysis_idx])).sum(0) and (~np.isnan(report_matrix[ pair[1] ][0][0:stat_analysis_idx])).sum(0) and (~np.isnan(report_matrix[ pair[1] ][1][0:stat_analysis_idx])).sum(0) and (~np.isnan(report_matrix[ pair[1] ][2][0:stat_analysis_idx])).sum(0):
            x1 = np.array(report_matrix[ pair[0] ][0][0:stat_analysis_idx])[~np.isnan(report_matrix[ pair[0] ][0][0:stat_analysis_idx])]
            y1 = np.array(report_matrix[ pair[0] ][1][0:stat_analysis_idx])[~np.isnan(report_matrix[ pair[0] ][1][0:stat_analysis_idx])]
            z1 = np.array(report_matrix[ pair[0] ][2][0:stat_analysis_idx])[~np.isnan(report_matrix[ pair[0] ][2][0:stat_analysis_idx])]
            x2 = np.array(report_matrix[ pair[1] ][0][0:stat_analysis_idx])[~np.isnan(report_matrix[ pair[1] ][0][0:stat_analysis_idx])]
            y2 = np.array(report_matrix[ pair[1] ][1][0:stat_analysis_idx])[~np.isnan(report_matrix[ pair[1] ][1][0:stat_analysis_idx])]
            z2 = np.array(report_matrix[ pair[1] ][2][0:stat_analysis_idx])[~np.isnan(report_matrix[ pair[1] ][2][0:stat_analysis_idx])]
            multiscatterplot3D(   data=[[x1, y1, z1], [x2, y2, z2]],
                                x_label='X'+label_postfix, y_label='Y'+label_postfix, z_label='Z'+label_postfix,
                                title="Scatterplot of X"+label_postfix+", Y"+label_postfix+", Z"+label_postfix+" at "+body_25_body_parts_dict.get(pair[0])+" and "+body_25_body_parts_dict.get(pair[1])+" pair",
                                directory=plots_folder_path,
                                x_lim_min=np.min([np.min(x1), np.min(x2)]), x_lim_max=np.max([np.max(x1), np.max(x2)]),
                                y_lim_min=np.min([np.min(y1), np.min(y2)]), y_lim_max=np.max([np.max(y1), np.max(y2)]),
                                z_lim_min=np.min([np.min(z1), np.min(z2)]), z_lim_max=np.max([np.max(z1), np.max(z2)]),
                                names=[body_25_body_parts_dict.get(pair[0]), body_25_body_parts_dict.get(pair[1])]
                            )


    # Do a scatterplot for all body parts detected in space
    data, names, x_mins, x_maxes, y_mins, y_maxes, z_mins, z_maxes, data_means = [], [], [], [], [], [], [], [], []
    all_data, normal_data = 0, 0
    for i in range(part):
        if (~np.isnan(report_matrix[i][0][0:stat_analysis_idx])).sum(0) and (~np.isnan(report_matrix[i][1][0:stat_analysis_idx])).sum(0) and (~np.isnan(report_matrix[i][2][0:stat_analysis_idx])).sum(0):
            x = np.array(report_matrix[i][0][0:stat_analysis_idx])[~np.isnan(report_matrix[i][0][0:stat_analysis_idx])]
            y = np.array(report_matrix[i][1][0:stat_analysis_idx])[~np.isnan(report_matrix[i][1][0:stat_analysis_idx])]
            z = np.array(report_matrix[i][2][0:stat_analysis_idx])[~np.isnan(report_matrix[i][2][0:stat_analysis_idx])]
            x_mins.append(np.min(x))
            x_maxes.append(np.max(x))
            y_mins.append(np.min(y))
            y_maxes.append(np.max(y))
            z_mins.append(np.min(z))
            z_maxes.append(np.max(z))
            data.append([x, y, z])
            names.append(body_25_body_parts_dict.get(i))
            all_data = all_data + 1
            normal_data = normal_data + 1
        
    # Add to the scatterplot a skeleton of the means of the body part pairs detected in space
    pair_data = 0
    for pair in body_25_body_part_pairs:
        if not np.isnan(report_matrix[pair[0]][0][mean_idx]) and not np.isnan(report_matrix[pair[0]][1][mean_idx]) and not np.isnan(report_matrix[pair[0]][2][mean_idx]) and not np.isnan(report_matrix[pair[1]][0][mean_idx]) and not np.isnan(report_matrix[pair[1]][1][mean_idx]) and not np.isnan(report_matrix[pair[1]][2][mean_idx]):
            data.append([[report_matrix[pair[0]][0][mean_idx], report_matrix[pair[1]][0][mean_idx]], [report_matrix[pair[0]][1][mean_idx], report_matrix[pair[1]][1][mean_idx]], [report_matrix[pair[0]][2][mean_idx], report_matrix[pair[1]][2][mean_idx]]])
            names.append(body_25_body_parts_dict.get(pair[0])+" and "+body_25_body_parts_dict.get(pair[1])+" pair")
            all_data = all_data + 1
            pair_data = pair_data + 1

    # 3D scatterplot
    multiscatterplot3D( data=data,
                        x_label='X'+label_postfix, y_label='Y'+label_postfix, z_label='Z'+label_postfix,
                        title="Scatterplot of X"+label_postfix+", Y"+label_postfix+", Z"+label_postfix+" for all body parts detected in space",
                        directory=plots_folder_path,
                        x_lim_min=np.min(x_mins), x_lim_max=np.max(x_maxes),
                        y_lim_min=np.min(y_mins), y_lim_max=np.max(y_maxes),
                        z_lim_min=np.min(z_mins), z_lim_max=np.max(z_maxes),
                        names=names,
                        border_idx=all_data-pair_data-1
                    )

    # 2D scatterplot
    multiscatterplot2D( data=data,
                        x_label='X'+label_postfix, y_label='Y'+label_postfix,
                        title="Scatterplot of X"+label_postfix+", Y"+label_postfix+" for all body parts detected in space",
                        directory=plots_folder_path,
                        x_lim_min=np.min(x_mins), x_lim_max=np.max(x_maxes),
                        y_lim_min=np.min(y_mins), y_lim_max=np.max(y_maxes),
                        names=names,
                        border_idx=all_data-pair_data-1
                    )

    # write statistical analysis report
    for i in range(part):
       # write in the appropriate CSV
        with open(csv_folder_path + body_25_body_parts_dict.get(i) + ".csv", 'a') as fp:
            print >> fp , "elem,t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,nobs,min,max,mean,variance,skewness,kurtosis,std_dev"
            for j in range(elem):
                print >> fp , element_dict.get(j) + "," + (",".join( str(e) for e in report_matrix[i][j] ))


    # report occurences accross frames
    with open(statistics_folder_path + "Statistics.txt", 'w') as fp:
        print >> fp , "BODY_25 human pose model body part,Occurences accross " + str(stat_analysis_idx) + " log frames"
        for i in range(part):
            print >> fp , body_25_body_parts_dict.get(i) + "," + str(occurences_accross_frames[i])


    # report z-table
    with open(statistics_folder_path + "z_table.txt", 'w') as fp:
        print >> fp , "BODY_25 human pose model body part,z-scores accross " + str(stat_analysis_idx) + " log frames" + "\n"
        for i in range(part):
            for j in range(elem):
                print >> fp , body_25_body_parts_dict.get(i) + ":" + element_dict.get(j) + "," + str(z_table[i][j])
            print >> fp , "\n"