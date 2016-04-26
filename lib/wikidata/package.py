import json

class Package:
    '''
    Class representing a package of wikidata items created using the wd-package.py command
    '''
    def __init__(self, packageFile):
        with open(packageFile) as packageInput:
            self.package = json.load(packageInput)

    def get(self, attribute, i):
        value = self.package[attribute][i]

        if isinstance(value, basestring):
            self.package[attribute][i] = self.package["items"][value]
            return self.package[attribute][i]

        return value

    def items(self, attribute):
        for item in [self.get(attribute, i) for i in range(len(self.package[attribute]))]:
            yield item

    def labels(self, attribute):
        for item in self.items(attribute):
            yield item["label"]

    def findInRange(self, attribute, label, start, end):
        if end - start <= 0:
            return None

        middleIndex = int((start + end) / 2)
        middleItem  = self.get(attribute, middleIndex)
        middleLabel = middleItem["label"]
        print middleLabel

        if label < middleLabel:
            return self.findInRange(attribute, label, start, middleIndex)

        if middleLabel < label:
            return self.findInRange(attribute, label, middleIndex + 1, end)

        return middleItem;

    def find(self, attribute, label):
        return self.findInRange(attribute, label, 0, len(self.package[attribute]))
