import sys
import numpy.matlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


def main():
    file_name = sys.argv[1]
    
    barcodes, y = np.genfromtxt(file_name, delimiter='\t', unpack=True)

    # pull out the list from pandas frame
    df = pd.read_csv(file_name, sep='\t')
    values=list(df[df.columns[1]])


    nPoints = len(values)
    allCoord = np.vstack((range(nPoints), values)).T

    firstPoint = allCoord[0]
    lineVec = allCoord[-1] - allCoord[0]
    lineVecNorm = lineVec / np.sqrt(np.sum(lineVec**2))

    vecFromFirst = allCoord - firstPoint

    scalarProduct = np.sum(vecFromFirst * np.matlib.repmat(lineVecNorm, nPoints, 1), axis=1)
    vecFromFirstParallel = np.outer(scalarProduct, lineVecNorm)
    vecToLine = vecFromFirst - vecFromFirstParallel

    # distance to line is the norm of vecToLine
    distToLine = np.sqrt(np.sum(vecToLine ** 2, axis=1))

    # knee/elbow is the point with max distance value
    idxOfBestPoint = np.argmax(distToLine)

    print("Knee of the curve is at index =",idxOfBestPoint)
    print("Knee value =", values[idxOfBestPoint])

    print("percentile = ", stats.percentileofscore(values, values[idxOfBestPoint]))

    x = np.arange(0, len(y),1)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    markers_on = [idxOfBestPoint]

    plt.xticks(x, barcodes)
    plt.plot(x,y,'-gD', markevery=markers_on, label='Inline label')

    A = {idxOfBestPoint}
    B = {values[idxOfBestPoint]}

    for xy in zip(A, B):
       ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
   
    # Plot graph
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Frequency Distribution\nBarcode')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
