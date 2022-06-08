from flask import Flask
import recordlinkage as rl
import pandas as pd
import gunicorn

app = Flask(__name__)

@app.route("/")
def matching():
    df1 = pd.read_excel(r"E:\SKRIPSI\bananaapps\testapi\UserAndreGorLokasSari.xlsx")
    df2 = pd.read_excel(r"E:\SKRIPSI\bananaapps\testapi\UserDatabase")
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
    clusterfinal = clustertwo[clustertwo.DistancePoint > 0.09]
    ecm = rl.ECMClassifier(binarize=0)
    match = ecm.fit_predict(clusterfinal)

    return match

if __name__ == "__main__":
    app.run()