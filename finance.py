import numpy as np
import pandas as pd


def fv(rate, pv, periods):
    rate = rate / 12 / 100
    return pv * (rate + 1) ** periods


def pv(rate, fv, periods):
    rate = rate / 12 / 100
    return fv / (rate + 1) ** periods


def pmt(rate, nper, pv):
    rate = rate / 12 / 100
    if rate == 0:
        return -pv / nper
    return -pv * rate * ((1 + rate) ** nper) / ((1 + rate) ** nper - 1)


def nper(rate, pmt, pv, fv=0):
    rate = rate / 12 / 100
    if rate == 0:
        return -(pv + fv) / pmt
    return np.log((pmt - (fv * rate)) / (pmt + (pv * rate))) / np.log(1 + rate)


def npv(rate, cashflows):
    total = 0.0
    r = rate / 100
    for t, cf in enumerate(cashflows):
        total += cf / (1 + r) ** t
    return total


def irr(cashflows, guess=0.1, max_iter=100, tol=1e-6):
    rate = guess
    for _ in range(max_iter):
        if rate <= -0.99:
            return None
        if rate > 10:
            return None
        npv_value = npv(rate * 100, cashflows)
        d_npv = sum(-(i + 1) * cf / (1 + rate) ** (i + 2) for i, cf in enumerate(cashflows[1:]))
        if abs(npv_value) < tol:
            return rate
        rate = rate - npv_value / d_npv
    return None


def dpp(rate, cashflows):
    balance = 0.0
    rate = rate / 12 / 100
    for t, cf in enumerate(cashflows):
        dcf = cf / (rate + 1) ** t
        prev_balance = balance
        balance += dcf
        if balance >= 0:
            if t == 0:
                return 0
            unrecovered = abs(prev_balance)
            fractional_year = unrecovered / dcf
            return (t - 1) + fractional_year
    return None


def amortization(pv, rate, years, payments_per_year: int = 12):
    rate = rate / 100 / payments_per_year
    nper = years * payments_per_year
    pmt = pv * rate * ((1 + rate) ** nper) / ((1 + rate) ** nper - 1)

    schedule = []
    balance = pv
    for i in range(1, nper + 1):
        beginning_balance = balance
        interest = beginning_balance * rate
        principal_paid = pmt - interest
        ending_balance = beginning_balance - principal_paid
        balance = ending_balance
        schedule.append({
            'Periods': i,
            'Beginning Balance': beginning_balance,
            'Payment': pmt,
            'Interest': interest,
            'Principal': principal_paid,
            'Ending Balance': ending_balance
        })
    return pd.DataFrame(schedule)


def ipmt(rate, pv, per, nper):
    rate = rate / 12 / 100
    pmt_value = pmt(rate, nper, pv)
    if per == 1:
        return -(rate * pv)
    ipmt_v = pv * (1 + rate) ** (per - 1) + pmt_value * ((1 + rate) ** (per - 1) - 1) / rate
    return -(ipmt_v * rate)


def ppmt(rate, per, nper, pv):
    pmt_value = pmt(rate, nper, pv)
    ipmt_value = ipmt(rate, pv, per, nper)
    return pmt_value - ipmt_value


def wacc(equity, debt, cost_of_equity, cost_of_debt, tax_rate):
    total_value = equity + debt
    return ((equity * cost_of_equity) / total_value) + ((debt * cost_of_debt * (1 - tax_rate)) / total_value)


def sharp_ratio(returns, annual_rf, frequency=252):
    periodic_rf = (1 + annual_rf) ** (1 / frequency) - 1
    returns = np.array(returns)
    excess_return = returns - periodic_rf
    mean_excess_return = excess_return.mean()
    std_dev = returns.std()
    periodic_sharp = mean_excess_return / std_dev
    return periodic_sharp * np.sqrt(frequency)


def dscr(net_operation_income, total_debt_service, round_to: int = 2):
    if total_debt_service <= 0:
        return float('inf')
    return round(net_operation_income / total_debt_service, round_to)


def roa(net_income, total_asset_first, total_asset_last):
    average = (total_asset_first + total_asset_last) / 2
    return net_income / average


def roi(final_value, initial_investment):
    return ((final_value - initial_investment) / initial_investment) * 100


def roe(net_income, equity):
    return net_income / equity
