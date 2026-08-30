import numpy as np
import pandas as pd

def fv(rate,pv, periods):
    rate = rate / 12 / 100
    fv= pv*(rate+1)**periods
    return fv

def pv(rate , fv , periods):
    rate = rate / 12 / 100
    pv = fv/(rate + 1)** periods
    return pv

def pmt(rate, nper, pv):
    rate = rate / 12 / 100  
    if rate == 0:
        return -pv / nper
    return -pv * rate * ((1 + rate) ** nper) / ((1 + rate) ** nper - 1)

def nper(rate , pmt ,pv , fv=0):
    rate = rate /12 /100

    if rate == 0 :
        return -(pv + fv)/ pmt

    n = np.log((pmt -(fv * rate))/(pmt+ (pv * rate )))/np.log(1 + rate)

    return n

def npv (rate , cashflows) :
    total = 0.0
    r = rate / 100
    for t ,cf in enumerate(cashflows):
        total += cf / (1 + r)**t

    return total


def irr(cashflows, guess=0.1, max_iter=100, tol=1e-6):
    rate = guess
    for _ in range(max_iter):
        if rate <= -0.99:  
            return None
        if rate > 10:     
            return None
        npv_value =npv (rate * 100 , cashflows)

        d_npv = sum(-(i+1) * cf / (1+rate)**(i+2) for i, cf in enumerate(cashflows[1:]))

        if abs(npv_value) < tol:

            return rate

        rate = rate - npv_value / d_npv

    return None

def dpp(rate ,cashflows):
    balance = 0.0
    rate = rate / 12 / 100
    for t , cf in enumerate(cashflows):
        dcf= cf/ (rate + 1) **t
        prev_balance = balance
        balance += dcf
        if balance >= 0 :
            if t == 0: 
                return 0
            
            unrecovered =abs(prev_balance)
            fractional_year = unrecovered /dcf

            return (t-1)+fractional_year
    return None

def amortization (pv, rate ,years , payments_per_year: int = 12 ):

    rate = rate /100/ payments_per_year
    nper = years * payments_per_year
    pmt =  pv * rate * ((1 + rate) ** nper) / ((1 + rate) ** nper - 1)
    
    schedule = []
    balance = pv
    for i in range (1 , nper + 1):
        beginning_balance = balance
        interest = beginning_balance * rate
        principal_paid = pmt - interest
        ending_balance = beginning_balance -  principal_paid
        balance = ending_balance
        schedule.append({
            'Periods' : i ,
            "Beginning Balance": beginning_balance,
            'Payment':pmt , 
            'Interest': interest , 
            'Principal' :principal_paid ,
            'Ending Balance' : ending_balance
        })
    return pd.DataFrame(schedule)

def ipmt (rate , pv , per , nper ):
    rate = rate / 12 / 100
    pmt_value = pmt(rate, nper, pv )
    if per == 1:
        return - (rate * pv)
    ipmt = pv*(1+rate)**(per-1) + pmt_value*((1+rate)**(per-1)-1)/rate
    return -(ipmt * rate)

def ppmt (rate , per, nper, pv) :
    pmt_value = pmt(rate, nper, pv)
    ipmt_value = ipmt(rate , pv , per , nper)
    ppmt_value = pmt_value - ipmt_value
    return ppmt_value


def wacc (equity , debt ,cost_of_equity , cost_of_debt, tax_rate ):
    total_value = equity + debt
    wacc_value = ((equity*cost_of_equity)/total_value) + ((debt * cost_of_debt * (1-tax_rate))/total_value)
    return wacc_value


def sharp_ratio (returns,annual_rf,frequency = 252):
    periodic_rf = (1+annual_rf)**(1/ frequency)-1
    returns = np.array(returns)
    excess_return = returns -periodic_rf
    mean_excess_return = excess_return.mean()
    std_dev = returns.std()
    periodic_sharp = mean_excess_return / std_dev
    annualized_sharp = periodic_sharp * np.sqrt(frequency)

    return annualized_sharp

def dscr (net_operation_income , total_debt_service , round_to :int =2):
    if total_debt_service<= 0:
        return float ('inf')
    dscr = net_operation_income / total_debt_service
    return round (dscr ,round_to)


def roa (net_income , total_asset_first , total_asset_last):
    average = (total_asset_first + total_asset_last)/2
    roa = net_income/average
    return roa

