from lex import tokens
import ply.yacc as yacc 
import argparse


parser = argparse.ArgumentParser()


# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------

import sys
inarg=sys.argv
inputfilename= inarg[1]
file = open(inputfilename, 'r')
newdata = file.read(-1)
file.close()

# --------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------



parser = argparse.ArgumentParser()
parser.add_argument('inp', type=str, help='Input Java file')
parser.add_argument('--out', type=str, dest='out', help='Output dot script')
args = parser.parse_args()

# start = 'translation_unit'
# define grammar and actions

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



def p_Goal(p):
    '''Goal : CompilationUnit   '''
    p[0] = Node('Goal', p[1:])


# Types, Values, Variables

def p_Type(p):
    '''Type : PrimitiveType
                | ReferenceType'''
    p[0] = Node('Type', p[1:])

def p_PrimitiveType(p):
    '''PrimitiveType : NumericType
                        | boolean'''
    p[0] = Node('PrimitiveType', p[1:])

def p_NumericType(p):
    '''NumericType : IntegralType
                    | FloatingPointType'''
    p[0] = Node('NumericType', p[1:])

def p_IntegralType(p):
    '''IntegralType : byte
                    | short
                    | int
                    | long
                    | char '''
    p[0] = Node('IntegralType', p[1:])
    

def p_FloatingPointType(p):
    '''FloatingPointType : float
                            | double '''
    p[0] = Node('FloatingPointType', p[1:])

def p_ReferenceType(p):
    '''ReferenceType : ClassOrInterfaceType
                        | ArrayType'''
    p[0] = Node('ReferenceType', p[1:])

def p_ClassOrInterfaceType(p):
    '''ClassOrInterfaceType : Name'''
    p[0] = Node('ClassOrInterfaceType', p[1:])

def p_ClassType(p):
    '''ClassType : ClassOrInterfaceType'''
    p[0] = Node('ClassType', p[1:])
    
def p_InterfaceType(p):
    '''InterfaceType : ClassOrInterfaceType'''
    p[0] = Node('InterfaceType', p[1:])

def p_ArrayType(p):
    '''ArrayType : PrimitiveType '[' ']' 
                    | Name '[' ']' 
                    | ArrayType '[' ']' '''
    p[0] = Node('ArrayType', p[1:])

# Names

def p_Name(p):
    '''Name : SimpleName
                | QualifiedName '''
    p[0] = Node('Name', p[1:])

def p_SimpleName(p):
    ''' SimpleName : Identifier '''
    p[0] = Node('SimpleName', p[1:])

def p_QualifiedName(p):
    '''QualifiedName : Name '.' Identifier '''
    p[0] = Node('QualifiedName', p[1:])








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
    p[0] = Node('ImportDeclaration', p[1:])

def p_TypeDeclarations(p):
    '''TypeDeclarations : TypeDeclaration
                        | TypeDeclarations TypeDeclaration'''
    p[0] = Node('TypeDeclarations', p[1:])

def p_PackageDeclaration(p):
    '''PackageDeclaration : package Name ';' '''
    p[0] = Node('PackageDeclaration', p[1:])

def p_ImportDeclaration(p):
    '''ImportDeclaration : SingleTypeImportDeclaration
                         | TypeImportOnDemandDeclaration'''
    p[0] = Node('ImportDeclaration', p[1:])

def p_SingleTypeImportDeclaration(p):
    '''SingleTypeImportDeclaration : import Name ';' '''
    p[0] = Node('SingleTypeImportDeclaration', p[1:])

def p_TypeImportOnDemandDeclaration(p):
    '''TypeImportOnDemandDeclaration : import Name '.' '*' ';' '''
    p[0] = Node('TypeImportOnDemandDeclaration', p[1:])

def p_TypeDeclaration(p):
    '''TypeDeclaration : ClassDeclaration
                       | InterfaceDeclaration
                       | ';' '''
    p[0] = Node('TypeDeclaration', p[1:])

