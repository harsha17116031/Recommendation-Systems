# Recommendation Systems

The task in collabartive filtering is to predict the utility og items to a particular user (the active user) based on a database of user votes from a sample or population of other users (the user database).

We are implementing a memory based algorithm that operate over the entire user database to make predictions.The user database consists of a set of votes $v_{ij}$ corresponding to the vote of user i on item j. If $I_{i}$ is the set of items on which user i has voted, then we can define the mean vote for user i as 
```math
\bar{v} _{i} = {1 \over  |I_{i}|} \sum_{j \in I_{i}} v_{i,j}
```

In memory-based collaborative filtering algorithms, we predict the votes of the active user indicated with a subscript a based on some partial information regarding the active user and a set of weights calculated from the user database. We assume that the predicted vote of the active user for item j, $p_{a,j}$ is a weighted sum of votes of the other users.

```math
p_{a,j} = \bar{v}_{a} + \kappa \sum_{i=1}^{n} w(a,i)(v_{i,j}- \bar{v}_{i})
```

where n is the number of users in the collaborative filtering database with nonzero weights. The weights w(i,a) can reflect distance, correlation, or similarity between each user i and the active user. $\kappa$ is a normalizing factor usch that the absolute values of the weights sum to unity.

Correlation between active user $a$ and $i^{th}$ user is given by:
```math
w(a,i) = {{\sum_{j}(v_{a,j}-\bar{v}_{a})(v_{i,j}-\bar{v}_{i})} \over {\sqrt{\sum_{j}(v_{a,j}-\bar{v}_a)^2 \sum_{j}(v_{i,j}-\bar{v}_{i})^2}}}

A matrix of weights is generated which is further used to predict the ratings. The dataset being used is a subset of movie ratings data from Netflix Prize. The dataset has 3.25 million user ratings that contains ~28000 users and ~1900 movies. Evaluation metrics used are Mean Absolute Error and Root Mean Squared Error.
