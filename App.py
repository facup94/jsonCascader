import json


class Product(object):
    def __init__(self, id, name, namePath, idPath):
        self.id = id
        self.name = name
        self.namePath = namePath
        self.idPath = idPath
        # self.hierachy = [int(elem) for elem in idPath.split(' > ')[:-1]]
        self.hierachy = [int(elem) for elem in idPath.split(' > ')]
        self.childs = []
        self.father = int(idPath.split(' > ')[-2]) if len(self.hierachy) > 1 else None

    def add_child(self, child):
        self.childs.append(child)

    def __repr__(self):
        return '{id: ' + str(self.id) + ', name: ' + self.name + ', idPath: ' + self.idPath + \
               ', hierachy: ' + str(self.hierachy) + ', childs: ' + str(self.childs) + \
               ', father: ' + str(self.father)

    def as_dict(self):
        d = dict()
        d['id'] = self.id
        d['name'] = self.name
        d['childs'] = [child.as_dict() for child in self.childs]
        return d


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.as_dict


def object_decoder(obj):
    return Product(obj['id'], obj['name'], obj['namePath'], obj['idPath'])


def search_id(list, id):
    for e in list:
        if e.id == id:
            return e

    return None


# Main Program
with open('new-tree.json') as f:
    data = [object_decoder(obj) for obj in json.load(f)]

for elem in data:
    if elem.father is not None:
        search_id(data, elem.father).add_child(elem)

for elem in data:
    if len(elem.hierachy) == 1:
        root = elem

with open('result.json', 'w') as f:
    f.write(json.dumps(root.as_dict()))
# print(root)
# print(json.dumps(data[0].as_dict()))
# print(json.dumps(root.as_dict()))

