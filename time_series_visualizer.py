import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", sep=",", index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025))
              & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
  # Draw line plot
  fig, ax = plt.subplots(figsize=(12, 4), linewidth=0.5)
  ax.plot(df.index, df['value'])
  ax.set(title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019',
         xlabel='Date',
         ylabel='Page Views')
  ax.xaxis.set_major_locator(plt.MaxNLocator(8))

  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_bar = df.copy()
  df_bar.reset_index(inplace=True)
  
  df_bar['date'] = pd.to_datetime(df_bar['date'])
  df_bar['month'] = df_bar['date'].dt.month_name()
  df_bar['month_number'] = df_bar['date'].dt.month
  df_bar['year'] = df_bar['date'].dt.year
  df_bar = df_bar.sort_values(by='month_number',ascending=True)

  # Draw bar plot
  fig = sns.catplot(
    data=df_bar,kind='bar',
    x='year', y='value', hue='month',
    errorbar=None, legend=False,
    height=8,palette='tab10'
    ).fig
  plt.legend(loc='upper left', title = 'Months')
  plt.xlabel('Years')
  plt.ylabel('Average Page Views')
  
  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig


def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['date'] = pd.to_datetime(df_box['date'])
  df_box['month'] = df_box['date'].dt.strftime('%b')
  df_box['month_number'] = df_box['date'].dt.month
  df_box['year'] = df_box['date'].dt.year
  df_box = df_box.sort_values(by='month_number',ascending=True)
  
  # Draw box plots (using Seaborn)
  fig,ax = plt.subplots(ncols=2,figsize=(16,6),linewidth=0.5)
  
  sns.boxplot(data=df_box,
              x='year',y='value',
              ax=ax[0],width=1)
  ax[0].title.set_text('Year-wise Box Plot (Trend)')
  ax[0].set_xlabel('Year')
  ax[0].set_ylabel('Page Views')
  
  sns.boxplot(data=df_box,
             x='month',y='value',
             ax=ax[1],width=0.5)
  ax[1].title.set_text('Month-wise Box Plot (Seasonality)')
  ax[1].set_xlabel('Month')
  ax[1].set_ylabel('Page Views')
  
  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
