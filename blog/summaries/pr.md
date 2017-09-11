---
title: "Paper Summary: Posterior Regularization for Structured Latent Variable Models"
date: September 10, 2017
slug: pr
---

[pdf](http://www.jmlr.org/papers/volume11/ganchev10a/ganchev10a.pdf)

> In many cases, prior knowledge is easy to specify in terms of posteriors, and much more difficult to specify as priors on model parameters or by explicitly adding constraints to the model.

Use the $KL(Q || P)$ to regularize. Let me explain. $P$ is the probability from your model and the data, and $Q$ is the probability that you desire. With this magic setup, $Q$ can be virtually any probability.
