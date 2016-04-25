import json

class Package:
    '''
    Class representing a package of wikidata items created using the wd-package.py command
    '''
    def __init__(self, packageFile):
        with open(packageFile) as packageInput:
            self.package = json.load(packageInput)

    def labels(self, attribute):
        for id in self.package[attribute]:
            yield self.package["items"][id]["label"]
