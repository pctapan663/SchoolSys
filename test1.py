import psycopg2
try:
    '''
    connection = psycopg2.connect(user = "altrahisusr",
                                  password = "kfT#47Mdt4",
                                  host = "95.216.232.109",
                                  port = "5432",
                                  database = "altrahis")
    '''
    connection = psycopg2.connect(user = "postgres",
                                  password = "",
                                  host = "localhost",
                                  port = "5432",
                                  database = "altrahis")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    #cursor.execute("select * from \"SchoolSys\".users;")
    
    cursor.execute("insert into \"SchoolSys\".users (email,password,created_date,modified_date) values ('ansuman1@altrasyscon.com', 'dilbert1', now(), now());")
    connection.commit()
    connection.close()
    '''
    records = []
    result = cursor.fetchall()
    for row in result:
           records.append(row)
    print("You are connected to - ", records,"\n")
    '''
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")