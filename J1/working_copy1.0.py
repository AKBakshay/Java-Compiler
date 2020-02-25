import sys
import re
import ply.lex as lex
import ply.yacc as yacc
import csv
from regex import *
from collections import defaultdict as ddict

filename = sys.argv[1]
input_data = open(filename,'r').read()

#initialize lexer
lexer=lex.lex()


def p_Start(p):
    '''Start : CompilationUnit   '''


def p_Identifier(p):
  '''Identifier : IDENTIFIER'''

def p_Literal(p):
  '''Literal : IntegerLiteral
        | FloatingPointLiteral
        | BooleanLiteral
        | CharacterLiteral
        | StringLiteral
        | NullLiteral'''

def p_IntegerLiteral(p):
  '''IntegerLiteral : INTVAL
              | LONGVAL'''

def p_FloatingPointLiteral(p):
  '''FloatingPointLiteral : FLOATVAL
              | DOUBLEVAL'''

def p_BooleanLiteral(p):
  '''BooleanLiteral : FALSEVAL
            | TRUEVAL'''

def p_CharacterLiteral(p):
  '''CharacterLiteral : CHARVAL'''

def p_StringLiteral(p):
  '''StringLiteral : STRINGVAL'''

def p_NullLiteral(p):
  '''NullLiteral : NULLVAL'''


def p_error(p):
    print("Syntax error in input!")

def p_empty(p):
  'empty :'
  pass

# Types, Values, Variables

def p_Type(p):
    '''Type : PrimitiveType
                | ReferenceType'''

def p_PrimitiveType(p):
    '''PrimitiveType : NumericType
                        | BOOLEAN'''
                
def p_NumericType(p):
    '''NumericType : IntegralType
                    | FloatingPointType'''

def p_IntegralType(p):
    '''IntegralType : BYTE
                    | SHORT
                    | INT
                    | LONG
                    | CHAR '''

def p_FloatingPointType(p):
    '''FloatingPointType : FLOAT
                            | DOUBLE '''

def p_ReferenceType(p):
    '''ReferenceType : ClassOrInterfaceType
                        | ArrayType'''

def p_ClassOrInterfaceType(p):
    '''ClassOrInterfaceType : Name'''

def p_ClassType(p):
    '''ClassType : ClassOrInterfaceType'''

def p_InterfaceType(p):
    '''InterfaceType : ClassOrInterfaceType'''

def p_ArrayType(p):
    '''ArrayType : PrimitiveType LSQR RSQR 
                    | Name LSQR RSQR 
                    | ArrayType LSQR RSQR '''

# Names

def p_Name(p):
    '''Name : SimpleName
                | QualifiedName '''

def p_SimpleName(p):
    ''' SimpleName : Identifier '''

def p_QualifiedName(p):
    '''QualifiedName : Name POINT Identifier '''

#Compilation Unit 

def p_CompilationUnit(p):
    '''CompilationUnit : PackageDeclaration ImportDeclarations TypeDeclarations
                       | PackageDeclaration ImportDeclarations 
                       | PackageDeclaration TypeDeclarations
                       | ImportDeclarations TypeDeclarations
                       | PackageDeclaration
                       | ImportDeclarations
                       | TypeDeclarations
                       | empty '''

def p_ImportDeclarations(p):
    '''ImportDeclarations : ImportDeclaration
                          | ImportDeclarations ImportDeclaration'''

def p_TypeDeclarations(p):
    '''TypeDeclarations : TypeDeclaration
                        | TypeDeclarations TypeDeclaration'''

def p_PackageDeclaration(p):
    '''PackageDeclaration : PACKAGE Name SCOLON '''
    
def p_ImportDeclaration(p):
    '''ImportDeclaration : SingleTypeImportDeclaration
                         | TypeImportOnDemandDeclaration'''

def p_SingleTypeImportDeclaration(p):
    '''SingleTypeImportDeclaration : IMPORT Name SCOLON '''
    
def p_TypeImportOnDemandDeclaration(p):
    '''TypeImportOnDemandDeclaration : IMPORT Name POINT STAR SCOLON '''
    
def p_TypeDeclaration(p):
    '''TypeDeclaration : ClassDeclaration
                       | InterfaceDeclaration
                       | SCOLON '''
    
