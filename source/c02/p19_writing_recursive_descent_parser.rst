============================
2.19 实现一个简单的递归下降分析器
============================

----------
问题
----------
你想根据一组语法规则解析文本并执行命令，或者构造一个代表输入的抽象语法树。
语法非常简单，所以你可以自己写这个解析器，而不是使用一些框架。

|

----------
解决方案
----------
在这个问题中，我们集中讨论根据特殊语法去解析文本的问题。
为了这样做，你首先要以BNF或者EBNF形式指定一个标准语法。
比如，一个简单数学表达式语法可能像下面这样：

.. code-block:: python

    expr ::= expr + term
        |   expr - term
        |   term

    term ::= term * factor
        |   term / factor
        |   factor

    factor ::= ( expr )
        |   NUM

或者，以EBNF形式：

.. code-block:: python

    expr ::= term { (+|-) term }*

    term ::= factor { (*|/) factor }*

    factor ::= ( expr )
        |   NUM

在EBNF中，被包含在{...}*中的规则是可选的。*代表0次或多次重复(跟正则表达式中意义是一样的)。

现在，如果你对BNF的工作机制还不是很明白的话，就把它当做是一组左右符号可相互替换的规则。
一般来讲，解析的原理就是你通过利用BNF完成多个替换和扩展以匹配输入文本和语法规则。
为了演示，假设你正在解析形如3 + 4 * 5的表达式。
这个表达式先要通过使用2.18节中介绍的技术分解为一组令牌流。
结果可能是像下列这样的令牌序列：

.. code-block:: python

    NUM + NUM * NUM

From there, parsing involves trying to match the grammar to input tokens by making
substitutions:
在此基础上， 解析动作会试着去通过替换操作匹配语法到输入令牌：

.. code-block:: python

    expr
    expr ::= term { (+|-) term }*
    expr ::= factor { (*|/) factor }* { (+|-) term }*
    expr ::= NUM { (*|/) factor }* { (+|-) term }*
    expr ::= NUM { (+|-) term }*
    expr ::= NUM + term { (+|-) term }*
    expr ::= NUM + factor { (*|/) factor }* { (+|-) term }*
    expr ::= NUM + NUM { (*|/) factor}* { (+|-) term }*
    expr ::= NUM + NUM * factor { (*|/) factor }* { (+|-) term }*
    expr ::= NUM + NUM * NUM { (*|/) factor }* { (+|-) term }*
    expr ::= NUM + NUM * NUM { (+|-) term }*
    expr ::= NUM + NUM * NUM

下面所有的解析步骤可能需要花点时间弄明白，但是它们原理都是查找输入并试着去匹配语法规则。
第一个输入令牌是NUM，因此替换首先会匹配那个部分。
一旦匹配成功，就会进入下一个令牌+，以此类推。
当已经确定不能匹配下一个令牌的时候，右边的部分(比如{ (*/) factor }*)就会被清理掉。
在一个成功的解析中，整个右边部分会完全展开来匹配输入令牌流。

有了前面的知识背景，下面我们举一个简单示例来展示如何构建一个递归下降表达式求值程序：

