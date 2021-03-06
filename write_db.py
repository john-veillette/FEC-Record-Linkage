import sqlite3
from util import line_to_dict, INDEX

def write_results(db, colName1, colName2, tableName, resultsFile):
	query = "CREATE TABLE " + tableName + " (" 
	query += colName1 + " text, "
	query += colName2 + " text)"
	db.execute(query)
	query = "INSERT INTO " + tableName + " VALUES (?, ?)"
	f = open(resultsFile)
	for line in f:
		line = line.strip()
		l = line.split('\t')
		t = (l[0], l[1].strip('\"'))
		db.execute(query, t)
	f.close()


def convert_date(date):
	'''
	Converts MMDDYYYY to YYYY-MM-DD
	'''
	try:
		month = date[:2]
		day = date[2:4]
		year = date[4:]
		return year + '-' + month + '-' + day
	except Exception as e:
		print(e)
		return None


def write_data(db, tableName = 'donations', dataFile = 'itcont.txt', 
	headerFile = "indiv_header_file.csv"):
	'''
	Writes FEC data to its own table
	'''
	query = "CREATE TABLE " + tableName + " ("
	query += "CMTE_ID" + " text, " # committee ID
	query += "AMNDT_IND" + " text, " # Amendment Indicator
	query += "RPT_TP" + " text," # report type
	query += "TRANSACTION_PGI" + " text, " # Primary-General Indicator
	query += "IMAGE_NUM" + " text,"
	query += "TRANSACTION_TP" + " text, " # transaction type
	query += "ENTITY_TP" + " text, "
	query += "NAME" + " text, "
	query += "CITY" + " text, "
	query += "STATE" + " text, "
	query += "ZIP_CODE" + " text, "
	query += "EMPLOYER" + " text, "
	query += "OCCUPATION" + " text, "
	query += "TRANSACTION_DT" + " date, " # date (MMDDYYYY in dataset,
	query += "TRANSACTION_AMT" + " real, "	# YYYY-MM-DD in SQL; we'll convert)
	query += "OTHER_ID" + " text, "
	query += "TRAN_ID" + " text, " # transaction ID (electronic only)
	query += "FILE_NUM" + " text, " # file number (sometimes null?)
	query += "MEMO_CD" + " text, " # memo code
	query += "MEMO_TEXT" + " text, "
	query += "SUB_ID" + " text)" # unique row idea (never null!)
	db.execute(query)
	f = open(headerFile)
	s = f.read()
	f.close()
	s = s.strip()
	keys = s.split(',')
	keys = [':' + key for key in keys]
	s = ', '.join(keys)
	query = "INSERT INTO " + tableName + " VALUES (" + s + ")"
	f = open(dataFile)
	for line in f:
		record = line_to_dict(line)
		record['TRANSACTION_AMT'] = float(record['TRANSACTION_AMT'])
		record['TRANSACTION_DT'] = convert_date(record['TRANSACTION_DT'])
		db.execute(query, record)
	f.close()

if __name__ == '__main__':
    conn = sqlite3.connect("donations.db")
    db = conn.cursor()
    write_data(db)
    conn.commit()
    write_results(db, "donor_ID", "SUB_ID", "donors", "results.txt")
    conn.commit()
    conn.close()











