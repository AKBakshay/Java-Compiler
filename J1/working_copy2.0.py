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



class Node:
    def __init__(self, name='', children=[]):
        self.name = name
        if children:
            self.children = children
        else:
            self.children = []
    def __str__(self):
        x = f'[{self.name}'
        for c in self.children:
            if(isinstance(c, Node)):
                x += str(c)
            else:
                x += str(c)
        x += ']' 
        return x



def p_Start(p):
    '''Start : CompilationUnit   '''
    p[0] = Node('CompilationUnit', p[1:])


def p_Identifier(p):
    '''Identifier : IDENTIFIER'''
    p[0] = Node('CompilationUnit', p[1:])

def p_Literal(p):
    '''Literal : IntegerLiteral
        | FloatingPointLiteral
        | BooleanLiteral
        | CharacterLiteral
        | StringLiteral
        | NullLiteral'''
    p[0] = Node('CompilationUnit', p[1:])

def p_IntegerLiteral(p):
    '''IntegerLiteral : INTVAL
              | LONGVAL'''
    p[0] = Node('CompilationUnit', p[1:])

def p_FloatingPointLiteral(p):
    '''FloatingPointLiteral : FLOATVAL
              | DOUBLEVAL'''
    p[0] = Node('CompilationUnit', p[1:])

def p_BooleanLiteral(p):
    '''BooleanLiteral : FALSEVAL
            | TRUEVAL'''
    p[0] = Node('CompilationUnit', p[1:])

def p_CharacterLiteral(p):
    '''CharacterLiteral : CHARVAL'''
    p[0] = Node('CompilationUnit', p[1:])

def p_StringLiteral(p):
    '''StringLiteral : STRINGVAL'''
    p[0] = Node('CompilationUnit', p[1:])

def p_NullLiteral(p):
    '''NullLiteral : NULLVAL'''
    p[0] = Node('CompilationUnit', p[1:])


def p_error(p):
    print("Syntax error in input!")
    p[0] = Node('CompilationUnit', p[1:])

def p_empty(p):
    'empty :'
    pass

# Types, Values, Variables

def p_Type(p):
    '''Type : PrimitiveType
                | ReferenceType'''
    p[0] = Node('CompilationUnit', p[1:])

def p_PrimitiveType(p):
    '''PrimitiveType : NumericType
                        | BOOLEAN'''
    p[0] = Node('CompilationUnit', p[1:])
                
def p_NumericType(p):
    '''NumericType : IntegralType
                    | FloatingPointType'''
    p[0] = Node('CompilationUnit', p[1:])

def p_IntegralType(p):
    '''IntegralType : BYTE
                    | SHORT
                    | INT
                    | LONG
                    | CHAR '''
    p[0] = Node('CompilationUnit', p[1:])

def p_FloatingPointType(p):
    '''FloatingPointType : FLOAT
                            | DOUBLE '''
    p[0] = Node('CompilationUnit', p[1:])

def p_ReferenceType(p):
    '''ReferenceType : ClassOrInterfaceType
                        | ArrayType'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ClassOrInterfaceType(p):
    '''ClassOrInterfaceType : Name'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ClassType(p):
    '''ClassType : ClassOrInterfaceType'''
    p[0] = Node('CompilationUnit', p[1:])

def p_InterfaceType(p):
    '''InterfaceType : ClassOrInterfaceType'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ArrayType(p):
    '''ArrayType : PrimitiveType LSQR RSQR 
                    | Name LSQR RSQR 
                    | ArrayType LSQR RSQR '''
    p[0] = Node('CompilationUnit', p[1:])

# Names

def p_Name(p):
    '''Name : SimpleName
                | QualifiedName '''
    p[0] = Node('CompilationUnit', p[1:])

def p_SimpleName(p):
    ''' SimpleName : Identifier '''
    p[0] = Node('CompilationUnit', p[1:])

def p_QualifiedName(p):
    '''QualifiedName : Name POINT Identifier '''
    p[0] = Node('CompilationUnit', p[1:])

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
    p[0] = Node('CompilationUnit', p[1:])

def p_ImportDeclarations(p):
    '''ImportDeclarations : ImportDeclaration
                          | ImportDeclarations ImportDeclaration'''
    p[0] = Node('CompilationUnit', p[1:])

def p_TypeDeclarations(p):
    '''TypeDeclarations : TypeDeclaration
                        | TypeDeclarations TypeDeclaration'''
    p[0] = Node('CompilationUnit', p[1:])

def p_PackageDeclaration(p):
    '''PackageDeclaration : PACKAGE Name SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])
    
