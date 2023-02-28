import numpy as np
import math

class Filter:

    def __init__(self):
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

        self.ratings=np.zeros([self.user_index,self.movie_index])
        self.mean_centered_ratings=np.zeros([self.user_index,self.movie_index])


        for i in lines:
            values=i.replace("\n","").split(',')
            index_of_movie=self.movie_indexer[values[0]]
            index_of_user=self.user_indexer[values[1]]

            self.ratings[index_of_user][index_of_movie]=values[2]

            if not values[1] in self.shortcut_ratings.keys():
                self.shortcut_ratings[values[1]]={}

            self.shortcut_ratings[values[1]][values[0]]=float(values[2])

    def calculate_mean_of_ratings(self):
        #self.mean_of_user_ratings=np.true_divide(self.ratings.sum(1),(self.ratings!=0).sum(1))

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
        print('strated matrix')
        for i in self.shortcut_mean_centered_ratings.keys():
            for j in self.shortcut_mean_centered_ratings[i].keys():
                self.mean_centered_ratings[self.user_indexer[i]][self.movie_indexer[j]]=self.shortcut_mean_centered_ratings[i][j]

        print('done with matrix')

    def calculate_mean_centered_ratings(self):
        pass
        
            

    def start(self):
        self.load_data()
        self.calculate_mean_of_ratings()
        self.calculate_mean_centered_ratings()
        self.matrix_from_shortcut()




filter=Filter()

print(filter.mean_centered_ratings)
