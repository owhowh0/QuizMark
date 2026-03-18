# Generated from Quiz.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,27,136,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,1,0,1,0,1,0,3,0,34,8,0,1,0,5,0,37,8,0,10,0,12,0,40,9,0,
        1,0,4,0,43,8,0,11,0,12,0,44,1,0,1,0,1,1,1,1,1,1,4,1,52,8,1,11,1,
        12,1,53,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,66,8,2,1,3,1,
        3,1,4,1,4,1,4,5,4,73,8,4,10,4,12,4,76,9,4,1,5,1,5,1,5,1,5,1,6,1,
        6,1,6,1,6,1,6,3,6,87,8,6,1,7,1,7,3,7,91,8,7,1,7,1,7,1,7,3,7,96,8,
        7,1,7,4,7,99,8,7,11,7,12,7,100,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,10,
        1,10,1,10,1,10,3,10,114,8,10,1,11,1,11,3,11,118,8,11,1,11,3,11,121,
        8,11,1,12,1,12,1,12,3,12,126,8,12,1,13,1,13,1,13,1,13,3,13,132,8,
        13,1,14,1,14,1,14,0,0,15,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,
        0,2,1,0,8,12,2,0,23,23,26,26,138,0,30,1,0,0,0,2,48,1,0,0,0,4,65,
        1,0,0,0,6,67,1,0,0,0,8,69,1,0,0,0,10,77,1,0,0,0,12,81,1,0,0,0,14,
        88,1,0,0,0,16,102,1,0,0,0,18,107,1,0,0,0,20,109,1,0,0,0,22,120,1,
        0,0,0,24,122,1,0,0,0,26,131,1,0,0,0,28,133,1,0,0,0,30,31,5,1,0,0,
        31,33,3,28,14,0,32,34,3,2,1,0,33,32,1,0,0,0,33,34,1,0,0,0,34,38,
        1,0,0,0,35,37,3,12,6,0,36,35,1,0,0,0,37,40,1,0,0,0,38,36,1,0,0,0,
        38,39,1,0,0,0,39,42,1,0,0,0,40,38,1,0,0,0,41,43,3,14,7,0,42,41,1,
        0,0,0,43,44,1,0,0,0,44,42,1,0,0,0,44,45,1,0,0,0,45,46,1,0,0,0,46,
        47,5,0,0,1,47,1,1,0,0,0,48,49,5,2,0,0,49,51,5,3,0,0,50,52,3,4,2,
        0,51,50,1,0,0,0,52,53,1,0,0,0,53,51,1,0,0,0,53,54,1,0,0,0,54,55,
        1,0,0,0,55,56,5,4,0,0,56,3,1,0,0,0,57,58,5,23,0,0,58,59,5,5,0,0,
        59,66,3,26,13,0,60,61,3,6,3,0,61,62,5,6,0,0,62,63,3,8,4,0,63,64,
        5,7,0,0,64,66,1,0,0,0,65,57,1,0,0,0,65,60,1,0,0,0,66,5,1,0,0,0,67,
        68,7,0,0,0,68,7,1,0,0,0,69,74,3,10,5,0,70,71,5,13,0,0,71,73,3,10,
        5,0,72,70,1,0,0,0,73,76,1,0,0,0,74,72,1,0,0,0,74,75,1,0,0,0,75,9,
        1,0,0,0,76,74,1,0,0,0,77,78,5,23,0,0,78,79,5,5,0,0,79,80,3,26,13,
        0,80,11,1,0,0,0,81,82,5,23,0,0,82,86,5,14,0,0,83,87,3,28,14,0,84,
        87,5,24,0,0,85,87,5,22,0,0,86,83,1,0,0,0,86,84,1,0,0,0,86,85,1,0,
        0,0,87,13,1,0,0,0,88,90,5,15,0,0,89,91,3,16,8,0,90,89,1,0,0,0,90,
        91,1,0,0,0,91,92,1,0,0,0,92,93,5,14,0,0,93,95,3,28,14,0,94,96,3,
        18,9,0,95,94,1,0,0,0,95,96,1,0,0,0,96,98,1,0,0,0,97,99,3,20,10,0,
        98,97,1,0,0,0,99,100,1,0,0,0,100,98,1,0,0,0,100,101,1,0,0,0,101,
        15,1,0,0,0,102,103,5,16,0,0,103,104,5,17,0,0,104,105,5,24,0,0,105,
        106,5,18,0,0,106,17,1,0,0,0,107,108,3,24,12,0,108,19,1,0,0,0,109,
        110,5,20,0,0,110,111,5,14,0,0,111,113,3,22,11,0,112,114,5,21,0,0,
        113,112,1,0,0,0,113,114,1,0,0,0,114,21,1,0,0,0,115,117,3,28,14,0,
        116,118,3,24,12,0,117,116,1,0,0,0,117,118,1,0,0,0,118,121,1,0,0,
        0,119,121,3,24,12,0,120,115,1,0,0,0,120,119,1,0,0,0,121,23,1,0,0,
        0,122,125,5,19,0,0,123,126,5,25,0,0,124,126,3,28,14,0,125,123,1,
        0,0,0,125,124,1,0,0,0,126,25,1,0,0,0,127,132,5,25,0,0,128,132,3,
        28,14,0,129,132,5,24,0,0,130,132,5,22,0,0,131,127,1,0,0,0,131,128,
        1,0,0,0,131,129,1,0,0,0,131,130,1,0,0,0,132,27,1,0,0,0,133,134,7,
        1,0,0,134,29,1,0,0,0,15,33,38,44,53,65,74,86,90,95,100,113,117,120,
        125,131
    ]

