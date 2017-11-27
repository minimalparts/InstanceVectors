# InstanceVectors

This is the repo accompanying the paper "Mr Darcy and Mr Toad, gentlemen: distributional names and their kinds" (Herbelot, 2015). If you use this code for a scientific publication, please cite:

Herbelot, A. 2015. Mr Darcy and Mr Toad, gentlemen: distributional names and their kinds. *International Conference on Computational Semantics (IWCS2015)*. London, UK.

Note that the background semantic space provided here was reconstructed and varies slightly from the one originally used in the paper. Some slight differences in results may arise as a consequence.


## Installation

Clone the repository and unpack the background space:

`bzip2 -d BNC.w5.4000c.5000r.ppmi.rownorm.dm.bz2`

You can perform the contextualisation of one of the character names in the data by running e.g.:

`python3 contextualise.py man_N bnc.dm bnc.cols ../data/pride/Darcy.chars 20 6`

The characteristic contexts for each character are in the data/ directory.