def p_Modifiers(p):
    '''Modifiers : Modifier
                 | Modifiers Modifier'''

def p_Modifier(p):
    '''Modifier : PUBLIC
                | PROTECTED 
                | PRIVATE
                | STATIC
                | ABSTRACT 
                | FINAL 
                | NATIVE 
                | SYNCHRONIZED 
                | TRANSIENT 
                | VOLATILE'''



def p_ClassDeclaration(p):
    '''ClassDeclaration : Modifiers CLASS Identifier Super Interfaces ClassBody
                        | Modifiers CLASS Identifier Super ClassBody
                        | Modifiers CLASS Identifier Interfaces ClassBody
                        | CLASS Identifier Super Interfaces ClassBody
                        | Modifiers CLASS Identifier ClassBody
                        | CLASS Identifier Interfaces ClassBody
                        | CLASS Identifier Super ClassBody
                        | CLASS Identifier ClassBody '''

def p_Super(p):
    '''Super : EXTENDS ClassType'''

def p_Interfaces(p):
    '''Interfaces : IMPLEMENTS InterfaceTypeList'''

def p_InterfaceTypeList(p):
    '''InterfaceTypeList : InterfaceType
                         | InterfaceTypeList COMMA InterfaceType'''

def p_ClassBody(p):
    '''ClassBody : LCURL ClassBodyDeclarations RCURL 
                 | LCURL RCURL '''

def p_ClassBodyDeclarations(p):
    '''ClassBodyDeclarations : ClassBodyDeclaration
                             | ClassBodyDeclarations ClassBodyDeclaration'''

def p_ClassBodyDeclaration(p):
    '''ClassBodyDeclaration : ClassMemberDeclaration
                            | StaticInitializer
                            | ConstructorDeclaration'''

def p_ClassMemberDeclaration(p):
    '''ClassMemberDeclaration : FieldDeclaration
                              | MethodDeclaration'''

    
def p_FieldDeclaration(p):
    '''FieldDeclaration : Modifiers Type VariableDeclarators SCOLON
                        | Type VariableDeclarators SCOLON '''

def p_VariableDeclarators(p):
    '''VariableDeclarators : VariableDeclarator
                           | VariableDeclarators COMMA VariableDeclarator'''

def p_VariableDeclarator(p):
    '''VariableDeclarator : VariableDeclaratorId
                          | VariableDeclaratorId EQ VariableInitializer'''

def p_VariableDeclaratorId(p):
    '''VariableDeclaratorId : Identifier
                            | VariableDeclaratorId LSQR RSQR '''

def p_VariableInitializer(p):
    '''VariableInitializer : Expression
                           | ArrayInitializer'''

#9.8.3 Productions from §8.4: Method Declarations

def p_MethodDeclaration(p):
    '''MethodDeclaration : MethodHeader MethodBody'''

def p_MethodHeader(p):
    '''MethodHeader : Type MethodDeclarator
                    | Type MethodDeclarator Throws
                    | Modifiers Type MethodDeclarator 
                    | Modifiers Type MethodDeclarator Throws
                    | VOID MethodDeclarator 
                    | VOID MethodDeclarator Throws
                    | Modifiers VOID MethodDeclarator
                    | Modifiers VOID MethodDeclarator Throws'''

def p_MethodDeclarator(p):
    '''MethodDeclarator : Identifier LPAR RPAR
                        | Identifier LPAR FormalParameterList RPAR
                        | MethodDeclarator LSQR RSQR '''

def p_FormalParameterList(p):
    '''FormalParameterList : FormalParameter
                            | FormalParameterList COMMA FormalParameter'''

def p_FormalParameter(p):
    '''FormalParameter : Type VariableDeclaratorId'''

def p_Throws(p):
    '''Throws : THROWS ClassTypeList'''

def p_ClassTypeList(p):
    '''ClassTypeList : ClassType
                     | ClassTypeList COMMA ClassType'''

def p_MethodBody(p):
    '''MethodBody : Block 
                   | SCOLON '''

#19.8.4 Productions from §8.5: Static Initializers

def p_StaticInitializer(p):
    '''StaticInitializer : STATIC Block'''

