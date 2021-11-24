import pandas as pd
import os
import plotly.graph_objs as go


def datacleaning():
    """Provide a clean datatable for visualizations

       Read in the original Ladesaeulenregister_CSV.csv file.
       Keeps data range of dates in keep_columns variable
       Changes datatypes of several columns
       Saves the results to a csv file

    """
    #Path where the original file is saved
    path = os.path.expanduser("~/Documents/Udacity/Nanodegree DataScientist/DataDashboard/data/Ladesaeulenregister_CSV.csv")
    #Read csv-file into df
    df = pd.read_csv(path, sep=';', encoding='iso8859_15', skiprows=5)
    #List of the columns to keep
    keep_columns = ['Betreiber', 'Postleitzahl', 'Bundesland', 'Kreis/kreisfreie Stadt', 'Inbetriebnahmedatum', 'Art der Ladeeinrichung', 'Anzahl Ladepunkte']
    df = df[keep_columns]
    #Change datatypes of the columns
    df['Postleitzahl'] = df['Postleitzahl'].astype('category')
    df['Bundesland'] = df['Bundesland'].astype('category')
    df['Kreis/kreisfreie Stadt'] = df['Kreis/kreisfreie Stadt'].astype('category')
    df['Inbetriebnahmedatum'] = pd.to_datetime(df['Inbetriebnahmedatum'])
    df['Art der Ladeeinrichung'] = df['Art der Ladeeinrichung'].astype('category')

    return df

def df_p1():
    """Group clean data by year and month
       Count rows, which equals the amount of chargers (not equals charging points!)
    """
    df = datacleaning()
    df = df.groupby(df['Inbetriebnahmedatum'].dt.to_period("M"))['Betreiber'].agg('count').reset_index()
    df['Inbetriebnahmedatum'] = df['Inbetriebnahmedatum'].astype('string')

    return df

def df_p2():
    """Use df_p1 dataframe to calculate the cumulative sum along each month
    """
    df = df_p1()
    df['Betreiber'] = df['Betreiber'].cumsum()

    return df

def df_p3():
    """Create a dataframe counting the amount of chargers per Bundesland
    """
    df = datacleaning()
    df = df.groupby('Bundesland')['Betreiber'].agg('count').reset_index()

    return df

def df_p4():
    """Create a dataframe counting chargers per Art der Ladeeinrichtung
    """
    df = datacleaning()
    df = df.groupby('Art der Ladeeinrichung')['Betreiber'].agg('count').reset_index()

    return df

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots arable land from 1990 to 2015 in top 10 economies
    # as a line chart

    graph_one = []
    df = df_p2()
    x_val = df['Inbetriebnahmedatum'].tolist()
    y_val = df['Betreiber'].tolist()
    graph_one.append(
      go.Scatter(
      x = x_val,
      y = y_val,
      mode = 'lines'
      )
    )

    layout_one = dict(title = 'Total amount of chargers installed',
                yaxis = dict(title = 'Total amout of chargers'),
                )

# second chart plots ararble land for 2015 as a bar chart
    graph_two = []
    df = df_p1()
    x_val = df['Inbetriebnahmedatum'].tolist()
    y_val = df['Betreiber'].tolist()
    graph_two.append(
      go.Bar(
      x = x_val,
      y = y_val,
      )
    )

    layout_two = dict(title = 'Newly installed chargers ',
                yaxis = dict(title = 'Amount of chargers installed'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    df = df_p3()
    x_val = df['Bundesland'].tolist()
    y_val = df['Betreiber'].tolist()
    graph_three.append(
      go.Bar(
      x = x_val,
      y = y_val,
      )
    )

    layout_three = dict(title = 'Amount of chargers installed per state',
                xaxis = dict(title = 'state'),
                yaxis = dict(title = 'Total amount of chargers')
                       )

# fourth chart shows rural population vs arable land
    graph_four = []
    df = df_p4()
    x_val = df['Art der Ladeeinrichung'].tolist()
    y_val = df['Betreiber'].tolist()
    graph_four.append(
      go.Bar(
      x = x_val,
      y = y_val,
      )
    )

    layout_four = dict(title = 'Amount of chargers per type',
                xaxis = dict(title = 'Type of charger'),
                yaxis = dict(title = 'Amount of chargers'),
                )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures
