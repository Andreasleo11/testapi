from cgi import test
from flask import Flask
import recordlinkage as rl
import pandas as pd
import openpyxl 
import gunicorn

app = Flask(__name__)

@app.route("/")
def matching():
    df = pd.read_excel('UserAndreGorLokasSari.xlsx')
    df1 = pd.read_excel('UserDatabase.xlsx')
    indexer = rl.Index()
    indexer.full()
    pairs = indexer.index(df,df1)
    compare_cl = rl.Compare()
    compare_cl.exact("SportType","SportType", label="SportTypePoint")
    compare_cl.numeric("Age","Age",scale=3,label="AgePoint")
    compare_cl.geo("X","Y","X","Y", method='exp', label="DistancePoint")
    features = compare_cl.compute(pairs, df, df1)
    clusterone = features[features.AgePoint > 0.4]
    clustertwo = clusterone[clusterone.SportTypePoint > 0]
    clusterfinal = clustertwo[clustertwo.DistancePoint > 0.09]
    ecm = rl.ECMClassifier(binarize=0)
    match = ecm.fit_predict(clusterfinal)
    # result = match.to_series().apply(lambda x: '{0}-{1}'.format(*x))
    result = match.index.values
    return result

if __name__ == "__main__":
    app.run()