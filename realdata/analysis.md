# Co-authorship Conflict Analysis

## Q1

The main network has 10855 nodes and 14,854 edges.
It is not connected and has 7 connected components.
Only 7 components means that the network is almost connected.
The network has a density of around 0.00025, meaning that the network is very sparse with many missing edges.
The average degree is 2.7, the maximum is 453 and the minimum degree is 1.
This means that few hub nodes are very connected while most nodes have very few connections.

The reviewer subgraph has 244 nodes and 390 edges.
It is also not connected but with 43 connected components. This means that many small components of reviewers exist that are not connected.
It is more dense than the main network with a density of around 0.013.
The degree distribution is not as skewed as the main graph but still skewed with an average degree of 3.2, a max of 18 and a min of 0.
Some reviewers are more connected than others.

Figure 1 shows the degree distributions for both networks.

![Figure 1](./figures/figure-1.png)

## Q2

To find the central nodes I checked all centralities covered in the course: degree , betweenness , closeness and PageRank.
All centralities were computed on the main network and split into reviewers and non-reviewers.

The most central reviewers in the network are Yifan Li, Jie Song, Feifei Li, Bingsheng He and Guoliang Li.
Yifan Li is first in degree centrality and PageRank meaning that they have the most co-authors and the most influence.
Guoliang Li ranks first in betweenness and closeness meaning that they are a bridge between different parts of the network and are on average closest to all other nodes.

The most central non-reviewer authors are H. V. Jagadish, Tim Kraska and Michael Stonebraker.
H. V. Jagadish ranks first on all centrality measures making them the most central non-reviewer in the network.
His centrality values are higher than other non-reviewers especially in betweenness which suggests they are important in connecting different parts of the network.

Overall, reviewers have much higher centrality values than non-reviewers which makes sense since reviewers are probably more experience and have more connections.

## Q3

To get communities I used the Louvain algorithm from the the Lecture 09b material. I also tried Girvan-Newman but it was too slow on the huge network.

Louvain found 49 communities.
We can see in Figure 2 that the community sizes decrease linearly from around 600 nodes in the largest community down to few nodes in the smallest.
There is no clear gap between large and small communities.

This means that there are no clearly distinguishable clusters in the network.
If there was a strong community structure we would see separated large groups with gaps.

![Figure 2](./figures/figure-2.png)

## Q4

The dataset only contains edges between pairs where at least one person is a reviewer.
This affects all of our answers.

For Q1, the network is much sparser than the full co-authorship network since many edges between non-reviewer authors exist but are not in the data.
The 7 components might be connected with a missing edge.
The degree of non-reviewer authors is also lower since we only see their connections to reviewers.
The reviewer sub-network is probably less affected since edges between reviewers are in the data.

For Q2, the centrality of non-reviewer authors is probably lower.
The top non-reviewer centrality values were much lower than the top reviewers.
Non-reviewer authors might have more connections which would increase their centrality.
Reviewer centrality is also affected since missing edges could create more paths that would change betweenness and closeness.

For Q3, the missing edges could merge some of the communities.
The real community structure could look different with the complete data.

In summary, all results are affected by the dataset limitation.
The network is a reviewer-focused and the missing data makes it impossible to draw conclusions about the full co-authorship network.
