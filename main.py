from traffic_analyser import TrafficAnalyser
import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)

file_name = './network_traffic_trace_csv.csv'
df = pd.read_csv(file_name)

columnNames = ['Source', 'Destination', 'Source port', 'Destination port', 'Protocol']
trafficAnalyser = TrafficAnalyser(df, columnNames)

networkStats = trafficAnalyser.getGeneralStats()
for stat in networkStats:
    print("\n{0}".format(stat.head()))

trafficAnalyser.buildTrafficAnalysisGraphs()
