import re

def test_input(key: str):
    if key == "":
        raise ValueError("Invalid Data Item: Key cannot be empty")
    keyParts = key.split("/")
    for part in keyParts:
        # Keyword Tests
        keyword_tests(part)

        # Naming Tests
        format_test(part)

def keyword_tests(key: str):
    zenohKeywords = ["STATE", "LINK", "TAGS"]
    list_test(key, zenohKeywords)
    
    sharedKeywords = [
        "abstract", "and", "assert", "auto", "boolean", 
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
        "true", "try", "typedef", "union", "unsigned", "var", 
        "void", "volatile", "while", "with", "yield"
    ]
    list_test(key, sharedKeywords)

    pythonKeywords = [ 
        "as", "def", "del", "elif", "except", "from", "global", "is", "lambda", "None", "nonlocal", "pass", "raise"
    ]
    list_test(key, pythonKeywords)

    javaKeywords = [
            "exports",  "module", "requires", "strictfp"
    ]
    list_test(key, javaKeywords)

    javaScriptKeywords = [
        "arguments", "await", "debugger", "eval", "export", "function","let", "throws", "typeof",
    ]
    list_test(key, javaScriptKeywords)

    cKeywords = [
        "extern", "register"
    ]
    list_test(key, cKeywords)

    cPlusPlusKeywords = [
        "and_eq", "bitand", "bitor", "bool", "compl", "friend", "namespace", "not_eq", "or_eq", "template", "using", "virtual", "xor", "xor_eq"
    ]
    list_test(key, cPlusPlusKeywords)

    goKeywords = [
        "chan", "defer", "fallthrough", "func", "go", "map", "range", "select", "type",
    ]
    list_test(key, goKeywords)

    SQLKeywords = [
        "ADD", "ADD CONSTRAINT", "ALL", "ALTER", "ALTER COLUMN",
        "ALTER TABLE", "ANY", "AS", "ASC",
        "BACKUP DATABASE", "BETWEEN", "CHECK", "COLUMN",
        "CONSTRAINT", "CREATE", "CREATE DATABASE", "CREATE INDEX", "CREATE OR REPLACE VIEW",
        "CREATE TABLE", "CREATE PROCEDURE", "CREATE UNIQUE INDEX", "CREATE VIEW", "DATABASE",
        "DESC", "DISTINCT", "DROP", 
        "DROP COLUMN", "DROP CONSTRAINT", "DROP DATABASE", "DROP DEFAULT", "DROP INDEX",
        "DROP TABLE", "DROP VIEW", "EXEC", "EXISTS", "FOREIGN KEY", 
        "FROM", "FULL OUTER JOIN", "GROUP BY", "HAVING",
        "INDEX", "INNER JOIN", "INNER INTO", "INNER INTO SELECT", "IS NULL",
        "IS NOT NULL", "JOIN", "LEFT JOIN", "LIKE", "LIMIT", 
        "NOT NULL", "ORDER BY", "OUTER JOIN",
        "PRIMARY KEY", "PROCEDURE", "RIGHT JOIN", "ROWNUM", "SELECT",
        "SELECT DISTINCT", "SELECT INTO", "SELECT TOP", "SET", "TABLE",
        "TOP", "TRUNCATE TABLE", "UNOIN ALL", "UNIQUE",
        "UPDATE", "VALUES", "VIEW", "WHERE"
    ]
    list_test(key, SQLKeywords)

def list_test(key: str, list: list[str]):
    for compKey in list:
        if key == compKey:
            raise ValueError(f"Invalid Data Item: '{key}' is a reserved keyword")
        
def format_test(key: str):
    # First character cannot be a number
    if (re.search(r"[0-9]", key[0]) is not None):
        raise ValueError(f"Invalid Data Item: {key} may not start with a number")
    
    # Python Convention, can only contain A-z, 0-9, and _ (more strict than others)
    if re.search(r"[^A-Za-z0-9_]", key) is not None:
        raise ValueError(f"Invalid Data Item: {key} may only contain A-Z, a-z, and _")
    
    # C++ Convention, variable names can range from 1 to 255
    if len(key) > 255:
        raise ValueError(f"Invalid Data Item: {key[0:255]}... is too long")