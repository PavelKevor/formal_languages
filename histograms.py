from plotly import *
from plotly import graph_objects as go
import re

graphs = ["LUBM300", "LUBM500", "LUBM1M", "LUBM1.5M", "LUBM1.9M"]
file = open('result.txt', "r")
regexp = []
ajm = []
sqr = []
num = 0
num_of_reg = 10
i = 0


    
for line in file:
    if num  == num_of_reg:
        fig = go.Figure()
        fig.add_trace(go.Bar(name ='adjacency matrix', x = regexp, y = ajm))
        fig.add_trace(go.Bar(name = 'squaring', x = regexp, y = sqr))

        fig.update_layout(
        title=graphs[i],
        title_x = 0.5,
        xaxis_title="регулярные выражения, пересекаемые с графом",
        yaxis_title="время",
        legend=dict(x=.5, xanchor="center", orientation="h"),
        margin=dict(l=0, r=0, t=30, b=0))


        
        fig.show()

        regexp = []
        ajm = []
        sqr = []
        i += 1
        num = 0
       
        
    if ('refinedDataForRPQ/') in line:
        regexp.append(re.search("q1\w*\+", line).group(0)[:-1])
    elif "transitive_closure_with_adjacency_matrix" in line:
        ajm.append(float(re.search("medium:.* ", line).group(0)[7:][:-1]))
    elif "transitive_closure_with_squaring" in line:
        sqr.append(float(re.search("medium:.* ", line).group(0)[7:][:-1]))
    elif not line.strip():
        num += 1
