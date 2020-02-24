from lex import tokens
import ply.yacc as yacc 
import argparse


parser = argparse.ArgumentParser()



# fuck

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



# Productions from Packages

def p_CompilationUnit(p):
	'''CompilationUnit : PackageDeclaration ImportDeclarations TypeDeclarations
								| ImportDeclarations TypeDeclarations
								| PackageDeclaration TypeDeclarations
								| TypeDeclarations
								| PackageDeclaration ImportDeclarations
								| ImportDeclarations
								| PackageDeclaration
								| '''
	p[0] = Node('CompilationUnit', p[1:])

def p_Modifiers(p):
	'''Modifiers : Modifiers Modifier
							| Modifier
			'''
	p[0] = Node('Modifiers', p[1:])


def p_Modifier(p):
	'''Modifier : Annotation
				| public
				| protected 
				| private 
				| abstract
				| static
				| final
				| strictfp
				| transient
				| volatile
				| synchronized
				| native
				| default
			'''
	p[0] = Node('Modifier', p[1:])


 
def p_PackageDeclaration(p):
	'''PackageDeclaration : Modifiers package dotIdentifiers
							| package dotIdentifiers'''
	p[0] = Node('PackageDeclaration', p[1:])




def p_dotIdentifiers(p):
	'''dotIdentifiers : dotIdentifiers DOT  Identifier
								| Identifier'''
	p[0] = Node('dotIdentifiers', p[1:])



def p_ImportDeclarations(p):
	'''ImportDeclarations : ImportDeclarations ImportDeclaration 
									| ImportDeclaration
			'''
	p[0] = Node('ImportDeclarations', p[1:])

# change import declarations 

# change import declarations 



def p_ImportDeclaration(p):
	'''ImportDeclaration : SingleTypeImportDeclaration
						| TypeImportOnDemandDeclaration
						| SingleStaticImportDeclaration
						| StaticImportOnDemandDeclaration'''
	p[0] = Node('ImportDeclaration', p[1:])


def p_SingleTypeImportDeclaration(p):
	'''SingleTypeImportDeclaration : import Name ';' '''
	p[0] = Node('SingleTypeImportDeclaration', p[1:])


def p_TypeImportOnDemandDeclaration(p):
	'''TypeImportOnDemandDeclaration : import Name DOT '*' ';' '''
	p[0] = Node('TypeImportOnDemandDeclaration', p[1:])


def p_SingleStaticImportDeclaration(p):
	'''SingleStaticImportDeclaration : import static Name DOT Identifier ';' '''
	p[0] = Node('SingleStaticImportDeclaration', p[1:])


def p_StaticImportOnDemandDeclaration(p):
	'''StaticImportOnDemandDeclaration : import static Name DOT '*' ';' '''
	p[0] = Node('StaticImportOnDemandDeclaration', p[1:])

def p_TypeDeclarations(p): 
	'''TypeDeclarations :  TypeDeclarations TypeDeclaration
							| TypeDeclaration'''
	p[0] = Node('TypeDeclarations', p[1:])

# change TypeDeclarations


def p_TypeDeclaration(p): 
	'''TypeDeclaration : ClassDeclaration 
						| InterfaceDeclaration
						| ';' '''
	p[0] = Node('TypeDeclaration', p[1:])





# Productions from Lexical Steucture
# No need



def p_Type(p):
	'''Type : PrimitiveType
			| ReferenceType'''
	p[0] = Node('Type', p[1:])

# def p_PrimitiveType(p):
# 	'''PrimitiveType : Annotations NumericType
# 					| Annotations boolean'''
# 	p[0] = Node('PrimitiveType', p[1:])


def p_PrimitiveType(p):
	'''PrimitiveType : Annotations NumericType
					| NumericType
					| Annotations boolean
					| boolean '''
	p[0] = Node('PrimitiveType', p[1:])


def p_Annotations(p):
	'''Annotations : Annotations Annotation
					| Annotation'''
	p[0] = Node('Annotations', p[1:])


def p_NumericType(p):
	'''NumericType : IntegralType
					| FloatingPointType'''
	p[0] = Node('NumericType', p[1:])

def p_IntegralType(p):
	'''IntegralType : byte 
					| short
					| int
					| long
					| char'''
	p[0] = Node('IntegralType', p[1:])



def p_FloatingPointType(p):
	'''FloatingPointType : float
							| double'''
	p[0] = Node('FloatingPointType', p[1:])


def p_ReferenceType(p):
	'''ReferenceType : ClassOrInterfaceType 
						| ArrayType'''
	p[0] = Node('ReferenceType', p[1:])




def p_ClassOrInterfaceType(p):
	'''
	ClassOrInterfaceType : Annotations Identifier TypeArguments
				| Annotations Identifier 
				| ClassOrInterfaceType DOT Annotations Identifier TypeArguments
				| ClassOrInterfaceType DOT Annotations Identifier
				| Identifier TypeArguments
				| Identifier 
				| ClassOrInterfaceType DOT Identifier TypeArguments
				| ClassOrInterfaceType DOT Identifier
	'''
	p[0] = Node('ClassOrInterfaceType', p[1:])



def p_ArrayType(p):
	'''
	ArrayType : PrimitiveType Dims 
			| ClassOrInterfaceType Dims
	'''
	p[0] = Node('ArrayType', p[1:])

def p_Dims(p):
	'''Dims : Dims Annotations '[' ']' 
			| Annotations '[' ']'
			| Dims '[' ']' 
			| '[' ']'  '''
	p[0] = Node('Dims', p[1:])


def p_TypeParameter(p): 
	'''TypeParameter : Modifiers Identifier TypeBound
						| Modifiers Identifier
						| Identifier TypeBound
						| Identifier'''
	p[0] = Node('TypeParameter', p[1:])






def p_TypeBound(p):
	'''TypeBound : extends ClassOrInterfaceType AdditionalBounds
							| extends ClassOrInterfaceType 
			'''
	p[0] = Node('TypeBound', p[1:])

def p_AdditionalBounds(p):
	'''AdditionalBounds : AdditionalBounds AdditionalBound
									| AdditionalBound'''
	p[0] = Node('AdditionalBounds', p[1:])


def p_AdditionalBound(p):
	'''AdditionalBound : '&' ClassOrInterfaceType'''
	p[0] = Node('AdditionalBound', p[1:])


