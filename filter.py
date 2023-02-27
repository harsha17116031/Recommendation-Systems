# ratings={}
# mean_of_users={}
# mean_centered_ratings={}
# weights_of_users={}

# with open('./netflix/TrainingRatings.txt') as f:
#     lines = f.readlines()

# for i in lines:
#     temp=i.replace("\n","").split(',')
#     if not temp[1] in ratings.keys():
#         ratings[temp[1]]={}

#     ratings[temp[1]][temp[0]]=float(temp[2])


# for i in ratings.keys():
#     sum_of_user_ratings=0
#     count=0
#     for j in ratings[i].keys():
#         sum_of_user_ratings+=ratings[i][j]
#         count+=1
    
#     mean_of_users[i]=sum_of_user_ratings/count

#     for j in ratings[i].keys():
#         ratings[i][j]=ratings[i][j]-mean_of_users[i]


# calculating weights of users

def find_similar_movie_ratings(first_user,second_user):
    common_movie_ratings=[]
    if len(first_user.keys())>len(second_user.keys()):
        for i in second_user.keys():
            if i in first_user.keys():
                common_movie_ratings.append([first_user[i],second_user[i]])
    else:
        for i in first_user.keys():
            if i in second_user.keys():
                common_movie_ratings.append([first_user[i],second_user[i]])

    return common_movie_ratings

for i in ratings.keys():
    for j in ratings.keys():
        if not i==j:
            common_movie_ratings=find_similar_movie_ratings(ratings[i],ratings[j])

            pass



class filter:

    def __init__(self):
        self.movie_ratings={}
        self.users_mean_ratings={}
        self.mean_centered_ratings={}
        self.common_ratings_between_users={}
        self.weights_of_users={}

    def load_data(self):
        with open('./netflix/TrainingRatings.txt') as f:
            lines = f.readlines()

        for i in lines:
            temp=i.replace("\n","").split(',')
            if not temp[1] in self.movie_ratings.keys():
                self.movie_ratings[temp[1]]={}

            self.movie_ratings[temp[1]][temp[0]]=float(temp[2])

    def calculate_mean_ratings_of_users(self):
        for i in self.movie_ratings.keys():
            sum_of_ratings=0
            count=0

            for j in self.movie_ratings[i].keys():
                sum_of_ratings+=self.movie_ratings[i][j]
                count+=1
            
            self.users_mean_ratings[i]=sum_of_ratings/count

            for j in self.movie_ratings[i].keys():
                if not i in self.movie_ratings.keys():
                    self.mean_centered_ratings[i]={}
                self.mean_centered_ratings[i][j]=self.movie_ratings[i][j]-self.users_mean_ratings[i]

    def find_common_ratings_between_users(self,user1,user2):
        common_ratings=[]
        if len(user1.keys())>len(user2.keys()):
            for i in user2.keys():
                if i in user1.keys():
                    common_ratings.append([user1[i],user2[i]])
        else:
            for i in user1.keys():
                if i in user2.keys():
                    common_ratings.append([user1[i],user2[i]])



    def calculate_weights_of_users(self):
        for i in self.movie_ratings.keys():
            for j in self.movie_ratings.keys():
                if not i ==j :
                    if not i in self.common_ratings_between_users.keys():
                        self.common_ratings_between_users[i]={}
                    self.common_ratings_between_users[i][j]=self.find_common_ratings_between_users(self.movie_ratings[i],self.movie_ratings[j])