from flask import Flask
from pymongo import MongoClient
from Helper import Helper
from flask import request
from flask import json
import pymongo
import os
import pickle

app = Flask(__name__)
@app.route("/")

def build_model():
    method = request.args.get('method')
    if method == 'build':
        helper = Helper()
        if not os.path.exists('active'):
            os.makedirs('active')
        else:
            helper.create_backup()
        
        connection = MongoClient('mongodb+srv://hrlanes-mongodb-reader:hrlanes%401234@hrlanes-production-i5mve.mongodb.net', 27017)
        db = connection['hrlanes-web-db']
        data = db['users']
        ex = data.find({"$and": [{'ProfileSummaryInfo': {"$exists": True}}, {'recommenderProcessed': {"$exists": True}}, {'recommenderProcessed': True }]})
        
        d = helper.createDictionary(ex)
        path = os.getcwd()+"\\active\\"
        with open(path+"dictionary.pkl", "wb") as output:
            pickle.dump(d, output)
        resumeList = []
        for key in d:
            if len(d[key])>0:  # check if resumes/details exist 
                doc_included = []
                for x in d[key]:
                    resumeList.append(x[1])
                    doc_included.append(x[0])
                documents = []
                for f in resumeList:
                    documents.append(f)
                    helper.create_tfidf(str(key), documents, doc_included)
        #reset recommenderProcessed to false
        '''filter  = {"$and": [{'ProfileSummaryInfo': {"$exists": True}}, {'recommenderProcessed': {"$exists": True}}, {'recommenderProcessed': True }]}
        data.update_many(filter, {"$set": { "recommenderProcessed": False }})
        '''
        return 'okay'
    elif method == 'recommend':
        exp = request.args.get('e')
        farea = request.args.get('f')
        jd = request.args.get('jd')
        if exp and farea and jd:
            helper = Helper()
            jobd = helper.extract_text_from_url(jd)  #for extracting text from pdf url -> from blob storage
            jobd = str(jd)
            preprocessed = helper.cleanTextAndTokenize(jobd) #tokenizing text
            sim_scores = helper.recommend(exp, farea, preprocessed) #returning candidate IDs
            if len(sim_scores)==0:
                return ("Sorry! No matching candidates!")
            response = app.response_class(
            response=json.dumps(str(dict(sim_scores))),
            status=200,
            mimetype='application/json')
            return response
        else:
            return "Please enter exp, f area and jd in the request body!"
            
    else:
        return "Please enter the method in request body: build or recommend!"
if __name__ == "__main__":
    app.run(debug=True)
