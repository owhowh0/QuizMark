# Generated from Quiz.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .QuizParser import QuizParser
else:
    from QuizParser import QuizParser

# This class defines a complete generic visitor for a parse tree produced by QuizParser.

class QuizVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by QuizParser#quiz.
    def visitQuiz(self, ctx:QuizParser.QuizContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#themeBlock.
    def visitThemeBlock(self, ctx:QuizParser.ThemeBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#themeStatement.
    def visitThemeStatement(self, ctx:QuizParser.ThemeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#selector.
    def visitSelector(self, ctx:QuizParser.SelectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#attributeList.
    def visitAttributeList(self, ctx:QuizParser.AttributeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#attribute.
    def visitAttribute(self, ctx:QuizParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#metadata.
    def visitMetadata(self, ctx:QuizParser.MetadataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#question.
    def visitQuestion(self, ctx:QuizParser.QuestionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#points.
    def visitPoints(self, ctx:QuizParser.PointsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#questionMedia.
    def visitQuestionMedia(self, ctx:QuizParser.QuestionMediaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#answer.
    def visitAnswer(self, ctx:QuizParser.AnswerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#answerContent.
    def visitAnswerContent(self, ctx:QuizParser.AnswerContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#image.
    def visitImage(self, ctx:QuizParser.ImageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#value.
    def visitValue(self, ctx:QuizParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuizParser#text.
    def visitText(self, ctx:QuizParser.TextContext):
        return self.visitChildren(ctx)



del QuizParser