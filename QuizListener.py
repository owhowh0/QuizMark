# Generated from Quiz.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .QuizParser import QuizParser
else:
    from QuizParser import QuizParser

# This class defines a complete listener for a parse tree produced by QuizParser.
class QuizListener(ParseTreeListener):

    # Enter a parse tree produced by QuizParser#quiz.
    def enterQuiz(self, ctx:QuizParser.QuizContext):
        pass

    # Exit a parse tree produced by QuizParser#quiz.
    def exitQuiz(self, ctx:QuizParser.QuizContext):
        pass


    # Enter a parse tree produced by QuizParser#themeBlock.
    def enterThemeBlock(self, ctx:QuizParser.ThemeBlockContext):
        pass

    # Exit a parse tree produced by QuizParser#themeBlock.
    def exitThemeBlock(self, ctx:QuizParser.ThemeBlockContext):
        pass


    # Enter a parse tree produced by QuizParser#themeStatement.
    def enterThemeStatement(self, ctx:QuizParser.ThemeStatementContext):
        pass

    # Exit a parse tree produced by QuizParser#themeStatement.
    def exitThemeStatement(self, ctx:QuizParser.ThemeStatementContext):
        pass


    # Enter a parse tree produced by QuizParser#selector.
    def enterSelector(self, ctx:QuizParser.SelectorContext):
        pass

    # Exit a parse tree produced by QuizParser#selector.
    def exitSelector(self, ctx:QuizParser.SelectorContext):
        pass


    # Enter a parse tree produced by QuizParser#attributeList.
    def enterAttributeList(self, ctx:QuizParser.AttributeListContext):
        pass

    # Exit a parse tree produced by QuizParser#attributeList.
    def exitAttributeList(self, ctx:QuizParser.AttributeListContext):
        pass


    # Enter a parse tree produced by QuizParser#attribute.
    def enterAttribute(self, ctx:QuizParser.AttributeContext):
        pass

    # Exit a parse tree produced by QuizParser#attribute.
    def exitAttribute(self, ctx:QuizParser.AttributeContext):
        pass


    # Enter a parse tree produced by QuizParser#metadata.
    def enterMetadata(self, ctx:QuizParser.MetadataContext):
        pass

    # Exit a parse tree produced by QuizParser#metadata.
    def exitMetadata(self, ctx:QuizParser.MetadataContext):
        pass


    # Enter a parse tree produced by QuizParser#question.
    def enterQuestion(self, ctx:QuizParser.QuestionContext):
        pass

    # Exit a parse tree produced by QuizParser#question.
    def exitQuestion(self, ctx:QuizParser.QuestionContext):
        pass


    # Enter a parse tree produced by QuizParser#points.
    def enterPoints(self, ctx:QuizParser.PointsContext):
        pass

    # Exit a parse tree produced by QuizParser#points.
    def exitPoints(self, ctx:QuizParser.PointsContext):
        pass


    # Enter a parse tree produced by QuizParser#questionMedia.
    def enterQuestionMedia(self, ctx:QuizParser.QuestionMediaContext):
        pass

    # Exit a parse tree produced by QuizParser#questionMedia.
    def exitQuestionMedia(self, ctx:QuizParser.QuestionMediaContext):
        pass


    # Enter a parse tree produced by QuizParser#answer.
    def enterAnswer(self, ctx:QuizParser.AnswerContext):
        pass

    # Exit a parse tree produced by QuizParser#answer.
    def exitAnswer(self, ctx:QuizParser.AnswerContext):
        pass


    # Enter a parse tree produced by QuizParser#answerContent.
    def enterAnswerContent(self, ctx:QuizParser.AnswerContentContext):
        pass

    # Exit a parse tree produced by QuizParser#answerContent.
    def exitAnswerContent(self, ctx:QuizParser.AnswerContentContext):
        pass


    # Enter a parse tree produced by QuizParser#image.
    def enterImage(self, ctx:QuizParser.ImageContext):
        pass

    # Exit a parse tree produced by QuizParser#image.
    def exitImage(self, ctx:QuizParser.ImageContext):
        pass


    # Enter a parse tree produced by QuizParser#value.
    def enterValue(self, ctx:QuizParser.ValueContext):
        pass

    # Exit a parse tree produced by QuizParser#value.
    def exitValue(self, ctx:QuizParser.ValueContext):
        pass


    # Enter a parse tree produced by QuizParser#text.
    def enterText(self, ctx:QuizParser.TextContext):
        pass

    # Exit a parse tree produced by QuizParser#text.
    def exitText(self, ctx:QuizParser.TextContext):
        pass



del QuizParser