#19.8.5 Productions from §8.6: Constructor Declarations
def p_ConstructorDeclaration(p):
    '''ConstructorDeclaration :   ConstructorDeclarator  ConstructorBody
                                |  ConstructorDeclarator Throws ConstructorBody
                                | Modifiers ConstructorDeclarator  ConstructorBody
                                | Modifiers ConstructorDeclarator Throws ConstructorBody'''

def p_ConstructorDeclarator(p):
    '''ConstructorDeclarator : SimpleName LPAR RPAR 
                             | SimpleName LPAR FormalParameterList RPAR '''

def p_ConstructorBody(p):
    '''ConstructorBody : LCURL RCURL 
                       | LCURL BlockStatements RCURL
                       | LCURL ExplicitConstructorInvocation  RCURL
                       | LCURL ExplicitConstructorInvocation BlockStatements RCURL '''

def p_ExplicitConstructorInvocation(p):
    '''ExplicitConstructorInvocation : THIS LPAR RPAR SCOLON
                                    | THIS LPAR ArgumentList RPAR SCOLON
                                    | SUPER LPAR  RPAR SCOLON 
                                     | SUPER LPAR ArgumentList RPAR SCOLON '''

#19.9 Productions from §9: Interfaces
#19.9.1 Productions from §9.1: Interface Declarations

def p_InterfaceDeclaration(p):
    '''InterfaceDeclaration :  INTERFACE Identifier  InterfaceBody 
                             |  INTERFACE Identifier ExtendsInterfaces InterfaceBody
                             | Modifiers INTERFACE Identifier  InterfaceBody
                             | Modifiers INTERFACE Identifier ExtendsInterfaces InterfaceBody'''

def p_ExtendsInterfaces(p):
    '''ExtendsInterfaces : EXTENDS InterfaceType
                         | ExtendsInterfaces COMMA InterfaceType'''

def p_InterfaceBody(p):
    '''InterfaceBody : LCURL  RCURL 
                    | LCURL InterfaceMemberDeclarations RCURL '''

def p_InterfaceMemberDeclarations(p):
    '''InterfaceMemberDeclarations : InterfaceMemberDeclaration
                                    | InterfaceMemberDeclarations InterfaceMemberDeclaration'''

def p_InterfaceMemberDeclaration(p):
    '''InterfaceMemberDeclaration : ConstantDeclaration
                                  | AbstractMethodDeclaration'''

def p_ConstantDeclaration(p):
    '''ConstantDeclaration : FieldDeclaration'''

def p_AbstractMethodDeclaration(p):
    '''AbstractMethodDeclaration : MethodHeader SCOLON '''

#19.10 Productions from §10: Arrays
def p_ArrayInitializer(p):
    '''ArrayInitializer : LCURL RCURL 
                        | LCURL COMMA RCURL 
                        | LCURL VariableInitializers  RCURL 
                        | LCURL VariableInitializers COMMA RCURL '''

def p_VariableInitializers(p):
    '''VariableInitializers :  VariableInitializer
                         |  VariableInitializers COMMA VariableInitializer'''



# productions from Blocks and Statements

def p_Block(p):
    '''Block : LCURL BlockStatements RCURL
                | LCURL  RCURL '''


def p_BlockStatements(p):
    '''
    BlockStatements : BlockStatement 
                    | BlockStatements BlockStatement
    '''
def p_BlockStatement(p):
    '''BlockStatement : LocalVariableDeclarationStatement
                      | Statement'''

def p_LocalVariableDeclarationStatement(p):
    '''LocalVariableDeclarationStatement : LocalVariableDeclaration SCOLON '''

def p_LocalVariableDeclaration(p):
    '''LocalVariableDeclaration : Type VariableDeclarators'''

def p_Statement(p):
    '''Statement : StatementWithoutTrailingSubstatement
                            | LabeledStatement
                            | IfThenStatement
                            | IfThenElseStatement
                            | WhileStatement
                            | ForStatement'''

def p_StatementNoShortIf(p):
    '''StatementNoShortIf : StatementWithoutTrailingSubstatement
                                    | LabeledStatementNoShortIf
                                    | IfThenElseStatementNoShortIf
                                    | WhileStatementNoShortIf
                                    | ForStatementNoShortIf'''


def p_StatementWithoutTrailingSubstatement(p):
    '''StatementWithoutTrailingSubstatement : Block
                                            | EmptyStatement
                                            | ExpressionStatement
                                            | SwitchStatement
                                            | DoStatement
                                            | BreakStatement
                                            | ContinueStatement
                                            | ReturnStatement
                                            | SynchronizedStatement
                                            | ThrowStatement
                                            | TryStatement'''

