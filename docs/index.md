---
title: Swiss Politics
layout: default
---

Political parties are often considered to be an essential part of democratic systems. Their existence is justified in two ways: First, they regroup politicians of similar opinions, which allows them to work towards their common goals. Second, they are needed in most political systems to form a government, by supporting presidential candidates like in the United States and France, or through coalitions like in most European countries. However, in the particular case of the Swiss democracy, the executive branch consists of a seven-headed council chosen to equally represent the entire voting population. This system doesn't inherently rely on political parties, raising the following question: Is their existence justified in the Swiss democratic model? We aim to answer this question by analysing the voting behavior of members of the national council, the larger of the two legislative chambers, over the course of 12 years.

# The Swiss Political System

Before getting started with the data analysis, we give a brief overview of the Swiss democratic system and introduce some terminology that we will use throughout the analysis. It is split up in a *legislative* (law-making) branch, an *executive* (governing) branch and a *judicative* (tribunal) branch. The legislative branch is further split up into two chambers: In the *National Council* with 200 members, every canton has a number of seats proportional to its population. It is thus responsible for keeping the interests of the population. In the smaller *Council of States*, every canton gets two seats, regardless of its size. It is therefore designed to keep the interests of the cantons. 

Whereas members of the executive and legislative branches of government are often members of political parties, their party affiliation should not have an impact on their work. Moreover, parties have a subsidiary role in the concil of states, since there the canton interest is more important than the interest of the individual politician. Hence, the political parties are only of real importance to the members of the national council, which is precisely the data we will look at in our analysis.

Politicians of the legislative branch are re-elected every 4 years. This period of 4 years where mostly the same politicians are working together making laws is called a legislative period. Within our analysis we will look at three such legislative periods, considering data from summer 2007 until summer 2019. Since many politicians change from period to another, we will split up our analysis into the individual legislative periods.

Finally there are a few politicians that come from minor, mostly regional parties in the national council. They can join forces with the large national parties by forming a parliamentary group. This is actually required for them if they want to join a comission, which is why only very few politicians never join a parliamentary group. In order to avoid having to look at very small parties, we will look at the parliamentary groups instead throughout our analysis.

# Recovering Political Parties

In order to first see whether the political parties make sense, we create a social network of politicians where every politician is connected to the politicians whose voting behavior is closest to theirs. If we plot this network and color it by parliamentary groups, it looks like this:

<div style="text-align: center;"><iframe src="assets/html/party_assignment.html" width="100%" height="425" scrolling="yes" seamless="seamless" frameborder="0"></iframe></div>
<div style="text-align: center;"><iframe src="assets/html/party_assignment_legend.html" width="100%" height="160" scrolling="yes" seamless="seamless" frameborder="0"></iframe></div>

We can already see that politicians within the same party strongly tend to be connected to members of their own party. 

Moreover, there are some interesting things that can be observed: First, the Green Party (PES, in light green) has become very close to the Socialist Party (PSS, in red) in the last legislature, making it hard to distinguish. Moreover, the Green Liberal Party (PVL, in purple) is very isolated in the second legislative period. This is probably due to the fact that this was the first period during which they were represented in parliament, and thus they tried to vote very similarly in order to gain profile and to achieve their goals. However, they've since gotten closer to the political middle, consisting of the Liberal Democrats (yellow) and Christian Democrats (orange).

Based on this network we try to divide the politicians into communities using the spectral clustering algorithm. Here are the results, visualized on the same graph as before with each color representing a community:

<div style="text-align: center;"><iframe src="assets/html/spectral_clustering.html" width="100%" height="425" scrolling="no" seamless="seamless" frameborder="0"></iframe></div>

We confirm what we already visually saw, that the political parties can be recovered very well just from the voting data. Sometimes, the parties are divided into one or more sub-clusters, which is due to the fact that the algorithm favors parties of the same size. Moreover, the politicians in the middle parties (Green Liberals, Liberal Democrats and Christian Democrats) are hard to tell apart. But the fact that we can recover the parties this robustly suggests that they do have a justification in Swiss politics.

# Picking an Executive Power 

In Switzerland the executive branch of government consists of a council of seven people, which are chosen to equally represent the entire voting population and is called the Federal Council. Party membership is very important in its constitution: It is an unwritten rule that every major party has a "right" to one or more federal councillors according to their share of the popular vote, in order to properly represent the will of the Swiss people. 

## The (Un-)Importance of Centrality

We first investigate who is chosen to become members of the executive: One would think that a federal councillor should be particularly central to their party, in order to well represent the party interest. To this effect, we look at the following four politicians which were simultaneously in the national council during the 2007-2011 legislative period:

- Parmelin Guy (UDC) in function as federal councillor from 2016
- Schneider-Ammann Johann N. (PLR) federal councillor from 2010 to 2018
- Amherd Viola (PDC) in function as federal councillor from 2010
- Cassis Ignazio (PLR) in function  as federal councillor from 2017 

