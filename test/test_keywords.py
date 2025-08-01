pythonKeywords = [
    "and", "as", "assert", "break", "class", 
    "continue", "def", "del", "elif", "else", 
    "except", "False", "finally", "for", "from", 
    "global", "if", "import", "in", "is", 
    "lambda", "None", "nonlocal", "not", "or", 
    "pass", "raise", "return", "True", "try", 
    "while", "with", "yield"
]
    
javaKeywords = [
    "abstract", "assert", "boolean", "break", "byte",
    "case", "catch", "char", "class", "continue", 
    "const", "default", "do", "double", "else",
    "enum", "exports", "extends", "false", "final", 
    "finally", "float", "for", "goto", "if", 
    "implements","import", "instanceof", "int", "interface", 
    "long", "module", "native", "new", "null", 
    "package", "private",  "protected", "public", "requires", 
    "return", "short", "static", "strictfp", "super", 
    "switch", "synchronized", "this", "throw", "transient", 
    "true", "try", "var", "void", "volatile", 
    "while" 
]

javaScriptKeywords = [
    "abstract", "arguments", "await", "boolean", "break",
    "byte", "case", "catch", "char", "class", 
    "const", "continue", "debugger", "default", "delete",
    "do", "double", "else", "enum", "eval",
    "export", "extends", "false", "final", "finally",
    "float", "for", "function", "goto", "if",
    "implements", "import", "in", "instanceof", "int",
    "interface", "let", "long", "native", "new",
    "null", "package", "private", "protected", "public",
    "return", "short", "static", "super", "switch",
    "synchronized", "this", "throw", "throws", "transient",
    "true", "try", "typeof", "var", "void", 
    "volatile", "while", "with", "yield"
]

cKeywords = [
    "auto", "break", "case", "char", "const",
    "continue", "default", "do", "double", "else",
    "enum", "extern", "float", "for", "goto",
    "if", "int", "long", "register", "return",
    "short", "signed", "sizeof", "static", "struct",
    "switch", "typedef", "union", "unsigned", "void",
    "volatile", "while"
]

cPlusPlusKeywords = [
    "and", "and_eq", "auto", "bitand", "bitor",
    "bool", "break", "case", "catch", "char",
    "class", "compl", "const", "continue", "default",
    "delete", "do", "double", "else", "enum",
    "false", "float", "for", "friend", "goto",
    "if", "int", "long", "namespace", "new",
    "not", "not_eq", "or", "or_eq", "private",
    "protected", "public", "return", "short", "signed",
    "sizeof", "static", "struct", "switch", "template",
    "this", "throw", "true", "try", "typedef",
    "unsigned", "using", "virtual", "void", "while",
    "xor", "xor_eq"
]

goKeywords = [
    "break", "case", "chan", "const", "continue",
    "default", "defer", "else", "fallthrough", "for",
    "func", "go", "goto", "if", "import",
    "interface", "map", "package", "range", "return",
    "select", "struct", "switch", "type", "var"
]

SQLKeywords = [
    "ADD", "ADD CONSTRAINT", "ALL", "ALTER", "ALTER COLUMN",
    "ALTER TABLE", "AND", "ANY", "AS", "ASC",
    "BACKUP DATABASE", "BETWEEN", "CASE", "CHECK", "COLUMN",
    "CONSTRAINT", "CREATE", "CREATE DATABASE", "CREATE INDEX", "CREATE OR REPLACE VIEW",
    "CREATE TABLE", "CREATE PROCEDURE", "CREATE UNIQUE INDEX", "CREATE VIEW", "DATABASE",
    "DEFAULT", "DELETE", "DESC", "DISTINCT", "DROP", 
    "DROP COLUMN", "DROP CONSTRAINT", "DROP DATABASE", "DROP DEFAULT", "DROP INDEX",
    "DROP TABLE", "DROP VIEW", "EXEC", "EXISTS", "FOREIGN KEY", 
    "FROM", "FULL OUTER JOIN", "GROUP BY", "HAVING", "IN",
    "INDEX", "INNER JOIN", "INNER INTO", "INNER INTO SELECT", "IS NULL",
    "IS NOT NULL", "JOIN", "LEFT JOIN", "LIKE", "LIMIT", 
    "NOT", "NOT NULL", "OR", "ORDER BY", "OUTER JOIN",
    "PRIMARY KEY", "PROCEDURE", "RIGHT JOIN", "ROWNUM", "SELECT",
    "SELECT DISTINCT", "SELECT INTO", "SELECT TOP", "SET", "TABLE",
    "TOP", "TRUNCATE TABLE", "UNION", "UNOIN ALL", "UNIQUE",
    "UPDATE", "VALUES", "VIEW", "WHERE"
]

sharedKeywords = [
    "assert", "abstract", "and", "auto", "boolean", 
    "break", "byte", "case", "catch", "char", 
    "class", "const", "continue", "default", "delete", 
    "do", "double", "else", "enum", "extends", 
    "false", "final", "finally", "float", "for", 
    "goto", "if", "implements", "import", "in", 
    "instanceof", "int", "interface", "long", "native", 
    "new", "not", "null", "or", "package", 
    "private", "protected", "public", "return", "short", 
    "signed", "sizeof", "static", "struct", "super", 
    "switch", "synchronized", "this", "throw", "transient", 
    "true", "try", "typedef", "unsigned", "var", 
    "void", "volatile", "while", "with", "yield"
]

allKeywordLists = [pythonKeywords, javaKeywords, javaScriptKeywords, cKeywords, cPlusPlusKeywords, goKeywords, SQLKeywords]

 
def test_keywords():
    sharedKeys: set[str] = set()
    for i in range(len(allKeywordLists)):
        for keyList in allKeywordLists:
            if (keyList == allKeywordLists[i]):
                break
            for key1 in allKeywordLists[i]:
                for key2 in keyList:
                    if key1 == key2:
                        if key1 not in sharedKeywords:
                            sharedKeys.add(key1)
    
    sharedKeysList = []
    for s_key in sharedKeys:
        sharedKeysList.append(s_key)

    sharedKeysList.sort()
    print(sharedKeysList)
    
    assert False