import pandas as pd
import plotly.graph_objs as go

def chart(name):
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(f'C:/Users/haris/OneDrive/Desktop/Harish/semester 4/dav lab project/stock market data/{name}.csv')

    # Convert the 'Date' column to a datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Create a line chart with the 'Date' column on the x-axis and 'Close' column on the y-axis, with a separate line for each symbol
    fig = go.Figure()

    for symbol in df['Symbol'].unique():
        fig.add_trace(go.Scatter(x=df[df['Symbol']==symbol]['Date'],
                                 y=df[df['Symbol']==symbol]['Close'],
                                 name=symbol))

    # Add a title and axis labels to the chart
    fig.update_layout(
        title={
            'text': "Stock Price",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Date",
        yaxis_title="Closing Price"
    )

    # Display the chart
    return fig

fig=chart('AXISBANK')
fig.show()