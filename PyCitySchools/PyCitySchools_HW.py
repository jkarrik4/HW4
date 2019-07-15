#!/usr/bin/env python
# coding: utf-8

# In[675]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# In[676]:


school_data_complete.head()


# In[677]:


#Create datdframe showing school enrollment data
school_enrollment = pd.DataFrame(data=school_data_complete['school_name'].value_counts())
school_enrollment.rename(columns = {'school_name':'enrolled_students'})


# In[678]:


#Display total num of schools
total_schools = school_enrollment.shape[0]
print("Total schools:")
print(total_schools)


# In[679]:


#Display total num of students
total_students = school_data_complete.student_name.count()
print("Total Students:")
print(total_students)


# In[680]:


#Calculate total district budget
budget_list = school_data_complete['budget'].unique().tolist()
total_dist_budget = sum(budget_list)
print("Total District Budget:")
total_dist_budget


# In[681]:


#Calculate district avg. math score
dist_avg_math = school_data_complete.math_score.mean()
print("Dist. Avg. Math Score:")
dist_avg_math


# In[682]:


#Calculate district avg. reading score
dist_avg_read = school_data_complete.reading_score.mean()
print("Dist. Avg. Reading Score:")
dist_avg_read


# In[683]:


#Calculate math pass rate
dist_pass_math = school_data_complete.loc[school_data_complete["math_score"] >= 70]
dist_mpass = dist_pass_math["math_score"].count()
dist_mpass_rate = (dist_mpass/total_students)*100
print("Dist. Math Pass Rate:")
print(dist_mpass_rate)


# In[684]:


#Calculate reading pass rate
dist_pass_read = school_data_complete.loc[school_data_complete["reading_score"] >= 70]
dist_rpass = dist_pass_read["reading_score"].count()
dist_rpass_rate = (dist_rpass/total_students)*100
print("Dist. Read. Pass Rate:")
print(dist_rpass_rate)


# In[685]:


#Calculate the overall passing rate (overall average score)
dist_pass_rate = (dist_mpass_rate + dist_rpass_rate)/2
print("Dist % Overall Passing Rate:")
dist_pass_rate


# In[686]:


#Create df to display the district info
district_summary = {"Total Schools" : total_schools,"Total Students" : total_students,"Total District Budget" : total_dist_budget,"Average Math Score" : dist_avg_math,"Average Reading Score" : dist_avg_read,"% Passing Math" : dist_mpass_rate,"% Passing Reading" : dist_rpass_rate,"% Overall Passing Rate" : dist_pass_rate }

district_summary_data = pd.DataFrame([district_summary])
district_summary_data


# In[687]:


#Part 2
#Calculate schools' budget per student
school_data['Budget per Student'] = school_data['budget']/school_data['size']
school_data


# In[688]:


#Group schools together with their average scores
avg_scores = school_data_complete.groupby(['school_name'])['reading_score', 'math_score']
avg_scores = avg_scores.mean().reset_index()
avg_scores


# In[689]:


#combine datdframes together
cumul_schools = school_data.merge(avg_scores, on='school_name', how="outer")
cumul_schools
del cumul_schools['School ID']
cumul_schools


# In[690]:


#Find % of passing scores
cumul_rpass = student_data[student_data['reading_score']>=70]
cumul_rpass

cumul_rpass_count = cumul_rpass.groupby(["school_name"])['reading_score'].count().reset_index()



cumul_mpass = student_data[student_data['math_score']>=70]
cumul_mpass

cumul_mpass_count = cumul_mpass.groupby(["school_name"])['math_score'].count().reset_index()


# In[691]:


cumul_mpass_count


# In[692]:


cumul_rpass_count


# In[693]:


cumul_pass_count = cumul_rpass_count.merge(cumul_mpass_count, on="school_name", how='inner')
cumul_pass_count.columns = ['school_name', 'reading_pass_count', 'math_pass_count']
cumul_pass_count


# In[694]:


cumul_schools = cumul_schools.merge(cumul_pass_count, on="school_name", how='outer')
cumul_schools


# In[695]:


cumul_schools['Reading Pass %'] = (cumul_schools['reading_pass_count']/cumul_schools['size'])*100
cumul_schools['Math Pass %'] = (cumul_schools['math_pass_count']/cumul_schools['size'])*100
cumul_schools


# In[696]:


#calculate overall pass percentage
cumul_schools['Overall Pass %'] = (cumul_schools['Reading Pass %'] + cumul_schools['Math Pass %'])/2
cumul_schools


# In[697]:


cumul_schools.columns = ['School Name', 'Type', 'Size', 'Budget', 'Budget per Student', 'AVg Reading Score', 'Avg Math Score', '# Pass Reading', '# Pass Math', 'Reading Pass %', 'Math Pass %', 'Overall Pass %']
cumul_schools


# In[698]:


#Top Performing Schools (By Passing Rate)
#Sort and display the top five schools in overall passing rate
top_perform_pass_rate = cumul_schools.sort_values(by=['Overall Pass %'], ascending=False)
del top_perform_pass_rate['# Pass Reading']
del top_perform_pass_rate['# Pass Math']
top_perform_pass_rate.head()


# In[699]:


#Bottom Performing Schools (By Passing Rate)
bottom_perform_pass_rate = top_perform_pass_rate.sort_values(by=['Overall Pass %'])
bottom_perform_pass_rate.head()


# In[700]:


#Create a table that lists the average math Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
grade_level_math = pd.pivot_table(school_data_complete, values=['math_score'], index=['school_name'], columns=['grade'])
grade_level_math
grade_level_math.reindex_axis(labels=['9th', '10th', '11th','12th'], axis=1, level=1)


# In[701]:


#Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
grade_level_read = pd.pivot_table(school_data_complete, values=['reading_score'], index=['school_name'], columns=['grade'])
grade_level_read
grade_level_read.reindex_axis(labels=['9th', '10th', '11th','12th'], axis=1, level=1)


# In[702]:


#Scores by School Spending
   ## Sample bins
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

school_spend_bin = pd.cut(cumul_schools['Budget per Student'], spending_bins, labels=group_names)

spending_bins = pd.DataFrame(spending_bins)
spending_bins
cumul_schools['Budget/Student'] = school_spend_bin
cumul_schools


# In[703]:


budget_per_student = cumul_schools.groupby(['Budget/Student'])['AVg Reading Score', 'Avg Math Score', 'Reading Pass %', 'Math Pass %','Overall Pass %'].mean()
budget_per_student


# In[704]:


# Scores by School Size
# Sample bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

school_size_bin = pd.cut(cumul_schools['Size'], size_bins, labels=group_names)

size_bins = pd.DataFrame(size_bins)
size_bins
cumul_schools['School Size'] = school_size_bin
cumul_schools


# In[705]:


school_size_group = cumul_schools.groupby(['School Size'])['AVg Reading Score', 'Avg Math Score', 'Reading Pass %', 'Math Pass %','Overall Pass %'].mean()
school_size_group


# In[708]:


# Scores by School Type
school_type_scores = cumul_schools.groupby(['Type'])['AVg Reading Score', 'Avg Math Score', 'Reading Pass %', 'Math Pass %','Overall Pass %'].mean()
school_type_scores


# In[ ]:


#Observations from the data


    ## Based on the budget_per_student dataframe, increased spending does not seem to lead to better test scores
    ## or passing rates. It almost seems to have a negative relationship.
    
    ## Based on the final dataframe, charter schools seem to do better than district schools. However, I think this
    ## could be correlated to school size. The top 5 schools in the dataset were all charter schools but of those, 
    ## only 1 falls into the Large school size category.