def p_Modifiers(p):
    '''Modifiers : Modifier
                 | Modifiers Modifier'''
    p[0] = Node('Modifiers', p[1:])

def p_Modifier(p):
    '''Modifier : public
                | protected 
                | private
                | static
                | abstract 
                | final 
                | native 
                | synchronized 
                | transient 
                | volatile'''
    p[0] = Node('Modifier', p[1:])


def p_ClassDeclaration(p):
    '''ClassDeclaration : Modifiers class Identifier Super Interfaces ClassBody
                        | Modifiers class Identifier Super ClassBody
                        | Modifiers class Identifier Interfaces ClassBody
                        | class Identifier Super Interfaces ClassBody
                        | Modifiers class Identifier ClassBody
                        | class Identifier Interfaces ClassBody
                        | class Identifier Super ClassBody
                        | class Identifier ClassBody '''
    p[0] = Node('ClassDeclaration', p[1:])

def p_Super(p):
    '''Super : extends ClassType'''
    p[0] = Node('Super', p[1:])

def p_Interfaces(p):
    '''Interfaces : implements InterfaceTypeList'''
    p[0] = Node('Interfaces', p[1:])

def p_InterfaceTypeList(p):
    '''InterfaceTypeList : InterfaceType
                         | InterfaceTypeList ',' InterfaceType'''
    p[0] = Node('InterfaceTypeList', p[1:])

def p_ClassBody(p):
    '''ClassBody : '{' ClassBodyDeclarations '}' 
                 | '{' '}' '''
    p[0] = Node('ClassBody', p[1:])

def p_ClassBodyDeclarations(p):
    '''ClassBodyDeclarations : ClassBodyDeclaration
                             | ClassBodyDeclarations ClassBodyDeclaration'''
    p[0] = Node('ClassBodyDeclarations', p[1:])

def p_ClassBodyDeclaration(p):
    '''ClassBodyDeclaration : ClassMemberDeclaration
                            | StaticInitializer
                            | ConstructorDeclaration'''
    p[0] = Node('ClassBodyDeclaration', p[1:])

def p_ClassMemberDeclaration(p):
    '''ClassMemberDeclaration : FieldDeclaration
                              | MethodDeclaration'''
    p[0] = Node('ClassMemberDeclaration', p[1:])

    
def p_FieldDeclaration(p):
    '''FieldDeclaration : Modifiers Type VariableDeclarators ';'
                        | Type VariableDeclarators ';' '''
    p[0] = Node('FieldDeclaration', p[1:])

def p_VariableDeclarators(p):
    '''VariableDeclarators : VariableDeclarator
                           | VariableDeclarators ',' VariableDeclarator'''
    p[0] = Node('VariableDeclarators', p[1:])

def p_VariableDeclarator(p):
    '''VariableDeclarator : VariableDeclaratorId
                          | VariableDeclaratorId '=' VariableInitializer'''
    p[0] = Node('VariableDeclarator', p[1:])

def p_VariableDeclaratorId(p):
    '''VariableDeclaratorId : Identifier
                            | VariableDeclaratorId '[' ']' '''
    p[0] = Node('QualifiedName', p[1:])

def p_VariableInitializer(p):
    '''VariableInitializer : Expression
                           | ArrayInitializer'''
    p[0] = Node('QualifiedName', p[1:])

#9.8.3 Productions from §8.4: Method Declarations

def p_MethodDeclaration(p):
    '''MethodDeclaration : MethodHeader MethodBody'''
    p[0] = Node('QualifiedName', p[1:])

def p_MethodHeader(p):
    '''MethodHeader : Type MethodDeclarator
                    | Type MethodDeclarator Throws
                    | Modifiers Type MethodDeclarator 
                    | Modifiers Type MethodDeclarator Throws
                    | void MethodDeclarator 
                    | void MethodDeclarator Throws
                    | Modifiers void MethodDeclarator
                    | Modifiers void MethodDeclarator Throws'''
    p[0] = Node('QualifiedName', p[1:])

