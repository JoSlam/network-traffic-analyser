from graph.graph import Axis, Graph, Options
from typing import List

from pandas.core.frame import DataFrame
from graph.models.outcome import Outcome

from graph.models.point import Point
from graph.entropyCalculator import calculateEntropy


class TrafficAnalyser:
    Data: DataFrame
    Columns: List[str]
    BucketIncrement: float = 0.5

    def __init__(self, dataFrame: DataFrame, columnNames: List[str]) -> None:
        self.Columns = columnNames
        self.Data = dataFrame

    def getGeneralStats(self):
        mostFrequent = []

        for colName in self.Columns:
            if colName in self.Data.columns:
                count = self.Data.groupby(colName).Source.count().sort_values(
                    ascending=False)
                mostFrequent.append(count)
        return mostFrequent

    def getItemStats(self, groupColumns: List, restrict: bool):
        groupedDataSet = self.Data.groupby(
            groupColumns).Source.count().sort_values(ascending=False)
        return groupedDataSet if not restrict else groupedDataSet.head()

    def getMaxBucket(self) -> float:
        return float(self.Data.tail(1).Time)

    def getBucketRows(self, bucket: float):
        return self.Data[self.Data.Time <= bucket]

    def getOutcomes(self, frame: DataFrame) -> List[Outcome]:
        outcomes = []
        for i in frame.keys():
            outcomes.append(Outcome(i, frame.get(i)))
        return outcomes

    def getGraphData(self, colName: str) -> List[Point]:
        maxBucketSize = self.getMaxBucket()
        graphPoints: List[Point] = []

        currBucket = 0.0
        while (currBucket <= maxBucketSize):
            # Get list of outcomes at time y
            # Get total outcomes at time y
            bucketFrame = self.getBucketRows(currBucket)

            aggregateSet = bucketFrame.groupby(colName)
            countData = aggregateSet.Source.count()

            outcomes = self.getOutcomes(countData)
            totalOutcomes = countData.sum()

            entropy = calculateEntropy(outcomes, totalOutcomes)
            graphPoints.append(Point(entropy, currBucket))

            currBucket += self.BucketIncrement

        return graphPoints

    def getGraphOptions(self, graphData: List[Point], columnName: str):
        xValues = list(map(lambda point: point.X, graphData))
        xAxis = Axis("Time buckets (seconds)", xValues)

        yValues = list(map(lambda point: point.Y, graphData))
        yAxis = Axis("{0} Entropy".format(columnName), yValues)

        options = Options()
        options.FileName = "{0}.png".format(columnName)
        options.Location = "./figures"
        options.SaveFile = True
        options.Title = "{0} Entropy vs. Time".format(columnName)
        options.XAxis = xAxis
        options.YAxis = yAxis

        return options

    def buildTrafficAnalysisGraphs(self):
        for col in self.Columns:
            graphData = self.getGraphData(col)
            graphOptions = self.getGraphOptions(graphData, col)

            Graph.renderGraph(graphOptions)