def p_TypeArguments(p):
	'''TypeArguments : '<' TypeArgumentList '>' '''
	p[0] = Node('TypeArguments', p[1:])



def p_TypeArgumentList(p):
	'''TypeArgumentList : TypeArgumentList ',' TypeArgument
						| TypeArgument  '''
	p[0] = Node('TypeArgumentList', p[1:])




def p_TypeArgument(p):
	'''TypeArgument : ReferenceType 
							 | Wildcard'''
	p[0] = Node('TypeArgument', p[1:])


def p_Wildcard(p):
	'''Wildcard : Annotations '?' WildcardBounds
				| Annotations '?'
				| '?' WildcardBounds
				| '?' '''
	p[0] = Node('Wildcard', p[1:])
 

def p_WildcardBounds(p):
	'''WildcardBounds : extends ReferenceType 
								| super ReferenceType'''
	p[0] = Node('WildcardBounds', p[1:])



# Production from Names:





def p_Name(p):
	'''Name : SimpleName 
						| QualifiedName 
	'''	
	p[0] = Node('Name', p[1:])

def p_SimpleName(p):
	'''SimpleName : Identifier'''
	p[0] = Node('SimpleName', p[1:])

def p_QualifiedName(p):
	'''QualifiedName : Name DOT Identifier'''
	p[0] = Node('QualifiedName', p[1:])




# Productions from classes


def p_ClassDeclaration(p):
	'''ClassDeclaration : NormalClassDeclaration 
							| EnumDeclaration'''
	p[0] = Node('ClassDeclaration', p[1:])


def p_NormalClassDeclaration(p):
	'''NormalClassDeclaration : Modifiers class Identifier TypeParameters Superclass Superinterfaces ClassBody
										| Modifiers class Identifier Superclass Superinterfaces ClassBody
										| Modifiers class Identifier TypeParameters Superinterfaces ClassBody
										| Modifiers class Identifier TypeParameters Superclass ClassBody
										| Modifiers class Identifier Superinterfaces ClassBody
										| Modifiers class Identifier TypeParameters ClassBody
										| Modifiers class Identifier Superclass ClassBody
										| Modifiers class Identifier ClassBody
										| class Identifier TypeParameters Superclass Superinterfaces ClassBody
										| class Identifier Superclass Superinterfaces ClassBody
										| class Identifier TypeParameters Superinterfaces ClassBody
										| class Identifier TypeParameters Superclass ClassBody
										| class Identifier Superinterfaces ClassBody
										| class Identifier TypeParameters ClassBody
										| class Identifier Superclass ClassBody
										| class Identifier ClassBody'''
	p[0] = Node('NormalClassDeclaration', p[1:])





def p_TypeParameters(p):
	'''TypeParameters : '<' TypeParameterList '>' '''
	p[0] = Node('TypeParameters', p[1:])


def p_TypeParameterList(p):
	'''TypeParameterList : TypeParameterList ',' TypeParameter
									| TypeParameter'''
	p[0] = Node('TypeParameterList', p[1:])


def p_Superclass(p):
	'''Superclass : extends ClassOrInterfaceType'''
	p[0] = Node('Superclass', p[1:])


def p_Superinterfaces(p):
	'''Superinterfaces : implements InterfaceTypeList'''
	p[0] = Node('Superinterfaces', p[1:])


def p_InterfaceTypeList(p):
	'''InterfaceTypeList : InterfaceTypeList ',' ClassOrInterfaceType
							| ClassOrInterfaceType'''
	p[0] = Node('InterfaceTypeList', p[1:])


def p_ClassBody(p): 
	'''ClassBody : '{' ClassBodyDeclarations '}'
					| '{'  '}' '''
	p[0] = Node('ClassBody', p[1:])


def p_ClassBodyDeclarations(p):
	'''ClassBodyDeclarations : ClassBodyDeclarations ClassBodyDeclaration
										| ClassBodyDeclaration'''
	p[0] = Node('ClassBodyDeclarations', p[1:])


def p_ClassBodyDeclaration(p):
	'''ClassBodyDeclaration : ClassMemberDeclaration 
										| InstanceInitializer
										| StaticInitializer 
										| ConstructorDeclaration'''
	p[0] = Node('ClassBodyDeclaration', p[1:])



def p_ClassMemberDeclaration(p):
	'''ClassMemberDeclaration : FieldDeclaration 
										| MethodDeclaration 
										| ClassDeclaration
										| InterfaceDeclaration 
										| ';' '''
	p[0] = Node('ClassMemberDeclaration', p[1:])


def p_FieldDeclaration(p):
	'''FieldDeclaration : Modifiers UnannType VariableDeclaratorList ';'
						| UnannType VariableDeclaratorList ';' '''
	p[0] = Node('FieldDeclaration', p[1:])



def p_VariableDeclaratorList(p):
	'''VariableDeclaratorList : VariableDeclaratorList ',' VariableDeclarator
								| VariableDeclarator'''
	p[0] = Node('VariableDeclaratorList', p[1:])


def p_VariableDeclaratorId(p):
	'''VariableDeclaratorId : Identifier Dims
										| Identifier '''
	p[0] = Node('VariableDeclaratorId', p[1:])


def p_VariableInitializer(p):
	'''VariableInitializer : Expression
									| ArrayInitializer'''
	p[0] = Node('VariableInitializer', p[1:])



def p_UnannType(p):
	'''UnannType : UnannPrimitiveType 
							| UnannReferenceType'''
	p[0] = Node('UnannType', p[1:])


def p_UnannPrimitiveType(p):
	'''UnannPrimitiveType : NumericType
							| boolean'''
	p[0] = Node('UnannPrimitiveType', p[1:])


def p_UnannReferenceType(p):
	'''UnannReferenceType : UnannClassOrInterfaceType
									| UnannArrayType '''
	p[0] = Node('UnannReferenceType', p[1:])


def p_UnannClassOrInterfaceType(p):
	'''UnannClassOrInterfaceType : Identifier TypeArguments
								| UnannClassOrInterfaceType DOT Annotations Identifier TypeArguments
								| UnannClassOrInterfaceType DOT Annotations Identifier 
								| UnannClassOrInterfaceType DOT Identifier TypeArguments
								| UnannClassOrInterfaceType DOT Identifier 
								| Identifier '''
	p[0] = Node('UnannClassOrInterfaceType', p[1:])



