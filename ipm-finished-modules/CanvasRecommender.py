import json
import sys
import pdb

def recommend(section_query):
    with open("canvasSections.json") as canvas_json:
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
            result = search_dict[section_query]
            for helper in result:
                print("Helper: " + helper[0] + " (" + helper[1] + ')')
        else:
            print("Did not find section")
    return

if __name__ == '__main__':
    # pdb.set_trace()
    query = ' '.join(sys.argv[1:])
    recommend(query)
