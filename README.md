# Recommendation Systems

The task in collabartive filtering is to predict the utility og items to a particular user (the active user) based on a database of user votes from a sample or population of other users (the user database).

We are implementing a memory based algorithms which operate over the entire user database to make predictions.The user database consists of a set of votes $v_{ij}$ corresponding to the vote of user i on item j. If $I_{i}$ is the set of items on which user i has voted, then we can define the mean vote for user i as 
$$\bar{v} _{i} = \frac{1}{\mod{I_{i}}} \sum_{j \in I_{i}}$$