.. code-block:: python

    #!/usr/bin/env python
    # -*- encoding: utf-8 -*-
    """
    Topic: 下降解析器
    Desc :
    """
    import re
    import collections

    # Token specification
    NUM = r'(?P<NUM>\d+)'
    PLUS = r'(?P<PLUS>\+)'
    MINUS = r'(?P<MINUS>-)'
    TIMES = r'(?P<TIMES>\*)'
    DIVIDE = r'(?P<DIVIDE>/)'
    LPAREN = r'(?P<LPAREN>\()'
    RPAREN = r'(?P<RPAREN>\))'
    WS = r'(?P<WS>\s+)'

    master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES,
                                      DIVIDE, LPAREN, RPAREN, WS]))
    # Tokenizer
    Token = collections.namedtuple('Token', ['type', 'value'])


    def generate_tokens(text):
        scanner = master_pat.scanner(text)
        for m in iter(scanner.match, None):
            tok = Token(m.lastgroup, m.group())
            if tok.type != 'WS':
                yield tok


    # Parser
    class ExpressionEvaluator:
        '''
        Implementation of a recursive descent parser. Each method
        implements a single grammar rule. Use the ._accept() method
        to test and accept the current lookahead token. Use the ._expect()
        method to exactly match and discard the next token on on the input
        (or raise a SyntaxError if it doesn't match).
        '''

        def parse(self, text):
            self.tokens = generate_tokens(text)
            self.tok = None  # Last symbol consumed
            self.nexttok = None  # Next symbol tokenized
            self._advance()  # Load first lookahead token
            return self.expr()

        def _advance(self):
            'Advance one token ahead'
            self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

        def _accept(self, toktype):
            'Test and consume the next token if it matches toktype'
            if self.nexttok and self.nexttok.type == toktype:
                self._advance()
                return True
            else:
                return False

        def _expect(self, toktype):
            'Consume next token if it matches toktype or raise SyntaxError'
            if not self._accept(toktype):
                raise SyntaxError('Expected ' + toktype)

        # Grammar rules follow
        def expr(self):
            "expression ::= term { ('+'|'-') term }*"
            exprval = self.term()
            while self._accept('PLUS') or self._accept('MINUS'):
                op = self.tok.type
                right = self.term()
                if op == 'PLUS':
                    exprval += right
                elif op == 'MINUS':
                    exprval -= right
            return exprval

        def term(self):
            "term ::= factor { ('*'|'/') factor }*"
            termval = self.factor()
            while self._accept('TIMES') or self._accept('DIVIDE'):
                op = self.tok.type
                right = self.factor()
                if op == 'TIMES':
                    termval *= right
                elif op == 'DIVIDE':
                    termval /= right
            return termval

        def factor(self):
            "factor ::= NUM | ( expr )"
            if self._accept('NUM'):
                return int(self.tok.value)
            elif self._accept('LPAREN'):
                exprval = self.expr()
                self._expect('RPAREN')
                return exprval
            else:
                raise SyntaxError('Expected NUMBER or LPAREN')


    def descent_parser():
        e = ExpressionEvaluator()
        print(e.parse('2'))
        print(e.parse('2 + 3'))
        print(e.parse('2 + 3 * 4'))
        print(e.parse('2 + (3 + 4) * 5'))
        # print(e.parse('2 + (3 + * 4)'))
        # Traceback (most recent call last):
        #    File "<stdin>", line 1, in <module>
        #    File "exprparse.py", line 40, in parse
        #    return self.expr()
        #    File "exprparse.py", line 67, in expr
        #    right = self.term()
        #    File "exprparse.py", line 77, in term
        #    termval = self.factor()
        #    File "exprparse.py", line 93, in factor
        #    exprval = self.expr()
        #    File "exprparse.py", line 67, in expr
        #    right = self.term()
        #    File "exprparse.py", line 77, in term
        #    termval = self.factor()
        #    File "exprparse.py", line 97, in factor
        #    raise SyntaxError("Expected NUMBER or LPAREN")
        #    SyntaxError: Expected NUMBER or LPAREN


    if __name__ == '__main__':
        descent_parser()

|

----------
讨论
----------
文本解析是一个很大的主题， 一般会占用学生学习编译课程时刚开始的三周时间。
如果你在找寻关于语法，解析算法等相关的背景知识的话，你应该去看一下编译器书籍。
很显然，关于这方面的内容太多，不可能在这里全部展开。

尽管如此，编写一个迭代下降解析器的整体思路是比较简单的。
开始的时候，你先获得所有的语法规则，然后将其转换为一个函数或者方法。
因此如果你的语法类似这样：

.. code-block:: python

    expr ::= term { ('+'|'-') term }*

    term ::= factor { ('*'|'/') factor }*

    factor ::= '(' expr ')'
        | NUM

你应该首先将它们转换成一组像下面这样的方法：

.. code-block:: python

    class ExpressionEvaluator:
        ...
        def expr(self):
        ...
        def term(self):
        ...
        def factor(self):
        ...

The task of each method is simple—it must walk from left to right over each part of the
grammar rule, consuming tokens in the process. In a sense, the goal of the method is
to either consume the rule or generate a syntax error if it gets stuck. To do this, the
following implementation techniques are applied:

*