def p_ImportDeclaration(p):
    '''ImportDeclaration : SingleTypeImportDeclaration
                         | TypeImportOnDemandDeclaration'''
    p[0] = Node('CompilationUnit', p[1:])

def p_SingleTypeImportDeclaration(p):
    '''SingleTypeImportDeclaration : IMPORT Name SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])
    
def p_TypeImportOnDemandDeclaration(p):
    '''TypeImportOnDemandDeclaration : IMPORT Name POINT STAR SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])
    
def p_TypeDeclaration(p):
    '''TypeDeclaration : ClassDeclaration
                       | InterfaceDeclaration
                       | SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])
    
def p_Modifiers(p):
    '''Modifiers : Modifier
                 | Modifiers Modifier'''
    p[0] = Node('CompilationUnit', p[1:])

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
    p[0] = Node('CompilationUnit', p[1:])



def p_ClassDeclaration(p):
    '''ClassDeclaration : Modifiers CLASS Identifier Super Interfaces ClassBody
                        | Modifiers CLASS Identifier Super ClassBody
                        | Modifiers CLASS Identifier Interfaces ClassBody
                        | CLASS Identifier Super Interfaces ClassBody
                        | Modifiers CLASS Identifier ClassBody
                        | CLASS Identifier Interfaces ClassBody
                        | CLASS Identifier Super ClassBody
                        | CLASS Identifier ClassBody '''
    p[0] = Node('CompilationUnit', p[1:])

def p_Super(p):
    '''Super : EXTENDS ClassType'''
    p[0] = Node('CompilationUnit', p[1:])

def p_Interfaces(p):
    '''Interfaces : IMPLEMENTS InterfaceTypeList'''
    p[0] = Node('CompilationUnit', p[1:])

def p_InterfaceTypeList(p):
    '''InterfaceTypeList : InterfaceType
                         | InterfaceTypeList COMMA InterfaceType'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ClassBody(p):
    '''ClassBody : LCURL ClassBodyDeclarations RCURL 
                 | LCURL RCURL '''
    p[0] = Node('CompilationUnit', p[1:])

def p_ClassBodyDeclarations(p):
    '''ClassBodyDeclarations : ClassBodyDeclaration
                             | ClassBodyDeclarations ClassBodyDeclaration'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ClassBodyDeclaration(p):
    '''ClassBodyDeclaration : ClassMemberDeclaration
                            | StaticInitializer
                            | ConstructorDeclaration'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ClassMemberDeclaration(p):
    '''ClassMemberDeclaration : FieldDeclaration
                              | MethodDeclaration'''
    p[0] = Node('CompilationUnit', p[1:])

    