def p_MethodDeclarator(p):
    '''MethodDeclarator : Identifier '(' ')'
                        | Identifier '(' FormalParameterList ')'
                        | MethodDeclarator '[' ']' '''
    p[0] = Node('QualifiedName', p[1:])

def p_FormalParameterList(p):
    '''FormalParameterList : FormalParameter
                            | FormalParameterList ',' FormalParameter'''
    p[0] = Node('QualifiedName', p[1:])

def p_FormalParameter(p):
    '''FormalParameter : Type VariableDeclaratorId'''
    p[0] = Node('QualifiedName', p[1:])

def p_Throws(p):
    '''Throws : throws ClassTypeList'''
    p[0] = Node('QualifiedName', p[1:])

def p_ClassTypeList(p):
    '''ClassTypeList : ClassType
                     | ClassTypeList ',' ClassType'''
    p[0] = Node('QualifiedName', p[1:])

def p_MethodBody(p):
    '''MethodBody : Block 
                   | ';' '''
    p[0] = Node('QualifiedName', p[1:])

#19.8.4 Productions from §8.5: Static Initializers

def p_StaticInitializer(p):
    '''StaticInitializer : static Block'''
    p[0] = Node('QualifiedName', p[1:])

#19.8.5 Productions from §8.6: Constructor Declarations
def p_ConstructorDeclaration(p):
    '''ConstructorDeclaration :   ConstructorDeclarator  ConstructorBody
                                |  ConstructorDeclarator Throws ConstructorBody
                                | Modifiers ConstructorDeclarator  ConstructorBody
                                | Modifiers ConstructorDeclarator Throws ConstructorBody'''
    p[0] = Node('QualifiedName', p[1:])

def p_ConstructorDeclarator(p):
    '''ConstructorDeclarator : SimpleName '(' ')' 
                             | SimpleName '(' FormalParameterList ')' '''
    p[0] = Node('QualifiedName', p[1:])

def p_ConstructorBody(p):
    '''ConstructorBody : '{'  '}' 
                       | '{'  BlockStatements '}'
                       | '{' ExplicitConstructorInvocation  '}'
                       | '{' ExplicitConstructorInvocation BlockStatements '}' '''
    p[0] = Node('QualifiedName', p[1:])

def p_ExplicitConstructorInvocation(p):
    '''ExplicitConstructorInvocation : this '(' ')' ';'
                                    | this '(' ArgumentList ')' ';'
                                    | super '('  ')' ';' 
                                     | super '(' ArgumentList ')' ';' '''
    p[0] = Node('QualifiedName', p[1:])

#19.9 Productions from §9: Interfaces
#19.9.1 Productions from §9.1: Interface Declarations

def p_InterfaceDeclaration(p):
    '''InterfaceDeclaration :  interface Identifier  InterfaceBody 
                             |  interface Identifier ExtendsInterfaces InterfaceBody
                             | Modifiers interface Identifier  InterfaceBody
                             | Modifiers interface Identifier ExtendsInterfaces InterfaceBody'''
    p[0] = Node('QualifiedName', p[1:])

def p_ExtendsInterfaces(p):
    '''ExtendsInterfaces : extends InterfaceType
                         | ExtendsInterfaces ',' InterfaceType'''
    p[0] = Node('QualifiedName', p[1:])

def p_InterfaceBody(p):
    '''InterfaceBody : '{'  '}' 
                    | '{' InterfaceMemberDeclarations '}' '''
    p[0] = Node('QualifiedName', p[1:])

def p_InterfaceMemberDeclarations(p):
    '''InterfaceMemberDeclarations : InterfaceMemberDeclaration
                                    | InterfaceMemberDeclarations InterfaceMemberDeclaration'''
    p[0] = Node('QualifiedName', p[1:])

def p_InterfaceMemberDeclaration(p):
    '''InterfaceMemberDeclaration : ConstantDeclaration
                                  | AbstractMethodDeclaration'''
    p[0] = Node('QualifiedName', p[1:])

