import json

def remove_steps(JSON_file, outfile):
    """

    :param JSON_file: orginal json file
    :param outfile: name for new json to be created
    :return: null
    """
    f = open(outfile, "w")
    f.write("{\"elements\": ")
    # loop through each item in the original array and add the ones that don't have "steps" as a tag to new array
    temp_obj = []
    for a in JSON_file['elements']:
        try:
            if (a["tags"]["highway"] != "steps"):
                temp_obj.append(a)
        # some elements don't have "tag" key, so searching for "steps" would through an error.  Ignore it
        except KeyError:
            temp_obj.append(a)
        except:
            temp_obj.append(a)
    # convert array object to json object
    json.dump(temp_obj, f, indent=2)
    f.write("}")
    f.close()

# name of original json file
filename = "4645508147a65be4e31c1cce9ade2840c6ac334f.json"
t = open(filename)
# load entire json file into a variable
data = json.load(t)

# file name for file to be created
out_file = "new_file.json"
remove_steps(data, out_file)
# open new file to read after writing new array to it for counting purposes
g = open(out_file, "r")
new_data = json.load(g)

print("There are", len(data["elements"]), "elements in the original json.")
print("There are", len(new_data["elements"]), "elements in the new json.")
print(len(data["elements"])-len(new_data["elements"]), "elements have been removed.")
