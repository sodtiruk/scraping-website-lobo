import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import urllib.parse
import os
import time

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
TABLEDATABASE = os.getenv('TABLE')

# HOST = "localhost" 
# PORT = 4001 
# USER = "user" 
# PASSWORD = "password" 
# DATABASE = "db" 
# TABLEDATABASE = "lobo"

def connectDatabaseMySql():
    #connect database mysql
    # conn = mysql.connector.connect(

    #     host=HOST,
    #     port=PORT,
    #     user=USER,
    #     password=PASSWORD,
    #     database=DATABASE

    # )
    # return conn 
   while True:
        try:
            conn = mysql.connector.connect(
                host=HOST,
                port=PORT,
                user=USER,
                password=PASSWORD,
                database=DATABASE
            )
            if conn.is_connected():
                print("Connected to the database")
                return conn
        except Error as e:
            print(f"Error: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

def createTableDatabase(tableName):
    conn = connectDatabaseMySql()
    cursor = conn.cursor()

    sql = f"""
        create table {tableName}(
        product_id int,
        name varchar(255),
        price float,
        image varchar(255),
        link varchar(255)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """ 

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.commit()


def insertDataToDatabase(dataLobo, tableName):
    #connect database
    conn = connectDatabaseMySql()
    cursor = conn.cursor()

    size = len(dataLobo['name'])

    sql = f" INSERT INTO {tableName} (product_id, name, price, image, link) "

    valueSql = ""
    if size == 1:
        valueSql = " VALUES ( (select ifnull(max(product_id)+1, 1) from lobo i), %s, %s, %s, %s) "
    else:
        valueSql = " VALUES ( (select ifnull(max(product_id)+1, 1) from lobo i), %s, %s, %s, %s) "
        for i in range(size-1):
            valueSql += " , ( (select ifnull(max(product_id)+1, 1) from lobo i), %s, %s, %s, %s) " 

        value = tuple() 
        for i in range(size):
            value += (dataLobo['name'][i], dataLobo['price'][i], dataLobo['image'][i], dataLobo['link'][i])
    sql += valueSql

    # print(sql)
    # print(value)

    # print(size)
    # print(valueSql)

    cursor.execute(sql, value)
    conn.commit()
    
    cursor.close()
    conn.close()


def fetchDataLobo():
    all_data = dict()
    name_list = []
    price_list = []
    image_list = []
    link_list = []
    item = 1
    for page in range(1,7):
        url = "https://www.lobo.co.th/category?tskp="+str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
            
        products = soup.find('div', {'class': 'productsArea tsk-dataview thumbnailArea size-250r frame-000'})
        all_products = products.find_all('div', {'class':'productArea productItem'})
        
        for product in all_products:
            # print("item", item)
            thumnail = product.find('a', {'class':'gadgetThumbnail'})
            image = thumnail.contents[1].get('data-srcset').split()[0]
        
            detail = product.find('div', {'class':'productDetail'})
            name = detail.find('div', {'class':'product_name'})
            name = name.text
        
            price = product.find('div', {'class':'product_price has_currency_unit'})
            price = price.text.split()[0]
        
            link = thumnail.get('href')
            #unquote link to thai
            link = urllib.parse.unquote(link)

            name_list.append(name)
            price_list.append(price)
            image_list.append(image)
            link_list.append(link)
            
            item+=1
        print("fetch data page " + str(page))

    all_data['name'] = name_list
    all_data['price'] = price_list
    all_data['image'] = image_list
    all_data['link'] = link_list
    
    return all_data


def main():

    print("insert to database")

    dataLobo = fetchDataLobo()
    tableDatabaseName = TABLEDATABASE

    createTableDatabase(tableDatabaseName) 
    insertDataToDatabase(dataLobo, tableDatabaseName)
    print("Done!!!")        
    

if __name__ == "__main__":
    main()












































