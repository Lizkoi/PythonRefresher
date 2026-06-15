import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
import scipy.stats as stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.graphics.tsaplots import plot_acf

# Load mtcars dataset
mtcars = sm.datasets.get_rdataset("mtcars", "datasets", cache=True).data

# Fit model
model = smf.ols('mpg ~ wt + hp', data=mtcars).fit()

# Plot 1: Linearity check (Residuals vs Fitted)
plt.figure(figsize=(8, 6))
sns.residplot(x=model.fittedvalues, y=mtcars['mpg'], lowess=True,
              scatter_kws={'alpha': 0.5}, line_kws={'color': 'red', 'lw': 2})
plt.title('Residuals vs Fitted (Linearity Check)')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.axhline(0, color='black', linestyle='--', alpha=0.5)
plt.savefig('linearity_check.png')
plt.close()

# Plot 2: ACF Plot (Independence)
plt.figure(figsize=(8, 6))
plot_acf(model.resid, lags=15, title='Autocorrelation Function (ACF) of Residuals')
plt.savefig('acf_plot.png')
plt.close()

# Plot 3: Homoscedasticity (Scale-Location)
plt.figure(figsize=(8, 6))
std_resid = np.sqrt(np.abs(model.get_influence().resid_studentized_internal))
plt.scatter(model.fittedvalues, std_resid, alpha=0.5)
sns.regplot(x=model.fittedvalues, y=std_resid, lowess=True, scatter=False, line_kws={'color': 'red'})
plt.title('Scale-Location (Homoscedasticity Check)')
plt.xlabel('Fitted values')
plt.ylabel('sqrt(|Standardized Residuals|)')
plt.savefig('homoscedasticity_check.png')
plt.close()

# Plot 4: Normality (Q-Q and Histogram)
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
stats.probplot(model.resid, dist="norm", plot=plt)
plt.title('Normal Q-Q Plot')

plt.subplot(1, 2, 2)
sns.histplot(model.resid, kde=True, color='lightblue', stat="density")
# Overlay normal curve
mu, std = stats.norm.fit(model.resid)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = stats.norm.pdf(x, mu, std)
plt.plot(x, p, 'r', linewidth=2)
plt.title('Histogram of Residuals')
plt.tight_layout()
plt.savefig('normality_check.png')
plt.close()

# Plot 5: Case Diagnostics
influence = model.get_influence()
cooks_d = influence.cooks_distance[0]
leverage = influence.hat_matrix_diag

plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
plt.stem(cooks_d, markerfmt=" ", basefmt="b-")
plt.axhline(y=4/32, color='red', linestyle='--')
plt.title("Cook's Distance")

plt.subplot(2, 2, 2)
plt.stem(leverage, markerfmt=" ", basefmt="b-")
plt.axhline(y=2*(3)/32, color='blue', linestyle='--')
plt.title("Leverage Values")

plt.subplot(2, 2, 3)
plt.scatter(model.fittedvalues, model.resid, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.title("Residuals vs Fitted")

plt.subplot(2, 2, 4)
plt.plot(influence.cov_ratio, 'o')
plt.axhline(1, color='green', linestyle='--')
plt.title("COVRATIO")

plt.tight_layout()
plt.savefig('case_diagnostics.png')
plt.close()

print("All plots generated successfully.")
