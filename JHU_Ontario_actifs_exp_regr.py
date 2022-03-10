#!/usr/bin/env python3
import pandas as pan
#
#World
#
path = "//home//jean-victor//GitHub_Clones//CSSEGISandData//COVID-19//csse_covid_19_data//csse_covid_19_time_series"
Deaths_csv = path + '//' + "time_series_covid19_deaths_global.csv"
Recovered_csv = path + '//' + "time_series_covid19_recovered_global.csv"
Confirmed_csv = path + '//' + "time_series_covid19_confirmed_global.csv"
#
Deaths_df = pan.read_csv(Deaths_csv)
Recovered_df = pan.read_csv(Recovered_csv)
Confirmed_df = pan.read_csv(Confirmed_csv)
#
#Canada
#
Canada_Deaths_df = Deaths_df[Deaths_df['Country/Region'] == "Canada"]
Canada_Recovered_df = Recovered_df[Recovered_df['Country/Region'] == "Canada"]
Canada_Confirmed_df = Confirmed_df[Confirmed_df['Country/Region'] == "Canada"]
#
Canada_Deaths_df.to_csv("data/Deaths.csv", index = False)
Canada_Recovered_df.to_csv("data/Recovered.csv", index = False)
Canada_Confirmed_df.to_csv("data/Confirmed.csv", index = False)
#
from datetime import datetime as dt
col_names = list(Canada_Recovered_df.iloc[:,65:].columns)
make_dates = lambda s: dt.date(dt.strptime(s,'%m/%d/%y'))
real_dates = [make_dates(s) for s in col_names]
print_dates = [d.strftime("%-j") for d in real_dates]
#
Total_Deaths = Canada_Deaths_df.iloc[:,65:].sum(axis=0)
Total_Recovered = Canada_Recovered_df.iloc[:,65:].sum(axis=0)
Total_Confirmed = Canada_Confirmed_df.iloc[:,65:].sum(axis=0)
Total_Active = Total_Confirmed - Total_Recovered - Total_Deaths
#
from numpy import ones, array
const = list(ones(len(Total_Confirmed)))
obs = list(range(len(Total_Confirmed)))
x = array([const,obs]).T
x_df = pan.DataFrame(x, columns = ["Const", "Observation"])
#
Deaths_vs_Recovered = Total_Deaths / Total_Recovered
Deaths_vs_Active = Total_Deaths / Total_Active
Recovered_vs_Active = Total_Recovered / Total_Active
#
Recovered_vs_Confirmed = Total_Recovered / Total_Confirmed
Recovered_vs_Alive = Total_Recovered / (Total_Confirmed - Total_Deaths)
Deaths_vs_Alive = Total_Deaths / (Total_Confirmed - Total_Deaths)
Deaths_vs_Closed = Total_Deaths / (Total_Recovered + Total_Deaths)
#
import matplotlib.pyplot as plt
'''
font = {
        "family" : "normal",
        "weight" : "bold",
        "size" : 8
        }
'''
plt.rcParams.update({"font.size": 10})
#
plt.clf()
plt.plot(print_dates,Total_Active, color = "c")
plt.title("Données pour le Canada du 20200323 au 20200425")
plt.xlabel("Jour de l'année")
plt.xticks(fontsize = 4)
plt.ylabel("Nombre cumulatif de cas actifs")
plt.savefig("Cas actifs vs dates Canada 20200425")
plt.show()
#
#Québec
#
Quebec_Confirmed_df = Canada_Confirmed_df[Canada_Confirmed_df["Province/State"] == "Quebec"]
Quebec_Confirmed = Quebec_Confirmed_df.iloc[:,65:].values.tolist()[0]
#
Quebec_Recovered = Quebec_Confirmed * Recovered_vs_Confirmed
#
Quebec_Deaths_df = Canada_Deaths_df[Canada_Deaths_df["Province/State"] == "Quebec"]
Quebec_Deaths = Quebec_Deaths_df.iloc[:,65:].values.tolist()[0]
#
Quebec_Active = Quebec_Confirmed - Quebec_Recovered - Quebec_Deaths
#
#Cas confirmés au Québec
#
#import matplotlib.pyplot as plt
plt.clf()
plt.plot(print_dates,Quebec_Confirmed, color = "c")
plt.title("Québec du 20200323 au 20200425")
plt.xlabel("Jour de l'année")
plt.xticks(fontsize = 4)
plt.ylabel("Nombre cumulatif de cas confirmés")
plt.savefig("Cas confirmés vs dates Québec 20200425")
plt.show()
#
'''
from numpy import ones, array
const = list(ones(len(Quebec_Confirmed)))
obs = list(range(len(Quebec_Confirmed)))
x = array([const,obs]).T
x_df = pan.DataFrame(x, columns = ["Const", "Observation"])
'''
#
import statsmodels.api as sm
Quebec_val = list(Quebec_Confirmed)
model = sm.OLS(endog = Quebec_val, exog = x_df)
results = model.fit()
ar=results.params[1]
br=results.params[0]
print(results.summary())
#
plt.clf()
plt.rc("figure", figsize = (12, 7))
plt.text(0.01,0.05, str(results.summary()), {"fontsize": 10}, fontproperties = "monospace")
plt.axis("off")
plt.tight_layout()
plt.savefig("Régression linéaire pour les cas confirmés au Québec du 20200323 au 20200425")
plt.show()
#
from math import log
Quebec_log_val = []
for v in Quebec_Confirmed:
    Quebec_log_val.append(log(v))
