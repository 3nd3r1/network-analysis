# Co-authorship Conflict Analysis

## Q1

The full network has 10855 nodes and 14,854 edges.
The network is not connected and has 7 connected components.
The largest component contains 10764 nodes (99%) meaning that almost all nodes are reachable from each other.
The network has a density of around 0.00025, meaning that the network is very sparse with many missing edges.
The average degree is 2.7, the maximum is 453 and the minimum degree is 1.
This means that few hub nodes are very connected while most nodes have very few connections.

The reviewer subgraph has 244 nodes and 390 edges.
It is less connected than the full network with 43 connected components.
The largest component contains 193 nodes (79%).
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

Table 1: Top-5 central reviewers by degree, betweenness, closeness and PageRank centrality.

| Rank | Degree Centrality     | Betweenness Centrality | Closeness Centrality   | Pagerank Centrality   |
| ---- | --------------------- | ---------------------- | ---------------------- | --------------------- |
| 1    | yifan li : 0.0417     | guoliang li : 0.0779   | guoliang li : 0.2960   | yifan li : 0.0179     |
| 2    | jie song : 0.0339     | yifan li : 0.0755      | h. jagadish : 0.2856   | jie song : 0.0139     |
| 3    | feifei li : 0.0263    | yuhao zhang : 0.0640   | feifei li : 0.2793     | yuhao zhang : 0.0100  |
| 4    | bingsheng he : 0.0247 | gao cong : 0.0637      | nan tang : 0.2786      | bingsheng he : 0.0090 |
| 5    | yuhao zhang : 0.0239  | feifei li : 0.0625     | xin luna dong : 0.2784 | hongzhi wang : 0.0078 |

Table 2: Top-5 central non-reviewer authors by degree, betweenness, closeness and PageRank centrality.

| Rank | Degree Centrality                    | Betweenness Centrality       | Closeness Centrality         | Pagerank Centrality                  |
| ---- | ------------------------------------ | ---------------------------- | ---------------------------- | ------------------------------------ |
| 1    | h. v. jagadish : 0.0019              | h. v. jagadish : 0.0268      | h. v. jagadish : 0.2839      | h. v. jagadish : 0.0005              |
| 2    | tim kraska : 0.0018                  | tim kraska : 0.0256          | michael stonebraker : 0.2692 | tim kraska : 0.0004                  |
| 3    | michael stonebraker : 0.0014         | michael stonebraker : 0.0148 | tim kraska : 0.2688          | michael stonebraker : 0.0003         |
| 4    | saravanan thirumuruganathan : 0.0013 | reynold cheng : 0.0137       | gang chen 0001 : 0.2672      | saravanan thirumuruganathan : 0.0003 |
| 5    | mourad ouzzani : 0.0011              | themis palpanas : 0.0130     | beng chin ooi : 0.2664       | themis palpanas : 0.0003             |

## Q3

To get communities I used the Louvain algorithm from the the Lecture 09b material. I also tried Girvan-Newman but it was too slow on the huge network.

Louvain found 49 communities.
We can see in Figure 2 that the community sizes decrease linearly from around 600 nodes in the largest community down to few nodes in the smallest.
There is no clear gap between large and small communities.

To understand the strength of communities, I compared the average number of co-authored papers between the authors inside and outside communities.
The average inside communities is 2.23 while between communities it is 2.56.
Because the between community edges are slightly stronger, the communities are not very strong or distinguishable.

In summary, the network does not have clearly distinguishable clusters.

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
