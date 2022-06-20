import random

#This function returns a list of books as [[<author_name>,book_name]] by reading the file name.
def read_books(file_name):
    book_list = []
    with open(file_name) as file:
        for line in file:
            line = line.strip().split(",")
            book_list.append(line)
    return book_list

#This function returns a dictionary as {"User_name" : [Ratings of 55 books]} by reading the file name.
def read_ratings(file_name):
    ratings_dict = {}
    with open(file_name) as file: 
        first = file.readline().strip()
        #The loop stops when the lines are finished
        while first != "":
            second = file.readline().strip().split()
            #This loop converts all the rating values into integers.
            for x in range(len(second)):
                second[x] = int(second[x])
            #First line(user_name) is added as the key and second line(ratings) is added as value to the dictionary.
            ratings_dict[first] = second
            first = file.readline().strip()
    return ratings_dict

#Files are read by calling the functions.
ratings_dict = read_ratings("ratings.txt")
book_list = read_books("books.txt")

#This returns a list of tuples as [("User name",similarity value)] where the list is sorted using the similarity values(high to low).
def similarities(user_name):
    similarity_list = []
    for user in ratings_dict:
        #This if statement prevents the function to do this algorithm on the user itself.
        if user != user_name:
            #dot product is used between the list of rating values of 2 users.
            similarity_value = sum(map(lambda x,y : x*y , ratings_dict[user_name],ratings_dict[user]))
            similarity_list.append((user,similarity_value))
            #Similarity_list is sorted (high to low) according to the dot product result/similarity value.
            similarity_list.sort(key=lambda tup: tup[1], reverse=True)
    return similarity_list

#table
def ratings_table():
    ratings = [-5,-3,0,1,3,5]
    meanings = ["Hated it!","Didn't like it","Haven't read it","OK","Liked it!","Really liked it!"]
    print("Ratings Meanings")
    for r, m in zip(ratings,meanings):
        print(str(r)+ "\t" + m)

#if user_name not in dict
def absent(new_user):
    new_user = len(book_list)*[0]
    ratings = [-5,-3,0,1,3,5]
    ratings_table()
    book_numbers = random.sample(range(54),round(len(book_list)/5))
    for i in range(round(len(book_list)/5)):
        rate = 2
        book_name = book_list[book_numbers[i]][1]+" by "+book_list[book_numbers[i]][0]
        while rate not in ratings:
            integer = False
            while integer==False: 
                try:  
                    rate = int(input("Please rate %s,using the RATINGS :" % book_name))
                    integer=True
                except ValueError: 
                    print("Please enter a value from the ratings table.")
        new_user[book_numbers[i]] = rate
    return new_user

#filtering the books
def filtering(user):
    user_books = []
    ratings = ratings_dict[user]
    if user == user_name:
        for i in range(len(ratings)):
           if ratings[i] != 0:
                user_books.append(book_list[i])
    else:
        for i in range(len(ratings)):
            if ratings[i] >= 3:
                user_books.append(book_list[i])
    return(user_books)

#recommendations
def recommend(user_name,recommends_no):
    recommends_list = []
    new_dict = {}
    i = 0
    if user_name not in ratings_dict:
        ratings_dict[user_name] = absent(user_name)
    list_similarity = similarities(user_name)
    books_not_read = filtering(user_name)
    while len(recommends_list) < recommends_no and i < len(list_similarity):
        name = list_similarity[i][0]
        filtered_books = filtering(name)
        new_dict[name] = []
        for book in filtered_books:
            if book not in books_not_read and book not in recommends_list:
                if len(recommends_list) != recommends_no:
                    new_dict[name] += [book]
                    recommends_list += [book]
        if len(new_dict[name]) == 0:
            del new_dict[name]
        i += 1
    return new_dict 

#printing
def output(new_dict,user_name,recommends_no):
    with open("output.txt","w") as file:
        if recommends_no != 0:
            print("\n"+str(recommends_no) + " recommendations for user " + user_name)
            print("\nRecommending based on similarity algorithm")
            print("+"*43)
            file.write(str(recommends_no) + " recommendations for user " + user_name+"\n")
            file.write("\nRecommending based on similarity algorithm\n")
            file.write("+"*43+"\n")
            for user in new_dict:
                i = 0
                print("Recommended by user "+user)
                file.write("Recommended by user "+user+"\n")
                while i != len(new_dict[user]):
                    print("\t\t"+str(new_dict[user][i][1])+" by "+str(new_dict[user][i][0]))
                    file.write("\t\t"+str(new_dict[user][i][1])+" by "+str(new_dict[user][i][0])+"\n")
                    i += 1
        else:
            print("No recommendations for user %s." % user_name)
            file.write("No recommendations for user %s." % user_name)

user_name = input("Please enter a user name: ").strip()
while user_name == "":
    user_name = input("Please enter a valid user name: ").strip()
integer = False 
while integer==False: 
    try:
        recommends_no = input("Please enter the number of recommendations: ")
        if recommends_no == "":
            recommends_no = 10
        elif int(recommends_no) < 0:
            raise ValueError
        else:
            recommends_no = int(recommends_no)
        integer=True
    except ValueError: 
        print("Please enter a positive integer.")

new_dict = recommend(user_name,recommends_no)
output(new_dict,user_name,recommends_no)

