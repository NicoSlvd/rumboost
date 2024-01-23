<img src="logo/rumboost_logo.png" width="950">

---------------------------------

[![Documentation Status](https://readthedocs.org/projects/rumboost/badge/?version=latest)](https://rumboost.readthedocs.io/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.org/NicoSlvd/rumboost/LICENSE.md) [![Python Versions](https://img.shields.io/pypi/pyversions/rumboost.svg?logo=python&logoColor=white)](https://pypi.org/project/rumboost) [![PyPI Version](https://img.shields.io/pypi/v/rumboost.svg?logo=pypi&logoColor=white)](https://pypi.org/project/rumboost) [![arXiv](https://img.shields.io/badge/arXiv-2401.11954-b31b1b.svg)](https://arxiv.org/abs/2401.11954)


## Description

RUMBoost is a python package to estimate Random Utility models with Gradient Boosted Decision Trees. More specifically, each parameter in the traditional utility function is replaced by an ensemble of regression trees with appropriate constraints to: i) ensure the guarantee of marginal utilities monotonicity; ii) incorporate alternative-specific attributes; and iii) provide an intrinsically interpretable non-linear form of the utility function, directly learnt from the data.

Currently RUMBoost can estimate the following RUMs:

- MNL
- Nested Logit
- Cross-Nested Logit
- An equivalent of the Mixed Effect model

For more details, you can refer to the [preprint](https://arxiv.org/abs/2401.11954) of our paper.

## Installation

RUMBoost is launched on [pypi](https://pypi.org/project/rumboost/). You can install it with the following command:

`pip install rumboost`

We recommend to install rumboost in a separate environment with its dependencies.

## Documentation and examples
The full documentation can be found [here](https://rumboost.readthedocs.io/en/latest/). In addition, you can find several examples on how to use RUMBoost under the [example](https://github.com/NicoSlvd/rumboost/tree/main/examples) folder. Currently, there are seven example notebooks. We recommend using them in this order:

1. [simple_rumboost](https://github.com/NicoSlvd/rumboost/blob/main/examples/1_simple_rumboost.ipynb): how to train and plot parameters of a simple RUMBoost model
2. [feature_interaction](https://github.com/NicoSlvd/rumboost/blob/main/examples/2_feature_interaction.ipynb): how to include feature interactions for training and plotting
3. [nested](https://github.com/NicoSlvd/rumboost/blob/main/examples/3_nested.ipynb): how to train a nested logit RUMBoost model
4. [functional_effect](https://github.com/NicoSlvd/rumboost/blob/main/examples/4_functional_effect.ipynb): how to train and plot a functional effect RUMBoost model
5. [cross-nested](https://github.com/NicoSlvd/rumboost/blob/main/examples/5_cross-nested.ipynb): how to train a cross-nested logit RUMBoost model
6. [bootstrap](https://github.com/NicoSlvd/rumboost/blob/main/examples/6_bootstrap.ipynb): how to test the model robustness
7. [smoothing_and_vot](https://github.com/NicoSlvd/blob/main/rumboost/examples/7_smoothing_and_vot.ipynb): how to smooth a RUMBoost output and plot the smoothed version, as well as computing and plotting VoT

## Bug reports and feature requests
If you encounter any issues or have ideas for new features, please open an [issue](https://github.com/NicoSlvd/rumboost/issues). You can also contact us at nicolas.salvade.22@ucl.ac.uk

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Reference paper (preprint)

Salvadé, N., & Hillel, T. (2024). Rumboost: Gradient Boosted Random Utility Models. *arXiv preprint [arXiv:2401.11954](https://arxiv.org/abs/2401.11954)*
