import matplotlib.pyplot as plt

from typing import List


class Axis:
    Label: str
    Values: List[float]

    def __init__(self, label, values) -> None:
        self.Label = label
        self.Values = values


class Options(object):
    Title: str
    XAxis: Axis
    YAxis: Axis
    Location: str
    SaveFile: bool
    FileName: str


class Graph:
    Options: Options

    @staticmethod
    def renderGraph(options):
        xValues = options.XAxis.Values
        xLabel = options.XAxis.Label

        yValues = options.YAxis.Values
        yLabel = options.YAxis.Label

        plt.plot(yValues, xValues)
        plt.title(options.Title)
        plt.ylabel(yLabel)
        plt.xlabel(xLabel)

        plt.grid(True)

        # Save figure before render
        if (options.SaveFile and options.Location):
            plt.savefig("{0}/{1}".format(options.Location, options.FileName))
            print("Graph saved: {0}".format(options.Title))
        plt.show()