def p_EmptyStatement(p):
    '''EmptyStatement : SCOLON '''

def p_LabeledStatement(p):
    '''LabeledStatement : Identifier COLON Statement'''

def p_LabeledStatementNoShortIf(p):
    '''LabeledStatementNoShortIf :  Identifier COLON StatementNoShortIf'''

def p_ExpressionStatement(p):
    '''ExpressionStatement : StatementExpression SCOLON '''

def p_StatementExpression(p):
    '''StatementExpression : Assignment
                                    | PreIncrementExpression
                                    | PreDecrementExpression
                                    | PostIncrementExpression
                                    | PostDecrementExpression
                                    | MethodInvocation
                                    | ClassInstanceCreationExpression'''

def p_IfThenStatement(p):
    '''IfThenStatement : IF LPAR Expression RPAR Statement'''

def p_IfThenElseStatement(p):
    '''IfThenElseStatement : IF LPAR Expression RPAR StatementNoShortIf ELSE Statement'''

def p_IfThenElseStatementNoShortIf(p):
    '''IfThenElseStatementNoShortIf : IF LPAR Expression RPAR StatementNoShortIf ELSE StatementNoShortIf'''

def p_SwitchStatement(p):
    '''SwitchStatement : SWITCH LPAR Expression RPAR SwitchBlock'''

def p_SwitchBlock(p):
    '''SwitchBlock : LCURL SwitchBlockStatementGroups SwitchLabels RCURL
                    | LCURL SwitchBlockStatementGroups  RCURL
                    | LCURL  SwitchLabels RCURL
                    | LCURL  RCURL '''

def p_SwitchBlockStatementGroups(p):
    '''SwitchBlockStatementGroups : SwitchBlockStatementGroup
                                    | SwitchBlockStatementGroups SwitchBlockStatementGroup'''

def p_SwitchBlockStatementGroup(p):
    '''SwitchBlockStatementGroup :  SwitchLabels BlockStatements'''

def p_SwitchLabels(p):
    '''SwitchLabels : SwitchLabel
                            | SwitchLabels SwitchLabel'''

def p_SwitchLabel(p):
    '''SwitchLabel : CASE ConstantExpression COLON
                            | DEFAULT COLON '''

def p_WhileStatement(p):
    '''WhileStatement : WHILE LPAR Expression RPAR Statement'''

def p_WhileStatementNoShortIf(p):
    '''WhileStatementNoShortIf : WHILE LPAR Expression RPAR StatementNoShortIf'''

def p_DoStatement(p):
    '''DoStatement : DO Statement WHILE LPAR Expression RPAR SCOLON '''

def p_ForStatement(p):
    '''ForStatement : FOR LPAR ForInit SCOLON Expression SCOLON ForUpdate RPAR Statement
                    | FOR LPAR  SCOLON Expression SCOLON ForUpdate RPAR Statement
                    | FOR LPAR ForInit SCOLON  SCOLON ForUpdate RPAR Statement
                    | FOR LPAR ForInit SCOLON Expression SCOLON  RPAR Statement
                    | FOR LPAR  SCOLON  SCOLON ForUpdate RPAR Statement
                    | FOR LPAR ForInit SCOLON  SCOLON  RPAR Statement
                    | FOR LPAR  SCOLON Expression SCOLON  RPAR Statement
                    | FOR LPAR  SCOLON  SCOLON  RPAR Statement
                    '''


def p_ForStatementNoShortIf(p):
    '''ForStatementNoShortIf : FOR LPAR ForInit SCOLON Expression SCOLON ForUpdate RPAR StatementNoShortIf
                                | FOR LPAR  SCOLON Expression SCOLON ForUpdate RPAR StatementNoShortIf
                                | FOR LPAR ForInit SCOLON  SCOLON ForUpdate RPAR    StatementNoShortIf
                                | FOR LPAR ForInit SCOLON Expression SCOLON  RPAR   StatementNoShortIf
                                | FOR LPAR  SCOLON  SCOLON ForUpdate RPAR   StatementNoShortIf
                                | FOR LPAR ForInit SCOLON  SCOLON  RPAR StatementNoShortIf
                                | FOR LPAR  SCOLON Expression SCOLON  RPAR  StatementNoShortIf
                                | FOR LPAR  SCOLON  SCOLON  RPAR    StatementNoShortIf

                                '''

