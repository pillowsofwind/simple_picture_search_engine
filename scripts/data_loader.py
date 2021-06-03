import csv
import json

def load_data():

	# data files
	f_base = open("validation-images-with-rotation.csv", "r", encoding="utf-8")
	f_label = open("validation-annotations-human-imagelabels.csv", "r", encoding="utf-8")
	f_label_dict = open("class-descriptions.csv", "r", encoding="utf-8")

	# temporary data structures
	label_description_dict = {}
	imgid_labellist_dict = {}
	dataset = []	# list of dict{imgID, verbose-info, descriptions}

	# build dict <label, description>
	reader_label_dict = csv.reader(f_label_dict)
	for ind, r in enumerate(reader_label_dict):
		if ind == 0:
			continue
		label_description_dict[r[0]] = r[1]

	# build dict <imgID, list of labels>
	reader_label = csv.reader(f_label)
	for ind, r in enumerate(reader_label):
		if ind == 0:
			continue
		if r[3] == "0":
			if r[0] not in imgid_labellist_dict.keys():
				imgid_labellist_dict[r[0]] = []
		elif r[0] in imgid_labellist_dict.keys():
			imgid_labellist_dict[r[0]].append(r[2])
		else:
			imgid_labellist_dict[r[0]] = [r[2]]

	# build dataset
	reader_base = csv.reader(f_base)
	for ind, r in enumerate(reader_base):
		if ind == 0:
			continue
		data = {}
		data["ID"] = r[0]
		data["url"] = r[2]
		data["verbose-info"] = {}
		data["descriptions"] = []
		data["verbose-info"]["author"] = r[6]
		data["verbose-info"]["title"] = r[7]
		data["verbose-info"]["original-size"] = r[8]
		labels = imgid_labellist_dict[data["ID"]]
		for label in labels:
			data["descriptions"].append(label_description_dict[label])
		dataset.append(data)
	return dataset

if __name__ == "__main__":
	dataset = load_data()
	f = open("data.json", "w")
	# f.write(json.dumps(dataset))
	json.dump(dataset, f, indent=2)
	f.close()