'''
Examples of working with JSON
KTN 2013 / 2014
'''
import json
'''
Converting a dictionary object to a JSON string:
'''
my_value = 3
my_list = [1, 2, 5]
my_dict = {'key': my_value, 'key2': my_list}
my_dict_as_string = json.dumps(my_dict)
print my_dict_as_string
'''
Output:
{"key2": [1, 2, 5], "key1": 3}
'''


'''
Converting a JSON string to a dictionary object:
'''
my_value = 3
my_list = [1, 2, 5]
my_dict = {'key': my_value, 'key2': my_list}
my_dict_as_string = json.dumps(my_dict)
my_dict_from_string = json.loads(my_dict_as_string)