Note that the fact that we only have this few future federal councillors in our data somewhat limit the conclusions that can be drawn from our analysis.

The following graph shows where the federal councillors lie on the social network:

<iframe src="assets/html/real_graph.html" width="100%" height="500" scrolling="no" seamless="seamless" frameborder="0"></iframe>

From the graph, it seems that none of the examples we have seen are very central to their party. Guy Parmelin is even at the edge of the group. This would indicate that having a voting pattern representative of one's party is not essential to be elected for the Federal Council. This can be further proven by ranking each members "closeness" to the rest of its party. Federal councillors are highlighted in pink:

<div style="text-align: center;">
    <div>
        <iframe src="assets/html/centrality_plot_0.html" width="100%" height="320" scrolling="yes" seamless="seamless" frameborder="0"></iframe>
        <iframe src="assets/html/cnetrality_plot_1.html" width="100%" height="320" scrolling="yes" seamless="seamless" frameborder="0"></iframe>
    </div>
</div>


None of the elected councillors (maybe with the exception of Ignazio Cassis) seem to have a voting pattern that is very representative of their political party. The reason for this is likely the fact that the federal council is elected by the entire political spectrum, and not only the politicians party. Take the case of the politician of the right party, Guy Parmelin: He likely was able to become elected *because* he isn't representative of his party. This means that in some cases, the way the federal councillors are chosen doesn't lead to a good representation of the will of the Swiss voters. 

If a party would want one of their members to represent them in the Federal Founcil, they would probably vote for the most representative politician in their ranks. Our findings suggest that this is not the case. This is therefore in opposition with the way the media depicts the election. The interpretability of those results is of course very limited by the scarcity of the data. 

## A Better Alternative

Having seen that the way the politicians are chosen is sub-optimal, we ask whether we can find a better way to choose the federal council. Note that this is very relevant today: Since the green party (PES) has gained many seats in the last election, they now also want a seat in the federal council. According to <a href="https://www.nzz.ch/schweiz/bunderatswahlen-die-zauberformel-verliert-ihre-magie-ld.1518450#subtitle-3-heute-2-2-2-1-passt-nicht-mehr-second">this article</a>, more voters aren't represented in the executive than ever before.

We therefore suggest another, data-driven alternative for choosing the federal council. To make our pick we make the following assumptions:





The generally accepted idea that a politician is elected to the Federal Council mostly based on his/her political party is challenged by our previous results. Yet, this is a key argument in all debates surrounding the elections. This is even more true now, as the recent election for the Federal Council has raised a new controversy. The new council is criticized for not being representative enough of the current swiss political landscape. The major issue is the continued absence of councillors from the Green Party (PES), which has significantly grown in size in the last decade.

We make the claim that we can make a pick that is not based on political party, but simply on the voting pattern of the national councillors. Of course the executive power is not only chosen from the national council, so our solution is not optimal.

To make our pick we make the following assumptions:

- Voting patterns are a good indication of the political orientation of a councillor
- The optimal pick for the Federal Council is seven members whose political orientation is best representing seven equal sized sub-groups of the National Council
- The best single point representation of a group is at its center

We therefore split the National Council in seven subgroups and pick the most central politican in each of them. This results in a set of federal councillors for the upcoming legislative that might be more representative that the one that got elected. Each group is represented by a color, federal councillors are shown in pink:

<div style="text-align: center;"><iframe src="assets/html/next_legislative_pick.html" width="100%" height="420" scrolling="no" seamless="seamless" frameborder="0"></iframe></div>


There is no overlap between our pick and the current federal councillors. None of "our" councillors were even a candidate at a Federal Council election. This indicates that our way of selecting an executive power is quite different from what is currently implemented. We also see that no member of the Green Party is part of our pick, even though a member of the Green Liberal Party (PVL) who historically never had a federal councillor make it into the list.

This choice is limited by the fact that it is only suggests national councillors for becoming members of the executive, even though in practice several members of the Council of States also move to the Federal Council. Moreover, we could only suggest the next federal council based on the previous legislative period. Large shifts in seats hence would only be represented in the executive 4 years later. This is however in the interest of Swiss democracy, which has a strong focus on ensuring continuity and to prevent rapid changes making the political system unstable. Finally, other considerations are important for choosing the federal council, such as the region of origin or the gender. 

If there is no way of knowing that this pick would make a good executive power, it would at least be a bold new choice. 

## Conclusion 

The need of political parties in Switzerland can be challenged by looking at the votes of some of the members of the legislative power over 12 years. Of the two common justifications for their existence, only one seems to hold up. 

Swiss political parties do regroup politicians of similar opinions. Regrouping people that vote in a similar way results in regrouping people by their party membership. 

However, they are not needed to form a government. The politicians that get elected are not a good representation of the party they belong to. Furthermore, they are criticized for being unrepresentative of the general population. We have suggested a new way to select the executive branch, which would better represent the interest of the Swiss people. 