#
import statsmodels.api as sm
model = sm.OLS(endog = Quebec_log_val, exog = x_df)
results = model.fit()
ar=results.params[1]
br=results.params[0]
print(results.summary())
#
plt.clf()
plt.rc("figure", figsize = (12, 7))
plt.text(0.01,0.05, str(results.summary()), {"fontsize": 10}, fontproperties = "monospace")
plt.axis("off")
plt.tight_layout()
plt.savefig("Régression exponentielle pour les cas confirmés au Québec du 20200323 au 20200425")
plt.show()
#
#Cas actifs
#
#import matplotlib.pyplot as plt
plt.clf()
plt.plot(print_dates,Quebec_Active, color = "c")
plt.title("Québec du 20200323 au 20200425 (# approx. de malades guéris)")
plt.xlabel("Jour de l'année")
plt.xticks(fontsize = 4)
plt.ylabel("Nombre cumulatif de cas confirmés")
plt.savefig("Cas actifs vs dates Québec 20200425")
plt.show()
#
#from numpy import ones, array
Quebec_val = list(Quebec_Active)
const = list(ones(len(Quebec_Active)))
obs = list(range(len(Quebec_Active)))
x = array([const,obs]).T
x_df = pan.DataFrame(x, columns = ["Const", "Observation"])
#
import statsmodels.api as sm
model = sm.OLS(endog = Quebec_val, exog = x_df)
results = model.fit()
ar=results.params[1]
br=results.params[0]
print(results.summary())
#
plt.clf()
plt.rc("figure", figsize = (12, 7))
plt.text(0.01,0.05, str(results.summary()), {"fontsize": 10}, fontproperties = "monospace")
plt.axis("off")
plt.tight_layout()
plt.savefig("Régression linéaire pour les cas actifs au Québec du 20200323 au 20200425")
plt.show()
#
from math import log
Quebec_log_val = []
for v in Quebec_Active:
    Quebec_log_val.append(log(v))
