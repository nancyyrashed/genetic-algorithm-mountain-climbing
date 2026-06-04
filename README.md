# Genetic Algorithm Mountain Climbing

## Overview

This project explores the use of Genetic Algorithms (GA) to evolve virtual creatures capable of climbing a mountain environment.

The objective was to modify an existing evolutionary simulation framework and design a fitness function that encourages creatures to develop effective climbing behaviours through natural selection and mutation.

The project investigates how population size, mutation strategies, and encoding schemes influence the evolutionary process and the ability of creatures to reach higher altitudes.

---

## Objectives

* Design a fitness function for mountain-climbing behaviour.
* Reward creatures for moving towards the mountain peak.
* Encourage stable and efficient movement patterns.
* Investigate the effects of mutation strategies on evolution.
* Compare evolutionary performance across different population sizes.
* Analyze how encoding schemes influence creature development.

---

## Fitness Function Design

The original fitness function was extended with several custom evaluation metrics:

### Altitude Reward

Rewards creatures for reaching higher elevations during the simulation.

### Proximity Reward

Rewards movement toward the mountain center and penalizes movement away from the target.

### Movement Reward

Encourages exploration and locomotion by considering total distance travelled.

### Stability (Consistency) Reward

Measures movement consistency and reduces rewards for unstable behaviour.

These metrics were combined into a unified fitness score used to guide evolution.

---

## Experiments

### Population Size Analysis

Population sizes tested:

* 10
* 20
* 30

The experiments evaluated how population diversity affects fitness growth and creature complexity.

### Point Mutation Analysis

Mutation rates tested:

* 0.05
* 0.1
* 0.2

The results showed that a mutation rate of 0.1 produced the most stable and effective evolutionary progress.

### Shrink Mutation Analysis

Shrink mutation rates tested:

* 0.1
* 0.2
* 0.3

The experiments explored the trade-off between stability and evolutionary speed.

### Grow Mutation Analysis

Grow mutation rates tested:

* 0.05
* 0.1
* 0.2

Results demonstrated how mutation intensity influences structural complexity and climbing performance.

### Encoding Scheme Experiments

Additional experiments were conducted by modifying:

* Link Length Scaling
* Joint Origin XYZ Parameters
* Link Recurrence
* Control Amplitude

These changes were evaluated to determine their impact on fitness and creature evolution.

---

## Technologies Used

* Python
* NumPy
* Genetic Algorithms
* Evolutionary Computation
* Data Visualization
* Jupyter Notebook
* Matplotlib

---

## Key Findings

* Larger populations generally produced more stable and effective climbing behaviour.
* Point Mutation 0.1 achieved the most balanced evolutionary performance.
* Moderate mutation rates produced more stable fitness improvements.
* Control Amplitude modifications generated the most consistent evolutionary results among the tested encoding schemes.
* Proper fitness design significantly improved mountain-climbing behaviour.

---

## Results

The repository includes:

* Genetic Algorithm implementation
* Modified fitness functions
* Experimental configurations
* Performance graphs
* Comparative analysis
* Final project report