def p_ConstantDeclaration(p):
    '''ConstantDeclaration : FieldDeclaration'''
    p[0] = Node('QualifiedName', p[1:])

def p_AbstractMethodDeclaration(p):
    '''AbstractMethodDeclaration : MethodHeader ';' '''
    p[0] = Node('QualifiedName', p[1:])

#19.10 Productions from §10: Arrays
def p_ArrayInitializer(p):
    '''ArrayInitializer : '{'   '}' 
                        | '{'  comma '}' 
                        | '{' VariableInitializers  '}' 
                        | '{' VariableInitializers comma '}' '''
    p[0] = Node('QualifiedName', p[1:])

def p_VariableInitializers(p):
    '''VariableInitializer :  VariableInitializer
                         |  VariableInitializers ',' VariableInitializer'''
    p[0] = Node('QualifiedName', p[1:])













# productions from Blocks and Statements

def p_Block(p):
	'''Block : '{' BlockStatements '}'
				| '{'  '}' '''
	p[0] = Node('Block', p[1:])


def p_BlockStatements(p):
	'''
	BlockStatements : BlockStatement 
						| BlockStatements BlockStatement
	'''
	p[0] = Node('BlockStatements', p[1:])


def p_BlockStatement(p):
	'''BlockStatement : LocalVariableDeclarationStatement
								| Statement'''
	p[0] = Node('BlockStatement', p[1:])

def p_LocalVariableDeclarationStatement(p):
	'''LocalVariableDeclarationStatement : LocalVariableDeclaration ';' '''
	p[0] = Node('LocalVariableDeclarationStatement', p[1:])

def p_LocalVariableDeclaration(p):
	'''LocalVariableDeclaration : Type VariableDeclarators'''
	p[0] = Node('LocalVariableDeclaration', p[1:])

def p_Statement(p):
	'''Statement : StatementWithoutTrailingSubstatement
							| LabeledStatement
							| IfThenStatement
							| IfThenElseStatement
							| WhileStatement
							| ForStatement'''
	p[0] = Node('Statement', p[1:])

def p_StatementNoShortIf(p):
	'''StatementNoShortIf : StatementWithoutTrailingSubstatement
									| LabeledStatementNoShortIf
									| IfThenElseStatementNoShortIf
									| WhileStatementNoShortIf
									| ForStatementNoShortIf'''
	p[0] = Node('StatementNoShortIf', p[1:])


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
	p[0] = Node('StatementWithoutTrailingSubstatement', p[1:])


def p_EmptyStatement(p):
	'''EmptyStatement : ';' '''
	p[0] = Node('EmptyStatement', p[1:])


def p_LabeledStatement(p):
	'''LabeledStatement : Identifier ':' Statement'''
	p[0] = Node('LabeledStatement', p[1:])


def p_LabeledStatementNoShortIf(p):
	'''LabeledStatementNoShortIf :	Identifier ':' StatementNoShortIf'''
	p[0] = Node('LabeledStatementNoShortIf', p[1:])


def p_ExpressionStatement(p):
	'''ExpressionStatement : StatementExpression ';' '''
	p[0] = Node('ExpressionStatement', p[1:])


def p_StatementExpression(p):
	'''StatementExpression : Assignment
									| PreIncrementExpression
									| PreDecrementExpression
									| PostIncrementExpression
									| PostDecrementExpression
									| MethodInvocation
									| ClassInstanceCreationExpression'''
	p[0] = Node('StatementExpression', p[1:])


def p_IfThenStatement(p):
	'''IfThenStatement : if '(' Expression ')' Statement'''
	p[0] = Node('IfThenStatement', p[1:])


def p_IfThenElseStatement(p):
	'''IfThenElseStatement : if '(' Expression ')' StatementNoShortIf else Statement'''
	p[0] = Node('IfThenElseStatement', p[1:])