#
plt.clf()
plt.plot(print_dates,Quebec_log_val, color = "c")
plt.title("Québec du 20200323 au 20200425 (# approx. de malades guéris)")
plt.xlabel("Jour de l'année")
plt.xticks(fontsize = 4)
plt.ylabel('Log. nat. du nombre cumulatif de cas actifs')
plt.savefig("Logarithme du nombre de cas actifs au Québec 20200425")
plt.show()
"""
# 
from numpy import ones, array
const = list(ones(len(Quebec_log_val)))
obs = list(range(len(Quebec_log_val)))
x = array([const,obs]).T
x_df = pan.DataFrame(x, columns = ["Const", "Observation"])
#
"""
#import statsmodels.api as sm
model = sm.OLS(endog = Quebec_log_val, exog = x_df)
results = model.fit()
ar=results.params[1]
br=results.params[0]
print(results.summary())
#
plt.clf()
plt.rc("figure", figsize = (12, 7))
plt.text(0.01,0.05, str(results.summary()), {"fontsize": 10}, fontproperties = "monospace")
plt.axis("off")
plt.tight_layout()
plt.savefig("Régression exponentielle pour les cas actifs au Québec du 20200323 au 20200425")
plt.show()
#
#Ontario
#
Ontario_Confirmed_df = Canada_Confirmed_df[Canada_Confirmed_df["Province/State"] == "Ontario"]
Ontario_Confirmed = Ontario_Confirmed_df.iloc[:,65:].values.tolist()[0]
#
Ontario_Recovered = Ontario_Confirmed * Recovered_vs_Confirmed
#
Ontario_Deaths_df = Canada_Deaths_df[Canada_Deaths_df["Province/State"] == "Ontario"]
Ontario_Deaths = Ontario_Deaths_df.iloc[:,65:].values.tolist()[0]
#
Ontario_Active = Ontario_Confirmed - Ontario_Recovered - Ontario_Deaths
#
#import matplotlib.pyplot as plt
plt.clf()
plt.plot(print_dates,Ontario_Active, color = "c")
plt.title("Ontario du 20200323 au 20200425 (# approx. de malades guéris)")
plt.xlabel("Jour de l'année")
plt.xticks(fontsize = 4)
plt.ylabel("Nombre cumulatif de cas actifs")
plt.savefig("Cas actifs vs dates Ontario 20200425")
plt.show()
#
#from numpy import ones, array
Ontario_val = list(Ontario_Active)
const = list(ones(len(Ontario_Active)))
obs = list(range(len(Ontario_Active)))
x = array([const,obs]).T
x_df = pan.DataFrame(x, columns = ["Const", "Observation"])
#
#import statsmodels.api as sm
model = sm.OLS(endog = Ontario_val, exog = x_df)
results = model.fit()
ar=results.params[1]
br=results.params[0]
print(results.summary())
#
plt.clf()
plt.rc("figure", figsize = (12, 7))
plt.text(0.01,0.05, str(results.summary()), {"fontsize": 10}, fontproperties = "monospace")
plt.axis("off")
plt.tight_layout()
plt.savefig("Régression linéaire pour les cas actifs en Ontario du 20200323 au 20200425")
plt.show()
#
#from math import log
Ontario_log_val = []
for v in Ontario_Active:
    Ontario_log_val.append(log(v))
#
plt.clf()
plt.plot(print_dates,Ontario_log_val, color = "c")
plt.title("Ontario du 20200323 au 20200425 (# approx. de malades guéris)")
plt.xlabel("Jour de l'année")
plt.xticks(fontsize = 4)
plt.ylabel('Log. nat. du nombre cumulatif de cas actifs')
plt.savefig("Logarithme du nombre de cas actifs en Ontario 20200425")
plt.show()
#
#from numpy import ones, array
const = list(ones(len(Ontario_log_val)))
obs = list(range(len(Ontario_log_val)))
x = array([const,obs]).T
x_df = pan.DataFrame(x, columns = ["Const", "Observation"])
#
import statsmodels.api as sm
model = sm.OLS(endog = Ontario_log_val, exog = x_df)
results = model.fit()
ar=results.params[1]
br=results.params[0]
print(results.summary())
#
plt.clf()
plt.rc("figure", figsize = (12, 7))
plt.text(0.01,0.05, str(results.summary()), {"fontsize": 12}, fontproperties = "monospace")
plt.axis("off")
plt.tight_layout()
plt.savefig("Régression exponentielle pour les cas actifs en Ontario du 20200323 au 20200425")
plt.show()
#
'''
from numpy import diff
list_diff_val = list(diff(list_val))
#
plt.clf()
plt.plot(list_val[1:],list_diff_val, color = "c")
plt.title("Données pour le Québec du 20200312 au 20200425")
plt.xlabel('Nombre cumulatif de cas confirmés')
plt.ylabel("Nombre additionnel de cas confirmés")
plt.savefig("Cas additionnels vs cas accumulés Québec 20200425")
plt.show()
#
from numpy import ones, array
const = list(ones(len(list_diff_val)))
x = array([const,list_val[1:]]).T
x_df = pan.DataFrame(x, columns = ["Const", "Cas accumulés"])
#
import statsmodels.api as sm
model = sm.OLS(endog = list_diff_val, exog = x_df)
results = model.fit()
ar=results.params[1]
br=results.params[0]
print(results.summary())
#
plt.rc("figure", figsize = (12, 7))
plt.text(0.01,0.05, str(results.summary()), {"fontsize": 10}, fontproperties = "monospace")
plt.axis("off")
plt.tight_layout()
plt.savefig("Sommaire Québec du 20200312 au 20200425")
plt.show()
#
'''