class QuizParser ( Parser ):

    grammarFileName = "Quiz.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'QUIZ:'", "'THEME'", "'{'", "'}'", "'='", 
                     "'['", "']'", "'quiz'", "'question'", "'answer'", "'correct'", 
                     "'wrong'", "','", "':'", "'QUESTION'", "'('", "'points='", 
                     "')'", "'IMAGE:'", "<INVALID>", "'*'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "OPTION_LABEL", "CORRECT_MARKER", "BOOLEAN", "IDENTIFIER", 
                      "NUMBER", "STRING_LITERAL", "TEXT_CONTENT", "WS" ]

    RULE_quiz = 0
    RULE_themeBlock = 1
    RULE_themeStatement = 2
    RULE_selector = 3
    RULE_attributeList = 4
    RULE_attribute = 5
    RULE_metadata = 6
    RULE_question = 7
    RULE_points = 8
    RULE_questionMedia = 9
    RULE_answer = 10
    RULE_answerContent = 11
    RULE_image = 12
    RULE_value = 13
    RULE_text = 14

    ruleNames =  [ "quiz", "themeBlock", "themeStatement", "selector", "attributeList", 
                   "attribute", "metadata", "question", "points", "questionMedia", 
                   "answer", "answerContent", "image", "value", "text" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    OPTION_LABEL=20
    CORRECT_MARKER=21
    BOOLEAN=22
    IDENTIFIER=23
    NUMBER=24
    STRING_LITERAL=25
    TEXT_CONTENT=26
    WS=27

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class QuizContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def text(self):
            return self.getTypedRuleContext(QuizParser.TextContext,0)


        def EOF(self):
            return self.getToken(QuizParser.EOF, 0)

        def themeBlock(self):
            return self.getTypedRuleContext(QuizParser.ThemeBlockContext,0)


        def metadata(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QuizParser.MetadataContext)
            else:
                return self.getTypedRuleContext(QuizParser.MetadataContext,i)


        def question(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QuizParser.QuestionContext)
            else:
                return self.getTypedRuleContext(QuizParser.QuestionContext,i)


        def getRuleIndex(self):
            return QuizParser.RULE_quiz

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuiz" ):
                listener.enterQuiz(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuiz" ):
                listener.exitQuiz(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuiz" ):
                return visitor.visitQuiz(self)
            else:
                return visitor.visitChildren(self)




    def quiz(self):

        localctx = QuizParser.QuizContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_quiz)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(QuizParser.T__0)
            self.state = 31
            self.text()
            self.state = 33
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==2:
                self.state = 32
                self.themeBlock()


            self.state = 38
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==23:
                self.state = 35
                self.metadata()
                self.state = 40
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 42 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 41
                self.question()
                self.state = 44 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==15):
                    break

            self.state = 46
            self.match(QuizParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ThemeBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def themeStatement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QuizParser.ThemeStatementContext)
            else:
                return self.getTypedRuleContext(QuizParser.ThemeStatementContext,i)


        def getRuleIndex(self):
            return QuizParser.RULE_themeBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterThemeBlock" ):
                listener.enterThemeBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitThemeBlock" ):
                listener.exitThemeBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitThemeBlock" ):
                return visitor.visitThemeBlock(self)
            else:
                return visitor.visitChildren(self)




    def themeBlock(self):

        localctx = QuizParser.ThemeBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_themeBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            self.match(QuizParser.T__1)
            self.state = 49
            self.match(QuizParser.T__2)
            self.state = 51 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 50
                self.themeStatement()
                self.state = 53 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 8396544) != 0)):
                    break

            self.state = 55
            self.match(QuizParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ThemeStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(QuizParser.IDENTIFIER, 0)

        def value(self):
            return self.getTypedRuleContext(QuizParser.ValueContext,0)


        def selector(self):
            return self.getTypedRuleContext(QuizParser.SelectorContext,0)


        def attributeList(self):
            return self.getTypedRuleContext(QuizParser.AttributeListContext,0)


        def getRuleIndex(self):
            return QuizParser.RULE_themeStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterThemeStatement" ):
                listener.enterThemeStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitThemeStatement" ):
                listener.exitThemeStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitThemeStatement" ):
                return visitor.visitThemeStatement(self)
            else:
                return visitor.visitChildren(self)




    def themeStatement(self):

        localctx = QuizParser.ThemeStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_themeStatement)
        try:
            self.state = 65
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.match(QuizParser.IDENTIFIER)
                self.state = 58
                self.match(QuizParser.T__4)
                self.state = 59
                self.value()
                pass
            elif token in [8, 9, 10, 11, 12]:
                self.enterOuterAlt(localctx, 2)
                self.state = 60
                self.selector()
                self.state = 61
                self.match(QuizParser.T__5)
                self.state = 62
                self.attributeList()
                self.state = 63
                self.match(QuizParser.T__6)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return QuizParser.RULE_selector

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelector" ):
                listener.enterSelector(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelector" ):
                listener.exitSelector(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelector" ):
                return visitor.visitSelector(self)
            else:
                return visitor.visitChildren(self)




    def selector(self):

        localctx = QuizParser.SelectorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_selector)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 7936) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def attribute(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QuizParser.AttributeContext)
            else:
                return self.getTypedRuleContext(QuizParser.AttributeContext,i)


        def getRuleIndex(self):
            return QuizParser.RULE_attributeList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttributeList" ):
                listener.enterAttributeList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttributeList" ):
                listener.exitAttributeList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttributeList" ):
                return visitor.visitAttributeList(self)
            else:
                return visitor.visitChildren(self)




    def attributeList(self):

        localctx = QuizParser.AttributeListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_attributeList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.attribute()
            self.state = 74
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 70
                self.match(QuizParser.T__12)
                self.state = 71
                self.attribute()
                self.state = 76
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(QuizParser.IDENTIFIER, 0)

        def value(self):
            return self.getTypedRuleContext(QuizParser.ValueContext,0)


        def getRuleIndex(self):
            return QuizParser.RULE_attribute

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttribute" ):
                listener.enterAttribute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttribute" ):
                listener.exitAttribute(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttribute" ):
                return visitor.visitAttribute(self)
            else:
                return visitor.visitChildren(self)




    def attribute(self):

        localctx = QuizParser.AttributeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_attribute)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self.match(QuizParser.IDENTIFIER)
            self.state = 78
            self.match(QuizParser.T__4)
            self.state = 79
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MetadataContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(QuizParser.IDENTIFIER, 0)

        def text(self):
            return self.getTypedRuleContext(QuizParser.TextContext,0)


        def NUMBER(self):
            return self.getToken(QuizParser.NUMBER, 0)

        def BOOLEAN(self):
            return self.getToken(QuizParser.BOOLEAN, 0)

        def getRuleIndex(self):
            return QuizParser.RULE_metadata

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMetadata" ):
                listener.enterMetadata(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMetadata" ):
                listener.exitMetadata(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMetadata" ):
                return visitor.visitMetadata(self)
            else:
                return visitor.visitChildren(self)




    def metadata(self):

        localctx = QuizParser.MetadataContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_metadata)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.match(QuizParser.IDENTIFIER)
            self.state = 82
            self.match(QuizParser.T__13)
            self.state = 86
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23, 26]:
                self.state = 83
                self.text()
                pass
            elif token in [24]:
                self.state = 84
                self.match(QuizParser.NUMBER)
                pass
            elif token in [22]:
                self.state = 85
                self.match(QuizParser.BOOLEAN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuestionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def text(self):
            return self.getTypedRuleContext(QuizParser.TextContext,0)


        def points(self):
            return self.getTypedRuleContext(QuizParser.PointsContext,0)


        def questionMedia(self):
            return self.getTypedRuleContext(QuizParser.QuestionMediaContext,0)


        def answer(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QuizParser.AnswerContext)
            else:
                return self.getTypedRuleContext(QuizParser.AnswerContext,i)


        def getRuleIndex(self):
            return QuizParser.RULE_question

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuestion" ):
                listener.enterQuestion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuestion" ):
                listener.exitQuestion(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuestion" ):
                return visitor.visitQuestion(self)
            else:
                return visitor.visitChildren(self)




    def question(self):

        localctx = QuizParser.QuestionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_question)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self.match(QuizParser.T__14)
            self.state = 90
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 89
                self.points()


            self.state = 92
            self.match(QuizParser.T__13)
            self.state = 93
            self.text()
            self.state = 95
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==19:
                self.state = 94
                self.questionMedia()


            self.state = 98 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 97
                self.answer()
                self.state = 100 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==20):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PointsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(QuizParser.NUMBER, 0)

        def getRuleIndex(self):
            return QuizParser.RULE_points

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPoints" ):
                listener.enterPoints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPoints" ):
                listener.exitPoints(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPoints" ):
                return visitor.visitPoints(self)
            else:
                return visitor.visitChildren(self)




    def points(self):

        localctx = QuizParser.PointsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_points)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.match(QuizParser.T__15)
            self.state = 103
            self.match(QuizParser.T__16)
            self.state = 104
            self.match(QuizParser.NUMBER)
            self.state = 105
            self.match(QuizParser.T__17)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuestionMediaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def image(self):
            return self.getTypedRuleContext(QuizParser.ImageContext,0)


        def getRuleIndex(self):
            return QuizParser.RULE_questionMedia

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuestionMedia" ):
                listener.enterQuestionMedia(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuestionMedia" ):
                listener.exitQuestionMedia(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuestionMedia" ):
                return visitor.visitQuestionMedia(self)
            else:
                return visitor.visitChildren(self)




    def questionMedia(self):

        localctx = QuizParser.QuestionMediaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_questionMedia)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.image()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnswerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OPTION_LABEL(self):
            return self.getToken(QuizParser.OPTION_LABEL, 0)

        def answerContent(self):
            return self.getTypedRuleContext(QuizParser.AnswerContentContext,0)


        def CORRECT_MARKER(self):
            return self.getToken(QuizParser.CORRECT_MARKER, 0)

        def getRuleIndex(self):
            return QuizParser.RULE_answer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnswer" ):
                listener.enterAnswer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnswer" ):
                listener.exitAnswer(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnswer" ):
                return visitor.visitAnswer(self)
            else:
                return visitor.visitChildren(self)




    def answer(self):

        localctx = QuizParser.AnswerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_answer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 109
            self.match(QuizParser.OPTION_LABEL)
            self.state = 110
            self.match(QuizParser.T__13)
            self.state = 111
            self.answerContent()
            self.state = 113
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==21:
                self.state = 112
                self.match(QuizParser.CORRECT_MARKER)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnswerContentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def text(self):
            return self.getTypedRuleContext(QuizParser.TextContext,0)


        def image(self):
            return self.getTypedRuleContext(QuizParser.ImageContext,0)


        def getRuleIndex(self):
            return QuizParser.RULE_answerContent

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnswerContent" ):
                listener.enterAnswerContent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnswerContent" ):
                listener.exitAnswerContent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnswerContent" ):
                return visitor.visitAnswerContent(self)
            else:
                return visitor.visitChildren(self)




    def answerContent(self):

        localctx = QuizParser.AnswerContentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_answerContent)
        self._la = 0 # Token type
        try:
            self.state = 120
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23, 26]:
                self.enterOuterAlt(localctx, 1)
                self.state = 115
                self.text()
                self.state = 117
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==19:
                    self.state = 116
                    self.image()


                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 2)
                self.state = 119
                self.image()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImageContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_LITERAL(self):
            return self.getToken(QuizParser.STRING_LITERAL, 0)

        def text(self):
            return self.getTypedRuleContext(QuizParser.TextContext,0)


        def getRuleIndex(self):
            return QuizParser.RULE_image

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImage" ):
                listener.enterImage(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImage" ):
                listener.exitImage(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImage" ):
                return visitor.visitImage(self)
            else:
                return visitor.visitChildren(self)




    def image(self):

        localctx = QuizParser.ImageContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_image)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 122
            self.match(QuizParser.T__18)
            self.state = 125
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [25]:
                self.state = 123
                self.match(QuizParser.STRING_LITERAL)
                pass
            elif token in [23, 26]:
                self.state = 124
                self.text()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_LITERAL(self):
            return self.getToken(QuizParser.STRING_LITERAL, 0)

        def text(self):
            return self.getTypedRuleContext(QuizParser.TextContext,0)


        def NUMBER(self):
            return self.getToken(QuizParser.NUMBER, 0)

        def BOOLEAN(self):
            return self.getToken(QuizParser.BOOLEAN, 0)

        def getRuleIndex(self):
            return QuizParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = QuizParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_value)
        try:
            self.state = 131
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [25]:
                self.enterOuterAlt(localctx, 1)
                self.state = 127
                self.match(QuizParser.STRING_LITERAL)
                pass
            elif token in [23, 26]:
                self.enterOuterAlt(localctx, 2)
                self.state = 128
                self.text()
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 3)
                self.state = 129
                self.match(QuizParser.NUMBER)
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 4)
                self.state = 130
                self.match(QuizParser.BOOLEAN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(QuizParser.IDENTIFIER, 0)

        def TEXT_CONTENT(self):
            return self.getToken(QuizParser.TEXT_CONTENT, 0)

        def getRuleIndex(self):
            return QuizParser.RULE_text

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterText" ):
                listener.enterText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitText" ):
                listener.exitText(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitText" ):
                return visitor.visitText(self)
            else:
                return visitor.visitChildren(self)




    def text(self):

        localctx = QuizParser.TextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_text)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 133
            _la = self._input.LA(1)
            if not(_la==23 or _la==26):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





