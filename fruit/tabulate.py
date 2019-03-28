class Column(object):
    TYPES = {t: i for i,t in enumerate([int, float, str])}

    def __init__(self, margin=1, separator="|", final=False):
        self.width = 0
        self.margin = " "*margin
        self.final = final
        self.separator = separator
        self.type = int

    def add_value(self, value):
        self.width = max((self.width, len(str(value))))

        try:
            pri = self.TYPES[type(value)]
            if pri > self.TYPES[self.type]:
                self.type = type(value)
        except KeyError:
            pass

    def separator_string(self):
        if self.final:
            return ""
        else:
            return self.separator + " "

    def value_str(self, value):
        s = self.separator + self.margin + value.ljust(self.width) + self.margin

        if self.final:
            s += self.separator

        return s

class Columns(dict):
    def __init__(self, keys):
        super().__init__({k: Column() for k in keys})
        self[keys[-1]].final = True

    def new_cell(self, key, item):
        if key in item:
            c = Cell(item[key], self[key])
        else:
            c = Cell("", self[key])

        return c

class Cell(object):
    def __init__(self, value, column):
        self.value = value
        self.column = column

        self.column.add_value(self.value)

    def __str__(self):
        return self.column.value_str(str(self.value))

    def get_value(self):
        try:
            return self.column.type(self.value)
        except TypeValue:
            return self.column.type()

class Tabular(object):
    def __init__(self, items, keys=None, sort_by=None):
        if keys == None:
            keys = list(set(k for item in items
                            for k in item.keys()))

        if sort_by == None:
            sort_idx = 0
        else:
            sort_idx = keys.index(sort_by)

        columns = Columns(keys)

        self.keys =  [Cell(key, columns[key]) for key in keys]
        self.data = sorted([[Cell(item[key], columns[key])
                             if key in item else
                             Cell(None, columns[key])
                             for key in keys]
                            for item in items],
                           key=lambda row : row[sort_idx].get_value())

    def __str__(self):
        s = ""

        s += "".join(str(k) for k in self.keys)
        s += "\n"

        s += "-"*(len(s)-1)
        s += "\n"

        for row in self.data:
            s += "".join(str(c) for c in row)
            s += "\n"

        return s