def p_UnannArrayType(p):
	'''UnannArrayType : UnannPrimitiveType Dims
								| UnannClassOrInterfaceType Dims
								'''
	p[0] = Node('UnannArrayType', p[1:])


def p_MethodDeclaration(p):
	'''MethodDeclaration : Modifiers MethodHeader MethodBody
							| MethodHeader MethodBody'''
	p[0] = Node('MethodDeclaration', p[1:])


def p_MethodHeader(p):
	'''MethodHeader : Result MethodDeclarator Throws
								| Result MethodDeclarator
								| TypeParameters Annotations Result MethodDeclarator Throws
								| TypeParameters Annotations Result MethodDeclarator
								| TypeParameters Result MethodDeclarator Throws
								| TypeParameters Result MethodDeclarator'''
	p[0] = Node('MethodHeader', p[1:])


def p_Result(p):
	'''Result : UnannType
						| void'''
	p[0] = Node('Result', p[1:])


def p_MethodDeclarator(p):
	'''MethodDeclarator : Identifier '(' FormalParameterList ')' Dims
									| Identifier '(' ')' Dims
									| Identifier '(' FormalParameterList ')' 
									| Identifier '('  ')' '''
	p[0] = Node('MethodDeclarator', p[1:])


def p_FormalParameterList(p):
	'''FormalParameterList : ReceiverParameter
							| FormalParameters ',' LastFormalParameter
							| LastFormalParameter'''
	p[0] = Node('FormalParameterList', p[1:])


def p_comma_FormalParameters(p):
	'''comma_FormalParameters : comma_FormalParameters ',' FormalParameter
										| ',' FormalParameter '''
	p[0] = Node('comma_FormalParameters', p[1:])



def p_FormalParameters(p):
	'''FormalParameters : FormalParameter comma_FormalParameters
									| ReceiverParameter comma_FormalParameters
									| FormalParameter 
									| ReceiverParameter '''
	p[0] = Node('FormalParameters', p[1:])


def p_FormalParameter(p):
	'''FormalParameter : Modifiers UnannType VariableDeclaratorId
						| UnannType VariableDeclaratorId'''
	p[0] = Node('FormalParameter', p[1:])





def p_LastFormalParameter(p):
	'''LastFormalParameter : Modifiers UnannType Annotations ELLIPSIS VariableDeclaratorId
							| Modifiers UnannType ELLIPSIS VariableDeclaratorId
							| UnannType Annotations ELLIPSIS VariableDeclaratorId
							| UnannType ELLIPSIS VariableDeclaratorId
							| FormalParameter'''
	p[0] = Node('LastFormalParameter', p[1:])


def p_ReceiverParameter(p):
	'''ReceiverParameter : Annotations UnannType Identifier DOT this
									|  Annotations UnannType this
									|  UnannType Identifier DOT this
									|  UnannType this'''
	p[0] = Node('ReceiverParameter', p[1:])

def p_Throws(p):
	'''Throws : throws ExceptionTypeList'''
	p[0] = Node('Throws', p[1:])


def p_ExceptionTypeList(p):
	'''ExceptionTypeList : ExceptionTypeList ','  ExceptionType
									|  ExceptionType'''
	p[0] = Node('ExceptionTypeList', p[1:])


def p_ExceptionType(p):
	'''ExceptionType : ClassOrInterfaceType
			'''
	p[0] = Node('ExceptionType', p[1:])

def p_MethodBody(p):
	'''MethodBody : Block
							| ';' 
			'''
	p[0] = Node('MethodBody', p[1:])

def p_InstanceInitializer(p):
	'''InstanceInitializer : Block'''
	p[0] = Node('InstanceInitializer', p[1:])


def p_StaticInitializer(p):
	'''StaticInitializer : static Block'''
	p[0] = Node('StaticInitializer', p[1:])


def p_ConstructorDeclaration(p):
	'''ConstructorDeclaration : Modifiers ConstructorDeclarator Throws ConstructorBody
										| Modifiers ConstructorDeclarator ConstructorBody
										| ConstructorDeclarator Throws ConstructorBody
										| ConstructorDeclarator ConstructorBody'''
	p[0] = Node('ConstructorDeclaration', p[1:])



def p_ConstructorDeclarator(p):
	'''ConstructorDeclarator : TypeParameters SimpleName '(' FormalParameterList ')' 
										| SimpleName '(' FormalParameterList ')' 
										| TypeParameters SimpleName '('  ')' 
										| SimpleName '('  ')' '''
	p[0] = Node('ConstructorDeclarator', p[1:])



def p_ConstructorBody(p):
	'''ConstructorBody : '{' ExplicitConstructorInvocation BlockStatements  '}'
								| '{' BlockStatements  '}'
								| '{' ExplicitConstructorInvocation   '}'
								| '{' '}' '''
	p[0] = Node('ConstructorBody', p[1:])


def p_ExplicitConstructorInvocation(p):
	'''ExplicitConstructorInvocation : TypeArguments this '(' ArgumentList ')' ';'
											| this '(' ArgumentList ')' ';'
											| TypeArguments this '(' ')' ';'
											| this '('  ')' ';'
											| TypeArguments super '(' ArgumentList ')' ';'
											| super '(' ArgumentList ')' ';'
											| TypeArguments super '(' ')' ';'
											| super '('  ')' ';'
											| Name DOT TypeArguments super '(' ArgumentList ')' ';'
											| Name DOT super '(' ArgumentList ')' ';'
											| Name DOT TypeArguments super '(' ')' ';'
											| Name DOT super '('  ')' ';'
											| Primary DOT TypeArguments super '(' ArgumentList ')' ';'
											| Primary DOT super '(' ArgumentList ')' ';'
											| Primary DOT TypeArguments super '(' ')' ';'
											| Primary DOT super '('  ')' ';' '''
	p[0] = Node('ExplicitConstructorInvocation', p[1:])


def p_EnumDeclaration(p):
	'''EnumDeclaration : Modifiers enum Identifier Superinterfaces EnumBody
								| Modifiers enum Identifier EnumBody
								| enum Identifier Superinterfaces EnumBody
								| enum Identifier EnumBody'''
	p[0] = Node('EnumDeclaration', p[1:])


