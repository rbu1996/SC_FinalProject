import os
import json

if __name__ == '__main__':
	datafiles = os.listdir("raw_data/")
	datafiles = [data for data in datafiles if "json" in data]
	news_id = 0
	with open("MainData.json", 'w', encoding='utf-8') as mf:
		for datafile in datafiles:
			print("Process data file: ", datafile)
			with open("raw_data/"+datafile) as f:
				for line in f:
					data = json.loads(line.strip())
					data['newsID'] = news_id
					news_id+=1
					json.dump(data, mf)
					mf.write("\n")