def p_IfThenElseStatementNoShortIf(p):
	'''IfThenElseStatementNoShortIf : if '(' Expression ')' StatementNoShortIf else StatementNoShortIf'''
	p[0] = Node('IfThenElseStatementNoShortIf', p[1:])


def p_SwitchStatement(p):
	'''SwitchStatement : switch '(' Expression ')' SwitchBlock'''
	p[0] = Node('SwitchStatement', p[1:])


def p_SwitchBlock(p):
	'''SwitchBlock : '{' SwitchBlockStatementGroups SwitchLabels '}'
					| '{' SwitchBlockStatementGroups  '}'
					| '{'  SwitchLabels '}'
					| '{'  '}' '''
	p[0] = Node('SwitchBlock', p[1:])


def p_SwitchBlockStatementGroups(p):
	'''SwitchBlockStatementGroups : SwitchBlockStatementGroup
									| SwitchBlockStatementGroups SwitchBlockStatementGroup'''
	p[0] = Node('SwitchBlockStatementGroups', p[1:])


def p_SwitchBlockStatementGroup(p):
	'''SwitchBlockStatementGroup :	SwitchLabels BlockStatements'''
	p[0] = Node('SwitchBlockStatementGroup', p[1:])


def p_SwitchLabels(p):
	'''SwitchLabels : SwitchLabel
							| SwitchLabels SwitchLabel'''
	p[0] = Node('SwitchLabels', p[1:])


def p_SwitchLabel(p):
	'''SwitchLabel : case ConstantExpression ':'
							| default ':' '''
	p[0] = Node('SwitchLabel', p[1:])


def p_WhileStatement(p):
	'''WhileStatement : while '(' Expression ')' Statement'''
	p[0] = Node('WhileStatement', p[1:])


def p_WhileStatementNoShortIf(p):
	'''WhileStatementNoShortIf : while '(' Expression ')' StatementNoShortIf'''
	p[0] = Node('WhileStatementNoShortIf', p[1:])


def p_DoStatement(p):
	'''DoStatement : do Statement while '(' Expression ')' ';' '''
	p[0] = Node('DoStatement', p[1:])


def p_ForStatement(p):
	'''ForStatement : for '(' ForInit ';' Expression ';' ForUpdate ')' Statement
					| for '('  ';' Expression ';' ForUpdate ')' Statement
					| for '(' ForInit ';'  ';' ForUpdate ')' Statement
					| for '(' ForInit ';' Expression ';'  ')' Statement
					| for '('  ';'  ';' ForUpdate ')' Statement
					| for '(' ForInit ';'  ';'  ')' Statement
					| for '('  ';' Expression ';'  ')' Statement
					| for '('  ';'  ';'  ')' Statement
					'''
	p[0] = Node('ForStatement', p[1:])


def p_ForStatementNoShortIf(p):
	'''ForStatementNoShortIf : for '(' ForInit ';' Expression ';' ForUpdate ')'	StatementNoShortIf
								| for '('  ';' Expression ';' ForUpdate ')'	StatementNoShortIf
								| for '(' ForInit ';'  ';' ForUpdate ')'	StatementNoShortIf
								| for '(' ForInit ';' Expression ';'  ')'	StatementNoShortIf
								| for '('  ';'  ';' ForUpdate ')'	StatementNoShortIf
								| for '(' ForInit ';'  ';'  ')'	StatementNoShortIf
								| for '('  ';' Expression ';'  ')'	StatementNoShortIf
								| for '('  ';'  ';'  ')'	StatementNoShortIf
								'''
	p[0] = Node('ForStatementNoShortIf', p[1:])

def p_ForInit(p):
	'''ForInit : StatementExpressionList 
						| LocalVariableDeclaration'''
	p[0] = Node('ForInit', p[1:])

def p_ForUpdate(p):
	'''ForUpdate :	StatementExpressionList'''
	p[0] = Node('ForUpdate', p[1:])

def p_StatementExpressionList(p):
	'''StatementExpressionList : StatementExpression
								| StatementExpressionList ',' StatementExpression'''
	p[0] = Node('StatementExpressionList', p[1:])


