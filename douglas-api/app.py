import json
import re
import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://delta:delta@ds011419.mlab.com:11419/pair-research'
app.config['MONGO_DBNAME'] = 'pair-research'
app.debug = True
mongo = PyMongo(app)

client = MongoClient('mongodb://delta:delta@ds011419.mlab.com:11419/pair-research')
mngo = client['pair-research']


@app.route("/")
def hello():
  return "Hello World!"

@app.route("/group")
def get_user_group():
  group =  mongo.db.groups.find_one({ '_id': 'sM3z5FkZfsABqcj3g'})
  return jsonify({'result' : group})

@app.route("/affinities_history")
def get_affinities_history():
  history = mongo.db.affinities_history.find({ 'groupId': 'sM3z5FkZfsABqcj3g' })
  ret_list = []
  for a in history:
    ret_list.append(a)
  return jsonify({'result' : ret_list})

@app.route("/tasks_history")
def get_tasks_history():
  history = mongo.db.tasks_history.find({ 'groupId': 'sM3z5FkZfsABqcj3g' })
  ret_list = []
  for a in history:
    ret_list.append(a)
  return jsonify({'result' : ret_list})

@app.route("/pairs_history")
def get_pairs_history():
  history = mongo.db.pairs_history.find({ 'groupId': 'sM3z5FkZfsABqcj3g' })
  ret_list = []
  for a in history:
    ret_list.append(a)
  return jsonify({'result' : ret_list})

@app.route("/affinity_graph")
def get_affinity_graph():
  affinities = master_affinity_list[:]
  return jsonify({'result' : get_user_skill_graph(affinities)})

@app.route("/get_helpers", methods=['POST'])
def get_helpers_response():
  print "Request made to /get_helpers"
  request_query = request.form['task_query']
  print "Searching for helpers with: {}".format(request_query)
  affinities = master_affinity_list[:]
  user_sk_graph = get_user_skill_graph(affinities)
  helper_and_tasks = get_helpers(user_sk_graph, request_query)
  guru_result = get_guru_helpers(request_query)
  result = {
      'pair-result': helper_and_tasks,
      'guru-result': guru_result
      }
  print "Returning to user: {}".format(result)
  return jsonify({'result' : result})


def get_affinities():
  raw_affinities = mongo.db.affinities_history.find({ 'groupId': 'sM3z5FkZfsABqcj3g' })
  affinities = []
  for a in raw_affinities:
    affinities.append(a)

  raw_tasks = mongo.db.tasks_history.find({ 'groupId': 'sM3z5FkZfsABqcj3g' })
  tasks = []
  for t in raw_tasks:
    tasks.append(t)

  raw_pairs = mongo.db.pairs_history.find({ 'groupId': 'sM3z5FkZfsABqcj3g' })
  pairs = []
  for p in raw_pairs:
    pairs.append(p)

  pairingIds = list(set([pair["pairingId"] for pair in pairs]))
  pairingIdDict = {}

  for pairingId in pairingIds:
    timestamp = pairingIdDict.get(pairingId, None);
    if timestamp:
        continue
    pairings_timestamps = [str(pairing["timestamp"]) for pairing in pairs if pairing["pairingId"] == pairingId]
    pairingIdDict[pairingId] = pairings_timestamps[0]

  value_mappings = {
      "-1": 1,
      "0": 2,
      "0.33": 3,
      "0.66": 4,
      "1": 5
  }

  # Build the nodes
  nodes = []

  error_nodes = []
  for affinity in affinities:
    new_affinity = {}
    new_affinity["helperId"] = affinity["helperId"]
    new_affinity["helpeeId"] = affinity["helpeeId"]
    new_affinity["value"] = value_mappings[str(affinity["value"])]
    new_affinity["pairingId"] = affinity["pairingId"]
    new_affinity["groupId"] = affinity["groupId"]
    new_affinity["timestamp"] = pairingIdDict[affinity["pairingId"]];
    # Filter to the task field of the given affinity
    # The userId of a task item is equal to the helpeeId (the person asking for help) in a given affinity
    pairing_session_tasks = [task for task in tasks if task["pairingId"] == affinity["pairingId"]]
    new_affinity["task"] = [task["task"] for task in pairing_session_tasks if task["userId"] == affinity["helpeeId"]]

    # Current tasks don't have a field for "pairingId" set yet so we can't join them
    if new_affinity["task"]:
      nodes.append(new_affinity)
    else:
      # print new_affinity # Commented out for performance
      # print "Node doesn't have matching task field:"
      error_nodes.append(new_affinity)

  print "Finished with {} error(s)".format(len(error_nodes))
  return nodes


def get_guru_helpers(input_phrase):
  guru_list = 'guru-words.json'
  with open(guru_list) as input_file:
    guru_list = json.load(input_file)

  guru_list = guru_list['categories']
  help_list = {}
  for category_key in guru_list:
    helpers = []
    for keyword in guru_list[category_key]['words']:
      matching_string = input_phrase.lower()
      keyword = keyword.lower()
      if re.search(r'' + keyword, matching_string):
        helpers.extend(guru_list[category_key]['people'])
    if helpers:
      helpers = list(set(helpers))
      help_list[category_key] = helpers

  return help_list


