import numpy as np
import math
import pickle

class Filter_Test:

    def __init__(self):

        self.files=['mean_centered_ratings.npy','nFactor.npy','weights_of_users.npy','mean_ratings_of_users.npy']
        self.user_indexer={}
        self.movie_indexer={}
        self.true_ratings=[]
        self.predicted_ratings=[]
        self.save_compute={}

        with open('mean_centered_ratings.npy','rb') as f:
            self.mean_centered_ratings=np.load(f)
            print('mean centered ratings loaded')

        
        with open('weights_of_users.npy','rb') as f:
            self.weights_of_users=np.load(f)
            #self.weights_of_users[np.isnan(self.weights_of_users)]=0
            # self.weights_of_users=self.weights_of_users+np.transpose(self.weights_of_users)
            # np.fill_diagonal(self.weights_of_users,0)
        
        # with open('weights_of_users.npy','wb') as f:
        #     np.save(f,self.weights_of_users)

        with open('nFactor.npy','rb') as f:
            self.nFactor=np.load(f)
            print('n factors loaded')
        # self.nFactor=np.sum(self.weights_of_users,axis=1)

        # with open('nFactor.npy','wb') as f:
        #     np.save(f,self.nFactor)
        #     print('n factors loaded')

            


        
        print(' weights of users loaded')

        with open('mean_ratings_of_users.npy','rb') as f:
            self.mean_ratings_of_users=np.load(f)
            print('mean ratings of users loaded')
        

        self.start()

    
    def merge_weights_and_ratings(self):
        # print(self.weights_of_users)
        # print(self.mean_centered_ratings)
        # print(self.nFactor)
        # print(self.mean_ratings_of_users)
        print(np.shape(self.weights_of_users),np.shape(self.mean_centered_ratings))

        print('started merging')
        self.merged_data=np.dot(self.weights_of_users,self.mean_centered_ratings)
        print('done merging')

        print(self.merged_data)

        with open('merged_data.npy','wb') as f:
            np.save(f,self.merged_data)



    def load_test_data(self):
        print('loading test data ...')

        with open('./netflix/TestingRatings.txt') as f:
            lines=f.readlines()

        with open('user_indexer.pk','rb') as f:
            self.user_indexer=pickle.load(f)
        
        with open('movie_indexer.pk','rb') as f:
            self.movie_indexer=pickle.load(f)
        
        self.merge_weights_and_ratings()
        
        self.test_data=np.zeros([len(self.user_indexer.keys()),len(self.movie_indexer.keys())])

        count=0
        for i in lines:
            #print(count)
            values=i.replace("\n","").split(',')
            
            self.predict(values)
            count+=1
    

    def predict(self,values):
        movie_id=values[0]
        user_id=values[1]
        rating=values[2]

        self.true_ratings.append(float(rating))

        user_id_index=self.user_indexer[user_id]
        movie_id_index=self.movie_indexer[movie_id]


        predicted_rating=self.mean_ratings_of_users[user_id_index]+((self.merged_data[user_id_index][movie_id_index])/self.nFactor[user_id_index])
        self.predicted_ratings.append(predicted_rating)

    def evaluate_predicted_values(self):
        print('evaluating test results...')
        

        with open('predicted_ratings.pk','wb') as f:
            pickle.dump(self.predicted_ratings,f)

        with open('true_ratings.pk','wb') as f:
            pickle.dump(self.true_ratings,f)

        self.predicted_ratings=np.array(self.predicted_ratings)
        self.predicted_ratings[np.isnan(self.predicted_ratings)]=0
        predicted_ratings=self.predicted_ratings

        true_ratings=np.array(self.true_ratings),

        print("MAE is : ",np.mean(np.abs(np.subtract(true_ratings,predicted_ratings))))

        print("RMSE is : ",math.sqrt(np.square(np.subtract(true_ratings,predicted_ratings)).mean()))


    def start(self):
        self.load_test_data()

        self.evaluate_predicted_values()


filter_test=Filter_Test()