def p_FieldDeclaration(p):
    '''FieldDeclaration : Modifiers Type VariableDeclarators SCOLON
                        | Type VariableDeclarators SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

def p_VariableDeclarators(p):
    '''VariableDeclarators : VariableDeclarator
                           | VariableDeclarators COMMA VariableDeclarator'''
    p[0] = Node('CompilationUnit', p[1:])

def p_VariableDeclarator(p):
    '''VariableDeclarator : VariableDeclaratorId
                          | VariableDeclaratorId EQ VariableInitializer'''
    p[0] = Node('CompilationUnit', p[1:])

def p_VariableDeclaratorId(p):
    '''VariableDeclaratorId : Identifier
                            | VariableDeclaratorId LSQR RSQR '''
    p[0] = Node('CompilationUnit', p[1:])

def p_VariableInitializer(p):
    '''VariableInitializer : Expression
                           | ArrayInitializer'''
    p[0] = Node('CompilationUnit', p[1:])

#9.8.3 Productions from §8.4: Method Declarations

def p_MethodDeclaration(p):
    '''MethodDeclaration : MethodHeader MethodBody'''
    p[0] = Node('CompilationUnit', p[1:])

def p_MethodHeader(p):
    '''MethodHeader : Type MethodDeclarator
                    | Type MethodDeclarator Throws
                    | Modifiers Type MethodDeclarator 
                    | Modifiers Type MethodDeclarator Throws
                    | VOID MethodDeclarator 
                    | VOID MethodDeclarator Throws
                    | Modifiers VOID MethodDeclarator
                    | Modifiers VOID MethodDeclarator Throws'''
    p[0] = Node('CompilationUnit', p[1:])

def p_MethodDeclarator(p):
    '''MethodDeclarator : Identifier LPAR RPAR
                        | Identifier LPAR FormalParameterList RPAR
                        | MethodDeclarator LSQR RSQR '''
    p[0] = Node('CompilationUnit', p[1:])

def p_FormalParameterList(p):
    '''FormalParameterList : FormalParameter
                            | FormalParameterList COMMA FormalParameter'''
    p[0] = Node('CompilationUnit', p[1:])

def p_FormalParameter(p):
    '''FormalParameter : Type VariableDeclaratorId'''
    p[0] = Node('CompilationUnit', p[1:])

def p_Throws(p):
    '''Throws : THROWS ClassTypeList'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ClassTypeList(p):
    '''ClassTypeList : ClassType
                     | ClassTypeList COMMA ClassType'''
    p[0] = Node('CompilationUnit', p[1:])

def p_MethodBody(p):
    '''MethodBody : Block 
                   | SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

#19.8.4 Productions from §8.5: Static Initializers

def p_StaticInitializer(p):
    '''StaticInitializer : STATIC Block'''
    p[0] = Node('CompilationUnit', p[1:])

#19.8.5 Productions from §8.6: Constructor Declarations
def p_ConstructorDeclaration(p):
    '''ConstructorDeclaration :   ConstructorDeclarator  ConstructorBody
                                |  ConstructorDeclarator Throws ConstructorBody
                                | Modifiers ConstructorDeclarator  ConstructorBody
                                | Modifiers ConstructorDeclarator Throws ConstructorBody'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ConstructorDeclarator(p):
    '''ConstructorDeclarator : SimpleName LPAR RPAR 
                             | SimpleName LPAR FormalParameterList RPAR '''
    p[0] = Node('CompilationUnit', p[1:])

def p_ConstructorBody(p):
    '''ConstructorBody : LCURL RCURL 
                       | LCURL BlockStatements RCURL
                       | LCURL ExplicitConstructorInvocation  RCURL
                       | LCURL ExplicitConstructorInvocation BlockStatements RCURL '''
    p[0] = Node('CompilationUnit', p[1:])

def p_ExplicitConstructorInvocation(p):
    '''ExplicitConstructorInvocation : THIS LPAR RPAR SCOLON
                                    | THIS LPAR ArgumentList RPAR SCOLON
                                    | SUPER LPAR  RPAR SCOLON 
                                     | SUPER LPAR ArgumentList RPAR SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

#19.9 Productions from §9: Interfaces
#19.9.1 Productions from §9.1: Interface Declarations

def p_InterfaceDeclaration(p):
    '''InterfaceDeclaration :  INTERFACE Identifier  InterfaceBody 
                             |  INTERFACE Identifier ExtendsInterfaces InterfaceBody
                             | Modifiers INTERFACE Identifier  InterfaceBody
                             | Modifiers INTERFACE Identifier ExtendsInterfaces InterfaceBody'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ExtendsInterfaces(p):
    '''ExtendsInterfaces : EXTENDS InterfaceType
                         | ExtendsInterfaces COMMA InterfaceType'''
    p[0] = Node('CompilationUnit', p[1:])

def p_InterfaceBody(p):
    '''InterfaceBody : LCURL  RCURL 
                    | LCURL InterfaceMemberDeclarations RCURL '''
    p[0] = Node('CompilationUnit', p[1:])