def roi (final_value , initial_investment):
    roi = ((final_value - initial_investment)/initial_investment) * 100
    return roi

def roe (net_income , equity):
    roe = net_income/equity
    return roe


print('Welcome! I’m glad to see you here.Here you can have your financial calculator,'
    ' and anything you need will be calculated for you. Stay with us and join along.')
    
print('This section is divided into three parts, and each part has its own parameters. Based on your needs, please choose one of the options.')
while True:
    main_input = input('Part one: time value of money calculations, where you can choose one option\n1)FV\n2)PV\n3)PMT\n4)NPER\n' \
                    'Part two: investment analysis\n5)NPV\n6)IRR\n7)DPP\n' \
                    'Part three: Loan Management \n8)Amortization\n9)IPMT\n10)PPMT'
                    'Part four: Risk analysis and cost of capital\n11)WACC\n12)Sharp_ratio\n13)DSCR\n14)ROA\n15)ROI\n16)ROE ')
    
    valid_choises = {'1' , '2' , '3' , '4' , '5' , '6' , '7' ,'8', '9' , '10' , '11' , '12' , '13' , '14' , '15' , '16'}
    if not main_input in valid_choises :
        print('You should pick a number between 1 and 16')


    if main_input=='1':
        while True:
            try:
                rate = float(input('Please enter your assessment rate as a decimal number:  '))
                break
            except ValueError:
                print('Enter a numeric value')
                
        while True :
            typ = input('Enter the duration in months or years:  ').strip().lower()
            if typ in ['year' , 'y' , 'سال' , 'yaers']:
                while True:
                    try:
                        year = int(input('Enter the year: '))
                        periods = year * 12
                        break
                    except ValueError:
                        print('Invalid input! Please enter a valid number for years')
                break
            elif typ in ['month' , 'monthes' , 'm' , "ماه"]:
                while True:
                    try:
                        months = int(input('Enter the months: '))
                        periods = months
                        break
                    except ValueError:
                        print('Invalid input! Please enter a valid number for monthes')
                break
            else:
                print("Erorr,You can't enter any other option")
        while True:
            try:
                pv_input = int(input('pv :'))
                break
            except ValueError:
                print('Enter a numeric value')
        result = fv(rate , pv_input , periods)
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40)
# *******************************************************************************************************************************************

    if main_input == '2':
        while True:
            try:
                rate = float(input('Please enter your assessment rate :  '))
                break
            except ValueError:
                print('Enter a numeric value')
                
        while True :
            typ = input('Enter the duration in months or years:  ').strip().lower()
            if typ in ['year' , 'y' , 'سال' , 'yaers']:
                while True:
                    try:
                        year = int(input('Enter the year: '))
                        periods = year * 12
                        break
                    except ValueError:
                        print('Invalid input! Please enter a valid number for years')
                break
            elif typ in ['month' , 'monthes' , 'm' , "ماه"]:
                while True:
                    try:
                        months = int(input('Enter the months: '))
                        periods = months
                        break
                    except ValueError:
                        print('Invalid input! Please enter a valid number for monthes')
                break
            else:
                print("Erorr,You can't enter any other option")
        while True:
            try:     
                fv_input = int (input('fv : '))
                break
            except ValueError:
                print('Enter a numeric value')
        result = pv(rate , fv_input , periods)
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40)
# **********************************************************************************************************
    if main_input == '3':
        while True:
            try:
                rate = float(input('Please enter your assessment rate as a decimal number:  '))
                break
            except ValueError:
                print('Enter a numeric value')
        while True :
            typ = input('Enter the duration in months or years:  ').strip().lower()
            if typ in ['year' , 'y' , 'سال' , 'years', 'س']:
                while True:
                    try:
                        year = int(input('Enter the year: '))
                        periods = year * 12
                        
                        break
                    except ValueError:
                        print('Invalid input! Please enter a valid number for years')
                break
            elif typ in ['month' , 'monthes' , 'm' , "ماه" ,'م']:
                while True:
                    try:
                        months = int(input('Enter the months: '))
                        periods = months
                        break
                    except ValueError:
                        print('Invalid input! Please enter a valid number for monthes')
                break
            else:
                print("Erorr,You can't enter any other option")
        while True:
            try:        
                pv_input = int(input('pv: '))
                break
            except ValueError:
                print('Enter a numeric value')
        result = pmt(rate , periods, pv_input )
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40)
#*****************************************************************************************
    if main_input == '4' :
        while True:
            try:
                rate = float(input('Please enter your assessment rate as a decimal number:  '))
                break
            except ValueError :
                print('Enter a numeric value')
        
        while True :
            try:
                pmt_input = int(input('Please enter your monthly installment: '))
                pmt_input = -abs(pmt_input)
                break
            except ValueError :
                print('Enter a numeric value')
        while True :
            try :
                pv_input =int(input('pv: '))
                break
            except ValueError:
                 print('Enter a numeric value')
        result = nper(rate , pmt_input , pv_input)
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40)

