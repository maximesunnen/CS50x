from flask.json import JSONEncoder

class Scout:
    def __init__(self, first_name, last_name, birthday, gender, number, branch, email, house_number, street, town, zip, country, allergies, diet, other):
        self.first_name = first_name.upper()
        self.last_name = last_name.upper()
        
        if isinstance(birthday, str):
            self.birthday = birthday
        else:
            self.birthday = birthday.strftime("%Y-%m-%d")
            
        self.gender = gender.upper()
        self.number = number
        self.branch = branch
        self.email = email
        self.house_number = house_number
        self.street = street.upper()
        self.town = town.upper()
        self.zip = zip
        self.country = country
        self.allergies = allergies
        self.diet = diet
        self.other = other
        
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
        
class Tutor:
    def __init__(self, first_name, last_name, number, email):
        self.first_name = first_name.upper()
        self.last_name = last_name.upper()
        self.number = number
        self.email = email
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
        
from collections import OrderedDict
class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Scout, Tutor)):
            return OrderedDict(obj.__dict__)
        return super().default(obj)
