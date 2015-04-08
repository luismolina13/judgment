import csv
import datetime
cr = csv.reader(open("combined_history.csv", "rU"))
temp = -1
count = 0
new_rows_list = []
row1 = next(cr)
for row in cr:
    date_time = row[0]
    new_date = datetime.datetime.strptime(date_time, '%m/%d/%Y').date()
    if temp == -1:
        old_date = new_date
        temp = 1
        filename = "csv" + str(count) + ".csv"
	new_rows_list.append(row)

    if old_date != new_date:
        filename = "csv" + str(count) + ".csv"
        file2 = open(filename, 'wb')
	writer = csv.writer(file2)
	writer.writerows(new_rows_list)
        file2.close()        
        count = count + 1
        old_date = new_date
        new_rows_list = []
        new_rows_list.append(row)
    else:
        new_rows_list.append(row)


    
        
