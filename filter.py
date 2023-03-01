import math
import numpy as np
import pickle

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
        print("loading data ")
        with open('./netflix/TrainingRatings.txt') as f:
            lines = f.readlines()

        for i in lines:
            temp=i.replace("\n","").split(',')
            if not temp[1] in self.movie_ratings.keys():
                self.movie_ratings[temp[1]]={}

            self.movie_ratings[temp[1]][temp[0]]=float(temp[2])
        
        print("data loaded successfully...")

    def calculate_mean_ratings_of_users(self):
        print('calculating mean ratings of users')
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
        
        print("done calculating means")

    def find_common_ratings_between_users(self,index_user1,index_user2,user1,user2):
        
        sum_of_product_of_ratings=0
        sum_of_squares_user1=0
        sum_of_squares_user2=0
        if len(user1.keys())>len(user2.keys()):
            
            for i in user2.keys():
                if i in user1.keys():
                    sum_of_product_of_ratings+=user1[i]*user2[i]
                    sum_of_squares_user1+=user1[i]**2
                    sum_of_squares_user2+=user2[i]**2

            if not index_user1 in self.weights_of_users.keys():
                self.weights_of_users[index_user1]={}  
            try: 
                self.weights_of_users[index_user1][index_user2]=sum_of_product_of_ratings/math.sqrt(sum_of_squares_user1*sum_of_squares_user2)
            except Exception:
                self.weights_of_users[index_user1][index_user2]=0
        else:
            for i in user1.keys():
                if i in user2.keys():
                    sum_of_product_of_ratings+=user1[i]*user2[i]
                    sum_of_squares_user1+=user1[i]**2
                    sum_of_squares_user2+=user2[i]**2
            
            if not index_user1 in self.weights_of_users.keys():
                self.weights_of_users[index_user1]={}    
            try: 
                self.weights_of_users[index_user1][index_user2]=sum_of_product_of_ratings/math.sqrt(sum_of_squares_user1*sum_of_squares_user2)
            except Exception:
                self.weights_of_users[index_user1][index_user2]=0
        print(index_user1,index_user2)

        




    def calculate_weights_of_users(self):
        print("finding common ratings between users")
        for i in self.movie_ratings.keys():
            for j in self.movie_ratings.keys():
                if not i in self.common_ratings_between_users.keys():
                    self.common_ratings_between_users[i]={}
                
                self.find_common_ratings_between_users(i,j,self.movie_ratings[i],self.movie_ratings[j])

        print("done finding common ratings between users")
        with open('weights.pk','wb') as f:
            pickle.dump(self.weights_of_users,f)

        print('calculating weights of users with respect to each other')
        # for i in self.common_ratings_between_users.keys():
        #     for j in self.common_ratings_between_users[i].keys():
        #         common_ratings=self.common_ratings_between_users[i][j]

        #         sum_of_product_user1_user2=0
        #         sum_of_squares_user1=0
        #         sum_of_squares_user2=0

        #         for k in common_ratings:
        #             sum_of_product_user1_user2+=k[0]*k[1]
        #             sum_of_squares_user1+=k[0]**2
        #             sum_of_squares_user2+=k[1]**2
                
        #         if not j in self.weights_of_users[i]:
        #             self.weights_of_users[i]={}
                
        #         self.weights_of_users[i][j]=sum_of_product_user1_user2/math.sqrt(sum_of_squares_user1*sum_of_squares_user2)

        print('done calculating weights')
    
    def calculate_normalizing_factors(self):
        print('calculating normalizing factors for users')
        for i in self.weights_of_users.keys():
            sum_of_weights=0
            for j in self.weights_of_users[i].keys():
                sum_of_weights+=self.weights_of_users[i][j]
            self.normalizing_factor[i]=sum_of_weights

        with open('normalizingFactors.pk','wb') as f:
            pickle.dump(self.normalizing_factor,f)
        
        print('done calularing normalizing factors...')


    def start(self):
        self.load_data()
        self.calculate_mean_ratings_of_users()
        self.calculate_weights_of_users()
        self.calculate_normalizing_factors()



algo=filter()

print(algo.normalizing_factor)



