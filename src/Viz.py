import plotly
import cufflinks as cf
import pandas as pd
from plotly.offline import init_notebook_mode
from ordered_set import OrderedSet

init_notebook_mode(connected=True)
cf.go_offline()


def parse_data_in_csv(file_in_csv):
    '''

    :param file_in_csv: csv file to parse
    :return: Panda Datagram representing parsed csv file
    '''
    return pd.read_csv(file_in_csv)


def initialize_dict(parsed_dataframe):
    '''

    :param parsed_dataframe: Panda Datagram representing parsed csv file
    :return: empty dict of form method :: []
    '''
    columns = parse_column(parsed_dataframe)
    return {i: [] for i in columns}


def parse_row_and_update_dict(parsed_dataframe):
    '''

    :param parsed_dataframe: Panda Datagram representing parsed csv file
    :return: updated dict of form method :: List of Runtimes
    '''
    res = initialize_dict(parsed_dataframe)

    for row in parsed_dataframe.itertuples():
        res[row.__getattribute__('method')].append(round(row.__getattribute__('runtime'), 3))

    return res


def parse_column(parsed_dataframe):
    '''

    :param parsed_dataframe: Panda Datagram representing parsed csv file
    :return: OrderedSet of methods
    '''
    return OrderedSet(parsed_dataframe['method'])


def render_box_plot_offline(data):
    '''
    saves html file with the iteractive box plot where x-axis is the methods, and y-axis being the runtime
    :param data: dictionary in form Method :: List of Runtimes
    :return: None
    '''
    df = pd.DataFrame.from_dict(data, orient='index')
    fig = df.transpose().iplot(kind='box', asFigure=True)
    plotly.offline.plot(fig, filename="testBoxplot.html")

# Test run - parses the csv data and saves html file with the interactive box plot
# parsed_dataframe = parse_data_in_csv("mockData.csv")
# render_box_plot_offline(parse_row_and_update_dict(parsed_dataframe))
