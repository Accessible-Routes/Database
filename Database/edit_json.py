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


# def remove_steps(JSON_file):
#     f = open("new_file.json", "w")
#     f.write("{\"elements\": [")
#     count = 0
#     outer_current = ""
#     for a in JSON_file['elements']:
#         count += 1
#         current = str(a)
#         for elem in current:
#             if (elem == "\'"):
#                 outer_current += "\""
#             else:
#                 outer_current += elem
#         outer_current += ", "
#     outer_current = outer_current.rstrip(outer_current[-1])
#     outer_current = outer_current.rstrip(outer_current[-1])
#
#     outer_current += "]}"
#
#     print(outer_current)
#
#     f.writelines(outer_current)
#     # for i in JSON_file['elements']:
#     #     try:
#     #         # print("ID: ", i["id"], "\t|\t", "Tags: ", i["tags"])
#     #         print(i)
#     #     except KeyError:
#     #         print("ID: ", i["id"], "\t|\t", "Tags: None")
#     # f.write("]")
#     # outer_current += "}"
#
#     f.close()
#     return count;

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

    # print(outer_current)

    f.writelines(outer_current)
    # for i in JSON_file['elements']:
    #     try:
    #         # print("ID: ", i["id"], "\t|\t", "Tags: ", i["tags"])
    #         print(i)
    #     except KeyError:
    #         print("ID: ", i["id"], "\t|\t", "Tags: None")
    # f.write("]")
    # outer_current += "}"

    f.close()
    return count;

# def remove_steps(JSON_file):
#     f = open("new_file.json", "w")
#     count = 0
#     # for a in JSON_file['elements']:
#     #     f.writelines(a)
#     #     count = 0
#     f.write("\"elements\": [")
#
#     # dict = [{1: "hello", 2:"greetings", 3:"howdy"}, {1: "bye", 2: "goodbye", 3:"adios"}]
#     # f.write(str(dict))
#     for i in JSON_file['elements']:
#         try:
#             if (i["tags"]["highway"] == "steps"):
#                 continue
#             # print("ID: ", i["id"], "\t|\t", "Tags: ", i["tags"])
#             # print(i)
#         except KeyError:
#             # temp_dict = i
#             # print(temp_dict)
#             # f.write(str(temp_dict))
#             # f.write("\n")         # f.writelines("{\"", i, "\"}: ", i[])
#             continue
#         # for j in i:
#
#             # f.writelines("\"" + str(j) + "\": "+ str(i[j]) + "}")
#                 # f.writelines(i)
#         count += 1
#     f.write("]")
#     # print("\nMOVING ON...")
#     # for i in f['elements']:
#     #     print(i);
#     #     count +=1
#     # f.close()
#
#     return count;



filename = '4645508147a65be4e31c1cce9ade2840c6ac334f.json';
f = open(filename)
data = json.load(f)
orig_count = read_json(data)
new_count = remove_steps(data)

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