def p_InterfaceMemberDeclarations(p):
    '''InterfaceMemberDeclarations : InterfaceMemberDeclaration
                                    | InterfaceMemberDeclarations InterfaceMemberDeclaration'''
    p[0] = Node('CompilationUnit', p[1:])

def p_InterfaceMemberDeclaration(p):
    '''InterfaceMemberDeclaration : ConstantDeclaration
                                  | AbstractMethodDeclaration'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ConstantDeclaration(p):
    '''ConstantDeclaration : FieldDeclaration'''
    p[0] = Node('CompilationUnit', p[1:])

def p_AbstractMethodDeclaration(p):
    '''AbstractMethodDeclaration : MethodHeader SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

#19.10 Productions from §10: Arrays
def p_ArrayInitializer(p):
    '''ArrayInitializer : LCURL RCURL 
                        | LCURL COMMA RCURL 
                        | LCURL VariableInitializers  RCURL 
                        | LCURL VariableInitializers COMMA RCURL '''
    p[0] = Node('CompilationUnit', p[1:])

def p_VariableInitializers(p):
    '''VariableInitializers :  VariableInitializer
                         |  VariableInitializers COMMA VariableInitializer'''
    p[0] = Node('CompilationUnit', p[1:])



# productions from Blocks and Statements

def p_Block(p):
    '''Block : LCURL BlockStatements RCURL
                | LCURL  RCURL '''
    p[0] = Node('CompilationUnit', p[1:])


def p_BlockStatements(p):
    '''
    BlockStatements : BlockStatement 
                    | BlockStatements BlockStatement
    '''
    p[0] = Node('CompilationUnit', p[1:])

def p_BlockStatement(p):
    '''BlockStatement : LocalVariableDeclarationStatement
                      | Statement'''
    p[0] = Node('CompilationUnit', p[1:])

def p_LocalVariableDeclarationStatement(p):
    '''LocalVariableDeclarationStatement : LocalVariableDeclaration SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

def p_LocalVariableDeclaration(p):
    '''LocalVariableDeclaration : Type VariableDeclarators'''
    p[0] = Node('CompilationUnit', p[1:])

def p_Statement(p):
    '''Statement : StatementWithoutTrailingSubstatement
                            | LabeledStatement
                            | IfThenStatement
                            | IfThenElseStatement
                            | WhileStatement
                            | ForStatement'''
    p[0] = Node('CompilationUnit', p[1:])

def p_StatementNoShortIf(p):
    '''StatementNoShortIf : StatementWithoutTrailingSubstatement
                                    | LabeledStatementNoShortIf
                                    | IfThenElseStatementNoShortIf
                                    | WhileStatementNoShortIf
                                    | ForStatementNoShortIf'''
    p[0] = Node('CompilationUnit', p[1:])


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
    p[0] = Node('CompilationUnit', p[1:])

def p_EmptyStatement(p):
    '''EmptyStatement : SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

def p_LabeledStatement(p):
    '''LabeledStatement : Identifier COLON Statement'''
    p[0] = Node('CompilationUnit', p[1:])

def p_LabeledStatementNoShortIf(p):
    '''LabeledStatementNoShortIf :  Identifier COLON StatementNoShortIf'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ExpressionStatement(p):
    '''ExpressionStatement : StatementExpression SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