def p_ForInit(p):
    '''ForInit : StatementExpressionList 
                        | LocalVariableDeclaration'''

def p_ForUpdate(p):
    '''ForUpdate :  StatementExpressionList'''

def p_StatementExpressionList(p):
    '''StatementExpressionList : StatementExpression
                                | StatementExpressionList COMMA StatementExpression'''

def p_BreakStatement(p):
    '''BreakStatement   : BREAK Identifier SCOLON 
                        | BREAK SCOLON '''

def p_ContinueStatement(p):
    '''ContinueStatement :  CONTINUE Identifier SCOLON
                        | CONTINUE SCOLON '''

def p_ReturnStatement(p):
    '''ReturnStatement : RETURN Expression SCOLON 
                        | RETURN SCOLON '''

def p_ThrowStatement(p):
    '''ThrowStatement : THROW Expression SCOLON '''

def p_SynchronizedStatement(p):
    '''SynchronizedStatement :  SYNCHRONIZED LPAR Expression RPAR Block'''


def p_TryStatement(p):
    '''TryStatement : TRY Block Catches
                            | TRY Block Catches Finally
                            | TRY Block Finally'''

def p_Catches(p):
    '''Catches : CatchClause
                        | Catches CatchClause'''

def p_CatchClause(p):
    '''CatchClause : CATCH LPAR FormalParameter RPAR Block'''

def p_Finally(p):
    '''Finally : FINALLY Block'''

#Expressions

def p_Primary(p):
    '''Primary : PrimaryNoNewArray
               | ArrayCreationExpression'''


def p_PrimaryNoNewArray(p):
    '''PrimaryNoNewArray  : Literal
                          | THIS
                          | LPAR Expression RPAR
                          | ClassInstanceCreationExpression
                          | FieldAccess
                          | MethodInvocation
                          | ArrayAccess'''

def p_ClassInstanceCreationExpression(p):
    '''ClassInstanceCreationExpression : NEW ClassType LPAR  RPAR 
                                       | NEW ClassType LPAR ArgumentList RPAR '''

def p_ArgumentList(p):
    '''ArgumentList : Expression
                    | ArgumentList COMMA Expression'''

def p_ArrayCreationExpression(p):
    '''ArrayCreationExpression  : NEW PrimitiveType DimExprs 
                                | NEW PrimitiveType DimExprs Dims
                                | NEW ClassOrInterfaceType DimExprs 
                                | NEW ClassOrInterfaceType DimExprs Dims '''


def p_DimExprs(p):
    '''DimExprs : DimExpr
                | DimExprs DimExpr'''

def p_DimExpr(p):
    '''DimExpr : LSQR Expression RSQR '''

def p_Dims(p):
    '''Dims : LSQR RSQR
            | Dims LSQR RSQR '''

def p_FieldAccess(p):
    '''FieldAccess : Primary POINT Identifier
                   | SUPER POINT Identifier '''

def p_MethodInvocation(p):
    '''MethodInvocation : Name LPAR RPAR
                        |  Name LPAR ArgumentList RPAR
                        | Primary POINT Identifier LPAR RPAR
                        | Primary POINT Identifier LPAR ArgumentList RPAR
                        | SUPER POINT Identifier LPAR RPAR 
                        | SUPER POINT Identifier LPAR ArgumentList RPAR '''

def p_ArrayAccess(p):
    '''ArrayAccess : Name LSQR Expression RSQR
                   | PrimaryNoNewArray LSQR Expression RSQR '''


def p_PostfixExpression(p):
    '''PostfixExpression : Primary
                         | Name
                         | PostIncrementExpression
                         | PostDecrementExpression'''

def p_PostIncrementExpression(p):
    '''PostIncrementExpression : PostfixExpression DPLUS '''


def p_PostDecrementExpression(p):
    '''PostDecrementExpression : PostfixExpression DMINUS '''

def p_UnaryExpression(p):
    '''UnaryExpression  : PreIncrementExpression
                        | PreDecrementExpression
                        | PLUS UnaryExpression
                        | MINUS UnaryExpression
                        | UnaryExpressionNotPlusMinus '''

