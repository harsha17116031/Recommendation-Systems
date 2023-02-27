import math

class filter:

    def __init__(self):
        self.movie_ratings={}
        self.users_mean_ratings={}
        self.mean_centered_ratings={}
        self.common_ratings_between_users={}
        self.sum_of_squares_of_ratings_for_users={}
        self.weights_of_users={}
        self.normalizing_factor={}
        self.start()

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
                if not i in self.mean_centered_ratings.keys():
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

        return common_ratings



    def calculate_weights_of_users(self):
        for i in self.movie_ratings.keys():
            for j in self.movie_ratings.keys():
                if not i ==j :
                    if not i in self.common_ratings_between_users.keys():
                        self.common_ratings_between_users[i]={}
                    self.common_ratings_between_users[i][j]=self.find_common_ratings_between_users(self.movie_ratings[i],self.movie_ratings[j])


        for i in self.common_ratings_between_users.keys():
            for j in self.common_ratings_between_users[i].keys():
                common_ratings=self.common_ratings_between_users[i][j]

                sum_of_product_user1_user2=0
                sum_of_squares_user1=0
                sum_of_squares_user2=0

                for k in common_ratings:
                    sum_of_product_user1_user2+=k[0]*k[1]
                    sum_of_squares_user1+=k[0]**2
                    sum_of_squares_user2+=k[1]**2
                
                if not j in self.weights_of_users[i]:
                    self.weights_of_users[i]={}
                
                self.weights_of_users[i][j]=sum_of_product_user1_user2/math.sqrt(sum_of_squares_user1*sum_of_squares_user2)

    
    def calculate_normalizing_factors(self):
        for i in self.weights_of_users.keys():
            sum_of_weights=0
            for j in self.weights_of_users[i].keys():
                sum_of_weights+=self.weights_of_users[i][j]
            self.normalizing_factor[i]=sum_of_weights


    def start(self):
        self.load_data()
        self.calculate_mean_ratings_of_users()
        self.calculate_weights_of_users()
        self.calculate_normalizing_factors()



algo=filter()

print(algo.normalizing_factor)



