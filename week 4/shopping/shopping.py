import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # Create the list and 
    # the months and bool list to transform them into integers
    evidence = []
    labels = []
    month = ['Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sep','Oct','Nov','Dec']
    bool_list = ['FALSE','TRUE']

    # Open the CSV, transform the data into integers 
    # and load each row into the corresponfing list (evidence and labels) 
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            
            row_evidence = []

            # If the row is the headers (first row) then skip it
            if count == 0:
                count +=1
                continue

            data = list(row)
            for column in range(len(row)):
                # Get evidence columns
                if column < 17:
                    # If column is month the look for the corresponding 
                    # int in the month list
                    if column == 10:
                        month_int = month.index(data[column])
                        row_evidence.append(month_int)
                    # If booleand the get the boolean integer 
                    # 1 if True, 0 if False / Weekend Column
                    elif column == 16 :
                        bool_int = bool_list.index(data[column])
                        row_evidence.append(bool_int)
                    # If Returning_Visitor the 1, 
                    # else 0
                    elif column == 15:
                        if data[column] == 'Returning_Visitor':
                            row_evidence.append(1)
                        else:
                            row_evidence.append(0)
                    else:
                        # If Administrative, 
                        # Informational, ProductRelated, Month, 
                        # OperatingSystems, Browser, Region, 
                        # TrafficType or VisitorTypecolumn the cast to integer
                        if column in (0,2,4,11,12,13,14) :
                            row_evidence.append(int(data[column]))
                        # If Administrative_Duration, Informational_Duration,
                        # ProductRelated_Duration, BounceRates, ExitRates,
                        # PageValues or SpecialDay column the cast to float
                        else:
                            row_evidence.append(float(data[column]))
                # Get Label column
                else:
                    bool_int = bool_list.index(data[column])
                    labels.append(bool_int)
            # Append row evidence into evidence list 
            # to get list of evidences list
            evidence.append(row_evidence)
    
    return evidence, labels

    # raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    # Get KNeighborsClassifier model from sklearn.neighbors 
    # and then fit it with the evidence and the labels
    # then return that model
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(evidence, labels)

    return neigh
    # raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # Dict for positive and negative values 
    # in labels and predictions
    counter_labels = {'positive':0,'negative':0}
    counter_predicts = {'positive':0,'negative':0}

    # Count positive and negative values in labels
    for label in labels:
        if label == 1:
            counter_labels['positive'] += 1
        elif label == 0:
            counter_labels['negative'] += 1

    # Count positive and negative values in predictions
    for x in range(len(predictions)):
        if predictions[x] == labels[x]:
            if predictions[x] == 1:
                counter_predicts['positive'] += 1
            elif predictions[x] == 0:
                counter_predicts['negative'] += 1

    # Calculate sensitivity and specificity and return them
    sensitivity = counter_predicts['positive'] / counter_labels['positive']
    specificity = counter_predicts['negative'] / counter_labels['negative']

    return sensitivity, specificity

    # raise NotImplementedError


if __name__ == "__main__":
    main()
