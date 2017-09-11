---
title: "Paper Summary: The wake-sleep algorithm for unsupervised neural networks"
date: September 2, 2017
slug: ws
---

[pdf](https://www.cs.toronto.edu/~fritz/absps/ws.pdf)

Consider a game where the goal is to minimize the number of required bits to send a message. The game is broken up into two stages: *training* and *inference*. During *training*, the two players (Sender and Receiver) may communicate with any size of message. During *inference*, the Sender must send a condensed message and the Receiver must predict what the original full-size message was. The players are scored on both the size of the condensed message and the accuracy of the Receiver's prediction. In this way, there is a penalty for simply sending the smallest size message without being able to recover the original message, and a similar penalty for sending a reasonably large message that the Receiver can trivially interpret. This paper presents an algorithm for training a neural network to participate in this game.

Research Ideas:

- Although Hemholtz Machines clearly improve the Receiver's score, the Sender's score is determined by selecting the size of the network. There's no straightforward way to distill the neural network following training. For a simple architecture (2 or 3 layers), performing something akin to grid search over layer sizes is not too difficult. For more complex architectures, there is an exponential large search space of potentially useful architectures of varying size. For this reason, Neural Architecture Search might be a useful technique for searching over the possible Hemholtz Machine configurations.