def get_user_skill_graph(matching_nodes):
  dtr_words = 'skill-words.json'  # Skill category words
  with open(dtr_words) as input_file:
    corpus = json.load(input_file)

  corpus = corpus["categories"]
  for category_key in corpus:  # category_key = "ui/ux design"
    for keyword in corpus[category_key]:  # keyword = "ui", "ux", ...
      for node in matching_nodes:
        # Perform text search here
        # Make more efficient by using DP instead of calculating each time
        matching_string = node["task"][0].lower()
        keyword = keyword.lower()

        # The list of categories associated with a given help request
        category_list = node.get("categories", [])

        if re.search(r'' + keyword, matching_string):
          category_list.append(category_key)

        node["categories"] = list(set(category_list))  # Remove duplicates

  return matching_nodes

def parse_phrase_for_categories(input_phrase, category_list):
    matching_categories = []
    input_phrase = input_phrase.lower()

    for category_key, keyword_list in category_list.items():
        for keyword in keyword_list:
            keyword = keyword.lower()

            if re.search(r'' + keyword, input_phrase):
                matching_categories.append(category_key)

    return list(set(matching_categories))


def get_top_in_category(category, n, skill_dataframe):

    # In adding the tasks users are good at, we have to modify the original datastructure that's returned
    # by "get_top_in_category", therefore, we keep the "top_five" data structure in the object returned by
    # this function
    top_five = {}

    current_df = skill_dataframe.loc[skill_dataframe['category'] == category].drop_duplicates(subset=['helperId', 'task', 'category', 'value'])
    people = mongo.db.groups.find_one({ '_id': 'sM3z5FkZfsABqcj3g'})
    top_users_df = current_df.groupby('helperId').mean().sort_values(by='value', ascending=False)
    top_five = top_users_df.iloc[:min(n, top_users_df.shape[0])].to_dict()

    for userId, avg_score in top_five['value'].items():
      print "User {}'s ({}) top tasks:".format(look_up_person(userId, people), userId)
      print current_df[current_df.helperId == userId][current_df.value >= 4].groupby('helperId').head().to_dict('records')
      top_five['value'][userId] = current_df[current_df.helperId == userId][current_df.value >= 4].groupby('helperId').head().to_dict('records')

    return top_five

def parse_phrase_for_people(phrase, n, category_list, skill_dataframe):
    people_category_dictionary = {}
    matching_categories = parse_phrase_for_categories(phrase, category_list)
    for category in matching_categories:
        top_people = get_top_in_category(category, n, skill_dataframe)
        people_category_dictionary[category] = top_people

    return people_category_dictionary

def look_up_person(userId, group):
    person_name = ""
    for person in group["members"]:
        if person["userId"] == userId:
            person_name = person["fullName"]

    return person_name

# In[3]:

def get_helpers(affinity_graph, input_phrase):
  import pdb;pdb.set_trace()
  df = pd.DataFrame(affinity_graph)
  # df = pd.DataFrame(data=affinity_graph, orient="records")
  with open("skill-words.json") as input_file:
      words = json.load(input_file)

  # with open("groups.json") as input_file:
  #     people = json.load(input_file)
  people = mongo.db.groups.find_one({ '_id': 'sM3z5FkZfsABqcj3g'})

  df['categories'] = df['categories'].apply(tuple)
  new_rows = []
  for index, row in df.iterrows():
      new_rows.extend([[row['helperId'], row['timestamp'], row['task'][0], nn, row['value']] for nn in row.categories])

  expanded_df = pd.DataFrame(new_rows,columns=['helperId', 'timestamp', 'task', 'category', 'value'])
  words = words['categories']

  people_and_categories = parse_phrase_for_people(input_phrase, 5, words, expanded_df)
  category_dict = {}

  for category, user_dict in people_and_categories.iteritems():
      people_list = []
      for userId, tasks in user_dict["value"].iteritems():
          person_name = look_up_person(userId, people)
          person = {}
          person["name"] = person_name
          person["userId"] = userId
          person["tasks"] = tasks
          people_list.append(person)
      category_dict[category] = people_list

  return category_dict

with app.app_context():
  pipeline_3 = [{
		'$match': {
		  'groupId': 'sM3z5FkZfsABqcj3g'
		}},
		{'$lookup':
		  {'from': 'tasks_history',
		   'localField': 'helperId',
		   'foreignField': 'userId',
		   'as': 'ratings'}}]
  pipeline_4 = [{
		'$match': {
		  'groupId': 'sM3z5FkZfsABqcj3g'
		}},
		{'$lookup':
		  {'from': 'tasks_history',
		   'localField': 'helperId',
		   'foreignField': 'userId',
		   'as': 'ratings'}}]
  pipeline_2 = [
		{'$lookup':
		  {'from': 'tasks_history',
		   'localField': 'pairingId',
		   'foreignField': 'pairingId',
		   'as': 'aff_tasks'}}]
  pipeline = [
      {"$match":{"groupId": "sM3z5FkZfsABqcj3g"}}
      ]
  # cursor = mongo.db.affinities_history.aggregate(pipeline_3)
  cursor = mongo.db.tasks_history.aggregate(pipeline_4)
  c_list = [c for c in cursor]
  import pdb;pdb.set_trace()
  print "test"
  master_affinity_list = get_affinities()

  # mongo.db.affinities_history.aggregate([])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
