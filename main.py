class function:
    def derive(self):
        raise NotImplementedError

    def simplify(self):
        return self


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

    def __eq__(self, other):
        if isinstance(other, int):
            return self.number == other
        elif isinstance(other,Number):
            return self.number == other.number




class Addition(function):
    addition_list: list[function,...]
    def __init__(self, addition_list):
        self.addition_list = addition_list

    def simplify(self):
        new=[]
        num=0
        for i in self.addition_list:
            i=i.simplify()
            if isinstance(i,Addition):
                for j in i.addition_list:
                    if isinstance(j,Number):
                        num+=j.number
                    else:
                        new.append(j)
            elif isinstance(i,Number):
                num+=i.number
            else:
                new.append(i)
        if num!=0:
            new.insert(0,Number(num))
        if len(new)==1:
            return new[0]
        return Addition(new)


    def derive(self):
        return Addition([func.derive() for func in self.addition_list])

    def __str__(self):
        return "(" + "+".join([str(func) for func in self.addition_list]) + ")"


    def __repr__(self):
        return f"Addition({self.addition_list})"

class Product(function):
    product_list: list[function, ...]

    def __init__(self, product_list):
        self.product_list = product_list

    def simplify(self):
        new = []
        num = 1
        for i in self.product_list:
            i=i.simplify()
            if isinstance(i,Product):
                for j in i.product_list:
                    if isinstance(j,Number):
                        num*=j.number
                    else:
                        new.append(j)
            elif isinstance(i,Number):
                num*=i.number
            else:
                new.append(i)
        if num==0:
            return Number(0)
        elif num!=1:
            new.insert(0,Number(num))
        if len(new)==1:
            return new[0]
        return Product(new)
    def derive(self):
        curr = self.product_list[0]
        for function in self.product_list[1:]:
            curr = self.productRule(curr, function)
        return curr

    def productRule(self, first: function, second: function):
        return Addition([Product([first, second.derive()]), Product([first.derive(), second])])

    def __str__(self):
        return "(" + "*".join([str(func) for func in self.product_list]) + ")"


    def __repr__(self):
        return f"Product({self.product_list})"


class Exponent(function):
    power: function
    base: function

    def __init__(self, power, base):
        self.power = power
        self.base = base

    def simplify(self):
        self.power=self.power.simplify()
        self.base=self.base.simplify()
        if self.power==1:
            return self.base
        elif self.power==0:
            return Number(1)
        elif self.base==1:
            return Number(1)
        elif self.base==0:
            return Number(0)
        return self
    def derive(self) -> function:
        return Product([Exponent(self.power,self.base), Addition([Product([self.power.derive(),self.base]), Product([self.power,self.base.derive(),Exponent(Number(-1),self.base)])])])

    def __str__(self):
        if self.power==1:
            return str(self.base)
        else:
            return f'{self.base}^{self.power}'

    def __repr__(self):
        return f"Exponent({self.power},{self.base})"

class VarX(function):
    def derive(self) -> function:
        return Number(1)

    def __str__(self):
        return 'x'

    def __repr__(self):
        return 'VarX()'

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

test=Exponent(VarX(),VarX())
print(repr(test.derive()))
print(test)
print(repr(test.derive().simplify()))
print(test.derive().simplify())
#print(Product([VarX(),Number(2)]).simplify())

#(2x)^2