def p_EnumBody(p):
	'''EnumBody : '{' EnumConstantList ',' EnumBodyDeclarations '}'
							| '{' ',' EnumBodyDeclarations '}'
							| '{' EnumConstantList EnumBodyDeclarations '}'
							| '{' EnumConstantList ',' '}'
							| '{'  EnumBodyDeclarations '}'
							| '{' EnumConstantList  '}'
							| '{' ',' '}'
							| '{' '}' '''
	p[0] = Node('EnumBody', p[1:])


def p_EnumConstantList(p):
	'''EnumConstantList : EnumConstantList ',' EnumConstant
									| EnumConstant'''
	p[0] = Node('EnumConstantList', p[1:])


def p_EnumConstant(p):
	'''EnumConstant : Modifiers Identifier '(' ArgumentList ')' ClassBody
								| Modifiers Identifier '(' ArgumentList ')'
								| Modifiers Identifier '('  ')' ClassBody
								| Modifiers Identifier '('  ')' 
								| Modifiers Identifier ClassBody
								| Identifier '(' ArgumentList ')' ClassBody
								| Identifier '(' ArgumentList ')'
								| Identifier '('  ')' ClassBody
								| Identifier '('  ')' 
								| Identifier ClassBody'''
	p[0] = Node('EnumConstant', p[1:])
					



def p_EnumBodyDeclarations(p):
	'''EnumBodyDeclarations : ';' ClassBodyDeclarations
							| ';' '''
	p[0] = Node('EnumBodyDeclarations', p[1:])



# Productions from Interfaces

def p_InterfaceDeclaration(p):
	'''InterfaceDeclaration : NormalInterfaceDeclaration
									| AnnotationTypeDeclaration'''
	p[0] = Node('InterfaceDeclaration', p[1:])


def p_NormalInterfaceDeclaration(p):
	'''NormalInterfaceDeclaration : Modifiers interface Identifier TypeParameters ExtendsInterfaces InterfaceBody 
											| Modifiers interface Identifier ExtendsInterfaces InterfaceBody 
											| Modifiers interface Identifier TypeParameters InterfaceBody 
											| Modifiers interface Identifier InterfaceBody
											| interface Identifier TypeParameters ExtendsInterfaces InterfaceBody 
											| interface Identifier ExtendsInterfaces InterfaceBody 
											| interface Identifier TypeParameters InterfaceBody 
											| interface Identifier InterfaceBody '''
	p[0] = Node('NormalInterfaceDeclaration', p[1:])




def p_ExtendsInterfaces(p):
	'''ExtendsInterfaces : extends InterfaceTypeList'''
	p[0] = Node('ExtendsInterfaces', p[1:])


def p_InterfaceBody(p):
	'''InterfaceBody : '{' InterfaceMemberDeclarations '}'
						| '{'  '}' '''
	p[0] = Node('InterfaceBody', p[1:])


def p_InterfaceMemberDeclarations(p):
	'''InterfaceMemberDeclarations : InterfaceMemberDeclarations InterfaceMemberDeclaration
											| InterfaceMemberDeclaration'''
	p[0] = Node('InterfaceMemberDeclarations', p[1:])


def p_InterfaceMemberDeclaration(p):
	'''InterfaceMemberDeclaration : ConstantDeclaration
											| InterfaceMethodDeclaration
											| ClassDeclaration
											| InterfaceDeclaration
											| ';' '''
	p[0] = Node('InterfaceMemberDeclaration', p[1:])




def p_ConstantDeclaration(p): 
	'''ConstantDeclaration : Modifiers UnannType VariableDeclaratorList ';'
							| UnannType VariableDeclaratorList ';' '''
	p[0] = Node('ConstantDeclaration(', p[1:])




def p_InterfaceMethodDeclaration(p):
	'''InterfaceMethodDeclaration : Modifiers MethodHeader MethodBody
									| MethodHeader MethodBody'''
	p[0] = Node('InterfaceMethodDeclaration', p[1:])



def p_AnnotationTypeDeclaration(p):
	'''AnnotationTypeDeclaration : Modifiers '@' interface Identifier AnnotationTypeBody
								| '@' interface Identifier AnnotationTypeBody'''
	p[0] = Node('AnnotationTypeDeclaration', p[1:])


def p_AnnotationTypeBody(p):
	'''AnnotationTypeBody : '{' AnnotationTypeMemberDeclarations '}' 
							| '{'  '}'  '''
	p[0] = Node('AnnotationTypeBody', p[1:])



def p_AnnotationTypeMemberDeclarations(p):
	'''AnnotationTypeMemberDeclarations : AnnotationTypeMemberDeclarations AnnotationTypeMemberDeclaration
													| AnnotationTypeMemberDeclaration '''
	p[0] = Node('AnnotationTypeMemberDeclarations', p[1:])


def p_AnnotationTypeMemberDeclaration(p):
	'''AnnotationTypeMemberDeclaration : AnnotationTypeElementDeclaration
												| ConstantDeclaration 
												| ClassDeclaration 
												| InterfaceDeclaration
												| ';' '''
	p[0] = Node('AnnotationTypeMemberDeclaration', p[1:])


def p_AnnotationTypeElementDeclaration(p):
	'''AnnotationTypeElementDeclaration : Modifiers UnannType Identifier '(' ')' Dims DefaultValue ';'
													| Modifiers UnannType Identifier '(' ')' DefaultValue ';'
													| Modifiers UnannType Identifier '(' ')' Dims ';'
													| Modifiers UnannType Identifier '(' ')'  ';' 
													| UnannType Identifier '(' ')' Dims DefaultValue ';'
													| UnannType Identifier '(' ')' DefaultValue ';'
													| UnannType Identifier '(' ')' Dims ';'
													| UnannType Identifier '(' ')'  ';' '''
	p[0] = Node('AnnotationTypeElementDeclaration', p[1:])




def p_DefaultValue(p):
	'''DefaultValue : default ElementValue'''
	p[0] = Node('DefaultValue', p[1:])


def p_Annotation(p):
	'''Annotation : NormalAnnotation
							| MarkerAnnotation
							| SingleElementAnnotation'''
	p[0] = Node('Annotation', p[1:])


def p_NormalAnnotation(p):
	'''NormalAnnotation : '@' Name '(' ElementValuePairList ')'
								| '@' Name '(' ')' '''
	p[0] = Node('NormalAnnotation', p[1:])