#*****************************************************************************************
    if main_input == '5' :
        while True:
            try:
                rate = float(input('Please enter your assessment rate as a decimal number:  '))
                break
            except ValueError :
                print('Enter a numeric value')
        cashflows = []
        while True:
            try:
                invest = int(input('Enter your invest:  '))
                invest = -abs(invest)

                cashflows.append(invest)
                print(invest)
                break
            except ValueError:
                print('Enter a numeric value')
        
        while True:
            try:
                investment_rounds = int(input('How many investment rounds have you completed? '))
                break
            except ValueError:
                print('Enter a numeric value')
           
        for i in range(1,investment_rounds+1):
            while True :
                try:
                    invest = int(input(f'invest {i}: '))
                    break
                except ValueError:
                    print('Enter a numeric value')
            cashflows.append(invest)
            
        print(cashflows)
            
        result = npv(rate , cashflows)
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40)

#*****************************************************************************************
    if main_input == '6' :
        cashflows = []
        while True :
            try :
                invest = float(input('Enter your invest: '))
                invest = -abs(invest)

                cashflows.append(invest)
                print(invest)
                break
            except ValueError:
                print('Enter a numeric value')
        
        while True:
            try :
                 n = int(input('How many investment rounds have you completed? '))
                 break
            except ValueError :
                    print('Enter a numeric value')
            
        for j in range (1 , n+1) :
            while True:
                try:
                    invest_user = float(input(f'invest {j}: '))
                    break
                except ValueError :
                    print('Enter a numeric value')                                               
            cashflows.append(invest_user) 

        print(cashflows)
        result = irr(cashflows)
        if result is None:
            print("IRR cannot be calculated (the cash flows did not converge)")
        else:
            print(result * 100)
        print("\n" + "—"*40)



