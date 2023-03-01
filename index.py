import numpy as np
import pickle

a=np.array([2,3,4,0,0,1,5])
b=np.array([0,4,0,1,0,2,0])

# ab=np.multiply(a,b)

# a=np.divide(ab,a)

# abb=np.multiply(ab,b)

# b=np.divide(ab,b)
# a[np.isnan(a)]=0
# b[np.isnan(b)]=0

print(a,b)
print(len(a))
print(np.mean(np.abs(np.subtract(a,b))),np.abs(np.subtract(a,b)))

# mean_o=np.true_divide(a.sum(1),(a!=0).sum(1))
# print(mean_o)

# with open('true_ratings.pk','rb') as f:
#     true_ratings=pickle.load(f)

with open('predicted_ratings.pk','rb') as f:
    predicted_ratings=np.array(pickle.load(f))
    print(predicted_ratings)
    print(predicted_ratings[np.isnan(predicted_ratings)])

# with open('mean_centered_ratings.npy','rb') as f:
#     mean_centered_ratings=np.load(f)

# with open('mean_ratings_of_users.npy','rb') as f:
#     mean_ratings_of_users=np.load(f)
#     print(mean_ratings_of_users)
#     print(mean_ratings_of_users[np.isnan(mean_ratings_of_users)])

# with open('merged_data.npy','rb') as f:
#     merged_data=np.load(f)
#     print(merged_data[0][0]/367.4)
#     print(merged_data[np.isnan(merged_data)])

# with open('nFactor.npy','rb') as f:
#     nFactors=np.load(f)
#     print(nFactors)
#     print(nFactors[np.isnan(nFactors)])


# #print(true_ratings)
# #print(mean_centered_ratings)
    








