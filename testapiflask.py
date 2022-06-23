from cgi import test
from crypt import methods
from urllib import request
from flask import Flask , request
from flask import jsonify
import recordlinkage as rl
import pandas as pd
import json
import openpyxl 
import gunicorn

app = Flask(__name__)

@app.route("/")
def hello_world():
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
    clusterfinal = clustertwo[clustertwo.DistancePoint > 0.2]
    ecm = rl.ECMClassifier(binarize=0)
    match = ecm.fit_predict(clusterfinal)
    # result = match.to_series().apply(lambda x: '{0}-{1}'.format(*x))
    rematch = match.get_level_values(1)
    rematch = list(rematch)
    resulttup = tuple(rematch)
    # pl = ','.join(''.join(x) for x in resulttup)
    pl = ','.join(map(str, resulttup))
    return jsonify(pl)

@app.route("/posts", methods=['POST'])
def matching():
    # print(request.get_json())
    data = request.get_json()
    df = pd.DataFrame(eval(data))
    df1 = df.head(1)
    df2 = df.iloc[1:]
    indexer = rl.Index()
    indexer.full()
    pairs = indexer.index(df1,df2)
    compare_cl = rl.Compare()
    compare_cl.exact("SportType","SportType", label="SportTypePoint")
    compare_cl.numeric("Age","Age",scale=3,label="AgePoint")
    compare_cl.geo("X","Y","X","Y", method='exp', label="DistancePoint")
    features = compare_cl.compute(pairs, df1, df2)
    clusterone = features[features.AgePoint > 0.4]
    clustertwo = clusterone[clusterone.SportTypePoint > 0]
    clusterfinal = clustertwo[clustertwo.DistancePoint > 0.2]
    ecm = rl.ECMClassifier(binarize=0)
    match = ecm.fit_predict(clusterfinal)
    # result = match.to_series().apply(lambda x: '{0}-{1}'.format(*x))
    rematch = match.get_level_values(1)
    rematch = list(rematch)
    resulttup = tuple(rematch)
    # pl = ','.join(''.join(x) for x in resulttup)
    pl = ','.join(map(str, resulttup))
    return jsonify(pl)





if __name__ == "__main__":
    app.run()