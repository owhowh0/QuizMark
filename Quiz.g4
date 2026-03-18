    grammar Quiz;

    /* Parser Rules */

    quiz
        : 'QUIZ:' text themeBlock? metadata* question+ EOF
        ;

    themeBlock
        : 'THEME' '{' themeStatement+ '}'
        ;

    themeStatement
        : IDENTIFIER '=' value
        | selector '[' attributeList ']'
        ;

    selector
        : 'quiz' | 'question' | 'answer' | 'correct' | 'wrong'
        ;

    attributeList
        : attribute (',' attribute)*
        ;

    attribute
        : IDENTIFIER '=' value
        ;

    metadata
        : IDENTIFIER ':' (text | NUMBER | BOOLEAN)
        ;

    question
        : 'QUESTION' points? ':' text questionMedia? answer+
        ;

    points
        : '(' 'points=' NUMBER ')'
        ;

    questionMedia
        : image
        ;

    answer
        : OPTION_LABEL ':' answerContent CORRECT_MARKER?
        ;

    answerContent
        : text image?
        | image
        ;

    image
        : 'IMAGE:' (STRING_LITERAL | text)
        ;

    value
        : STRING_LITERAL
        | text
        | NUMBER
        | BOOLEAN
        ;

    text
        : IDENTIFIER
        | TEXT_CONTENT
        ;

    /* Lexer Rules */

    // Specific Labels
    OPTION_LABEL   : [A-E] ;
    CORRECT_MARKER : '*' ;
    BOOLEAN        : 'true' | 'false' ;

    // Keywords and IDs
    IDENTIFIER     : [a-zA-Z] [a-zA-Z0-9_]* ;

    // Numbers and Percentages
    NUMBER         : [0-9]+ ('.' [0-9]+)? '%'? ;

    // Quoted Strings
    STRING_LITERAL : '"' ~["\r\n]* '"' ;

    // General text for questions/titles (captures spaces and punctuation)
    // Note: No backslashes needed for . or ? inside []
    TEXT_CONTENT   : [a-zA-Z0-9] [a-zA-Z0-9 \t.,?!/]* ;

    // Ignore whitespace
    WS : [ \t\r\n]+ -> skip ;
