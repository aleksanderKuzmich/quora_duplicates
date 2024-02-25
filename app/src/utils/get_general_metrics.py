from sklearn.metrics import confusion_matrix


def get_general_metrics(y_true: list, y_pred: list):
    """
    confusion matrix whose i-th row and j-th column entry indicates the number
    of samples with true label being i-th class and predicted label being j-th class.
    'tn': true negatives
    'fp': false positives
    'fn': false negatives
    'tp': true positives
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[False,True]).ravel()
    return tn, fp, fn, tp