def p_StatementExpression(p):
    '''StatementExpression : Assignment
                                    | PreIncrementExpression
                                    | PreDecrementExpression
                                    | PostIncrementExpression
                                    | PostDecrementExpression
                                    | MethodInvocation
                                    | ClassInstanceCreationExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_IfThenStatement(p):
    '''IfThenStatement : IF LPAR Expression RPAR Statement'''
    p[0] = Node('CompilationUnit', p[1:])

def p_IfThenElseStatement(p):
    '''IfThenElseStatement : IF LPAR Expression RPAR StatementNoShortIf ELSE Statement'''
    p[0] = Node('CompilationUnit', p[1:])

def p_IfThenElseStatementNoShortIf(p):
    '''IfThenElseStatementNoShortIf : IF LPAR Expression RPAR StatementNoShortIf ELSE StatementNoShortIf'''
    p[0] = Node('CompilationUnit', p[1:])

def p_SwitchStatement(p):
    '''SwitchStatement : SWITCH LPAR Expression RPAR SwitchBlock'''
    p[0] = Node('CompilationUnit', p[1:])

def p_SwitchBlock(p):
    '''SwitchBlock : LCURL SwitchBlockStatementGroups SwitchLabels RCURL
                    | LCURL SwitchBlockStatementGroups  RCURL
                    | LCURL  SwitchLabels RCURL
                    | LCURL  RCURL '''
    p[0] = Node('CompilationUnit', p[1:])

def p_SwitchBlockStatementGroups(p):
    '''SwitchBlockStatementGroups : SwitchBlockStatementGroup
                                    | SwitchBlockStatementGroups SwitchBlockStatementGroup'''
    p[0] = Node('CompilationUnit', p[1:])

def p_SwitchBlockStatementGroup(p):
    '''SwitchBlockStatementGroup :  SwitchLabels BlockStatements'''
    p[0] = Node('CompilationUnit', p[1:])

def p_SwitchLabels(p):
    '''SwitchLabels : SwitchLabel
                            | SwitchLabels SwitchLabel'''
    p[0] = Node('CompilationUnit', p[1:])

def p_SwitchLabel(p):
    '''SwitchLabel : CASE ConstantExpression COLON
                            | DEFAULT COLON '''
    p[0] = Node('CompilationUnit', p[1:])
    p[0] = Node('CompilationUnit', p[1:])

def p_WhileStatement(p):
    '''WhileStatement : WHILE LPAR Expression RPAR Statement'''
    p[0] = Node('CompilationUnit', p[1:])

def p_WhileStatementNoShortIf(p):
    '''WhileStatementNoShortIf : WHILE LPAR Expression RPAR StatementNoShortIf'''
    p[0] = Node('CompilationUnit', p[1:])

def p_DoStatement(p):
    '''DoStatement : DO Statement WHILE LPAR Expression RPAR SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

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

    p[0] = Node('CompilationUnit', p[1:])

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
    p[0] = Node('CompilationUnit', p[1:])

def p_ForInit(p):
    '''ForInit : StatementExpressionList 
                        | LocalVariableDeclaration'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ForUpdate(p):
    '''ForUpdate :  StatementExpressionList'''
    p[0] = Node('CompilationUnit', p[1:])

def p_StatementExpressionList(p):
    '''StatementExpressionList : StatementExpression
                                | StatementExpressionList COMMA StatementExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_BreakStatement(p):
    '''BreakStatement   : BREAK Identifier SCOLON 
                        | BREAK SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

def p_ContinueStatement(p):
    '''ContinueStatement :  CONTINUE Identifier SCOLON
                        | CONTINUE SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

def p_ReturnStatement(p):
    '''ReturnStatement : RETURN Expression SCOLON 
                        | RETURN SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

def p_ThrowStatement(p):
    '''ThrowStatement : THROW Expression SCOLON '''
    p[0] = Node('CompilationUnit', p[1:])

def p_SynchronizedStatement(p):
    '''SynchronizedStatement :  SYNCHRONIZED LPAR Expression RPAR Block'''

    p[0] = Node('CompilationUnit', p[1:])

def p_TryStatement(p):
    '''TryStatement : TRY Block Catches
                            | TRY Block Catches Finally
                            | TRY Block Finally'''
    p[0] = Node('CompilationUnit', p[1:])

def p_Catches(p):
    '''Catches : CatchClause
                        | Catches CatchClause'''
    p[0] = Node('CompilationUnit', p[1:])

def p_CatchClause(p):
    '''CatchClause : CATCH LPAR FormalParameter RPAR Block'''
    p[0] = Node('CompilationUnit', p[1:])

def p_Finally(p):
    '''Finally : FINALLY Block'''

#Expressions
    p[0] = Node('CompilationUnit', p[1:])

def p_Primary(p):
    '''Primary : PrimaryNoNewArray
               | ArrayCreationExpression'''

    p[0] = Node('CompilationUnit', p[1:])

def p_PrimaryNoNewArray(p):
    '''PrimaryNoNewArray  : Literal
                          | THIS
                          | LPAR Expression RPAR
                          | ClassInstanceCreationExpression
                          | FieldAccess
                          | MethodInvocation
                          | ArrayAccess'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ClassInstanceCreationExpression(p):
    '''ClassInstanceCreationExpression : NEW ClassType LPAR  RPAR 
                                       | NEW ClassType LPAR ArgumentList RPAR '''
    p[0] = Node('CompilationUnit', p[1:])

