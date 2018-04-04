import pandas as pd

df1 = pd.read_csv('D:/Google Drive/ENSAE/Dataviz/Olympics.tsv', sep='\t')

#isoler les jo d'hiver
df_winter = df1[df1['Event']=='Winter']

p = df_winter.groupby(['Country', 'Sport', 'Gender'] )['Total'].agg('sum')
print("Nombre de médailles par pays, par sport et par sexe")
print(p)

#nb de disciplines auxquelles participent les pays
p1 = df_winter.groupby(['Country', 'Year', 'Sport'] )['Athlete'].agg('count').reset_index()
print("Nombre de participants par pays, par année et par sport")
print(p1)

#nb de disciplines auxquelles les pays obtiennent des médailles
p2 = df_winter.groupby(['Country', 'Year', 'Sport'] )[['Total']].agg('sum').reset_index()
print("Nombre de médailles par pays, par année et par sport")
p2

#jointure => table avec dimensions : pays, année et sport 
                        #indicateurs : nombre participants, nombre médailles
p3 = pd.merge(p1, 
              p2, 
              how='left', 
              left_on=['Country', 'Year', 'Sport'], 
              right_on=['Country', 'Year', 'Sport'])
p3.rename(columns={'Athlete': 'Participants', 'Total':'Medals'}, inplace=True)
p3['Ratio'] = p3.Medals / p3.Participants
p3

p3.to_csv(path_or_buf='D:/Google Drive/ENSAE/Dataviz/olimpics_agg.csv', sep = ',', index=False)



#pays qui envoient systématiquement des athlètes sans avoir des médailles???
#par pays, tous sports, tous types de médailles, évolution dans le temps
p3\
    .groupby([p3.Year.name, p3.Country.name])['Medals']\
    .sum()\
    .unstack()\
    .plot(figsize=(12,12), title='Évolution nb médailles par pays', legend=False)
    
p3\
    .groupby([p3.Year.name, p3.Country.name])['Participants']\
    .sum()\
    .unstack()\
    .plot(figsize=(12,12), title='Évolution nb participants par pays', legend=False)
        
    
#focus sur un pays    
c = 'France'     
p3[p3.Country == c]\
    .groupby([p3.Year.name, p3.Country.name])['Medals', 'Participants']\
    .sum()\
    .unstack()\
    .plot(figsize=(12,12))
#Pour la France, le nombre de participants semble augmenter beaucoup plus vite que le nombre de médailles gagnées
#Plus d'athlètes sont envoyés,  mais moins d'entre eux gagnent une médaille

#??? plus d'athlètes puisque plus de disciplines auquelles ils participent ou juste plus de participants par discipline?
    
    
#focus sur quelques pays
#comparer pour un nombre plus petit de pays l'évolution dans le temps du ratio de médailles/participants    
liste_pays = ['France', 'United States', 'Canada', 'Australia', 'Norway' ]
p3[p3.Country.isin(liste_pays)]\
    .groupby([p3.Year.name, p3.Country.name])['Ratio']\
    .mean()\
    .unstack()\
    .plot(kind='bar',figsize=(12,12), title = 'Évolution du ratio médailles / participants pour un ensemble de pays')    
    
p3[p3.Country.isin(liste_pays)]\
    .groupby([p3.Year.name, p3.Country.name])['Medals']\
    .sum()\
    .unstack()\
    .plot(kind='bar', figsize=(12,12),title = 'Évolution du nb de médailles obtenues pour un ensemble de pays')        
    
p3[p3.Country.isin(liste_pays)]\
    .groupby([p3.Year.name, p3.Country.name])['Participants']\
    .sum()\
    .unstack()\
    .plot(kind='bar',figsize=(12,12),title = 'Évolution du nb de participants envoyés pour un ensemble de pays')   
#trend dernières années : ratio descend, puisque le nb de médailles baisse, mais le nb de participants envoyés augmente     
    
    
#revenir sur un seul pays en particulier    
liste_pays = ['France']
  
p3[p3.Country.isin(liste_pays)]\
    .groupby([p3.Year.name, p3.Country.name])['Ratio']\
    .mean()\
    .unstack()\
    .plot(kind='bar', figsize=(12,12), title = 'Comparaison des évolutions : \n nb de participants \n nb de médailles  \n ratio médailles/participants pour un pays')     
    

#variation d'une année à l'autre en pourcentage     !!!!à revérifier logique !!!  
p3['Medals_t_1'] = p3.groupby(['Country', 'Sport'])['Medals'].shift(1)
p3['Participants_t_1'] = p3.groupby(['Country', 'Sport'])['Participants'].shift(1)
p3['Ratio_t_1'] = p3.groupby(['Country', 'Sport'])['Ratio'].shift(1)
    
p3['Medals_delta'] = (p3.Medals - p3.Medals_t_1)  / p3.Medals_t_1 
p3['Participants_delta'] = (p3.Medals - p3.Medals_t_1)  / p3.Medals_t_1
p3['Ratio_delta'] = (p3.Ratio - p3.Ratio_t_1)  / p3.Ratio_t_1
      
p3[p3.Country.isin(liste_pays)]\
    .groupby([p3.Year.name, p3.Country.name])['Ratio_delta', 'Medals_delta', 'Participants_delta']\
    .mean()\
    .unstack()\
    .plot(kind='bar', figsize=(12,12))     
    
    
    
#nb de disciplines auxquelles les pays obtiennent des médailles
import numpy as np
p4 = df_winter.groupby(['Country', 'Year', 'Sport'] )[['Age']].agg(np.mean).reset_index()
print("Nombre de médailles par pays, par année et par sport")
p2    


#####################################################################################
df_agg_FR = p3[p3.Country=='France'].groupby(['Year'] )[['Participants', 'Medals']].agg('sum').reset_index()

df_agg_FR['Medals_t_1'] = df_agg_FR['Medals'].shift(1)
df_agg_FR['Participants_t_1'] = df_agg_FR['Participants'].shift(1)
    
df_agg_FR['Medals_delta_pct'] = (df_agg_FR.Medals - df_agg_FR.Medals_t_1) / df_agg_FR.Medals_t_1 *100
df_agg_FR['Participants_delta_pct'] = (df_agg_FR.Participants - df_agg_FR.Participants_t_1)  / df_agg_FR.Participants_t_1 *100

df_agg_FR[['Medals_delta_pct','Participants_delta_pct' ]].plot(kind='bar', figsize=(12,12))

df_agg_FR['Ratio'] = df_agg_FR['Medals'] / df_agg_FR['Participants'] * 100
df_agg_FR['Ratio_t_1'] = df_agg_FR['Ratio'].shift(1)

df_agg_FR['Ratio_delta_pct'] = (df_agg_FR.Ratio - df_agg_FR.Ratio_t_1)  / df_agg_FR.Ratio_t_1 *100


df_agg_FR[['Medals_delta_pct','Participants_delta_pct', 'Ratio_delta_pct' ]].plot(kind='bar', figsize=(12,12))

df_agg_FR[['Medals','Participants', 'Ratio' ]].plot( figsize=(12,12))

import numpy as np
df_agg_FR['Medals_cum'] = np.cumsum(df_agg_FR['Medals']) 
df_agg_FR['Participants_cum'] = np.cumsum(df_agg_FR['Participants']) 

df_agg_FR[['Medals_cum','Participants_cum', 'Ratio' ]].plot( figsize=(12,12))

df_agg_FR[['Year', 'Medals_cum','Participants_cum', 'Ratio' ]].to_csv(path_or_buf='D:/Google Drive/ENSAE/Dataviz/fr_agg.csv', sep = ',', index=False)