import pandas as pd
import numpy as np
import os


path="/Users/Sal/Desktop/files/"
cwd=os.getcwd
os.chdir(path)

year=2017
variable_list = ['Assets']

while (year>2016):

	q1_sub = pd.read_csv(str(year)+'q1sub.csv')
	q2_sub = pd.read_csv(str(year)+'q2sub.csv')
	q3_sub = pd.read_csv(str(year)+'q3sub.csv')
	q4_sub = pd.read_csv(str(year)+'q4sub.csv')

	q1_num = pd.read_csv(str(year)+'q1num.csv')
	q2_num = pd.read_csv(str(year)+'q2num.csv')
	q3_num = pd.read_csv(str(year)+'q3num.csv')
	q4_num = pd.read_csv(str(year)+'q4num.csv')

	companies=q1_sub.append(q2_sub).append(q3_sub).append(q4_sub)
	values=q1_num.append(q2_num).append(q3_num).append(q4_num)
	values.sort_values(['adsh', 'tag','ddate', 'coreg','value'], inplace=True)

	# Complete sub file for for 4 quarters with values sorted
	companies.sort_values(['adsh','period','form'], inplace=True)

	# Add the cik field to value 
	cik_merge=companies[['adsh','cik','fy','fye','period']]
	val=values.merge(cik_merge,on='adsh',how='left')


	for keyword in variable_list:

		val=val[val['tag']==keyword].loc[:,['adsh','cik','ddate','coreg','value']]

		# Get 10-K [Assumption One: All the companies we want have filed a 10-K]
		con_10k = companies[companies.form == '10-K']

		# FOR COMPANIES WITH NCIK==1
		con=con_10k[con_10k['nciks']==1]
		rest=con_10k[con_10k['nciks']!=1][['adsh','cik','fy','fye','period']]

		# The total number of entries in con_10k increase as multiple values with the same adsh get stacked
		con_10k = con_10k.merge(val[['adsh','ddate','coreg','value']],on='adsh',how='left')
		# We first get the entries with empty values before we filter them out
		missing_10k=con_10k[con_10k['value'].isnull()]


		# PART ONE ; FOR COMPANIES WITH NON-MISSING VALUES 

		# We will drop some companies with mismatching periods and ddates. We keep track of all the ciks 
		# of the companies that we have dropped. Later we will check if all the values for the ciks we have
		# dropped are present because what if we drop a firm with mismatched dates but that turned out to 
		# be the only entry for the firm?
		dropped_cik_nonmiss=con_10k[con_10k.period!=con_10k.ddate].drop_duplicates(['cik'],keep='last')
		# We drop all the entries with mismatched periods and ddates because we only want values for one specific date
		con_10k=con_10k[con_10k['value'].isnull()==False]
		con_10k=con_10k[con_10k.period==con_10k.ddate]
		

		# The entries we want containing firms with empty coreg entries
		con_10k_emptycoreg=con_10k[con_10k['coreg'].isnull()]

		# Total CIK of every firm with non-empty coreg field
		con_10k_notemptycoreg_total=con_10k[con_10k['coreg'].isnull()==False]
		# con_10k_notemptycoreg contains entries of firms that do not have empty coreg fields
		# Compare total cik of firms with non-empty coreg field with total cik of firms with empty coreg fields. If the cik of 
		# firm with non-empty coreg field is not in the cik of firm with empty coreg field, the company does not have empty coreg field
		# This we also want 
		con_10k_notemptycoreg=con_10k_notemptycoreg_total[con_10k_notemptycoreg_total.cik.isin(con_10k_emptycoreg.cik)==False]
		value_not_missing= [con_10k_emptycoreg,con_10k_notemptycoreg]
		value_not_missing=pd.concat(value_not_missing)[['adsh','cik','fy','fye','period','ddate','coreg','value']]

		# PART TWO : FOR COMPANIES WITH MISSING VALUES 

		# Get the cik for companies with missing values
		missing_cik=missing_10k['cik']
		missing_merge=missing_10k[['cik','period','fy','fye']]

		# Get all the possible asset values for missing companies by matching the missing ciks with ciks in the num file
		missing_values=val[val['cik'].isin(missing_cik)]
		missing_values=missing_values.merge(missing_merge,on='cik',how='left')
		# get the dropped ciks of the possibly repetivie missing values 
		dropped_cik_miss=missing_values[missing_values.period!=missing_values.ddate].drop_duplicates(['cik'],keep='last')
		# get the values with matching period and dates
		missing_value=missing_values[missing_values.period==missing_values.ddate]
		# Dropping repetitive entries for asset with same values and dates but different adshs
		missing_value=missing_value.drop_duplicates(subset=['ddate','value'])

		missing_value_emptycoreg=missing_value[missing_value['coreg'].isnull()]
		missing_value_notemptycoreg_total=missing_value[missing_value['coreg'].isnull()==False]
		missing_value_notemptycoreg=missing_value_notemptycoreg_total[missing_value_notemptycoreg_total.cik.isin(missing_value_emptycoreg.cik)==False]
		value_missing=[missing_value_emptycoreg,missing_value_notemptycoreg]
		value_missing=pd.concat(value_missing)[['adsh','cik','fy','fye','period','ddate','coreg','value']]
		nciks1=[value_missing,value_not_missing]
		nciks1=pd.concat(nciks1,ignore_index=True)

		dropped=pd.concat([dropped_cik_nonmiss[['adsh','cik','fy','fye','period', 'ddate','coreg','value']],dropped_cik_miss[['adsh','cik','fy','fye','period', 'ddate','coreg','value']]]).drop_duplicates(['cik'],keep='last')
		droppedandmissing_cik=dropped[dropped.cik.isin(nciks1.cik)==False]

		rest_total=droppedandmissing_cik.append(rest).drop_duplicates(['cik'],keep='last')
		rest_merge=rest_total[['cik','period','fy','fye']]
		rest_val=val[val['cik'].isin(rest_total.cik)].merge(rest_merge,on='cik',how='left')[['adsh','cik','fy','fye','period','ddate','coreg','value']]
		rest_val=rest_val[rest_val.ddate==rest_val.period]	
		total=pd.concat([nciks1,rest_val],ignore_index=True)
		total.to_csv(str(year)+'.csv')

	year=year-1


