class function:
    def derive(self):
        raise NotImplementedError


class Number(function):
    number: int

    def __init__(self, number: int):
        self.number = number

    def derive(self):
        return Number(0)

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return f"Number({self.number})"

class Addition(function):
    addition_list: list[function,...]
    def __init__(self, addition_list):
        self.addition_list = addition_list


    def derive(self):
        return [func.derive() for func in self.addition_list]

    def __str__(self):
        return "(" + " + ".join(str([str(func) for func in self.addition_list])) + ")"


    def __repr__(self):
        return f"Addition({self.addition_list})"

class Product(function):
    product_list: list[function, ...]

    def __init__(self, product_list):
        self.product_list = product_list

    def derive(self):
        curr = self.product_list[0]
        for function in self.product_list[1:]:
            curr = self.productRule(curr, function)
        return curr

    def productRule(self, first: function, second: function):
        return Addition([Product([first, second.derive()]), Product([first.derive(), second])])

    def __str__(self):
        return "(" + " * ".join([str(func) for func in self.product_list]) + ")"


    def __repr__(self):
        return f"Product({self.product_list})"


class Exponent(function):
    power: int

    def __init__(self, power):
        self.power = power

    def derive(self) -> function:
        return Product([Number(self.power), Exponent(self.power - 1)])

    def __str__(self):
        if self.power == 1:
            return "x"
        else:
            return "x^" + str(self.power)


    def __repr__(self):
        return f"Exponent({self.power})"


class Composition(function):
    parent: function
    child: function

    def __init__(self, parent: function, child: function):
        self.parent = parent
        self.child = child


    def derive(self):
        return Product([self.child.derive(), Composition(self.parent.derive(), self.child)])


    def __str__(self):
        return str(self.parent).replace("x", str(self.child))


    def __repr__(self):
        return f"Composition({self.parent.__repr__()}, {self.child.__repr__()})"

print(Composition(Exponent(2), Product([Number(2), Exponent(1)])).derive().__repr__())

#(2x)^2