def p_BreakStatement(p):
	'''BreakStatement : break Identifier ';' 
						| break ';' '''
	p[0] = Node('BreakStatement', p[1:])


def p_ContinueStatement(p):
	'''ContinueStatement :	continue Identifier ';' 
						| continue  ';' '''
	p[0] = Node('ContinueStatement', p[1:])

def p_ReturnStatement(p):
	'''ReturnStatement : return Expression ';' 
						| return  ';' '''
	p[0] = Node('ReturnStatement', p[1:])


def p_ThrowStatement(p):
	'''ThrowStatement : throw Expression ';' '''
	p[0] = Node('ThrowStatement', p[1:])


def p_SynchronizedStatement(p):
	'''SynchronizedStatement :	synchronized '(' Expression ')' Block'''
	p[0] = Node('SynchronizedStatement', p[1:])


def p_TryStatement(p):
	'''TryStatement : try Block Catches
							| try Block Catches Finally
							| try Block Finally'''
	p[0] = Node('TryStatement', p[1:])


def p_Catches(p):
	'''Catches : CatchClause
						| Catches CatchClause'''
	p[0] = Node('Catches', p[1:])

def p_CatchClause(p):
	'''CatchClause : catch '(' FormalParameter ')' Block'''
	p[0] = Node('CatchClause', p[1:])


def p_Finally(p):
	'''Finally : finally Block'''
	p[0] = Node('Finally', p[1:])



#Expressions

def p_Primary(p):
    '''Primary : PrimaryNoNewArray
               | ArrayCreationExpression'''


def p_PrimaryNoNewArray(p):
    '''PrimaryNoNewArray  : Literal
                          | this
                          | '(' Expression ')'
                          | ClassInstanceCreationExpression
                          | FieldAccess
                          | MethodInvocation
                          | ArrayAccess'''

def p_ClassInstanceCreationExpression(p):
    '''ClassInstanceCreationExpression : new ClassType '('  ')' 
                                       : new ClassType '(' ArgumentList ')' '''

def p_ArgumentList(p):
    '''ArgumentList : Expression
                    | ArgumentList ',' Expression'''

def p_ArrayCreationExpression(p):
    '''ArrayCreationExpression  : new PrimitiveType DimExprs 
                                | new PrimitiveType DimExprs Dims
                                | new ClassOrInterfaceType DimExprs 
                                | new ClassOrInterfaceType DimExprs Dims '''


def p_DimExprs(p):
    '''DimExprs : DimExpr
                | DimExprs DimExpr'''

def p_DimExpr(p):
    '''DimExpr : '[' Expression ']' '''

def p_Dims(p):
    '''Dims : '[' ']'
            | Dims '[' ']' '''

def p_FieldAccess(p):
    '''FieldAccess : Primary '.' Identifier
                   | super '.' Identifier '''

def p_MethodInvocation(p):
    '''MethodInvocation : Name '('  ')'
                        |  Name '(' ArgumentList ')'
                        | Primary '.' Identifier '('  ')'
                        | Primary '.' Identifier '(' ArgumentList ')'
                        | super '.' Identifier '('  ')' 
                        | super '.' Identifier '(' ArgumentList ')' '''

def p_ArrayAccess(p):
    '''ArrayAccess : Name '[' Expression ']'
                   | PrimaryNoNewArray '[' Expression ']' '''


def p_PostfixExpression(p):
    '''PostfixExpression : Primary
                         | Name
                         | PostIncrementExpression
                         | PostDecrementExpression'''

def p_PostIncrementExpression(p):
    '''PostIncrementExpression : PostfixExpression PLUSPLUS '''


def p_PostDecrementExpression(p):
    '''PostDecrementExpression : PostfixExpression MINUSMINUS '''

def p_UnaryExpression(p):
    '''UnaryExpression  : PreIncrementExpression
                        | PreDecrementExpression
                        | '+' UnaryExpression
                        | '-' UnaryExpression
                        | UnaryExpressionNotPlusMinus '''

