---
title: Swiss Politics
layout: default
---

Political parties are often considered to be an essential part of democratic systems. Their existence is justified in two ways: First, they regroup politicians of similar opinions, which allows them to work towards their common goals. Second, they are needed in most political systems to form a government, by supporting presidential candidates like in the United States and France, or through coalitions like in most European countries. However, in the particular case of the Swiss democracy, the executive branch consists of a 7-headed council chosen to equally represent the entire voting population. This system doesn't inherently rely on political parties, raising the following question: Is their existence justified in the Swiss democratic model? We aim to answer this question by analysing the voting behavior of members of the national council, the larger of the two legislative chambers, over the course of 12 years.

# The Swiss Political System

Before getting started with the data analysis, we give a brief overview of the Swiss democratic system and introduce some terminology that we will use throughout the analysis. It is split up in a *legislative* (law-making) branch, an *executive* (governing) branch and a *judicative* (tribunal) branch. The legislative branch is further split up into two chambers: In the *national council* with 200 members, every canton has a number of seats proportional to its population. It is thus responsible for keeping the interests of the population. In the smaller *council of states*, every canton gets two seats, regardless of its size. It is therefore designed to keep the interests of the cantons. 

Whereas members of the executive and legislative branches of government are often members of political parties, their party affiliation should not have an impact on their work. Moreover, parties have a subsidiary role in the concil of states, since there the canton interest is more important than the interest of the individual politician. Hence, the political parties are only of real importance to the members of the national council, which is precisely the data we will look at in our analysis.

Politicians of the legislative branch are re-elected every 4 years. This period of 4 years where mostly the same politicians are working together making laws is called a legislative period. Within our analysis we will look at three such legislative periods, considering data from summer 2007 until summer 2019. Since many politicians change from period to another, we will split up our analysis into the individual legislative periods.

Finally there are a few politicians that come from minor, mostly regional parties in the national council. They can join forces with the large national parties by forming a parliamentary group. This is actually required for them if they want to join a comission, which is why only very few politicians never join a parliamentary group. In order to avoid having to look at very small parties, we will look at the parliamentary groups instead throughout our analysis.

# Recovering Political Parties

In order to first see whether the political parties make sense, we create a social network of politicians where every politician is connected to the politicians whose voting behavior is closest to theirs. Based on this network we try to divide the politicians into communities using the spectral clustering algorithm. We visualize this on a two-dimensional representation of the network, where nodes are closer to each other if they're closer on the network. 

**TODO THE PLOT**

We see that the clustering consistently splits the conservative party (UDC) into two fractions. Moreover, the green party seems to get increasingly close to the socialdemocratic party.

**Witere stuss**





