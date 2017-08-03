---
title: Random Sampling in Transition Based Parsing
date: August 1, 2017
slug: catalan
---

Abstract: When iteratively sampling transitions in transition based sampling, using a uniform distribution will result in frequency counts over unique trees resembling a step function. Rather, sampling over a distribution tied to the remaining viable transition sequences given the sequence of already taken transitions will give a smooth, uniform-like set of frequency counts. Providing this distribution naively is exponential over the length of the sequence. Fortunately, there is a closed form solution for this distribution in the case of binary trees.

Shift-Reduce parsing is a useful way to _linearize_ binary trees. The word _linearize_ here means to represent a binary tree as a sequence of elements. In this case, each element is either a Shift or Reduce transition.

This is how Shift-Reduce parsing works. We take the leaves of our binary tree and put them on queue. We also initialize an empty stack. The transitions are defined as follows:

- Shift - Pop an element from the queue and push it on to the stack.
- Reduce - Pop two elements from the stack. Create a parent node (the two elements are its children). Push the parent on to the stack.

Simple enough! This is a convenient representation for binary trees for multiple reasons. For one, imagine you were tasked with predicting the most likely binary tree structure given only the values of the leaf elements. We can reduce this problem to predicting the next transition given all the previous ones.

Here is another task: randomly sample a binary tree with $N$ leaves. One way to do this would be to list all possible binary trees of $N$ leaves, and randomly choose one. The [Catalan Numbers](https://en.wikipedia.org/wiki/Catalan_number) are a sequence of integers, which among other things, represent how many binary trees can be made with N leaves. Here are the first 15:

$$1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012, 742900, 2674440$$

As is obvious, for any large number $N$, it's not feasible to iterate all possible binary trees and choose one. By 15 leaves we are choosing among more than 2 million options. The Catalan numbers continue to grow exponentially and by 25 leaves, there are more than 1 trillion options. There must be a better way.

There are probably many alternatives, but perhaps we can make use of the Shift-Reduce transitions that we have discussed a moment ago.

<section id="uniform-transitions">Uniformly Sampling Transitions</section>

We can try randomly choosing a Shift or Reduce $2N-1$ times, but will find this doesn't quite give the desired outcome. For this to work at all, it's necessary to only choose a Shift or Reduce if they are _valid_. The word _valid_ here means that using the transition would retain a tree that has $N$ leaves. Some transitions are obviously invalid (like Reducing in one of the first two steps, or Shifting on the final step). Otherwise, we perform the following checks:

- Is the stack empty or only has size 1? Then we must Shift.
- Is the queue empty? Then we must Reduce.

Since we not all transitions are not always valid at each time step (depending on the transitions we've chosen so far), there is _bias_ in the types of trees that are created this way. Specifically, certain trees will be more likely than others. In effect, uniformly sampling Shift-Reduce transitions does not uniformly sample binary trees.

<section id="uniform-trees">Uniformly Sampling Binary Trees</section>

We can still sample binary trees using Shift-Reduce transitions, we only need to be careful about which distribution to use when sampling the Shift-Reduce transitions at each step.

...to be continued...