def p_ElementValuePairList(p):
	'''ElementValuePairList : ElementValuePairList ',' ElementValuePair
										| ElementValuePair'''
	p[0] = Node('ElementValuePairList', p[1:])


def p_ElementValuePair(p):
	'''ElementValuePair : Identifier '=' ElementValue'''
	p[0] = Node('ElementValuePair', p[1:])


def p_ElementValue(p):
	'''ElementValue : ConditionalExpression
								| ElementValueArrayInitializer
								| Annotation'''
	p[0] = Node('ElementValue', p[1:])


def p_ElementValueArrayInitializer(p):
	'''ElementValueArrayInitializer : '{' ElementValueList ',' '}' 
									| '{' ',' '}'  
									| '{' ElementValueList '}' 
									| '{' '}'  '''
	p[0] = Node('ElementValueArrayInitializer', p[1:])


def p_ElementValueList(p):
	'''ElementValueList : ElementValueList ',' ElementValue
								| ElementValue'''
	p[0] = Node('ElementValueList', p[1:])


def p_MarkerAnnotation(p):
	'''MarkerAnnotation : '@' Name'''
	p[0] = Node('MarkerAnnotation', p[1:])


def p_SingleElementAnnotation(p):
	'''SingleElementAnnotation : '@' Name '(' ElementValue ')' '''
	p[0] = Node('SingleElementAnnotation', p[1:])


# Productions from arrays 


def p_ArrayInitializer(p):
	'''ArrayInitializer : '{' VariableInitializerList ',' '}' 
						| '{' ',' '}'  
						| '{' VariableInitializerList '}' 
						| '{' '}'  '''
	p[0] = Node('ArrayInitializer', p[1:])


def p_VariableInitializerList(p):
	'''VariableInitializerList : VariableInitializerList ',' VariableInitializer
										| VariableInitializer'''
	p[0] = Node('VariableInitializerList', p[1:])



# Productions from block and Statements

def p_Block(p): 
	'''Block : '{' BlockStatements '}' 	
						| '{' '}' '''
	p[0] = Node('Block', p[1:])


def p_BlockStatements(p):
	'''BlockStatements : BlockStatements BlockStatement
								| BlockStatement'''
	p[0] = Node('BlockStatements', p[1:])


def p_BlockStatement(p):
	'''BlockStatement : LocalVariableDeclarationStatement
								| ClassDeclaration
								| Statement'''
	p[0] = Node('BlockStatement', p[1:])


def p_LocalVariableDeclarationStatement(p):
	'''LocalVariableDeclarationStatement : LocalVariableDeclaration ';' '''
	p[0] = Node('LocalVariableDeclarationStatement', p[1:])


def p_LocalVariableDeclaration(p):
	'''LocalVariableDeclaration : Modifiers UnannType VariableDeclaratorList
								| UnannType VariableDeclaratorList'''
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
												| AssertStatement
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
	'''LabeledStatementNoShortIf : Identifier ':' StatementNoShortIf'''
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


def p_AssertStatement(p):
	'''AssertStatement : assert Expression ';' 
								| assert Expression ':' Expression ';' '''
	p[0] = Node('AssertStatement', p[1:])


def p_SwitchStatement(p):
	'''SwitchStatement : switch '(' Expression ')' SwitchBlock'''
	p[0] = Node('SwitchStatement', p[1:])


def p_SwitchBlock(p):
	'''SwitchBlock : '{'  SwitchBlockStatementGroups SwitchLabelss '}'
						| '{'  SwitchLabelss '}' 
						| '{'  SwitchBlockStatementGroups  '}'
						| '{'  '}' '''
	p[0] = Node('SwitchBlock', p[1:])

def p_SwitchBlockStatementGroups(p):
	'''SwitchBlockStatementGroups : SwitchBlockStatementGroups SwitchBlockStatementGroup
											| SwitchBlockStatementGroup'''
	p[0] = Node('SwitchBlockStatementGroups', p[1:])



def p_SwitchBlockStatementGroup(p):
	'''SwitchBlockStatementGroup : SwitchLabels BlockStatements'''
	p[0] = Node('SwitchBlockStatementGroup', p[1:])


def p_SwitchLabelss(p):
	'''SwitchLabelss : SwitchLabelss SwitchLabel
								| SwitchLabel '''
	p[0] = Node('SwitchLabelss', p[1:])


def p_SwitchLabels(p):
	'''SwitchLabels : SwitchLabels SwitchLabel
								| SwitchLabel'''
	p[0] = Node('SwitchLabels', p[1:])


def p_SwitchLabel(p):
	'''SwitchLabel : case ConstantExpression ':'
					| case EnumConstantName ':'
					| default ':' '''
	p[0] = Node('SwitchLabel', p[1:])


def p_EnumConstantName(p):
	'''EnumConstantName : Identifier'''
	p[0] = Node('EnumConstantName', p[1:])


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
	'''ForStatement : BasicForStatement
						| EnhancedForStatement'''
	p[0] = Node('ForStatement', p[1:])


def p_ForStatementNoShortIf(p):
	'''ForStatementNoShortIf : BasicForStatementNoShortIf
										| EnhancedForStatementNoShortIf
			'''
	p[0] = Node('ForStatementNoShortIf', p[1:])

def p_BasicForStatement(p):
	'''BasicForStatement : for '(' ForInit ';' Expression ';' ForUpdate ')' Statement
								| for '('  ';' Expression ';' ForUpdate ')' Statement
								| for '(' ForInit ';'  ';' ForUpdate ')' Statement
								| for '(' ForInit ';' Expression ';'  ')' Statement
								| for '('  ';'  ';' ForUpdate ')' Statement
								| for '('  ';' Expression ';'  ')' Statement
								| for '(' ForInit ';'  ';'  ')' Statement
								| for '('  ';'  ';'  ')' Statement'''
	p[0] = Node('BasicForStatement', p[1:])



def p_BasicForStatementNoShortIf(p):
	'''BasicForStatementNoShortIf : for '(' ForInit ';' Expression ';' ForUpdate ')' StatementNoShortIf
											| for '('  ';' Expression ';' ForUpdate ')' StatementNoShortIf
											| for '(' ForInit ';'  ';' ForUpdate ')' StatementNoShortIf
											| for '(' ForInit ';' Expression ';'  ')' StatementNoShortIf
											| for '('  ';'  ';' ForUpdate ')' StatementNoShortIf
											| for '('  ';' Expression ';'  ')' StatementNoShortIf
											| for '(' ForInit ';'  ';'  ')' StatementNoShortIf
											| for '('  ';'  ';'  ')' StatementNoShortIf'''
	p[0] = Node('BasicForStatementNoShortIf', p[1:])


