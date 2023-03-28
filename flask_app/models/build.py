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

    @classmethod
    def get_builds_by_user(cls, id):
        data = {
            'id' : id
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
    def create_build(cls, data):
        print(data)
        query = """INSERT INTO builds (race, build_class, background, proficiencies, race_description, bg_description, img_path, user_id) VALUES (%(race)s, %(buildClass)s, %(background)s, %(proficiencies)s, %(raceDescription)s, %(bgDescription)s, %(img_path)s, %(user_id)s);"""
        build_id = connectToMySQL(DATABASE).query_db( query, data )
        return build_id
    
    @classmethod
    def delete_build(cls, build_id):
        data = {
            'id': build_id
        }
        query = """DELETE FROM builds WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db( query, data )