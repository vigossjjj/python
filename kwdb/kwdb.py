from bs4 import BeautifulSoup
import urllib2
import xlwt
import time
import MySQLdb
import xlrd

class CONVERT():
    PATCH_TO_ID = 0
    ID_TO_PATCH = 1
    KW_TO_ID = 2
    ID_TO_KW = 3
    @staticmethod
    def convertID(srcID, dstType):
        if dstType == CONVERT.PATCH_TO_ID:
	  if srcID == "":
	    return 0
	  tmp = srcID.split("/")
	  return int(tmp[-2])
        elif dstType == CONVERT.ID_TO_PATCH:
            tmp = "android.intel.com:8080/#/c/" + str(srcID)
            return tmp
        elif dstType == CONVERT.KW_TO_ID:
            tmp = srcID[1:]
            return int(tmp)
        elif dstType == CONVERT.ID_TO_KW:
            tmp = "#" + str(strID)
            return tmp
        else:
            return ""
class XLS_CONSTANT():
  COLUMN_KW = 3
  COLUMN_STATUS = 9
  COLUMN_PATCH = 10

def readOldFile(fileName, sheetName, keyWeek):  
  try:      
      conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306)
      cur=conn.cursor()
      
      #cur.execute('create database if not exists kw2')
      conn.select_db('kw2')
      #cur.execute('create table kw3(id int, kw_id int, patch_id int, date_id int, status text, start_time int, end_time int, primary key(kw_id))')
      
      data = xlrd.open_workbook(fileName)

      table = data.sheet_by_name(sheetName)

      rows = table.nrows

      for i in range(rows):
	  row = table.row_values(i)        
	  xlscell = row[XLS_CONSTANT.COLUMN_KW]
	  if xlscell != "":
	      kw_id = CONVERT.convertID(xlscell, CONVERT.KW_TO_ID)
	      sqlcmd = 'select * from kw3 where kw_id = %d' % kw_id           
	      ret = cur.execute(sqlcmd)
	      if (ret == 0):	     
		patch_id = CONVERT.convertID(row[XLS_CONSTANT.COLUMN_PATCH], CONVERT.PATCH_TO_ID)
		sqlcmd = "insert into kw3(kw_id, patch_id, start_time, end_time, status)  values(%d, %d, %d, %d, \'%s\')" % (kw_id, patch_id, keyWeek, keyWeek + 1, row[XLS_CONSTANT.COLUMN_STATUS])
		cur.execute(sqlcmd)
	      else:
		sqlrow = cur.fetchall()[0]	      
		if sqlrow[2] != 'merged':
		  sqlcmd = 'update kw3 set end_time=%d where kw_id=%d' % (keyWeek + 1, sqlrow[0])
		  cur.execute(sqlcmd)
		  if row[XLS_CONSTANT.COLUMN_STATUS] == 'merged':
		    sqlcmd = 'update kw3 set status=\'merged\' where kw_id=%d' % sqlrow[0]
		    cur.execute(sqlcmd)
		    if row[XLS_CONSTANT.COLUMN_PATCH] != "" and  row[XLS_CONSTANT.COLUMN_PATCH] != 0:
		      patch_id = CONVERT.convertID(row[XLS_CONSTANT.COLUMN_PATCH], CONVERT.PATCH_TO_ID)
		      print patch_id
		      sqlcmd = 'update kw3 set patch_id=%d where kw_id=%d' % (patch_id, sqlrow[0])
		      cur.execute(sqlcmd)
      conn.commit()
      cur.close()
      conn.close()
  except MySQLdb.Error,e:
      print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    
def readNewFile(dataDic, keyWeek):
  try:
    conn = MySQLdb.connect(host='localhost', user = 'root', passwd = 'root', port = 3306)
    cur = conn.cursor()
    
    conn.select_db('kw2')   
    
    for key, value in dataDic.items():
      kw_id = CONVERT.convertID(value[XLS_CONSTANT.COLUMN_KW - 1], CONVERT.KW_TO_ID)
      sqlcmd = 'select * from kw3 where kw_id = %d' % kw_id           
      ret = cur.execute(sqlcmd)
      if (ret == 0):
	sqlcmd = "insert into kw3(kw_id, start_time, end_time)  values(%d, %d, %d)" % (kw_id, keyWeek, keyWeek + 1)
	cur.execute(sqlcmd)
      else:
	sqlrow = cur.fetchall()[0]
	value.append(sqlrow[2])
	if (sqlrow[2] == 'merged' and sqlrow[1] != 0):
	  patch = CONVERT.convertID(sqlrow[1], CONVERT.ID_TO_PATCH)
	  value.append(patch)
	  
    conn.commit()
    cur.close()
    conn.close()
  except MySQLdb.Error,e:
      print "Mysql Error %d: %s" % (e.args[0], e.args[1])




webaddr = "http://umgsw-cis3.jf.intel.com:8080/job/AndroidKW96_r44b_stable_byt_t_ffrd8/18/artifact/BuildData/HTML/kw_issues_AOSP.html"

result = {}
G_ID = 1

def itemParser(args):
  item = str(args).decode('utf8')
  node = []
  global G_ID
  link = BeautifulSoup(item)
  node.append(link.a['href'])
  node.append(link.a.string)
  itemContainter = item.split("<br/>")
  is_arkham = False  
  for i in range(len(itemContainter)):
    if i == 0:
      a = itemContainter[i].index("#")
      b = itemContainter[i].index(":")
      kw_id = itemContainter[i][a:b]
      node.append(str(kw_id))
    if i == 1:
      start = itemContainter[i].index(":")
      node.append(itemContainter[i][start + 1:])
      if "arkham" in itemContainter[i].lower():
	is_arkham = True
    if i == 2:
      otherInformation = itemContainter[i][8:-4].split("|")	
      for other in otherInformation:
	node.append(other.split(":")[1].strip())
  if is_arkham == True and "Critical(1)" in node:
    result[str(G_ID)] = node
    G_ID += 1
    
def writeXLS():
  content = urllib2.urlopen(webaddr).read()
  soup = BeautifulSoup(content)
  file = xlwt.Workbook()
  table = file.add_sheet('kw')
  items = soup.find_all('p')

  for item in items:
    itemParser(item)
    
  readNewFile(result, 11)

  for key, value in result.items():
    table.write(int(key) - 1, 0, key)
    for i in range(len(value)):
      table.write(int(key) - 1, i + 1, value[i])
  name =  time.ctime() + ".xls"
  file.save(name)
  
writeXLS()


