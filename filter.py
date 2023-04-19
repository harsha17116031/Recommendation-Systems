import numpy as np
import math
import pickle
import warnings

class Filter:

    def __init__(self):

        warnings.filterwarnings('ignore')

        self.update=True

        self.user_indexer={}
        self.movie_indexer={}
        self.movie_index=0
        self.user_index=0
        self.shortcut_ratings={}
        self.shortcut_mean_ratings={}
        self.shortcut_mean_centered_ratings={}
        self.mean_of_user_ratings=[]
        self.predicted_ratings=[]
        self.true_ratings=[]


        self.start()


    def load_data(self):
        print("loading data ..")
        with open('./netflix/TrainingRatings.txt') as f:
            lines=f.readlines()

        for i in lines:
            values=i.replace("\n","").split(',')
            if not  values[0] in self.movie_indexer:
                self.movie_indexer[values[0]]=self.movie_index
                self.movie_index+=1
            
            if not values[1] in self.user_indexer:
                self.user_indexer[values[1]]=self.user_index
                self.user_index+=1

        self.ratings=np.zeros([self.user_index,self.movie_index])
        self.mean_centered_ratings=np.zeros([self.user_index,self.movie_index])
        self.weights_of_users=np.zeros([self.user_index,self.user_index])

        
        for i in lines:
            values=i.replace("\n","").split(',')
            index_of_movie=self.movie_indexer[values[0]]
            index_of_user=self.user_indexer[values[1]]

            self.ratings[index_of_user][index_of_movie]=values[2]

            if not values[1] in self.shortcut_ratings.keys():
                self.shortcut_ratings[values[1]]={}

            self.shortcut_ratings[values[1]][values[0]]=float(values[2])

    def calculate_mean_of_ratings(self):
        self.mean_of_user_ratings=np.true_divide(self.ratings.sum(1),(self.ratings!=0).sum(1))
    
        print('calculating mean ratings of users')
        for i in self.shortcut_ratings.keys():
            sum_of_ratings=0
            count=0

            for j in self.shortcut_ratings[i].keys():
                sum_of_ratings+=self.shortcut_ratings[i][j]
                count+=1
            
            self.shortcut_mean_ratings[i]=sum_of_ratings/count

            for j in self.shortcut_ratings[i].keys():
                if not i in self.shortcut_mean_centered_ratings.keys():
                    self.shortcut_mean_centered_ratings[i]={}
                
                self.shortcut_mean_centered_ratings[i][j]=self.shortcut_ratings[i][j]-self.shortcut_mean_ratings[i]
        print("done calculating means")
    
    def matrix_from_shortcut(self):
        print('started matrix')
        for i in self.shortcut_mean_centered_ratings.keys():
            for j in self.shortcut_mean_centered_ratings[i].keys():
                self.mean_centered_ratings[self.user_indexer[i]][self.movie_indexer[j]]=self.shortcut_mean_centered_ratings[i][j]

        print('done with matrix')

    def find_denominator_and_weights(self):
        for i in range(0,self.user_index):
            print(i)
            for j in range(i,self.user_index):
                A=self.mean_centered_ratings[i]
                B=self.mean_centered_ratings[j]

                AB=np.multiply(A,B)
                ABB=np.multiply(AB,B)

                A=np.divide(AB,B)
                A[np.isnan(A)]=0

                B=np.divide(ABB,A)
                B[np.isnan(B)]=0

                A=np.square(A)

                self.weights_of_users[i][j]=self.product_of_user_ratings[i][j]/math.sqrt(np.sum(A)*np.sum(B))

        self.weights_of_users=self.weights_of_users+np.transpose(self.weights_of_users)
        self.weights_of_users[np.isnan(self.weights_of_users)]=0
        np.fill_diagonal(self.weights_of_users,1)

        return 


    def calculate_weights_of_users(self):
        self.sum_of_squares_of_centered_ratings=np.sum(np.square(self.mean_centered_ratings),axis=1)

        self.product_of_user_ratings=np.dot(self.mean_centered_ratings,np.transpose(self.mean_centered_ratings))

        self.find_denominator_and_weights()
        self.n_factors=np.sum(self.weights_of_users,axis=1)
        

    def is_it_nan(self,value):
        if value=='nan':
            return 0
        else:
            return value

    def predict(self,values):
        movie_id=values[0]
        user_id=values[1]
        rating=values[2]

        self.true_ratings.append(float(rating))

        user_id_index=self.user_indexer[user_id]
        movie_id_index=self.movie_indexer[movie_id]


        predicted_rating=self.mean_of_user_ratings[user_id_index]+self.is_it_nan(((self.merged_data[user_id_index][movie_id_index])/self.n_factors[user_id_index]))
        self.predicted_ratings.append(predicted_rating)

    def load_test_data(self):
        print('loading test data.....')

        with open('./netflix/TestingRatings.txt') as f:
            lines=f.readlines()

        count=0
        for i in lines:
            #print(count)
            values=i.replace("\n","").split(',')
            
            self.predict(values)
            count+=1



    def test(self):
        
        print('merging data ....')
        self.merged_data=np.dot(self.weights_of_users,self.mean_centered_ratings)
        print('done merging..')
        self.load_test_data()

    
    def evaluate_test_results(self):

        self.predicted_ratings=np.array(self.predicted_ratings)
        self.predicted_ratings[np.isnan(self.predicted_ratings)]=0
        predicted_ratings=self.predicted_ratings

        true_ratings=np.array(self.true_ratings),

        print("MAE is : ",np.mean(np.abs(np.subtract(true_ratings,predicted_ratings))))

        print("RMSE is : ",math.sqrt(np.square(np.subtract(true_ratings,predicted_ratings)).mean()))


    def start(self):
        self.load_data()
        self.calculate_mean_of_ratings()
        self.matrix_from_shortcut()
        self.calculate_weights_of_users()

        self.test()

        self.evaluate_test_results()




filter=Filter()

