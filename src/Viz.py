import plotly
import cufflinks as cf
import pandas as pd
from plotly.offline import init_notebook_mode
from ordered_set import OrderedSet
import plotly.express as px

init_notebook_mode(connected=True)
cf.go_offline()


def parse_data_in_csv(file_in_csv):
    '''

    :param file_in_csv: csv file to parse
    :return: Panda Datagram representing parsed csv file
    '''
    return pd.read_csv(file_in_csv)


def initialize_dict(parsed_dataframe, with_file_name=True):
    '''

    :param with_file_name: true if initializing dict for methods with the file name as a prefix
    :param parsed_dataframe: Panda Datagram representing parsed csv file
    :return: empty dict of form method :: []
    '''
    if with_file_name:
        columns = column_with_file_name(parsed_dataframe)
        return {i: [] for i in columns}

    else:
        columns = parse_column(parsed_dataframe)
        return {i: [] for i in columns}


def parse_row_and_update_dict(parsed_dataframe, with_file_name=True):
    '''

    :param with_file_name: true if called for methods with the file name as a prefix
    :param parsed_dataframe: Panda Datagram representing parsed csv file
    :return: updated dict of form method :: List of Runtimes
    '''
    res = initialize_dict(parsed_dataframe, with_file_name)

    if with_file_name:
        for row in parsed_dataframe.itertuples():
            res[row.__getattribute__('file_name') + " :: " + row.__getattribute__('method')] \
                .append(round(row.__getattribute__('runtime'), 3))

    else:
        for row in parsed_dataframe.itertuples():
            res[row.__getattribute__('method')].append(round(row.__getattribute__('runtime'), 5))

    return res


def parse_column(parsed_dataframe):
    '''

    :param parsed_dataframe: Panda Datagram representing parsed csv file
    :return: OrderedSet of methods
    '''
    return OrderedSet(parsed_dataframe['method'])


def column_with_file_name(parsed_dataframe):
    '''

    :param parsed_dataframe: Panda Datagram representing parsed csv file
    :return: an OrderedSet of form file name :: method name
    '''

    return OrderedSet(parsed_dataframe['file_name'] + " :: " + parsed_dataframe['method'])


def count_method_frequency(parsed_dataframe):
    '''
    count how many time a method was called based on it's file name :: method name
    :param parsed_dataframe: Panda Datagram representing parsed csv file
    :return:
    '''
    columns = column_with_file_name(parsed_dataframe)
    res = {i: 0 for i in columns}
    for row in parsed_dataframe.itertuples():
        res[row.__getattribute__('file_name') + " :: " + row.__getattribute__('method')] += 1

    return res


def find_max_min_frequency(data_dict):
    '''

    :param data_dict:
    :return: the maximum method frequency
    '''
    x = [*data_dict]
    max_frequency = -1
    min_frequency = 1

    for k in x:
        max_frequency = len(data_dict[k]) if len(data_dict[k]) > max_frequency else max_frequency
        min_frequency = len(data_dict[k]) if len(data_dict[k]) < min_frequency else min_frequency

    return max_frequency, min_frequency


def unzip_runtimes(data_dict):
    '''

    :param data_dict:
    :return:
    '''
    x = [*data_dict]

    methods = []
    runtimes = []

    for key, value in data_dict.items():
        print(key)
        print(value)

    for k in x:
        print(k + " was called " + str(len(data_dict[k])))
        runtimes += data_dict[k]
        for i in range(len(data_dict[k])):
            methods.append(k)

    print(methods)
    print(runtimes)
    return methods, runtimes


def render_box_plot_offline(data):
    '''
    saves html file with the iteractive box plot where x-axis is the methods, and y-axis being the runtime
    :param data: dictionary in form Method :: List of Runtimes
    :return: None
    '''
    df = pd.DataFrame.from_dict(data, orient='index')
    fig = df.transpose().iplot(kind='box', asFigure=True)
    plotly.offline.plot(fig, filename="testBoxplot.html")


def get_figs_from_plotly(data_dict, color_map):
    '''

    :param data_dict: updated dict of form method :: List of Runtimes
    :return:
    '''
    # df = pd.DataFrame.from_dict(data_dict, orient='index')
    x, y = unzip_runtimes(data_dict)

    data = {'method': x, 'runtime': y}

    fig1 = px.box(data, x='method', y='runtime', log_y=False, color="method",
                  color_discrete_map=color_map, points="all",
                  title="Plot of all methods with runtime (ms) and frequency - more blue, higher frequency")

    plotly.offline.plot(fig1, filename="frost_graph.html")


def count_frequency(parsed_dataframe):
    '''
    count how many time a method was called solely based on it's method name
    :param parsed_dataframe: Panda Datagram representing parsed csv file
    :return:
    '''
    columns = parse_column(parsed_dataframe)
    res = {i: 0 for i in columns}
    for row in parsed_dataframe.itertuples():
        res[row.__getattribute__('method')] += 1  # TODO: Data give the data

    return res


def make_color_discrete_map(columns):
    '''

    :param columns: OrderedSet of methods representing columns
    :return: color_discrete_map in form of dict method :: color
    '''
    blues = ['rgb(30, 30,' + str(b) + ')' for b in colors_based_on_frequency(data_dict)]

    res = {i: 0 for i in columns}
    index = 0

    for column in columns:
        res[column] = blues[index]
        index += 1

    return res


def colors_based_on_frequency(data_dict):
    '''

    :param data_dict:
    :return:
    '''

    x = [*data_dict]
    colors = []
    data_max, data_min = find_max_min_frequency(data_dict)

    old_range = (data_max - data_min)
    new_range = 255

    for k in x:
        colors.append((((len(data_dict[k]) - data_min) * new_range) / old_range))

    return colors


# TODO: Apply Amdal's law
parsed_dataframe = parse_data_in_csv("data2.csv")
data_dict = parse_row_and_update_dict(parsed_dataframe)
get_figs_from_plotly(data_dict, make_color_discrete_map(column_with_file_name(parsed_dataframe)))