def p_ForInit(p):
	'''ForInit : StatementExpressionList
						| LocalVariableDeclaration'''
	p[0] = Node('ForInit', p[1:])


def p_ForUpdate(p):
	'''ForUpdate : StatementExpressionList
			'''
	p[0] = Node('ForUpdate', p[1:])

def p_StatementExpressionList(p):
	'''StatementExpressionList : StatementExpressionList ',' StatementExpression
										| StatementExpression'''
	p[0] = Node('StatementExpressionList', p[1:])


def p_EnhancedForStatement(p):
	'''EnhancedForStatement : for '(' Modifiers UnannType VariableDeclaratorId ':' Expression ')' Statement
							| for '(' UnannType VariableDeclaratorId ':' Expression ')' Statement '''
	p[0] = Node('EnhancedForStatement', p[1:])


def p_EnhancedForStatementNoShortIf(p):
	'''EnhancedForStatementNoShortIf : for '(' Modifiers UnannType VariableDeclaratorId ':' Expression ')' StatementNoShortIf
										| for '(' UnannType VariableDeclaratorId ':' Expression ')' StatementNoShortIf'''
	p[0] = Node('EnhancedForStatementNoShortIf', p[1:])


def p_BreakStatement(p):
	'''BreakStatement : break Identifier ';'
								| break ';' '''
	p[0] = Node('BreakStatement', p[1:])


def p_ContinueStatement(p):
	'''ContinueStatement : continue Identifier ';'
											| continue ';' '''
	p[0] = Node('ContinueStatement', p[1:])


def p_ReturnStatement(p):
	'''ReturnStatement : return Expression ';'
								| return ';' '''
	p[0] = Node('ReturnStatement', p[1:])


def p_ThrowStatement(p):
	'''ThrowStatement : throw Expression ';' '''
	p[0] = Node('ThrowStatement', p[1:])


def p_SynchronizedStatement(p):
	'''SynchronizedStatement : synchronized '(' Expression ')' Block'''
	p[0] = Node('SynchronizedStatement', p[1:])


def p_TryStatement(p):
	'''TryStatement : try Block Catches
								| try Block Catches Finally
								| try Block Finally
								| TryWithResourcesStatement'''
	p[0] = Node('TryStatement', p[1:])


def p_Catches(p):
	'''Catches : Catches CatchClause 
					| CatchClause'''
	p[0] = Node('Catches', p[1:])


def p_CatchClause(p):
	'''CatchClause : catch '(' CatchFormalParameter ')' Block'''
	p[0] = Node('CatchClause', p[1:])


def p_CatchFormalParameter(p):
	'''CatchFormalParameter : Modifiers CatchType VariableDeclaratorId
								| CatchType VariableDeclaratorId'''
	p[0] = Node('CatchFormalParameter', p[1:])


def p_CatchType(p):
	'''CatchType : UnannClassOrInterfaceType orClassOrInterfaceType
					| UnannClassOrInterfaceType '''
	p[0] = Node('CatchType', p[1:])


def p_orClassOrInterfaceType(p):
	'''orClassOrInterfaceType : orClassOrInterfaceType '|' ClassOrInterfaceType
							| '|' ClassOrInterfaceType'''
	p[0] = Node('orClassOrInterfaceType', p[1:])
 

def p_Finally(p):
	'''Finally : finally Block'''
	p[0] = Node('Finally', p[1:])


def p_TryWithResourcesStatement(p):
	'''TryWithResourcesStatement : try ResourceSpecification Block Catches Finally
											| try ResourceSpecification Block Finally
											| try ResourceSpecification Block Catches
											| try ResourceSpecification Block '''
	p[0] = Node('TryWithResourcesStatement', p[1:])


def p_ResourceSpecification(p):
	'''ResourceSpecification : '(' ResourceList ';' ')'
										| '(' ResourceList ')' '''
	p[0] = Node('ResourceSpecification', p[1:])


def p_ResourceList(p):
	'''ResourceList : ResourceList ';' Resource
							| Resource'''
	p[0] = Node('ResourceList', p[1:])


def p_Resource(p):
	'''Resource : Modifiers UnannType VariableDeclaratorId '=' Expression
					| UnannType VariableDeclaratorId '=' Expression'''
	p[0] = Node('Resource', p[1:])


def p_VariableDeclarator(p):
	'''VariableDeclarator : VariableDeclaratorId '=' VariableInitializer   
							| VariableDeclaratorId'''
	p[0] = Node('VariableDeclarator', p[1:])


# Productions from Expressions



def p_Primary(p):
	'''Primary : PrimaryNoNewArray
						| ArrayCreationExpression'''
	p[0] = Node('Primary', p[1:])


def p_PrimaryNoNewArray(p):
	'''PrimaryNoNewArray : Literal
						| ClassLiteral
						| this
						| Name DOT this
						| '(' Expression ')'
						| ClassInstanceCreationExpression
						| FieldAccess
						| ArrayAccess
						| MethodInvocation
						| MethodReference'''
	p[0] = Node('PrimaryNoNewArray', p[1:])


def p_ClassLiteral(p):
	'''ClassLiteral : Name Brackets  DOT class
								| NumericType Brackets  DOT class
								| boolean Brackets  DOT class
								| void DOT class
								| Name  DOT class
								| NumericType  DOT class
								| boolean  DOT class
	'''
	p[0] = Node('ClassLiteral', p[1:])


def p_Brackets(p):
	'''Brackets : Brackets '[' ']'
						| '[' ']' '''
	p[0] = Node('Brackets', p[1:])


def p_ClassInstanceCreationExpression(p):
	'''ClassInstanceCreationExpression : UnqualifiedClassInstanceCreationExpression
											| Name DOT UnqualifiedClassInstanceCreationExpression
											| Primary DOT UnqualifiedClassInstanceCreationExpression'''
	p[0] = Node('ClassInstanceCreationExpression', p[1:])


