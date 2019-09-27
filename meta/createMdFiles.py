# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 12:05:31 2019

@author: admin
"""

import pandas as pd
import csv
import string
import codecs


meta = pd.read_excel("C:\\Users\\admin\\Desktop\\MetaDns\\Output_DNS_Metadaten_De.xlsx",index_col=0)

dic = {"1":{"1":["ab"]},
       "2":{"1":["a","b"],"2":[""]},
       "3":{"1":["ab","cd","e","f"],"2":["a","b"]},
       "4":{"1":["a","b"],"2":["ab"]},
       "5":{"1":["a","b","c"]},
       "6":{"1":["a","b"],"2":[""]},
       "7":{"1":["ab"],"2":["a","b"]},
       "8":{"1":[""],"2":["ab","c"],"3":[""],"4":[""],"5":["ab"],"6":[""]},
       "9":{"1":[""]},
       "10":{"1":[""],"2":[""]},
       "11":{"1":["a","b","c"],"2":["a","b","c"],"3":[""]},
       "12":{"1":["a","b"],"2":[""],"3":[""]},
       "13":{"1":["a","b"]},
       "14":{"1":["a","b"]},
       "15":{"1":[""],"2":[""],"3":[""]},
       "16":{"1":[""],"2":[""],"3":["ab"]},
       "17":{"1":[""],"2":[""],"3":[""]}}

counter = -1

for goal in dic:
    for target in dic[goal]:
        for indicator in dic[goal][target]:
            #---previous Indicator---------------------------------------------
            counter += 1
            previousI = meta.loc[meta.index[counter-1],'Zusammenfassung'].replace(',','').replace('.','-')
            if len(previousI)<5:
                previousI = previousI + '-a'
            #------------------------------------------------------------------
                
            if len(goal) == 1:
                index = '0'+goal
                index2 = '0'+goal
            else:
                index = goal
                index2 = goal
                        
            #case 1: v.w
            if indicator == "":
                fileName = goal + '-' + target +'-a'
                indicatorDisplay = goal + '.' + target
                index += target + '0'              
                
            #case 2: v.w.x    
            else:
                fileName = goal+'-'+ target+'-' + indicator
                index += target + indicator[0]
                
                #case 2.1: v.w.y
                if len(indicator)==1:
                    indicatorDisplay = goal + '.' + target + '.' + indicator
                    
                #case 2.2: v.w.yz
                else:
                    counter += 1
                    indicatorDisplay = goal + '.' + target + '.' + indicator[0] + ', ' + indicator[-1]
                    index2 += target + indicator[-1]
            
            
            #---next Indicator------------------------------------------------    
            try:
                nextI = meta.loc[meta.index[counter+1],'Zusammenfassung'].replace(',','').replace('.','-')
            except IndexError:
                nextI = meta.loc[meta.index[0],'Zusammenfassung'].replace(',','').replace('.','-')
            if len(nextI)<5:
                nextI = nextI + '-a'
            #------------------------------------------------------------------
            
            print(index, "  ", index2)
        
            file = codecs.open(fileName+".md", "w", "utf-8")
            file.write("---\
                       \nlayout: indicator\
                       \nsdg_goal: '" + goal + "'\
                       \nindicator: " + fileName.replace('-','.') + "\
                       \nindicator_display: '" + indicatorDisplay + "'\
                       \nindicator_sort_order: '" + fileName + "'\
                       \npermalink: /" + fileName + "/\
                       \n\n#\
                       \nreporting_status: complete\
                       \npublished: true\
                       \ndata_non_statistical: false\
                       \n\n\n#Metadata\
                       \nnational_indicator_available: "+ meta.loc[index,'Titel_De'] + "\
                       \ndns_indicator_definition: "+ meta.loc[index,'Definition_DE'] + "\
                       \ndns_indicator_intention: "+ meta.loc[index, 'Intention_DE'] + "\
                       \ndns_content_url: https://nachhaltige-entwicklung-deutschland.github.io/open-sdg-site-starter/public/content/"+fileName.replace('-','.')+".pdf\
                       \ndns_content_url_text: Link zum PDF\
                       \n\nindicator_name: "+ meta.loc[index, 'Titel_2_DE'] + "\
                       \ntarget: "+ meta.loc[index, '1_Indikatorenbereiche.Bezeichnung_DE'] + ' - ' + meta.loc[index, '0_Goal.Bezeichnung_DE' ] + "\
                       \ntarget_id: '" + str(meta.loc[index, 'Bereich']) +"'\
                       \n\nprevious: " + previousI + "\
                       \nnext: " + nextI + "\
                       \n\n#Sources")
            #---Sources--------------------------------------------------------          
            for srcs in range(1,7):
                if not pd.isnull(meta.loc[index, 'Quelle_'+str(srcs)+'_DE']):
                    file.write('\nsource_active_'+str(srcs)+': true\
                               \nsource_organisation_'+str(srcs)+': '+meta.loc[index, 'Quelle_'+str(srcs)+'_DE']+'\
                               \nsource_organisation_logo'+str(srcs)+': \
                               \nsource_url_'+str(srcs)+': \
                               \nsource_url_text_'+str(srcs)+': \
                               \n')
            
            #---Status---------------------------------------------------------
            lStts, lYears = [], []
            l = list(string.ascii_lowercase)[0:9]
            check = 0
            for stts in reversed(range(2010,2019)):
                if not pd.isnull(meta.loc[index, str(stts)]):
                    lYear.append(str(stts))
                    lStts.append(meta.loc[index, str(stts)])
                    check = 1
            if check == 1:
                file.write('\n#Status\
                           \nhistory_active_1: true\
                           \nhistory_indicator_1: '+meta.loc[index, 'DNS']+' - '+meta.loc[index, '3_Indikatoren.Bezeichnung_DE']+'\
                           \nhistory_target_1: ' + meta.loc[index, 'Ziel_Text_DE'])
                
                for i in range(len(lStts)):
                    file.write('\nhistory_year_'+l[i]+"_1: '"+lYear[i]+"'\
                               \nhistory_status_year_"+l[i]+'_1: <img src="https://g205sdgs.github.io/sdg-indicators/public/Wettersymbole/'+lStts[i]+'.png" alt="'+lStts[i]+'" />')
            #---Status for 2nd indicator---------------------------------------                  
            if len(index2) > 2:
                lStts, lYears = [], []
                l = list(string.ascii_lowercase)[0:9]
                check = 0
                for stts in reversed(range(2010,2019)):
                    if not pd.isnull(meta.loc[index2, str(stts)]):
                        lYear.append(str(stts))
                        lStts.append(meta.loc[index2, str(stts)])
                        check = 1
                if check == 1:
                    file.write('\n\
                               \nhistory_active_2: true\
                               \nhistory_indicator_2: '+meta.loc[index2, 'DNS']+' - '+meta.loc[index2, '3_Indikatoren.Bezeichnung_DE']+'\
                               \nhistory_target_2: ' + meta.loc[index2, 'Ziel_Text_DE'])
                
                    for i in range(len(lStts)):
                        file.write('\nhistory_year_'+l[i]+"_2: '"+lYear[i]+"'\
                                   \nhistory_status_year_"+l[i]+'_2: <img src="https://g205sdgs.github.io/sdg-indicators/public/Wettersymbole/'+lStts[i]+'.png" alt="'+lStts[i]+'" />')
            #------------------------------------------------------------------
            if not pd.isnull(meta.loc[index, 'Einheit_DE']):
                Einheit = meta.loc[index, 'Einheit_DE']
            else:
                Einheit = ''
            if not pd.isnull(meta.loc[index, 'Anmerkung_DE']):
                Anmerkung = meta.loc[index, 'Anmerkung_DE']
            else:
                Anmerkung = ''
            file.write('\n\ndata_show_map: \
                       \ndata_keyword: \
                       \ndata_start_values: \
                       \ndata_footnote: ' + Anmerkung + '\
                       \n\ncomputation_units: ' + Einheit +"\
                       \ncopyright: '&copy; Statistisches Bundesamt (Destatis), 2019)'\
                       \n\ngraph_title: \
                       \ngraph_type: line\
                       \ngraph_min_value: \
                       \ngraph_max_value: \
                       \n\nnational_geographical_coverage: Deutschland (Insgesamt)\
                       \n---")
            
                       
            if len(index2) > 2:
                file.write("\n<h3>" + meta.loc[index, 'Ziel_Indikator_DE'] + '\
                           \n  <a href="https://nachhaltige-entwicklung-deutschland.github.io/open-sdg-site-starter/status/"><img src="https://g205sdgs.github.io/sdg-indicators/public/Wettersymbole/'+ meta.loc[index, 'Aktuell'] + '.png" alt="' + meta.loc[index, 'Aktuell'] + '" />\
                           \n  </a>\
                           \n</h3>\
                           \n\n<h3>' + meta.loc[index2, 'Ziel_Indikator_DE'] + '\
                           \n  <a href="https://nachhaltige-entwicklung-deutschland.github.io/open-sdg-site-starter/status/"><img src="https://g205sdgs.github.io/sdg-indicators/public/Wettersymbole/'+ meta.loc[index2, 'Aktuell'] + '.png" alt="' + meta.loc[index2, 'Aktuell'] + '" />\
                           \n  </a>\
                           \n</h3>')
            else:
                file.write('\n<a href="https://nachhaltige-entwicklung-deutschland.github.io/open-sdg-site-starter/status/"><img src="https://g205sdgs.github.io/sdg-indicators/public/Wettersymbole/'+ meta.loc[index, 'Aktuell'] + '.png" alt="' + meta.loc[index, 'Aktuell'] + '" />\
                           \n</a>')
                               
                    
            file.close()

                    

         
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            