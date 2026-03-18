from QuizVisitor import QuizVisitor
from QuizParser import QuizParser
from models import AnswerData, QuestionData, ThemeData, QuizData


class QuizVisitorImpl(QuizVisitor):
    """
    Concrete visitor that builds the QuizData model from the parse tree.
    Every visit* method corresponds directly to a rule in Quiz.g4 and
    returns a typed value instead of delegating to visitChildren.
    """

    # ── quiz ─────────────────────────────────────────────────────────────────

    def visitQuiz(self, ctx: QuizParser.QuizContext) -> QuizData:
        title = self.visitText(ctx.text())
        theme = self.visitThemeBlock(ctx.themeBlock()) if ctx.themeBlock() else None
        metadata = dict(self.visitMetadata(m) for m in ctx.metadata())
        questions = [self.visitQuestion(q) for q in ctx.question()]
        return QuizData(title=title, theme=theme, metadata=metadata, questions=questions)

    # ── theme ─────────────────────────────────────────────────────────────────

    def visitThemeBlock(self, ctx: QuizParser.ThemeBlockContext) -> ThemeData:
        theme = ThemeData()
        for stmt in ctx.themeStatement():
            self.visitThemeStatement(stmt, theme)
        return theme

    def visitThemeStatement(self, ctx: QuizParser.ThemeStatementContext, theme: ThemeData = None):
        # Alt 1:  IDENTIFIER '=' value
        if ctx.IDENTIFIER() and ctx.value():
            key = ctx.IDENTIFIER().getText()
            val = self.visitValue(ctx.value())
            if theme is not None:
                theme.properties[key] = val
            return key, val
        # Alt 2:  selector '[' attributeList ']'
        if ctx.selector() and ctx.attributeList():
            sel = self.visitSelector(ctx.selector())
            attrs = self.visitAttributeList(ctx.attributeList())
            if theme is not None:
                theme.styles[sel] = attrs
            return sel, attrs

    def visitSelector(self, ctx: QuizParser.SelectorContext) -> str:
        return ctx.getText()

    def visitAttributeList(self, ctx: QuizParser.AttributeListContext) -> dict:
        return dict(self.visitAttribute(a) for a in ctx.attribute())

    def visitAttribute(self, ctx: QuizParser.AttributeContext) -> tuple:
        key = ctx.IDENTIFIER().getText()
        val = self.visitValue(ctx.value())
        return key, val

    # ── metadata ──────────────────────────────────────────────────────────────

    def visitMetadata(self, ctx: QuizParser.MetadataContext) -> tuple:
        key = ctx.IDENTIFIER().getText()
        if ctx.NUMBER():
            raw = ctx.NUMBER().getText().rstrip('%')
            val = float(raw) if '.' in raw else int(raw)
        elif ctx.BOOLEAN():
            val = ctx.BOOLEAN().getText() == 'true'
        else:
            val = self.visitText(ctx.text())
        return key, val

    # ── question ──────────────────────────────────────────────────────────────

    def visitQuestion(self, ctx: QuizParser.QuestionContext) -> QuestionData:
        text = self.visitText(ctx.text())
        points = self.visitPoints(ctx.points()) if ctx.points() else None
        image = self.visitQuestionMedia(ctx.questionMedia()) if ctx.questionMedia() else None
        answers = [self.visitAnswer(a) for a in ctx.answer()]
        return QuestionData(text=text, points=points, image=image, answers=answers)

    def visitPoints(self, ctx: QuizParser.PointsContext):
        raw = ctx.NUMBER().getText()
        return float(raw) if '.' in raw else int(raw)

    def visitQuestionMedia(self, ctx: QuizParser.QuestionMediaContext) -> str:
        return self.visitImage(ctx.image())

    # ── answer ────────────────────────────────────────────────────────────────

    def visitAnswer(self, ctx: QuizParser.AnswerContext) -> AnswerData:
        label = ctx.OPTION_LABEL().getText()
        correct = ctx.CORRECT_MARKER() is not None
        text, image = self.visitAnswerContent(ctx.answerContent())
        return AnswerData(label=label, text=text, image=image, correct=correct)

    def visitAnswerContent(self, ctx: QuizParser.AnswerContentContext) -> tuple:
        text = self.visitText(ctx.text()) if ctx.text() else None
        image = self.visitImage(ctx.image()) if ctx.image() else None
        return text, image

    # ── image / value / text ──────────────────────────────────────────────────

    def visitImage(self, ctx: QuizParser.ImageContext) -> str:
        if ctx.STRING_LITERAL():
            return ctx.STRING_LITERAL().getText().strip('"')
        return self.visitText(ctx.text())

    def visitValue(self, ctx: QuizParser.ValueContext):
        if ctx.STRING_LITERAL():
            return ctx.STRING_LITERAL().getText().strip('"')
        if ctx.NUMBER():
            raw = ctx.NUMBER().getText()
            return float(raw) if '.' in raw else raw
        if ctx.BOOLEAN():
            return ctx.BOOLEAN().getText() == 'true'
        return self.visitText(ctx.text())

    def visitText(self, ctx: QuizParser.TextContext) -> str:
        return ctx.getText()