def p_UnqualifiedClassInstanceCreationExpression(p):
	'''UnqualifiedClassInstanceCreationExpression : new TypeArguments ClassOrInterfaceTypeToInstantiate '(' ArgumentList ')' ClassBody
													| new ClassOrInterfaceTypeToInstantiate '(' ArgumentList ')' ClassBody
													| new TypeArguments ClassOrInterfaceTypeToInstantiate '('  ')' ClassBody
													| new TypeArguments ClassOrInterfaceTypeToInstantiate '(' ArgumentList ')' 
													| new ClassOrInterfaceTypeToInstantiate '(' ')' ClassBody
													| new TypeArguments ClassOrInterfaceTypeToInstantiate '('  ')' 
													| new ClassOrInterfaceTypeToInstantiate '(' ArgumentList ')' 
													| new ClassOrInterfaceTypeToInstantiate '('  ')'  '''
	p[0] = Node('UnqualifiedClassInstanceCreationExpression', p[1:])





def p_ClassOrInterfaceTypeToInstantiate(p):
	'''ClassOrInterfaceTypeToInstantiate : Annotations Identifier dotAnnotationsIdentifier TypeArgumentsOrDiamond
												| Annotations Identifier dotAnnotationsIdentifier 
												| Identifier dotAnnotationsIdentifier TypeArgumentsOrDiamond
												| Identifier dotAnnotationsIdentifier 
												| Annotations Identifier TypeArgumentsOrDiamond
												| Annotations Identifier 
												| Identifier TypeArgumentsOrDiamond
												| Identifier 
			'''
	p[0] = Node('ClassOrInterfaceTypeToInstantiate', p[1:])


def p_dotAnnotationsIdentifier(p):
	'''dotAnnotationsIdentifier : dotAnnotationsIdentifier DOT Annotations Identifier
									| dotAnnotationsIdentifier DOT Identifier
									| DOT Annotations Identifier
									| DOT Identifier
			'''
	p[0] = Node('dotAnnotationsIdentifier', p[1:])


def p_TypeArgumentsOrDiamond(p):
	'''TypeArgumentsOrDiamond : TypeArguments 
										| '<' '>' '''
	p[0] = Node('TypeArgumentsOrDiamond', p[1:])


def p_FieldAccess(p):
	'''FieldAccess : Primary DOT Identifier
							| super DOT Identifier
							| Name DOT super DOT Identifier'''
	p[0] = Node('FieldAccess', p[1:])


def p_ArrayAccess(p):
	'''ArrayAccess : Name Expression 
							| Name 
							| PrimaryNoNewArray Expression 
							| PrimaryNoNewArray 
			'''
	p[0] = Node('ArrayAccess', p[1:])	

def p_MethodInvocation(p):
	'''MethodInvocation : SimpleName '(' ArgumentList ')'	
						| SimpleName '(' ')'
						| Name DOT TypeArguments Identifier '(' ArgumentList ')'
						| Name DOT Identifier '(' ArgumentList ')'
						| Name DOT TypeArguments Identifier '('  ')'
						| Name DOT  Identifier '('  ')'
						| Primary DOT TypeArguments Identifier '(' ArgumentList ')'
						| Primary DOT Identifier '(' ArgumentList ')'
						| Primary DOT TypeArguments Identifier '('  ')'
						| Primary DOT  Identifier '('  ')'
						| super DOT TypeArguments Identifier '(' ArgumentList ')'
						| super DOT Identifier '(' ArgumentList ')'
						| super DOT TypeArguments Identifier '('  ')'
						| super DOT  Identifier '('  ')'
						| Name DOT super DOT TypeArguments Identifier '(' ArgumentList ')'
						| Name DOT super DOT Identifier '(' ArgumentList ')'
						| Name DOT super DOT TypeArguments Identifier '('  ')'
						| Name DOT super DOT  Identifier '('  ')' 
								'''
	p[0] = Node('MethodInvocation', p[1:])	



def p_ArgumentList(p):
	'''ArgumentList : ArgumentList ',' Expression 
			 				| Expression''' 
	p[0] = Node('ArgumentList', p[1:])	


def p_MethodReference(p):
	'''MethodReference : Name DOUBLECOLON TypeArguments Identifier
								| Name DOUBLECOLON Identifier
								| ReferenceType DOUBLECOLON TypeArguments Identifier
								| ReferenceType DOUBLECOLON Identifier
								| Primary DOUBLECOLON TypeArguments Identifier
								| Primary DOUBLECOLON Identifier
								| super DOUBLECOLON TypeArguments Identifier
								| super DOUBLECOLON Identifier
								| Name DOT super DOUBLECOLON TypeArguments Identifier
								| Name DOT super DOUBLECOLON Identifier
								| ClassOrInterfaceType DOUBLECOLON TypeArguments new
								| ClassOrInterfaceType DOUBLECOLON new
								| ArrayType DOUBLECOLON new'''
	p[0] = Node('MethodReference', p[1:])	
					


def p_ArrayCreationExpression(p):
	'''ArrayCreationExpression : new PrimitiveType DimExprs Dims
										| new PrimitiveType DimExprs 
										| new ClassOrInterfaceType DimExprs Dims
										| new ClassOrInterfaceType DimExprs
										| new PrimitiveType Dims ArrayInitializer
										| new ClassOrInterfaceType Dims ArrayInitializer'''
	p[0] = Node('ArrayCreationExpression', p[1:])	


def p_DimExprs(p):
	'''DimExprs : DimExprs DimExpr
						| DimExpr'''
	p[0] = Node('DimExprs', p[1:])	


def p_DimExpr(p):
	'''DimExpr : Annotations '[' Expression ']'
						| '[' Expression ']'
	'''
	p[0] = Node('DimExpr', p[1:])	


def p_Expression(p):
	'''Expression : LambdaExpression
							| AssignmentExpression'''
	p[0] = Node('Expression', p[1:])	


def p_LambdaExpression(p):
	'''LambdaExpression : LambdaParameters LAMBDAARROW LambdaBody '''
	p[0] = Node('LambdaExpression', p[1:])	


def p_LambdaParameters(p):
	'''LambdaParameters : Identifier
								| '(' FormalParameterList ')'
								| '(' InferredFormalParameterList ')'
								| '(' ')' '''
	p[0] = Node('LambdaParameters', p[1:])	


def p_InferredFormalParameterList(p):
	'''InferredFormalParameterList : InferredFormalParameterList ',' Identifier
											| Identifier'''
	p[0] = Node('InferredFormalParameterList', p[1:])	


