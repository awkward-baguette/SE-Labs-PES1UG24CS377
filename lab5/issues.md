   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | Hardcoded SQL expressions | Security Vulnerability (SQL Injection / CWE-89) | 33 | Constructs the SQL query using an f-string with raw user input (name), allowing attackers to inject malicious SQL commands and manipulate query logic. | Replace the f-string with a parameterized query placeholder (?) and pass the input separately as a tuple to cur.execute(). |
   | Unsafe open| Reliability / Compatibility | 69, 77| Using unsafe open without specifying an encoding in load_stock and export_prescription | Changed to use with open and utf-8 |
   | Use of global | Code Quality / Design Anti-Pattern | 55 |Using the global statement unneccessarily in load_stock | Return the stock value, and pass it to all other functions using it |
   | No exception cases| Error handling| 38 | No specific exception case specified in the try clauses of load_stock and dispense| Added KeyError to dispense and FileNotFound error to load_stock |
   | Naming convention violation| Style / PEP 8 Violation | 61 | Function name "printStock" doesn't conform to snake_case naming style| Changed the name and subsequent call to print_stock |
   | Missing module/function docstrings| Maintainability / Documentation | 1, 11, 19, 24, 29, 41, 49, 54, 61, 66| No comments documenting the purpose of the file and the functions| Added a module defnition comment and comments defining each function |
   | Unused import | Code quality | 3 | os is imported but never used| Removed import |
   | Line too long | Code readability | 36 | Calculated new units in during insertion| Calculated new_units and later assigned it to units |