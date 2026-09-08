# The Simple Index
## Objective
The index tracks the S&P 500 at a 10% annual volatility target. Exposure is reset on the last business day of each month. The index uses price returns (no dividiends) and subtract a 1% annual running cost.

## Index Calculations
The index level is calcuateld as:

$IL_{t} = IL_{t-1} + H_{r} \times (SP_{t}-SP_{t-1}) - IL_{r} \times C \times \frac{ days(t-1, t)}{365}$

The holding of S&P 500 is calculated on each leverage reset day $r$ as:
$H_{r} = LEV_{r} \times \frac{IL_{r}}{SP_{r}}$

The leverage is calculated on each leverage reset day $r$ as:
$LEV_{r} = \frac{TV}{RV_{r}}$

The realized volatility is calculated on each leverage reset day $r$ as:
$RV_{r} = \sqrt{\frac{252}{n-1} \times \sum_{i=r-n+1}^{r} \left( ln \frac{SP_{i}}{SP_{i-1}} \right)^{2}}$

Where:

- $IL_{t}$ is the index level on day $t$
- $IL_{t-1}$ is the index level on day $t-1$
- $H_{r}$ is the holding calculated on the previous leverage reset day $r$ before day $t$
- $LEV_{r}$ is the leverage calculated on the previous leverage reset day $r$ before day $t$. On the first moneth-end, there is no $r-1$, so $LEV_{r}$ is set to 1
- $TV$ is the target volatility, set to 10%
- $SP_{t}$ is the S&P 500 price on day $t$
- $SP_{t-1}$ is the S&P 500 price on day $t-1$
- $days(t-1, t)$ is the number of calendar days between day $t-1$ and day $t$
- $C$ is the annual running cost rate, set to 1%
- $n$ is the number of business days from the second last leverage reset day $r-1$ to the last leverage reset day $r$
- $t$ is the index calculation day
- $r$ is the previous leverage reset day
- $RV_{r}$ is the realized volatility calculated on each leverage reset day $r$

## Index Calclation Calendar
The index is calculated on each day the New York Stock Exchange is open, uisng the official S&P 500 closing level

## Index Inception Calculations
On the index inception date, the index level is set to 100. The intial leverage will be set to 1, till the first leverage reset day.