def p_ArgumentList(p):
    '''ArgumentList : Expression
                    | ArgumentList COMMA Expression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ArrayCreationExpression(p):
    '''ArrayCreationExpression  : NEW PrimitiveType DimExprs 
                                | NEW PrimitiveType DimExprs Dims
                                | NEW ClassOrInterfaceType DimExprs 
                                | NEW ClassOrInterfaceType DimExprs Dims '''

    p[0] = Node('CompilationUnit', p[1:])

def p_DimExprs(p):
    '''DimExprs : DimExpr
                | DimExprs DimExpr'''
    p[0] = Node('CompilationUnit', p[1:])

def p_DimExpr(p):
    '''DimExpr : LSQR Expression RSQR '''
    p[0] = Node('CompilationUnit', p[1:])

def p_Dims(p):
    '''Dims : LSQR RSQR
            | Dims LSQR RSQR '''
    p[0] = Node('CompilationUnit', p[1:])

def p_FieldAccess(p):
    '''FieldAccess : Primary POINT Identifier
                   | SUPER POINT Identifier '''
    p[0] = Node('CompilationUnit', p[1:])

def p_MethodInvocation(p):
    '''MethodInvocation : Name LPAR RPAR
                        |  Name LPAR ArgumentList RPAR
                        | Primary POINT Identifier LPAR RPAR
                        | Primary POINT Identifier LPAR ArgumentList RPAR
                        | SUPER POINT Identifier LPAR RPAR 
                        | SUPER POINT Identifier LPAR ArgumentList RPAR '''
    p[0] = Node('CompilationUnit', p[1:])

def p_ArrayAccess(p):
    '''ArrayAccess : Name LSQR Expression RSQR
                   | PrimaryNoNewArray LSQR Expression RSQR '''

    p[0] = Node('CompilationUnit', p[1:])

def p_PostfixExpression(p):
    '''PostfixExpression : Primary
                         | Name
                         | PostIncrementExpression
                         | PostDecrementExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_PostIncrementExpression(p):
    '''PostIncrementExpression : PostfixExpression DPLUS '''

    p[0] = Node('CompilationUnit', p[1:])

def p_PostDecrementExpression(p):
    '''PostDecrementExpression : PostfixExpression DMINUS '''
    p[0] = Node('CompilationUnit', p[1:])

def p_UnaryExpression(p):
    '''UnaryExpression  : PreIncrementExpression
                        | PreDecrementExpression
                        | PLUS UnaryExpression
                        | MINUS UnaryExpression
                        | UnaryExpressionNotPlusMinus '''
    p[0] = Node('CompilationUnit', p[1:])

def p_PreIncrementExpression(p):
    '''PreIncrementExpression : DPLUS UnaryExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_PreDecrementExpression(p):
    '''PreDecrementExpression : DMINUS UnaryExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_UnaryExpressionNotPlusMinus(p):
    '''UnaryExpressionNotPlusMinus  : PostfixExpression
                                    | TILDE UnaryExpression
                                    | EXCLAIM UnaryExpression
                                    | CastExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_CastExpression(p):
    '''CastExpression   : LPAR PrimitiveType RPAR UnaryExpression
                        | LPAR PrimitiveType Dims RPAR UnaryExpression
                        | LPAR Expression RPAR UnaryExpressionNotPlusMinus
                        | LPAR Name Dims RPAR UnaryExpressionNotPlusMinus'''
    p[0] = Node('CompilationUnit', p[1:])

def p_MultiplicativeExpression(p):
    '''MultiplicativeExpression : UnaryExpression
                                | MultiplicativeExpression STAR UnaryExpression
                                | MultiplicativeExpression FSLASH UnaryExpression
                                | MultiplicativeExpression MOD UnaryExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_AdditiveExpression(p):
    '''AdditiveExpression : MultiplicativeExpression
                          | AdditiveExpression PLUS MultiplicativeExpression
                          | AdditiveExpression MINUS MultiplicativeExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ShiftExpression(p):
    '''ShiftExpression  : AdditiveExpression
                        | ShiftExpression LSHIFT AdditiveExpression
                        | ShiftExpression RSHIFT AdditiveExpression
                        | ShiftExpression URSHIFT AdditiveExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_RelationalExpression(p):
    '''RelationalExpression : ShiftExpression
                            | RelationalExpression LETHAN ShiftExpression
                            | RelationalExpression GRTHAN ShiftExpression
                            | RelationalExpression LEEQ ShiftExpression
                            | RelationalExpression GREQ ShiftExpression
                            | RelationalExpression INSTANCEOF ReferenceType'''
    p[0] = Node('CompilationUnit', p[1:])

