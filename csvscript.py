def f8():

	import csv
	import datetime
	import pandas as pd
	import os

	# import necessary packages
	import csv
	
	with open('dates.csv') as file_obj:
		reader_obj = csv.reader(file_obj)
		for row in reader_obj:
			filenameDate=row[0]
		
	def get_csv_file_name(start_with):
		for root, dirs, files in os.walk("."):
			for file in files:
				if file.endswith(".csv") and file.startswith(start_with):
					return os.path.join(root, file)
		return None

	csv_file_name = get_csv_file_name("file8.")
	if csv_file_name:
		print(csv_file_name)
		filename=csv_file_name.split('.csv')[0].split('file8.')[1]
		print(filename)
	else:
		print("No CSV file found.")

# --------------------------------------------------------------------------------------

	import pandas as pd

	df = pd.read_csv(csv_file_name, header=None)
	df = df[df[0] != 'FF']
	invalid_rows = df[df[16] == 'Invalid'].copy()
	df = df[df[16] != 'Invalid']

	INVALID_FILE = filename+"."+"invalid"+"."+filenameDate+".csv"
	invalid_rows.to_csv(INVALID_FILE, index=False, header=False)



	blacklist = pd.read_csv('blacklist.csv', header=None)
	blacklist_rows = df[df[10].isin(blacklist[0])].copy()
	df = df[~df[10].isin(blacklist[0])]
	blacklist_rows.to_csv(INVALID_FILE, mode='a', index=False, header=False)

	df = df.drop(columns=[0, 1])



	df.loc[df[4] == 'NOTICE', 5] = 247450
	df.loc[df[4].isin(['DISCONTINUANCE', 'VOLUNTARY']), 5] = 247452
	df[5].fillna(247449, inplace=True)
	df[2] = df[2].str[:15].str.strip() + ' - '+filename
	df = df.drop(columns=[3, 4])
	df[7] = df[5]
	df[5] = df[10]
	df[6] = df[18]
	df[8] = "CST-New.Venture"
	df[12] = df[9]
	df[9]=""
	df[10]="Pipeline"
	df[11]="New"
	df[13]=""
	df = df.drop(columns=[14, 15,16,17,18])





	df.to_csv("output.csv", index=False, header=False)


	import csv


	with open('output.csv', 'r') as f1:
		reader = csv.reader(f1)
		data = list(reader)


	with open('assigned2.csv', 'r') as f2:
		reader = csv.reader(f2)
		assigned_data = list(reader)
		try:
			csr_id = assigned_data[0][2]
		except:
			csr_id = None


	for i, row in enumerate(data):
		row[5]=assigned_data[i % len(assigned_data)][0]
		row[9]=assigned_data[i % len(assigned_data)][1]
	

	with open('output.csv', 'w', newline='') as f3:
		writer = csv.writer(f3)
		for row in data:
			if row[3]=="True":
				row[3] = 247449
			writer.writerow(row)


	import pandas as pd

	try:
		header = ["business_name","phone","email","source_id","tag","assigned_to","pipeline","stage","dot_number","location_id"]
		df = pd.read_csv("output.csv")
		df.columns = header
		if csr_id != None:
			csr_column = []
			for _ in range(0, df.__len__()):
				csr_column.append(csr_id)
			df.insert(loc = 6, column="csr_id", value = csr_column)

	
		df.to_csv(filename+"."+filenameDate+".csv", index=False)


	except:
		header = ["business_name","phone","email","source_id","tag","assigned_to","pipeline","stage","dot_number","location_id",""]
	
		df = pd.read_csv("output.csv")
		df.columns = header

		if csr_id != None:
			csr_column = []
			for _ in range(0, df.__len__()):
				csr_column.append(csr_id)
			df.insert(loc = 6, column="csr_id", value = csr_column)
	
		

		# Write the DataFrame back to the same CSV file with the header
		df.to_csv(filename+"."+filenameDate+".csv", index=False)


	import shutil

	original='output.csv'
	target = 'leads-input.csv'
	shutil.copyfile(original, target)
	shutil.copyfile(filename+"."+filenameDate+".csv", target)
	# os.rename(ilfename+"."+filenameDate+".csv", 'leads-input.csv')
	os.remove("output.csv")
