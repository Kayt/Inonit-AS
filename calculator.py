" A Simple calculator Submission for Technical Interview"

HISTORY = []

class Calculator:
    """Calculator Class handling Basic arithmetic with History Function"""
    
    _stack = []

    # Flag that signfies if it's the first character in the expression
    INITIAL = True

    # exit perenthesis
    EXIST_PARENS = False
    # in number
    IN_NUM = False
    # in operator
    IN_OPERATOR = False

    OPERATORS = {
        '+': lambda x, y: x+y,
        '-': lambda x, y: x-y,
        '*': lambda x, y: x*y,
        '/': lambda x, y: x/y,
        '^': lambda x, y: x**y
    }

    OPS_ORDER = (('^',), ('*', '/'), ('+', '-'))

    def __int__(self):
        self._stack = []
        self.INITIAL = True

        self.EXIST_PARENS = False
        self.IN_NUM = False
        self.IN_OPERATOR = False

    class ErrorInvalidExpression(Exception):
        pass

    def parse(self, input_eq):
        """Method to handle infix arithmethic expressions to postfix eqv"""
        HISTORY.append(input_eq)
        for c in input_eq:
            try:
                # check if its a number
                current = int(c)
            except ValueError:
                # its not a number
                self.IN_NUM = False
                # if it's an operator
                if c in self.OPERATORS.keys():
                    if not self._stack:
                        raise ErrorInvalidExpression(
                            "You can't start an expression with an operator")

                    if self.IN_OPERATOR:
                        raise ErrorInValidExpression(
                            "More than one operator in a sequance")
                    else:
                        self._append_element(c)
                        self.IN_OPERATOR = True
                elif c == '(':
                    self._add_new_parentheses()
                    self.EXITS_PARENS = False
                elif c == ')':
                    self.EXIST_PARENS = True
                else:
                    raise ErrorInvalidExpression("Syntax Error")

                continue

            # runs when its a number

            self.IN_OPERATOR = False

            # add the number to the stack
            self._add_new_num(current)

            # if its a new number
            if not self.IN_NUM:
                self.IN_NUM = True

            if self.INITIAL:
                self.INITIAL = False

    def _get_last_position(self):
        """ Returns the last inner most list in the stack """

        list_ref = list_prev = self._stack
        try:
            # While there's a list
            while list_ref[-1] or list_ref[-1] == []:
                if isinstance(list_ref[-1], list):
                    # make a reference to the list
                    list_prev = list_ref
                    list_ref = list_ref[-1]
                else:
                    break
        except IndexError:
            pass

        if self.EXIST_PARENS == True:
            self.EXIST_PARENS = False
            return list_prev
        else:
            return list_ref

    def _append_element(self, el):
        last_pos = self._get_last_position()
        last_pos.append(el)

    def _add_new_num(self, num):
        # if its the first character in an expression
        if not self._stack or self._get_last_position() == []:
            self._append_element(num)
        else:
            prev_c = self._get_last_position()[-1]
            # check if previous char is a number
            is_int = isinstance(prev_c, int)

            if is_int:
                self._add_to_previous_num(num, self._stack)
            elif prev_c in self.OPERATORS.keys():
                self._append_element(num)
            else:
                is_list = isinstance(self._stack[-1], list)
                # if it's a list search the last element in the list's children
                if is_list:
                    list_ref = self._get_last_position()
                    self._add_to_previous_num(num, list_ref)
                else:
                    # this should never happen
                    raise Exception("A fatal error has occured")

    def _add_to_previous_num(self, num, stack):
        try:
            last_pos = self._get_last_position()
            last_pos[-1] = last_pos[-1]*10+num
        except IndexError:
            last_pos.append(num)

    def _add_new_parentheses(self):
        last_pos = self._get_last_position()
        last_pos.append([])

    def calculate(self, expr):
        self.parse(''.join(expr.split()))
        # do the actual calculation
        result = self._rec_calc(self._stack)
        # initialize the stack
        self._stack = []

        return result

    def _rec_calc(self, stack):
        while len(stack) > 1:
            for ops in self.OPS_ORDER:
                for el in range(len(stack)):
                    try:
                        if isinstance(stack[el], list):
                            result = self._rec_calc(stack[el])
                            del stack[el]
                            stack.insert(el, result)
                        elif stack[el] in ops:
                            result = self._calc_binary(stack, el)
                            # delete all three elements that were used in the binary operation
                            del stack[el-1]
                            del stack[el-1]
                            del stack[el-1]
                            stack.insert(el-1, result)
                    except IndexError:
                        break
                else:
                    continue
                break

        return stack[0]

    def _calc_binary(self, stack, index):
        op = stack[index]
        prev = stack[index-1]
        next = stack[index+1]

        for symbol, action in self.OPERATORS.items():
            if symbol == op:
                return action(prev, next)


if __name__ == '__main__':
    import sys

    calc = Calculator()

    if len(sys.argv) == 2:
        print(calc.calculate(sys.argv[1]))
        raise SystemExit(0)

    print(calc.calculate("1 + 1"))  # 124
    print(calc.calculate("2*32-4+456+(1+2)+3+(1/2*3+3+(1+2))"))
      # 528
    print(calc.calculate("2 * (7+1) / (2 + 5 + (10-9)) "))  # 2

    print(HISTORY)