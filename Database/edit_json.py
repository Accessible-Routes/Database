import json

def read_json(JSON_File):
    count = 0
    for i in JSON_File['elements']:
        # try:
            # print("ID: ", i["id"], "\t|\t", "Tags: ", i["tags"])
        # except KeyError:
            # print("ID: ", i["id"], "\t|\t", "Tags: None")
        count += 1
    f.close()
    return count


def remove_steps(JSON_file):
    f = open("new_file.json", "w")
    f.write("{\"elements\": [")
    count = 0
    outer_current = ""
    for a in JSON_file['elements']:
        # print(a)
        try:
            if (a["tags"]["highway"] == "steps"):
                continue
        except KeyError:
            pass
        else:
            count += 1
            current = str(a)
            for elem in current:
                if (elem == "\'"):
                    outer_current += "\""
                else:
                    outer_current += elem
            outer_current += ", "
    outer_current = outer_current.rstrip(outer_current[-1])
    outer_current = outer_current.rstrip(outer_current[-1])

    outer_current += "]}"
    f.writelines(outer_current)
    f.close()
    return count;

# def remove_steps(JSON_file, new_filename):
#     g = open(new_filename, "w")
#     # f.write("{\"elements\": [")
#     count = 0
#     out_str = json.dumps(JSON_file)
#     g.write(out_str)
#     temp = json.loads(g)
#     for item in temp["elements"]:
#         if ("steps" in item["highway"]["tags"]):
#             print("working")
#
#
# #try copying json file, loading it as a json into the program, then just popping the array items from "elements" array
#     g.close()
#     return count;



filename = "4645508147a65be4e31c1cce9ade2840c6ac334f.json"
f = open(filename)
data = json.load(f)
orig_count = read_json(data)

out_file = "new_file.json"
new_count = remove_steps(data) #, out_file)

print("There are", orig_count, "elements in the original json.")
print("There are", new_count, "elements in the new json.")
# step_count = 0
#
# for i in data["elements"]:
#     try:
#         if (i["tags"]["highway"] == "steps"):
#             print("steps")
#             step_count += 1
#     except KeyError:
#         continue
#
# print(step_count)

# for i in data['elements']:
#     print(i)