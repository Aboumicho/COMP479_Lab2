

class QueryHandler:
    def __init__(self, query):
        self.query = query
        self.infix = ""
        self.operators = "&|"
        self.postfix = ""

    def getPrecedence(self, c):
        result = 0
        for char in self.operators:
            result += 1
        return result

    def toPostfix(self):
        result = ""
        stack = list()
        result = "" 
        result_final = ""
        temp = ""
        count = 0
        for char in self.query:
            
            if self.isOperand(char): 
                result += char
            elif self.isOperator(char):
                while True:
                    if len(stack)> 0:
                        topChar = stack[-1]

                    if len(stack) == 0 or topChar == '(':
                        stack.append(char)
                        break
                    else:
                        precedence_char = self.getPrecedence(char)
                        precedence_top_char = self.getPrecedence(topChar)

                        if precedence_char > precedence_top_char:
                            stack.append(char)
                            break
                        else:    
                            result += stack.pop()

            elif char == '(':
                stack.append(char)
            elif char == ")":
                cpop = stack.pop()
                while cpop != '(':
                    result +=cpop
                    cpop = stack.pop()

        while len(stack) > 0:
            cpop = stack.pop()
            result+=cpop
        
        return result

    def isOperand(self, char):
        return ((char >= 'A' and char <= 'Z') or (char >= 'a' and char <="z"))  
    def isOperator(self, char):
        return char in self.operators

test = QueryHandler("al & (va| sa)")
print(test.toPostfix())