#*****************************************************************************************
    if main_input == '7':
        while True :
            try:
                rate = int(input('Please enter your assessment rate as a decimal number:  '))
                break
            except ValueError :
                print('Enter a numeric value') 

        cashflows = []
        while True:
            try:
                invest = int(input('Enter your invest:  '))
                invest = -abs(invest)

                cashflows.append(invest)
                print(invest)
                break
            except ValueError:
                print('Enter a numeric value')
        while True:
            try:
                n = int(input('How many investment rounds have you completed? '))
                break
            except ValueError:
                print('Enter a numeric value') 
        for i in range(1 ,n + 1):
            while True :
                try:
                    user_invest = int(input(f'invest {i}: '))
                    cashflows.append(user_invest)
                    break
                    
                except ValueError :
                     print('Enter a numeric value')
        result = dpp(rate ,cashflows)
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40)
#***********************************************************************
    if main_input == '8' :
        while True :
            try:
                rate = int(input('Please enter your assessment rate as a decimal number:  '))
                break
            except ValueError :
                print('Enter a numeric value') 
        while True :
            try:
                years = int(input('Please enter years:  '))
                break
            except ValueError :
                print('Enter a numeric value') 
        while True :
            try :
                pv_input =int(input('pv: '))
                break
            except ValueError:
                 print('Enter a numeric value')
        while True :
            try:
                payments_per_year = int(input('Please enter payments_per_year:  '))
                break
            except ValueError :
                print('Enter a numeric value')         
        result =  amortization(pv_input, rate ,years ,payments_per_year )
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40)
#***********************************************************************
    if main_input == '9' :
        while True :
            try:
                rate = int(input('Please enter your assessment rate as a decimal number:  '))
                break
            except ValueError :
                print('Enter a numeric value') 
        while True :
            try :
                pv_input =int(input('pv: '))
                break
            except ValueError:
                 print('Enter a numeric value')        
        while True :
            try :
                per =int(input('per: '))
                break
            except ValueError:
                 print('Enter a numeric value')
        while True :
            try :
                nper_input =int(input('nper: '))
                break
            except ValueError:
                 print('Enter a numeric value')
        result =  ipmt (rate , pv_input , per , nper_input )
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40)
#***********************************************************************
    if main_input == '10' :
        while True :
            try:
                rate = int(input('Please enter your assessment rate as a decimal number:  '))
                break
            except ValueError :
                print('Enter a numeric value') 
        while True :
            try :
                pv_input =int(input('pv: '))
                break
            except ValueError:
                 print('Enter a numeric value')        
        while True :
            try :
                per =int(input('per: '))
                break
            except ValueError:
                 print('Enter a numeric value')
        while True :
            try :
                nper_input =int(input('nper: '))
                break
            except ValueError:
                 print('Enter a numeric value')
        result =  ppmt (rate , per, nper_input, pv_input )
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40)
#***********************************************************************
    if main_input == '11' :
        while True :
            try:
                equity = int(input('equity:  '))
                break
            except ValueError :
                print('Enter a numeric value') 
        while True :
            try:
                debt = int(input('debt:  '))
                break
            except ValueError :
                print('Enter a numeric value') 
        while True :
            try:
                cost_of_equity = float(input('cost_of_equity:  '))
                break
            except ValueError :
                print('Enter a numeric value') 
        while True :
            try:
                cost_of_debt= float(input('cost_of_debt:  '))
                break
            except ValueError :
                print('Enter a numeric value') 
        while True :
            try:
                tax_rate= float(input('tax_rate:  '))
                break
            except ValueError :
                print('Enter a numeric value')
        result = wacc (equity , debt ,cost_of_equity , cost_of_debt, tax_rate )
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40) 
#***********************************************************************
    if main_input == '12' :
        while True :
            try:
                rf_year = float(input('Annual bank interest rate:  '))
                break
            except ValueError :
                print('Enter a numeric value') 
        while True :
            try:
                interest_rate = int(input('days:  '))
                break
            except ValueError :
                print('Enter a numeric value') 
        daily=[]
        for i in range (1 , interest_rate + 1) :
            while True :
                try:
                    daily_returns = float(input('daily_returns:  '))
                    daily.append(daily_returns)
                    break
                except ValueError :
                    print('Enter a numeric value')  
        result = sharp_ratio(daily , rf_year)  
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40) 
#***********************************************************************
    if main_input == '13' :
        while True :
            try :
                net_operation_income = float(input('net_operation_income: '))
                break
            except ValueError :
                    print('Enter a numeric value')
        while True :
            try :
                total_debt_service = float(input('total_debt_service: '))
                break
            except ValueError :
                    print('Enter a numeric value')

        result = dscr (net_operation_income , total_debt_service)  
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40) 
#*********************************************************************** 
    if main_input == '14':
        while True :
            try:
                net_income = int(input('net_income: '))
                break
            except ValueError :
                    print('Enter a numeric value')
        while True :
            try:
                total_asset_first = int(input('total_asset_first: '))
                break
            except ValueError :
                    print('Enter a numeric value')
        while True :
            try:
                total_asset_last = int(input('total_asset_last: '))
                break
            except ValueError :
                    print('Enter a numeric value')
        result = roa (net_income , total_asset_first , total_asset_last)  
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40) 

#***********************************************************************
    if main_input == '15' :
        while True :
            try:
                final_value= int(input('final_value: '))
                break
            except ValueError :
                    print('Enter a numeric value')
        while True :
            try:
                initial_investment= int(input('initial_investment: '))
                break
            except ValueError :
                    print('Enter a numeric value')
        result = roi (final_value , initial_investment)  
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40) 
#***********************************************************************  
    if main_input == '16':
        while True :
            try:
                net_income= int(input('net_income: '))
                break
            except ValueError :
                    print('Enter a numeric value') 
        while True :
            try:
                equity= int(input('equity: '))
                break
            except ValueError :
                    print('Enter a numeric value') 
        result =  roe (net_income , equity)  
        print("\n" + "—"*40)
        print(result)
        print("\n" + "—"*40) 
