from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
import ast

class Build:
    def __init__(self, data):
        self.id = data['id']
        self.race = data['race']
        self.build_class = data['build_class']
        self.background = data['background']
        self.proficiencies = data['proficiencies']
        self.race_description = data['race_description']
        self.bg_description = data['bg_description']
        self.img_path = data['img_path']
        self.build_name = data['build_name']
        self.user_id = data['user_id']

    @classmethod
    def get_builds_by_user(cls, user_id):
        data = {
            'id' : user_id
        }
        query = """SELECT * FROM builds WHERE user_id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db( query, data )
        if len(results) < 0:
            return False
        # print(f"\nRESULTS FROM DB >> {results}\n")
        all_builds = []
        for row in results:
            row['proficiencies'] = ast.literal_eval(row['proficiencies']) #convert string from database to a python list
            this_build = cls(row)
            all_builds.append(this_build)
        return all_builds
    
    @classmethod
    def get_build_by_id(cls, build_id):
        data = {
            'id' : build_id
        }
        query = """SELECT * FROM builds WHERE id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db( query, data )
        results[0]['proficiencies'] = ast.literal_eval(results[0]['proficiencies']) #convert string from database to a python list
        this_build = cls(results[0])
        return this_build
    
    @classmethod
    def create_build(cls, data):
        print(data)
        query = """INSERT INTO builds (race, build_class, background, proficiencies, race_description, bg_description, img_path, user_id, build_name) VALUES (%(race)s, %(buildClass)s, %(background)s, %(proficiencies)s, %(raceDescription)s, %(bgDescription)s, %(img_path)s, %(user_id)s, %(build_name)s);"""
        build_id = connectToMySQL(DATABASE).query_db( query, data )
        return build_id
    
    @classmethod
    def update_build(cls, data):
        query = """UPDATE builds SET race = %(race)s, build_class = %(build_class)s, background = %(background)s, race_description = %(race_description)s, proficiencies = %(proficiencies)s, bg_description = %(bg_description)s, img_path = %(img_path)s, build_name = %(build_name)s WHERE id = %(build_id)s;"""
        return connectToMySQL(DATABASE).query_db( query, data )
    
    @classmethod
    def delete_build(cls, build_id):
        data = {
            'id': build_id
        }
        query = """DELETE FROM builds WHERE id = %(id)s;"""
        connectToMySQL(DATABASE).query_db( query, data )
        return build_id
    
    @classmethod
    def make_build_name(cls, user_builds):
        def_build_name = f"Build {len(user_builds) + 1}"
        names_list = {}
        names_values = names_list.values()
        print("User Builds:")
        for build in user_builds:
            print(build.build_name)
            names_list[build.id] = build.build_name
        if def_build_name in names_values:
            highest_val = 0
            for name in names_values:
                # print(name[-2::])
                try: #test to see if the last two values in a build's name can be converted to an int
                    if int(name[-2::]) > highest_val:
                        highest_val = int(name[-2::]) #sets new highest value if the ending number is higher than any previous
                except: #if it can't convert into int, print NaN and skip
                    print(f"'{name[-2::]}' is not a number")
                print(f"Highest Val = {highest_val}")
            print("Found it")
            build_name = f"Build {highest_val+1}"
        else:
            build_name = def_build_name

        print(f"Name: {build_name}")
        return build_name
    
    @classmethod
    def find_next_build(cls, deleted_build):
        print(f"DELETED BUILD'S USER >> {deleted_build.user_id}")
        print(f"DELETED BUILD'S ID >> {deleted_build.id}")
        all_builds = cls.get_builds_by_user(deleted_build.user_id)
        next_build = False
        for idx in range(len(all_builds) - 1):
            print(all_builds[idx].id)
            if all_builds[idx].id == deleted_build.id:
                    next_build = all_builds[idx+1]
                    print(f"Next build >> {next_build.id}")
        return next_build
    
    @staticmethod
    def listify(data):
        newList = data.split("\r\n") #converts raw input into list, getting rid of empty lines
        newString = '[' #declares string that will store converted list at the end
        # print(f"OLD LIST ---- {newList}")
        if '' in newList:
            occurrence = [] #empty array to keep track of indexes where an empty space is found
            for i in range(len(newList)):
                if newList[i] == '': #look for empty space
                    occurrence.append(i) #add index to list of occurrences
            for j in range(len(occurrence)-1, -1, -1): #go backwards through occurrences
                newList.pop(occurrence[j]) #get rid of each occurrence in the list in reverse, to avoid altering length of list and going out of bounds
        for x in range(len(newList)-1): #go through created list (before last entry)
            newString += f"'{newList[x]}', " #concatonate string with list entries and a comma
        newString += f"'{newList[len(newList)-1]}']" #cap off string with last entry
        # print(newString)
        return newString
    
    # @staticmethod
    # def validate(data):
    #     is_valid = True
    #     if data['build_name']:
    #         pass
    #     return is_valid