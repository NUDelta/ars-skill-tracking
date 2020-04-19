import json
import sys


def recommend(query):
    with open("canvasSections.json") as canvas_json:
        canvas_map = json.load(canvas_json)
        search_dict = {}
        for user in canvas_map:
            name = user["name"]
            sections = user["sections"][0]
            for section in sections:
                for prompt_list in sections[section]:
                    cur_key = section + " --> " + prompt_list["prompt"]
                    if cur_key in search_dict:
                        search_dict[cur_key].append((name, prompt_list["status"]))
                    else:
                        search_dict[cur_key] = [(name, prompt_list["status"])]
        match = dict(filter(lambda item: query in item[0], search_dict.items()))
        if match:
            for section in match:
                for helper in match[section]:
                    if helper[1] != "Unfilled":
                        print("Helper: " + helper[0] + " (" + helper[1] + ')')
        else:
            print("Did not find section")
    return


if __name__ == '__main__':
    query = ' '.join(sys.argv[1:])
    recommend(query)
