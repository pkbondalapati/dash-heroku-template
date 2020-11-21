import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from dash import Dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# import plotly.offline as pyo
# pyo.init_notebook_mode()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

gender_pay_text = """From PayScale's ["The State of the Gender Pay Gap in 2020"](https://www.payscale.com/data/gender-pay-gap) report, the gender pay gap between men and women has marginally diminished every year from 2015. When considering the raw, uncontrolled gender pay gap, which compares median salaries without regard for job type or seniority, women earn $0.81 for every dollar earned by men. When considering men and women with the same job and under the same qualifications, women earn $0.98 for every dollar earned by men. PayScale details how women lose around $900,000 over their 40-year career period when considering the uncontrolled gender pay gap. Similarly, women lose around $80,000 over their 40-year career period when considering the controlled gender pay gap. Most of this lost income is attributed to the compounded interest for potential investments and retirement savings. 
                  """

gss_desc_text = """The General Social Survey (GSS) conducts a biennial survey that measures the social characteristics and contemporary attitudes of residents in the United States. The majority of the data from these surveys come from face-to-face and telephone interviews. The survey collects general background information of the respondent (e.g. age, sex, education, residence) as well as some measures of attitudes (e.g. confidence in institutions, gun control favorability) and behaviors (e.g. religious service attendance). These surveys have a target sample size of 1,500 respondents; the target population are adults living in U.S. households.
                """

gss2_df = gss_clean.loc[:, ['sex','income', 'job_prestige', 'socioeconomic_index', 'education']].groupby(by=['sex']).mean().reset_index().round(2)
gss2_df.columns = ['sex', 'mean income', 'mean occupational prestige', 'mean socioeconomic index', 'mean years of education']
table2 = ff.create_table(gss2_df)
# table2.show()

gss3_df = gss_clean.loc[:, ['male_breadwinner', 'sex']].groupby(by=["male_breadwinner", "sex"]).agg({'sex':'size'})
gss3_df = gss3_df.rename({'sex':'frequency'}, axis=1)
gss3_df = gss3_df.reset_index()
gss3_df.male_breadwinner = [x.title() for x in gss3_df.male_breadwinner.values]
gss3_df.sex = [x.title() for x in gss3_df.sex.values]
gss3_df = gss3_df.reindex([4, 5, 0, 1, 2, 3, 6, 7])
# gss3_df

fig3 = px.bar(gss3_df, x="male_breadwinner", y="frequency", color="sex", barmode="group", 
              color_discrete_map = {'Male':'deepskyblue', 'Female':'palevioletred'}, 
              labels={"male_breadwinner":"Level of Agreement", "frequency":"Frequency", "sex":"Sex"})
# fig3.show()

gss4_df = gss_clean.loc[:, ['job_prestige', 'income', 'sex', 'education', 'socioeconomic_index']]
gss4_df.sex = [x.title() for x in gss4_df.sex.values]
# gss4_df

fig4 = px.scatter(gss4_df, x="job_prestige", y="income", color="sex", trendline="ols",
                  color_discrete_map = {'Male':'deepskyblue', 'Female':'palevioletred'},
                  labels={"income":"Annual Income ($)", "job_prestige":"Occupational Prestige Scores", "sex":"Sex",
                          "education":"Years of Education", "socioeconomic_index":"Socioeconomic Index"},
                  hover_data=['education', 'socioeconomic_index'])

gss5_df = gss_clean.loc[:, ['income', 'sex', 'job_prestige']]
gss5_df.sex = [x.title() for x in gss5_df.sex.values]

fig5a = px.box(gss5_df, x="income", y="sex", color="sex",
               color_discrete_map = {'Male':'deepskyblue', 'Female':'palevioletred'},
               labels={"sex":"Sex", "income":"Annual Income ($)"})
fig5a.update_layout(showlegend=False)

fig5b = px.box(gss5_df, x="job_prestige", y="sex", color="sex",
               color_discrete_map = {'Male':'deepskyblue', 'Female':'palevioletred'},
               labels={"sex":"Sex", "job_prestige":"Occupational Prestige Scores"})
fig5b.update_layout(showlegend=False)

gss6_df = gss_clean.loc[:, ['income', 'sex', 'job_prestige']]
gss6_df.sex = [x.title() for x in gss6_df.sex.values]
gss6_df['job_prestige_category'] = pd.cut(gss6_df.job_prestige, bins=6, 
                                          labels=["Occupational Prestige 16-26", "Occupational Prestige 27-37",
                                                  "Occupational Prestige 38-48", "Occupational Prestige 49-58",
                                                  "Occupational Prestige 59-69", "Occupational Prestige 70-80"])
gss6_df = gss6_df.dropna()
gss6_df = gss6_df.sort_values(by="job_prestige_category")
# gss6_df

fig6 = px.box(gss6_df, x="income", y="sex", color="sex", facet_col="job_prestige_category", facet_col_wrap=3,
              color_discrete_map = {'Male':'deepskyblue', 'Female':'palevioletred'},
              labels={"income":"Annual Income ($)", "sex":"Sex", "job_prestige":"Occupational Prestige Scores"})
fig6.update_layout(showlegend=False)
fig6.for_each_annotation(lambda a: a.update(text=a.text.replace("job_prestige_category=", "")))

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Analysis of Gender Differences from the General Social Survey (GSS)"),
        
        dcc.Markdown(children = gender_pay_text),
        
        dcc.Markdown(children = gss_desc_text),
        
        html.H2("Comparison of Gender Differences on Economic and Societal Factors"),
        
        dcc.Graph(figure=table2),
        
        html.H2("Attitudes Towards a Male Breadwinner by Gender"),
        
        dcc.Markdown(children = """The barplot shown below depicts the level of agreement to the following sentiment: "it is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family." """),
        
        dcc.Graph(figure=fig3),
        
        html.H2("Annual Income Against Occupational Prestige by Gender"),
        
        dcc.Graph(figure=fig4),
        
        html.Div([
            
            html.H2("Box Plot of Annual Income by Gender"),
            
            dcc.Graph(figure=fig5a)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2("Box Plot of Occupational Prestige by Gender"),
            
            dcc.Graph(figure=fig5b)
                        
        ], style = {'width':'48%', 'float':'right'}),
        
        html.H2("Box Plot of Annual Income by Gender and Occupational Prestige"),
        
        dcc.Graph(figure=fig6)
        
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