# Method Two: Webscraping 
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.by import By
# browser = webdriver.Chrome(executable_path=r'/Applications/Python 3.6/chromedriver')
# for index, row in missing.iterrows():
# 	url='https://www.sec.gov/cgi-bin/viewer?action=view&cik='+str(row['cik'])+'&accession_number='+str(row['adsh'])+'&xbrl_type=v#'
# 	url='https://www.sec.gov/cgi-bin/viewer?action=view&cik=882291&accession_number=0001683168-17-001671&xbrl_type=v#'
# 	browser.get(url)
# 	element1 = browser.find_element_by_id("menu_cat2")
# 	element1.click()
# 	element2 = browser.find_element_by_id("r2")
# 	element2.click()
    
#     break


# meh=browser.findElement(By.xpath("//*[contains('CONSOLIDATED BALANCE SHEETS')]"))

# Code that proved to be inefficient

		# for index, row in missing_10k.iterrows():
		# 	if missing_values[missing_values['cik']==row['cik']].empty==False:
		# 		match_cik=missing_values[missing_values['cik']==row['cik']]
		# 		if row['nciks']==1:
		# 			if match_cik[match_cik['ddate']==row['period']].drop_duplicates(['value'],keep='last').empty==False:
		# 				match_cik.sort_values(['value'], inplace=True)
		# 				missing.at[index,'value']=match_cik[match_cik['ddate']==row['period']].drop_duplicates(['value'],keep='last').iloc[0]['value']
		# 			else:
		# 				missing.at[index,'value']=-1
		# 		else:
		# 			missing.at[index,'value']=-2
		# 	else:
		# 		missing.at[index,'value']= -3	



