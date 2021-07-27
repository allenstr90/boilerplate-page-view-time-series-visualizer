import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=["date"], index_col="date")

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025))
        & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    # todo: check https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html#matplotlib.axes.Axes.plot
    ax.plot(df.index, df['value'], color='red', linestyle='solid')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar = df_bar.groupby([df_bar.index.year, df_bar.index.month])['value'].mean()
    df_bar = df_bar.unstack()
    #print(df_bar)
    # Draw bar plot
    ax = df_bar.plot(figsize=(10, 5), kind='bar')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(labels=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                      "November", "December"], title="Months")
    fig = ax.figure
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    # todo check https://seaborn.pydata.org/generated/seaborn.boxplot.html
    ax1 = sns.boxplot(x=df_box['year'], y=df_box['value'], ax=ax1)
    ax1.set(title='Year-wise Box Plot (Trend)', xlabel='Year', ylabel='Page Views')

    ax2 = sns.boxplot(x=df_box['month'], y=df_box['value'], ax=ax2,
                      order=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], )
    ax2.set(title='Month-wise Box Plot (Seasonality)', xlabel='Month', ylabel='Page Views')
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
