Computational Design and Dynamics of Soft Systems
&middot;
[![license](https://img.shields.io/badge/license-MIT-green)](https://mit-license.org/)
=====

This is a repository that contains the source code for generating the lecture
notes, handouts, exercises for the computational lab-sessions of the course
offered at UIUC.

## Description
> This course provides a hands-on introduction to modern modeling and
simulations techniques for heterogeneous structures made of assemblies of soft,
elastic slender elements. Such systems are ubiquitous in nature, from animal
musculoskeletal architectures to ‘birds-nest’ composite materials. They are also
becoming increasingly relevant in robotics. Students will implement in python
their own Cosserat rods-based solver. The developed solver will be then coupled
with evolutionary optimization techniques for design, and reinforcement learning
for control.

## Prerequisities
None.

## Content
-	Introduction to modeling and simulation for inverse design
-	Basics of evolutionary strategies
-	Covariance Matrix Adaptation – Evolution Strategy (CMA-ES)
-	Basic concepts of Reinforcement Learning
-	Soft robotic modeling with Cosserat rods
-	Space and time discretization
-	Application to snake slithering
-	Complex creatures modeling
-	Examples of potential experimental applications

## Organization
The course is organized in three modules listed below.
- Python for engineers
  - [Crash course in Python for engineers](lectures/01_intro)
	- [Scientific computing via Python](lectures/02_scicomp)
- Non-linear stochastic optimization
  - [Implementing CMA-es for nonlinear stochastic optimization](lectures/03_cma)
	- [Adopting CMA-es to tackle real-life inverse-design
    problems](lectures/03_cma)
- Modeling of soft systems
  - [Rotational dynamics of slender rods and its numerical resolution](lectures/04_elastica)
  - [Temporal dynamics of soft systems and its numerical resolution](lectures/05_timeintegration)
  - [Spatial dynamics of soft systems and its numerical resolution](lectures/06_spaceintegration)
	- [Putting the components together](lectures/07_timespace)
- [Visualizing soft-system dynamics](lectures/08_povray)

## Setup
To get started with the course, please consult [this folder](handouts/00_linux).
