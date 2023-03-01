import numpy as np
import math
import pickle

class Filter_Train:

    def __init__(self):

        self.update=False

        self.user_indexer={}
        self.movie_indexer={}
        self.movie_index=0
        self.user_index=0
        self.ratings=[]

        self.shortcut_ratings={}
        self.shortcut_mean_ratings={}
        self.shortcut_mean_centered_ratings={}

        self.mean_of_user_ratings=[]
        self.mean_centered_ratings=[]


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

        with open('user_indexer.pk','wb') as f:
            pickle.dump(self.user_indexer,f)
        

        with open('movie_indexer.pk','wb') as f:
            pickle.dump(self.movie_indexer,f)

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
        with open('mean_ratings_of_users.npy','wb') as f:
            np.save(f,self.mean_of_user_ratings)

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

                A1=np.divide(AB,B)
                A2=np.divide(ABB,AB)

                A1[np.isnan(A1)]=0
                A2[np.isnan(A2)]=0

                self.weights_of_users[i][j]=self.product_of_user_ratings[i][j]/math.sqrt(np.sum(np.square(A1))*np.sum(np.square(A2)))

        self.weights_of_users=self.weights_of_users+np.transpose(self.weights_of_users)

        return 


    def calculate_weights_of_users(self):
        #self.weights_of_users=np.zeros([self.user_index,self.user_index])

        self.sum_of_squares_of_centered_ratings=np.sum(np.square(self.mean_centered_ratings),axis=1)

        if not self.update:
            print("loading variables ...")
            with open('product_ratings.npy','rb') as f:
                self.product_of_user_ratings=np.load(f)
            
            
            with open('weights_of_users.npy','rb') as f:
                self.weights_of_users=np.load(f)
            
            self.weights_of_users[np.isnan(self.weights_of_users)]=0

            with open('mean_ratings.npy','rb') as f:
                self.mean_centered_ratings=np.load(f)

            with open('nFactor.npy','rb') as f:
                self.temp=np.load(f)

            print('successfull loaded varibales')
        else:

            self.product_of_user_ratings=np.dot(self.mean_centered_ratings,np.transpose(self.mean_centered_ratings))
            with open('product_ratings.npy','wb') as f:
                np.save(f,self.product_of_user_ratings)

            self.find_denominator_and_weights()
            

            with open('weights_of_users.npy','wb') as f:
                np.save(f,self.weights_of_users)
        
            with open('mean_ratings.npy','wb') as f:
                np.save(f,self.mean_centered_ratings)

            self.temp=np.sum(self.weights_of_users,axis=1)
            with open('nFactor.npy','wb') as f:
                np.save(f,self.temp)
            print(self.temp)
     

    def start(self):
        self.load_data()
        self.calculate_mean_of_ratings()
        self.matrix_from_shortcut()
        self.calculate_weights_of_users()




filter=Filter_Train()


print(filter.weights_of_users)
print(np.shape(filter.weights_of_users))
