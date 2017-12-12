# InstanceVectors

This is the repo accompanying the paper "Mr Darcy and Mr Toad, gentlemen: distributional names and their kinds" (Herbelot, 2015). If you use this code for a scientific publication, please cite:

Herbelot, A. 2015. Mr Darcy and Mr Toad, gentlemen: distributional names and their kinds. *International Conference on Computational Semantics (IWCS2015)*. London, UK.

**Abstract**

This paper investigates the representation of proper names in distributional semantics. We define
three properties we expect names to display: uniqueness (being a unique entity), instantiation (being
an instance of a relevant kind) and individuality (being separable from the subspace of concepts).
We show that taking a standard distribution as the representation of a name does not satisfy those
properties particularly well. We propose an alternative method to compute a name vector, which
relies on re-weighting the distribution of the appropriate named entity type – in effect, producing an
individual out of a kind. We illustrate the behaviour of such representations over some characters
from two English novels.

## Installation

Clone the repository and unpack the background space:

`bzip2 -d BNC.w10.4000c.5000r.ppmi.rownorm.dm.bz2`

## Usage

You can run the baseline on a particular book and character in the following way:

`python3 baseline.py Darcy_N data/pride/pride.dm data/pride/pride.cols`

You can perform the contextualisation of one of the character names in the data by running e.g.:

`python3 contextualise.py man_N data/pride/Darcy.chars 20 6`

The characteristic contexts for each character are in the data/ directory.