def p_PreIncrementExpression(p):
    '''PreIncrementExpression : DPLUS UnaryExpression'''

def p_PreDecrementExpression(p):
    '''PreDecrementExpression : DMINUS UnaryExpression'''

def p_UnaryExpressionNotPlusMinus(p):
    '''UnaryExpressionNotPlusMinus  : PostfixExpression
                                    | TILDE UnaryExpression
                                    | EXCLAIM UnaryExpression
                                    | CastExpression'''

def p_CastExpression(p):
    '''CastExpression   : LPAR PrimitiveType RPAR UnaryExpression
                        | LPAR PrimitiveType Dims RPAR UnaryExpression
                        | LPAR Expression RPAR UnaryExpressionNotPlusMinus
                        | LPAR Name Dims RPAR UnaryExpressionNotPlusMinus'''

def p_MultiplicativeExpression(p):
    '''MultiplicativeExpression : UnaryExpression
                                | MultiplicativeExpression STAR UnaryExpression
                                | MultiplicativeExpression FSLASH UnaryExpression
                                | MultiplicativeExpression MOD UnaryExpression'''

def p_AdditiveExpression(p):
    '''AdditiveExpression : MultiplicativeExpression
                          | AdditiveExpression PLUS MultiplicativeExpression
                          | AdditiveExpression MINUS MultiplicativeExpression'''

def p_ShiftExpression(p):
    '''ShiftExpression  : AdditiveExpression
                        | ShiftExpression LSHIFT AdditiveExpression
                        | ShiftExpression RSHIFT AdditiveExpression
                        | ShiftExpression URSHIFT AdditiveExpression'''

def p_RelationalExpression(p):
    '''RelationalExpression : ShiftExpression
                            | RelationalExpression LETHAN ShiftExpression
                            | RelationalExpression GRTHAN ShiftExpression
                            | RelationalExpression LEEQ ShiftExpression
                            | RelationalExpression GREQ ShiftExpression
                            | RelationalExpression INSTANCEOF ReferenceType'''

def p_EqualityExpression(p):
    '''EqualityExpression   : RelationalExpression
                            | EqualityExpression DEQ RelationalExpression
                            | EqualityExpression NTEQ RelationalExpression'''

def p_AndExpression(p):
    '''AndExpression : EqualityExpression
                     | AndExpression AND EqualityExpression'''

def p_ExclusiveOrExpression(p):
    '''ExclusiveOrExpression : AndExpression
                             | ExclusiveOrExpression XOR AndExpression'''

def p_InclusiveOrExpression(p):
    '''InclusiveOrExpression : ExclusiveOrExpression
                             | InclusiveOrExpression OR ExclusiveOrExpression'''

def p_ConditionalAndExpression(p):
    '''ConditionalAndExpression : InclusiveOrExpression
                                | ConditionalAndExpression DAND InclusiveOrExpression'''

def p_ConditionalOrExpression(p):
    '''ConditionalOrExpression  : ConditionalAndExpression
                                | ConditionalOrExpression DOR ConditionalAndExpression'''

def p_ConditionalExpression(p):
    '''ConditionalExpression : ConditionalOrExpression
                             | ConditionalOrExpression QMARK Expression COLON ConditionalExpression'''

def p_AssignmentExpression(p):
    '''AssignmentExpression : ConditionalExpression
                            | Assignment'''

def p_Assignment(p):
    '''Assignment : LeftHandSide AssignmentOperator AssignmentExpression'''

def p_LeftHandSide(p):
    '''LeftHandSide : Name
                    | FieldAccess
                    | ArrayAccess'''

def p_AssignmentOperator(p):
    '''AssignmentOperator  : EQ
                           | STAREQ
                           | FSLASHEQ 
                           | MODEQ
                           | PLUSEQ 
                           | MINUSEQ
                           | LSHIFTEQ
                           | RSHIFTEQ
                           | URSHIFTEQ
                           | ANDEQ
                           | XOREQ 
                           | OREQ '''

def p_Expression(p):
    '''Expression : AssignmentExpression'''

def p_ConstantExpression(p):
    '''ConstantExpression : Expression'''

parser = yacc.yacc()     # Return parser object
result = parser.parse(input_data+'\n',lexer=lexer,debug=True)