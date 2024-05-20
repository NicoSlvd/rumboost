import numpy as np

def accuracy(preds, labels):
    """
    Compute accuracy of the model.

    Parameters
    ----------
    preds : numpy array
        Predictions for all data points and each classes from a softmax function. preds[i, j] correspond
        to the prediction of data point i to belong to class j.
    labels : numpy array
        The labels of the original dataset, as int.

    Returns
    -------
    Accuracy: float
        The computed accuracy, as a float.
    """
    return np.mean(np.argmax(preds, axis=1) == labels)


def cross_entropy(preds, labels):
    """
    Compute negative cross entropy for given predictions and data.

    Parameters
    ----------
    preds: numpy array
        Predictions for all data points and each classes from a softmax function. preds[i, j] correspond
        to the prediction of data point i to belong to class j.
    labels: numpy array
        The labels of the original dataset, as int.

    Returns
    -------
    Cross entropy : float
        The negative cross-entropy, as float.
    """
    num_data = len(labels)
    data_idx = np.arange(num_data)
    return -np.mean(np.log(preds[data_idx, labels]))