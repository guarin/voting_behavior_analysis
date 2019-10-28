**Title**
=========

**Abstract**
============

Political parties are often considered to be an essential part of
democratic systems. Their existence is justified in two ways: First,
they regroup politicians of similar opinions, which allows them to work
towards their common goals. Second, they are needed in most political
systems to form a government, by supporting presidential candidates like
in the United States and France, or through coalitions like in most
European countries. However, in the particular case of the Swiss
democracy, the executive branch consists of a 7-headed council chosen to
equally represent the entire voting population. This system doesn\'t
inherently rely on political parties, raising the following question: Is
their existence justified in the Swiss democratic model? We aim to
answer this question by analysing the voting behavior of members of the
national council, the larger of the two legislative chambers, over the
course of 12 years.

**Research questions**
======================

As stated in the abstract, our main research question is the following:

*Is the existence of political parties justified in the Swiss
democracy?*

We will divide the problem into three distinct subproblems for our
analysis. Each of them raises practical questions that can be answered
using our data, which are listed below.

1.  *Do the political parties efficiently group politicians with common
    interests?*

Can we recover the existing political parties using politician voting
behavior without further a priori knowledge?

Do we observe divides within existing political parties?

2.  *Is having party support useful to furthering a political agenda?\
    *Do politicians show up to vote for motions that come from their own
    party?*\
    *Do people tend to vote yes for motions that come from members of
    their own party?

3.  *Are political parties essential for choosing the executive federal
    council?\
    *How are members of the federal council related to their positioning
    within a party?

If we were to abolish political parties, who would be ideal members of
the federal council to best represent the voting population?

**Dataset**
===========

Our research is based on two datasets:

1.  Votes of council members between 2007 and 2019

2.  Information on each council member since 1848

The first dataset is about 900MB in size (uncompressed). It has
\~200'000 entries per year. Each entry contains information on a motion
and how one member of the council voted on that motion. With the
national council having 200 members we have results for \~1'000 votes
per year. The data covers 12 years and therefore 3 legislative periods
(2007-2011, 2011-2015, 2015-2019).

The second dataset contains background information of every member of
the national council and the council of states since 1884. It is only a
few megabytes large and has 6'400 entries. Each entry states information
such as name, canton of origin, political party, mandates and start/end
dates of entering/leaving the council for each member.

The datasets need some cleaning as they contain html artifacts and
non-standard character escaping patterns. The goal is to join the two
datasets on the council members. Furthermore, we have to find optimal
representations of the data for the data analysis part. Both steps are
further described in the internal milestones.

***Sources:***

1.  [[https://www.parlament.ch/en/ratsbetrieb/abstimmungen/abstimmungs-datenbank-nr]{.underline}](https://www.parlament.ch/en/ratsbetrieb/abstimmungen/abstimmungs-datenbank-nr)

2.  [[https://www.parlament.ch/en/ratsmitglieder?k=PdMemberCouncilCouncil:1+PdMemberCouncilActive:true\#k=]{.underline}](https://www.parlament.ch/en/ratsmitglieder?k=PdMemberCouncilCouncil:1+PdMemberCouncilActive:true#k=)

**A list of internal milestones up until project milestone 2**
==============================================================

***Data exploration:***

-   What information do we have access to?

-   What is the format of the data, is some missing, are values in all
    columns in similar format?

-   Restructure data to get a table of politicians as columns and issues
    with their sponsors as rows.

-   Join data about politicians (age, party, etc.) with the vote
    dataset.

***Data wrangling:***

-   Find inconsistent, incoherent, missing values and find appropriate
    ways of dealing with them

-   Handle language inconsistencies between data sets

-   Handle abstentions and absences for numerical analysis

***Data Analysis:***

Part 1:

-   Apply dimensionality reduction to the issues, to get a dataset with politicians as observations and principal voting directions as features

-   Cluster politicians according to the reduced data using k-means, validate using spectral clustering on a kNN graph

-   Compare resulting clustering with the existing political parties

-   Calculate measures of "isolatedness", "closeness" and "dividedness" of existing political parties, observe their evolution over time

Part 2:

-   Visualization of general attendance compared to attendance to one's own party proposed votation

-   Visualization proportion of "yes" to one's own party proposed votation compared to rest of votations

Part 3:

-   Analyze political positions of politicians who later entered the federal council

-   Determine ideal members of federal council as cluster means when performing k-means clustering with k=7.

**Questions for TAs**
=====================

-   Do you have any additional datasets in your laboratory that could provide interesting information on the subject?
