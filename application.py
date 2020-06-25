from flask import Flask
from Helper import Helper
from flask import request
from flask import json

app = Flask(__name__)
@app.route("/", methods=["GET"])

def candidate_recommender():
    exp = request.args.get('e')
    farea = request.args.get('f')
    jd = request.args.get('jd')
    if exp and farea and jd:
        helper = Helper()
        '''with open (jd, 'r') as f:
            jobd = f.read()
        #for local storage path
     
        jobd = helper.extract_text_from_url(jd) 
        #for extracting text from pdf url -> from blob storage
        '''
        jobd = str(jd)
        preprocessed = helper.cleanTextAndTokenize(jobd) #tokenizing text
        sim_scores = helper.recommend(exp, farea, preprocessed) #returns [(score, candidate ID), (),....] 
        if len(sim_scores)==0:
            return ("Sorry! No matching candidates!")
        response = app.response_class(
        response=json.dumps(str(dict(sim_scores))),
        status=200,
        mimetype='application/json')
        return response
        
    else:
        return "Hello. Please enter the f area, exp and jd path"
if __name__ == "__main__":
    app.run(debug=True)

