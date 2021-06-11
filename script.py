import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd 
import gspread
from gspread_dataframe import set_with_dataframe

paises =['CHL', 'FRA', 'AUS', 'FIN', 'DEU', 'USA']
rows = []
for index in range(6):
    print(index)
    r= requests.get(f'http://tarea-4.2021-1.tallerdeintegracion.cl/gho_{paises[index]}.xml')
    root = ET.fromstring(r.content)


    #tree = ET.ElementTree(root)
    #tree.write("test.xml", encoding="utf-8")

    df_cols = ["Country","GHO","Year","Sex","GHEcauses", "AgeGroup","Display","Numeric","High","Low"]
   
    indicadores = ["Number of deaths", "Number of infant deaths", "Number of under-five deaths", "Mortality rate for 5-14 year-olds (probability of dying per 1000 children aged 5-14 years)",
                "Adult mortality rate (probability of dying between 15 and 60 years per 1000 population)", "Estimates of number of homicides", "Crude suicide rates (per 100 000 population)",
                "Mortality rate attributed to unintentional poisoning (per 100 000 population)", "Number of deaths attributed to non-communicable diseases, by type of disease and sex",
                "Estimated road traffic death rate (per 100 000 population)", "Estimated number of road traffic deaths", "Mean BMI (kg/m&#xb2;) (crude estimate)", "Mean BMI (kg/m&#xb2;) (age-standardized estimate)",
                "Prevalence of obesity among adults, BMI &GreaterEqual; 30 (age-standardized estimate) (%)", "Prevalence of obesity among children and adolescents, BMI > +2 standard deviations above the median (crude estimate) (%)",
                "Prevalence of overweight among adults, BMI &GreaterEqual; 25 (age-standardized estimate) (%)", "Prevalence of overweight among children and adolescents, BMI > +1 standard deviations above the median (crude estimate) (%)",
                "Prevalence of underweight among adults, BMI < 18.5 (age-standardized estimate) (%)", "Prevalence of thinness among children and adolescents, BMI < -2 standard deviations below the median (crude estimate) (%)",
                "Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)", "Estimate of daily cigarette smoking prevalence (%)", "Estimate of daily tobacco smoking prevalence (%)",
                "Estimate of current cigarette smoking prevalence (%)", "Estimate of current tobacco smoking prevalence (%)", "Mean systolic blood pressure (crude estimate)", "Mean fasting blood glucose (mmol/l) (crude estimate)", "Mean Total Cholesterol (crude estimate)"]

    for node in root: 
        c_name = node.find("COUNTRY").text 
        if node.find("YEAR") is not None:
            c_year = node.find("YEAR").text
        else:
            c_year=None
        if node.find("GHO") is not None:
            c_gho = node.find("GHO").text
        else:
            c_gho=None
        if node.find("SEX") is not None:
            c_sex = node.find("SEX").text 
        else:
            c_sex=None
        if node.find("GHECAUSES") is not None:
            c_ghe = node.find("GHECAUSES").text
        else:
            c_ghe=None
        if node.find("AGEGROUP") is not None:
            c_agegroup = node.find("AGEGROUP").text 
        else:
            c_agegroup=None
        if node.find("Display") is not None:
            c_display = node.find("Display").text 
        else:
            c_display=None
        if node.find("Numeric") is not None:
            c_numeric = node.find("Numeric").text 
        else:
            c_numeric=None
        if node.find("Low") is not None:
            c_low = node.find("Low").text
        else:
            c_low=None
        if node.find("High") is not None:
            c_high = node.find("High").text
        else:
            c_high=None
        rows.append({"Country": c_name, "GHO":c_gho,"Year": c_year,"Sex": c_sex,"GHEcauses": c_ghe,"AgeGroup": c_agegroup,"Display": c_display,"Numeric": c_numeric,"Low": c_low, "High": c_high  })

out_df = pd.DataFrame(rows, columns = df_cols)
out_df["Numeric"] = pd.to_numeric(out_df["Numeric"], downcast="float")
df = out_df[out_df["GHO"].isin(indicadores)]


gc=gspread.service_account(filename='tdi-tarea4-86587c1ced31.json')
sh = gc.open_by_key('1pYUQeCaOjJUCm2q4IKCNs5PB3fN6gL0EZ5V9ySotrjE')
worksheet = sh.get_worksheet(0)
worksheet.clear()
set_with_dataframe(worksheet,df)

