import argparse
import sys

import pandas as pd
import pygal


def pie_chart_date_range(df, title, start, end):
    pie_chart = pygal.Pie()
    pie_chart.title = title
    # Expense or Income.
    type = df.columns[1]

    sliced_df = date_range_slice(df, start, end)
    unique_categories = pd.unique(sliced_df['Category'])
    for category in unique_categories:
        # Sum all transactions of the current category.
        sum = abs(sliced_df.loc[sliced_df['Category'] == category][type].sum())
        pie_chart.add(category, sum)
    pie_chart.render_to_file('pie_chart.svg')

def total_bar_graph(i_df, e_df, title):
    line_chart = pygal.Bar()
    line_chart.legend_at_bottom=True
    # Make it so the whole legend will be on just one line.
    line_chart.legend_at_bottom_columns=3
    line_chart.title = title

    # Sum entire Income/Expense column.
    i_sum = i_df.iloc[:, 1].sum()
    e_sum = e_df.iloc[:, 1].sum()
    savings = i_sum + e_sum

    line_chart.add('Total Income', i_sum)
    line_chart.add('Total Expenses', e_sum)
    line_chart.add('Total Savings', savings)
    line_chart.render_to_file('bar_graph.svg')

def date_range_slice(df, start, end):
    mask = (df['Date'] >= start) & (df['Date'] <= end)
    sliced_df = df.loc[mask]
    return sliced_df

def get_time(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    unique = pd.unique(df['Date'].dt.year)
    print(df['Date'].dt.year)
    print(unique)

def main():
    parser = argparse.ArgumentParser(description='Visualize organzied ' \
                                     'finances.')
    parser.add_argument('-d', '--debug', action='store_true', help='enable ' \
                        'debug output')
    parser.add_argument('income', help='CSV containing income')
    parser.add_argument('expenses', help='CSV containing expenses')

    args = parser.parse_args()

    try:
        income_df = pd.read_csv(args.income)
        expenses_df = pd.read_csv(args.expenses)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    # pie_chart_date_range(expenses_df, 'Test title.svg', '2020-07-04', '2020-07-06')
    # total_bar_graph(income_df, expenses_df, 'Total Income, Expenses, and Savings')
    get_time(expenses_df)

if __name__ == "__main__":
    main()