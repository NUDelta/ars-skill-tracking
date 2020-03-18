import json
import sys
from flask import Flask
from flask import request, redirect
from flask import render_template

def recommend(section_query):
    with open("app/canvasSections.json") as canvas_json:
        canvas_map = json.load(canvas_json)
        search_dict = {}
        for user in canvas_map:
            name = unicode(user["name"])
            sections = user["sections"][0]
            for section in sections:
                for prompt_list in sections[section]:
                    # pdb.set_trace()
                    cur_key = unicode(section) + " --> " + unicode(prompt_list["prompt"])
                    if cur_key in search_dict:
                        search_dict[cur_key].append((name, unicode(prompt_list["status"])))
                    else:
                        search_dict[cur_key] = [(name, unicode(prompt_list["status"]))]
        if section_query in search_dict:
            # result = search_dict[section_query]
            # for helper in result:
            #     print("Helper: " + helper[0] + " (" + helper[1] + ')')
            return search_dict[section_query]
        else:
            return [section_query + " not found in the canvas"]
    return

app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def index():
    with open("app/canvasKeys.json") as f:
        canvasKeys = json.load(f)
    canvasKeys = sorted(canvasKeys.keys())
    helpers = []
    not_found = False
    sectionCell = ""
    if request.form:
        sectionCell = request.form["section"] + " -- " + request.form["cell"]
        query = request.form["section"] + " --> " + request.form["cell"]
        helpers = recommend(query)
        if len(helpers) == 1:
            not_found = True
    return render_template('index.html', canvasKeys=canvasKeys, helpers=helpers, not_found=not_found, sectionCell=sectionCell)

if __name__ == '__main__':
    # pdb.set_trace()
    app.run(debug=True, host='0.0.0.0')