def p_EqualityExpression(p):
    '''EqualityExpression   : RelationalExpression
                            | EqualityExpression DEQ RelationalExpression
                            | EqualityExpression NTEQ RelationalExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_AndExpression(p):
    '''AndExpression : EqualityExpression
                     | AndExpression AND EqualityExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ExclusiveOrExpression(p):
    '''ExclusiveOrExpression : AndExpression
                             | ExclusiveOrExpression XOR AndExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_InclusiveOrExpression(p):
    '''InclusiveOrExpression : ExclusiveOrExpression
                             | InclusiveOrExpression OR ExclusiveOrExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ConditionalAndExpression(p):
    '''ConditionalAndExpression : InclusiveOrExpression
                                | ConditionalAndExpression DAND InclusiveOrExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ConditionalOrExpression(p):
    '''ConditionalOrExpression  : ConditionalAndExpression
                                | ConditionalOrExpression DOR ConditionalAndExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ConditionalExpression(p):
    '''ConditionalExpression : ConditionalOrExpression
                             | ConditionalOrExpression QMARK Expression COLON ConditionalExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_AssignmentExpression(p):
    '''AssignmentExpression : ConditionalExpression
                            | Assignment'''
    p[0] = Node('CompilationUnit', p[1:])

def p_Assignment(p):
    '''Assignment : LeftHandSide AssignmentOperator AssignmentExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_LeftHandSide(p):
    '''LeftHandSide : Name
                    | FieldAccess
                    | ArrayAccess'''
    p[0] = Node('CompilationUnit', p[1:])

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
    p[0] = Node('CompilationUnit', p[1:])

def p_Expression(p):
    '''Expression : AssignmentExpression'''
    p[0] = Node('CompilationUnit', p[1:])

def p_ConstantExpression(p):
    '''ConstantExpression : Expression'''
    p[0] = Node('CompilationUnit', p[1:])

parser = yacc.yacc()     # Return parser object
result_output = parser.parse(input_data+'\n',lexer=lexer,debug=True)

count = 1
def number_nodes(node):
    global count
    node.num = count
    count += 1
    for c in node.children:
        if isinstance(c, Node):
            number_nodes(c)
    c_list = []
    for x in node.children:
        if isinstance(x, Node):
            c_list += [x]
        else:
            c_list += [(x, count)]
            count += 1
    node.children = c_list




# create dot script from node information         
def create_dot_script(node):
    def make_nodes(node):
        y = str(node.num) + f' [label="{node.name}"]\n'
        for c in node.children:
            if isinstance(c, Node):
                y += f'{node.num} -- {c.num}\n'
                y += make_nodes(c)
            else:
                if '"' not in c[0]:
                    y += str(c[1]) + f' [label="{c[0]}"]\n'
                else:
                    y += str(c[1]) + f' [label={c[0]}]\n'    #handling string
                y += f'{node.num} -- {c[1]}\n'
        return y
    sc = 'strict graph G {\n'
    sc += make_nodes(node)
    sc += '}'
    return sc


# create dot script
# prune_node(result)
number_nodes(result_output) #number nodes to remove duplicates
with open("graph.dot", 'w') as f:
    f.write(create_dot_script(result_output))

