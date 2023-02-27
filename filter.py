ratings={}
mean_of_users={}

with open('./netflix/TestingRatings.txt') as f:
    lines = f.readlines()

for i in lines:
    temp=i.replace("\n","").split(',')
    if not temp[0] in ratings.keys():
        ratings[temp[0]]={}

    ratings[temp[0]][temp[1]]=temp[2]


for i in ratings.keys():
    sum_of_user_ratings=0
    count=0
    for j in ratings[i].keys():
        sum_of_user_ratings+=float(ratings[i][j])
        count+=1
    
    mean_of_users[i]=sum_of_user_ratings/count



print(mean_of_users)