from asyncio import constants
import sqlite3
from turtle import title
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connections

@api_view(['GET', 'POST'])
def users_data(request):
    
    if request.method == 'GET':
        try:
            request.session["userid"]
        except KeyError:
            print("<,,,,,something")
            return Response(data={"isLogin":False})    
        conn = sqlite3.connect('problem_sets.db')
        cur = conn.cursor()
        cur.execute("select * from user")
        get_user = cur.fetchall()
        my_list = []
        index = 1
        for t in get_user:
            my_list.append({'index': index, 'first_name': t[0], 'last_name': t[1],'email':t[2],'password': t[3],'contact':t[4]})
            index += 1
        # return Response({"message": "THIS IS ALL ABOUT GET!", "data": my_list})
        return Response(my_list)
    
    elif request.method == 'POST':
        try:
            request.session["userid"]
        except KeyError:
            print("<,,,,,something in post")
            return Response(data={"isLogin":False}) 
        
        new_data = request.data
       
        print(new_data)
        
        first_name = new_data["first_name"]
        last_name = new_data["last_name"]
        contact =new_data["contact"]
        email = new_data["email"]
        password = new_data["password"]
        try:
            request.session("userid")
        except:
            pass
                
        try:
            sqliteConnection = sqlite3.connect('problem_sets.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_insert_with_param = """INSERT INTO user
                            (first_name,last_name,contact,email,password) 
                            VALUES (?, ?, ?,?,?);"""

            data_tuple = (first_name,last_name,contact,email,password)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            print("Python Variables inserted successfully into SqliteDb_developers table")

            cursor.close()

        except sqlite3.Error as error:
            print(error)
            return Response({"message": "Failed to insert Python variable into sqlite table" })
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
        
        return Response({"message": "data added successfully"})
    
@api_view(['PUT','DELETE'])
def users_update_delete(request,id):
    if request.method == 'PUT':
        new_data = request.data
        
        print(new_data)
        user_id = new_data["user_id"]
        first_name = new_data["first_name"]
        last_name = new_data["last_name"]
        email = new_data["email"]
        password = new_data["password"]
        try:
            sqliteConnection = sqlite3.connect('problem_sets.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            updatedata = """update user set user_id = ?, first_name = ?, last_name = ?, email = ?,password = ? where user_id =?"""

            # data_tuple = (user_id,first_name,last_name,email,password)
            cursor.execute(updatedata,(user_id,first_name,last_name,email,password,id))
            sqliteConnection.commit()
            print("Python Variables inserted successfully into SqliteDb_developers table")

            cursor.close()

        except sqlite3.Error as error:
            print(error)
            return Response({"message": "Failed to insert Python variable into sqlite table" })
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
        
        return Response({"message": "data added successfully"})
    
    # ===================================== login =================================

@api_view(['GET','POST'])  
def login(request):
    if request.method == 'GET':
        try:
            request.session["userid"]
        except KeyError:
            return Response({"isLogin":False})
        return Response({"isLogin":True})
                
    if request.method == 'POST':
        try:
            request.session["userid"]
        except KeyError:
            
            # print("<,,,,,something in post")
            # return Response(data={"isLogin":False}) 
            new_data = request.data
        
            print(new_data)
            
            email = new_data["email"]
            password = new_data["password"]
        
            try:
                sqliteConnection = sqlite3.connect('problem_sets.db')
                cursor = sqliteConnection.cursor()
                print("Connected to SQLite")

                check_user = """SELECT Rowid  FROM USER WHERE email=? AND password=?"""
                print("print check:",check_user)
                checked=cursor.execute(check_user,(email,password))
                get_user = cursor.fetchone()
                request.session["userid"]=get_user
            
                print("get_user:->>>>>>>>",get_user)
                
                sqliteConnection.commit()
                

                cursor.close()
                # if get_user == None:
                #     return Response({"login":False})
                # else:
                #     return Response({"login":True})
                

            except sqlite3.Error as error:
                print(error)
                return Response({"message": "Failed to check Python variable into sqlite table" })
            finally:
                if (sqliteConnection):
                    sqliteConnection.close()
                    print("The SQLite connection is closed")
            
        return Response({"isLogin": True})
 
@api_view(['GET','POST'])  
def logout(request):  
    try:
        request.session["userid"]
    except KeyError:
        return Response({"isLogin":False})  
    del request.session["userid"] 
    return Response({"isLogin":False})     
    
    
    
          
    
    
    
    
        
     


