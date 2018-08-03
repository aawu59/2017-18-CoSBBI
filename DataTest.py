import DataAnalysis

DataAnalysis.point_cutoffs()
DataAnalysis.data_processing()

try:
    DataAnalysis.firstplot()
    # Displays plot in Matplotlib and saves png file to temp.png
except:
    pass

try:
    DataAnalysis.extrapoints()
except:
    pass
