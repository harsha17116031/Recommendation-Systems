ratings={}
mean_of_users={}
mean_centered_ratings={}

with open('./netflix/TrainingRatings.txt') as f:
    lines = f.readlines()

for i in lines:
    temp=i.replace("\n","").split(',')
    if not temp[1] in ratings.keys():
        ratings[temp[1]]={}

    ratings[temp[1]][temp[0]]=float(temp[2])


for i in ratings.keys():
    sum_of_user_ratings=0
    count=0
    for j in ratings[i].keys():
        sum_of_user_ratings+=ratings[i][j]
        count+=1
    
    mean_of_users[i]=sum_of_user_ratings/count

    for j in ratings[i].keys():
        ratings[i][j]=ratings[i][j]-mean_of_users[i]