def p_PreIncrementExpression(p):
    '''PreIncrementExpression : PLUSPLUS UnaryExpression'''

def p_PreDecrementExpression(p):
    '''PreDecrementExpression : MINUSMINUS UnaryExpression'''

def p_UnaryExpressionNotPlusMinus(p):
    '''UnaryExpressionNotPlusMinus  : PostfixExpression
                                    | '~' UnaryExpression
                                    | '!' UnaryExpression
                                    | CastExpression'''

def p_CastExpression(p):
    '''CastExpression   : '(' PrimitiveType  ')' UnaryExpression
                        | '(' PrimitiveType Dims ')' UnaryExpression
                        | '(' Expression ')' UnaryExpressionNotPlusMinus
                        | '(' Name Dims ')' UnaryExpressionNotPlusMinus'''

def p_MultiplicativeExpression(p):
    '''MultiplicativeExpression : UnaryExpression
                                | MultiplicativeExpression '*' UnaryExpression
                                | MultiplicativeExpression '/' UnaryExpression
                                | MultiplicativeExpression '%' UnaryExpression'''

def p_AdditiveExpression(p):
    '''AdditiveExpression : MultiplicativeExpression
                          | AdditiveExpression '+' MultiplicativeExpression
                          | AdditiveExpression '-' MultiplicativeExpression'''

def p_ShiftExpression(p):
    '''ShiftExpression  : AdditiveExpression
                        | ShiftExpression LSHIFT AdditiveExpression
                        | ShiftExpression RSHIFT AdditiveExpression
                        | ShiftExpression RRSHIFT AdditiveExpression'''

def p_RelationalExpression(p):
    '''RelationalExpression : ShiftExpression
                            | RelationalExpression '<' ShiftExpression
                            | RelationalExpression '>' ShiftExpression
                            | RelationalExpression LTEQ ShiftExpression
                            | RelationalExpression GTEQ ShiftExpression
                            | RelationalExpression instanceof ReferenceType'''

def p_EqualityExpression(p):
    '''EqualityExpression   : RelationalExpression
                            | EqualityExpression EQ RelationalExpression
                            | EqualityExpression NEQ RelationalExpression'''

def p_AndExpression(p):
    '''AndExpression : EqualityExpression
                     | AndExpression '&' EqualityExpression'''

def p_ExclusiveOrExpression(p):
    '''ExclusiveOrExpression : AndExpression
                             | ExclusiveOrExpression '^' AndExpression'''

def p_InclusiveOrExpression(p):
    '''InclusiveOrExpression : ExclusiveOrExpression
                             | InclusiveOrExpression '|' ExclusiveOrExpression'''

def p_ConditionalAndExpression(p):
    '''ConditionalAndExpression : InclusiveOrExpression
                                | ConditionalAndExpression AND InclusiveOrExpression'''

def p_ConditionalOrExpression(p):
    '''ConditionalOrExpression  : ConditionalAndExpression
                                | ConditionalOrExpression OR ConditionalAndExpression'''

def p_ConditionalExpression(p):
    '''ConditionalExpression : ConditionalOrExpression
                             | ConditionalOrExpression '?' Expression ':' ConditionalExpression'''

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
    '''AssignmentOperator : '='
                            | TIMES_EQUAL
                            | DIVIDE_EQUAL
                            | REMAINDER_EQUAL
                            | PLUS_EQUAL
                            | MINUS_EQUAL
                            | LSHIFT_EQUAL
                            | RSHIFT_EQUAL
                            | RRSHIFT_EQUAL
                            | AND_EQUAL
                            | XOR_EQUAL
                            | OR_EQUAL'''
    p[0] = Node('AssignmentOperator', p[1:])

def p_Expression(p):
    '''Expression : AssignmentExpression'''

def p_ConstantExpression(p):
    '''ConstantExpression : Expression'''