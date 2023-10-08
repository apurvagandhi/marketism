""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""MC2-P1: Market simulator.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  		 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  		 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  		 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  		 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 		  		  		    	 		 		   		 		  
or edited.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  		 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  		 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Apurva Gandhi  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: agandhi301		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 903862828			  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
from matplotlib import pyplot as plt  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		  		 		  		  		    	 		 		   		 		  
import pandas as pd
from util import get_data, plot_data  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def compute_portvals(orders_file="./orders/orders-01.csv", start_val=1000000, commission=9.95, impact=0.005):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    Computes the portfolio values.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param orders_file: Path of the order file or the file object  		  	   		  		 		  		  		    	 		 		   		 		  
    :type orders_file: str or file object  		  	   		  		 		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		  		 		  		  		    	 		 		   		 		  
    :type start_val: int  		  	   		  		 		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		  		 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		  		 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: pandas.DataFrame  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   	
    ### Step 1 		 		  		  		    	 		 		   		 		    		 		  		  		    	 		 		   		 		  
    # read in the orders file
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])    
    # read in the dates for the orders 
    orders_df = orders_df.sort_index()
    start_date = orders_df.index[0]		  	   		  		 		  		  		    	 		 		   		 		  
    end_date = orders_df.index[-1] 
    dates = pd.date_range(start_date, end_date)	 
    # Get symbols for the orders		
    symbols = orders_df["Symbol"].unique()
    # Read in adjusted closing prices for given symbols, date range  	   		
    prices_df = get_data(symbols, dates)  
    prices_df = prices_df.sort_index()
    # Just the spy 		
    df_prices_SPY = prices_df['SPY']	  	
    # Remove spy	 		  		  		    	 		 		   		 		  
    prices_df = prices_df[symbols]  
     # Add cash column
    prices_df['Cash'] = 1.0  
    
    ### Step 2
    trades_df  = prices_df.copy()
    trades_df[symbols] = 0
    trades_df['Cash'] = 0
    
    ### Step 3
    for index, order_row in orders_df.iterrows():
        number_of_shares = int(order_row["Shares"])
        price_of_share = prices_df.loc[index][order_row["Symbol"]]
        if order_row['Order'] == 'SELL':
            trades_df.loc[index, order_row["Symbol"]] += number_of_shares * -1
            trades_df.loc[index, "Cash"] += number_of_shares * price_of_share * 1
            trades_df.loc[index, "Cash"] -= commission
            trades_df.loc[index, "Cash"] -= (impact * price_of_share * number_of_shares)
        elif order_row['Order'] == 'BUY':
            trades_df.loc[index, order_row["Symbol"]] += number_of_shares * 1
            trades_df.loc[index, "Cash"] += number_of_shares * price_of_share * -1
            trades_df.loc[index, "Cash"] -= commission 
            trades_df.loc[index, "Cash"] -= (impact * price_of_share * number_of_shares)
    
    ### Step 4   
    holdings_df  = trades_df.copy()
    for count, (index, holdings_df_row) in enumerate(holdings_df.iterrows()):
        if count == 0:
            holdings_df.loc[index, "Cash"] +=  start_val
            prev_index = index
        else: 
            holdings_df.loc[index, :] +=  holdings_df.loc[prev_index, :]
            prev_index = index
    
    ### Step 5    
    values_df = holdings_df.copy()
    values_df = prices_df * holdings_df

    # Step 6
    portfolio_value = values_df.sum(axis=1)
    return portfolio_value  		  	   		  		 		  		  		    	 		 		   		 		  
  		
def author():  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    return "agandhi301"	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def test_code():  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    Helper function to test code  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		    		  	   		  		 		  		  		    	 		 		   		 		  
    of = "./orders/orders-01.csv"  		  	   		  		 		  		  		    	 		 		   		 		  
    sv = 1000000  		  	   		  		 		  		  		    	 		 		   		 		  	   		  		 		  		  		    	
    com = 0.0
    imp = 0.0 
    		 		   		 		  
    # Process orders  		  	   		  		 		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file=of, start_val=sv, commission=com, impact = imp )  		  	   		  		 		  		  		    	 		 		   		 		  
    if isinstance(portvals, pd.DataFrame):  		  	   		  		 		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		  		 		  		  		    	 		 		   		 		  
    else:  		  	   		  		 		  		  		    	 		 		   		 		  
        "warning, code did not return a DataFrame"  		  	   		  		 		  		  		    	 		 		   		 		    	   		  		 		  		  		    	 		 		   		 	

    # Get SPY performance over same period
    start_date = portvals.index[0]
    end_date = portvals.index[-1]
    spy = get_data([], pd.date_range(start_date, end_date))

    # Get SPY stats
    daily_ret_SPY = spy.copy()
    daily_ret_SPY[1:] = (daily_ret_SPY[1:] / daily_ret_SPY[:-1].values) - 1
    daily_ret_SPY.loc[daily_ret_SPY.index[0]] = 0

    cr_SPY = (spy.iloc[-1] / spy.iloc[0]) - 1
    adr_SPY = daily_ret_SPY[1:].mean()
    stdr_SPY = daily_ret_SPY[1:].std()
    sr_SPY = np.sqrt(252) * adr_SPY / stdr_SPY

    # Get fund stats
    daily_ret = portvals.copy()
    daily_ret[1:] = (daily_ret[1:] / daily_ret[:-1].values) - 1
    daily_ret.loc[daily_ret.index[0]] = 0

    cr = (portvals[-1] / portvals[0]) - 1
    adr = daily_ret[1:].mean()
    stdr = daily_ret[1:].std()
    sr = np.sqrt(252) * adr / stdr

    def clean(stat):
        return round(float(stat), 8)

    # Compare portfolio against $SPX
    print ("Date Range: {} to {}".format(start_date, end_date))
    print
    print ("Sharpe Ratio of Fund: {}".format(clean(sr)))
    print ("Sharpe Ratio of SPY : {}".format(clean(sr_SPY)))
    print
    print ("Cumulative Return of Fund: {}".format(clean(cr)))
    print ("Cumulative Return of SPY : {}".format(clean(cr_SPY)))
    print
    print ("Standard Deviation of Fund: {}".format(clean(stdr)))
    print ("Standard Deviation of SPY : {}".format(clean(stdr_SPY)))
    print
    print ("Average Daily Return of Fund: {}".format(clean(adr)))
    print ("Average Daily Return of SPY : {}".format(clean(adr_SPY)))
    print
    print ("Final Portfolio Value: {}".format(portvals[-1]))	  
    
    # Plot comparison to SPY
    normed_SPY = spy.div(spy.iloc[0, :], axis='columns')

    normed_portvals = portvals / portvals[0]
    plt.figure()
    plt.plot(spy.index, normed_portvals)
    plt.plot(normed_SPY.index, normed_SPY.iloc[:, 0])
    plt.legend(['Fund', 'S&P 500'])
    plt.title('Daily Portfolio Value Compared to S&P 500', fontsize=20)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Price', fontsize=18)
    plt.draw()	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		    	   		  		 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		  		 		  		  		    	 		 		   		 		  
    test_code()  		  	   		  		 		  		  		    	 		 		   		 		  