def p_LambdaBody(p):
	'''LambdaBody : Expression
							| Block'''
	p[0] = Node('LambdaBody', p[1:])	


def p_AssignmentExpression(p):
	'''AssignmentExpression : ConditionalExpression
							| Assignment'''
	p[0] = Node('AssignmentExpression', p[1:])	


def p_Assignment(p):
	'''Assignment : LeftHandSide AssignmentOperator Expression '''
	p[0] = Node('Assignment', p[1:])	


def p_LeftHandSide(p):
	'''LeftHandSide : Name
							| FieldAccess
							| ArrayAccess'''
	p[0] = Node('LeftHandSide', p[1:])	


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



def p_ConditionalExpression(p):
	'''ConditionalExpression : ConditionalOrExpression 
										| ConditionalOrExpression '?' Expression ':' ConditionalExpression
										| ConditionalOrExpression '?' Expression ':' LambdaExpression'''
	p[0] = Node('ConditionalExpression', p[1:])	


def p_ConditionalOrExpression(p):
	'''ConditionalOrExpression : ConditionalAndExpression
								| ConditionalOrExpression OR ConditionalAndExpression'''
	p[0] = Node('ConditionalOrExpression', p[1:])


def p_ConditionalAndExpression(p):
	'''ConditionalAndExpression : InclusiveOrExpression 
										| ConditionalAndExpression AND InclusiveOrExpression'''
	p[0] = Node('ConditionalAndExpression', p[1:])


def p_InclusiveOrExpression(p):
	'''InclusiveOrExpression : ExclusiveOrExpression
										| InclusiveOrExpression '|' ExclusiveOrExpression'''
	p[0] = Node('InclusiveOrExpression', p[1:])


def p_ExclusiveOrExpression(p):
	'''ExclusiveOrExpression : AndExpression
								| ExclusiveOrExpression '^' AndExpression'''
	p[0] = Node('ExclusiveOrExpression', p[1:])


def p_AndExpression(p):
	'''AndExpression : EqualityExpression
								| AndExpression '&' EqualityExpression'''
	p[0] = Node('AndExpression', p[1:])


def p_EqualityExpression(p):
	'''EqualityExpression : RelationalExpression 
									| EqualityExpression EQ RelationalExpression
									| EqualityExpression NEQ RelationalExpression'''
	p[0] = Node('EqualityExpression', p[1:])


def p_RelationalExpression(p):
	'''RelationalExpression : ShiftExpression
									| RelationalExpression '<' ShiftExpression
									| RelationalExpression '>' ShiftExpression
									| RelationalExpression LTEQ ShiftExpression
									| RelationalExpression GTEQ ShiftExpression
									| RelationalExpression instanceof ReferenceType'''
	p[0] = Node('RelationalExpression', p[1:])


def p_ShiftExpression(p):
	'''ShiftExpression : AdditiveExpression 
								| ShiftExpression LSHIFT AdditiveExpression
								| ShiftExpression RSHIFT AdditiveExpression
								| ShiftExpression RRSHIFT AdditiveExpression'''
	p[0] = Node('ShiftExpression(', p[1:])


def p_AdditiveExpression(p):
	'''AdditiveExpression : MultiplicativeExpression
									| AdditiveExpression '+' MultiplicativeExpression
									| AdditiveExpression '-' MultiplicativeExpression'''
	p[0] = Node('AdditiveExpression', p[1:])


def p_MultiplicativeExpression(p):
	'''MultiplicativeExpression : UnaryExpression
										| MultiplicativeExpression '*' UnaryExpression
										| MultiplicativeExpression '/' UnaryExpression
										| MultiplicativeExpression '%' UnaryExpression'''
	p[0] = Node('MultiplicativeExpression', p[1:])


def p_UnaryExpression(p):
	'''UnaryExpression : PreIncrementExpression
								| PreDecrementExpression
								| '+' UnaryExpression
								| '-' UnaryExpression
								| UnaryExpressionNotPlusMinus'''
	p[0] = Node('UnaryExpression', p[1:])


def p_PreIncrementExpression(p):
	'''PreIncrementExpression : PLUSPLUS UnaryExpression '''
	p[0] = Node('PreIncrementExpression', p[1:])


def p_PreDecrementExpression(p):
	'''PreDecrementExpression : MINUSMINUS UnaryExpression'''
	p[0] = Node('PreDecrementExpression', p[1:])


def p_UnaryExpressionNotPlusMinus(p):
	'''UnaryExpressionNotPlusMinus : PostfixExpression
										| '~' UnaryExpression
										| '!' UnaryExpression
										| CastExpression'''
	p[0] = Node('UnaryExpressionNotPlusMinus', p[1:])


def p_PostfixExpression(p):
	'''PostfixExpression : Primary
								| Name
								| PostIncrementExpression
								| PostDecrementExpression'''
	p[0] = Node('PostfixExpression', p[1:])


def p_PostIncrementExpression(p):
	'''PostIncrementExpression : PostfixExpression PLUSPLUS'''
	p[0] = Node('PostIncrementExpression', p[1:])


def p_PostDecrementExpression(p):
	'''PostDecrementExpression : PostfixExpression MINUSMINUS'''
	p[0] = Node('PostDecrementExpression', p[1:])


def p_CastExpression(p):
	'''CastExpression : '(' PrimitiveType ')' UnaryExpression
								| '(' ReferenceType AdditionalBounds ')' UnaryExpressionNotPlusMinus
								| '(' ReferenceType AdditionalBounds ')' LambdaExpression
								| '(' ReferenceType ')' UnaryExpressionNotPlusMinus
								| '(' ReferenceType ')' LambdaExpression'''
	p[0] = Node('CastExpression', p[1:])


def p_ConstantExpression(p):
	'''ConstantExpression : Expression'''
	p[0] = Node('ConstantExpression', p[1:])


def p_empty(p):
	'''empty : '''
	pass
	# p[0]=None

def p_error(p):
	print('ERROR')
	sys.exit()



# making the parser 
parser = yacc.yacc()

# parsing
result_output = parser.parse(newdata)


# ==============================================================================================================================================

# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI
# YE BHAVY KA TEPA HAI CHANGE KARNA HAI





# number nodes to remove duplicates
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
with open(args.out, 'w') as f:
    f.write(create_dot_script(result_output))



