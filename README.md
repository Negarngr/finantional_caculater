# Financial Calculator (CLI)

A command-line financial calculator covering time value of money, investment
analysis, loan management, and risk/cost-of-capital metrics — built in
Python with a clean separation between the finance logic and the CLI menu.

## Features

**Time Value of Money**
- Future Value (FV)
- Present Value (PV)
- Payment (PMT)
- Number of Periods (NPER)

**Investment Analysis**
- Net Present Value (NPV)
- Internal Rate of Return (IRR) — Newton-Raphson solver
- Discounted Payback Period (DPP)

**Loan Management**
- Full Amortization Schedule
- Interest Portion of a Payment (IPMT)
- Principal Portion of a Payment (PPMT)

**Risk Analysis & Cost of Capital**
- Weighted Average Cost of Capital (WACC)
- Sharpe Ratio
- Debt Service Coverage Ratio (DSCR)
- Return on Assets (ROA)
- Return on Investment (ROI)
- Return on Equity (ROE)

## Project Structure

```
.
├── finance.py   # Pure calculation functions — no I/O, fully reusable
└── main.py      # CLI menu: one function per option, imports from finance.py
```

Keeping the finance functions separate from the menu means they can be
reused as-is in a different interface (e.g. a Streamlit app) without
touching the calculation logic.

## Requirements

- Python 3.9+
- numpy
- pandas

```bash
pip install numpy pandas
```

## Usage

```bash
python main.py
```

You'll be shown a numbered menu (1–16) grouped into the four sections
above. Pick a number, follow the prompts, and the result is printed
below a divider line.

## Example

```
Please enter your assessment rate as a decimal number: 12
Enter the duration in months or years: year
Enter the year: 1
pv: 1000

————————————————————————————————————————
1126.83
————————————————————————————————————————
```

## Notes

- Rates are entered as annual percentages (e.g. `12` for 12%) and are
  converted to a monthly rate internally.
- IRR returns `None` when the cash flows don't converge to a root (e.g.
  no sign change in the cash flow series); the menu reports this instead
  of crashing.

## Roadmap

- [ ] Streamlit UI on top of the existing `finance.py` functions
- [ ] Unit tests for each finance function
- [ ] Type hints and docstrings across `finance.py`
