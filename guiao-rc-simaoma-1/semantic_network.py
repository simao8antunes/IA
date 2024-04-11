# Guiao de representacao do conhecimento
# -- Redes semanticas
#
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

from collections import Counter

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)
#   Exemplo:
#   a = Association('socrates','professor','filosofia')

class AssocOne(Association):
    one = dict()

    def __init__(self, e1, assoc, e2):
        if assoc not in AssocOne.one:
            AssocOne.one[assoc] = dict()
        assert e2 not in AssocOne.one[assoc] or AssocOne.one[assoc][e2].entity1 == e1
        AssocOne.one[assoc][e2] = self

        Association.__init__(self, e1, assoc, e2)

class AssocNum(Association):
    def __init__(self, e1, assoc, e2):
        assert isinstance(e2, (int, float))
        Association.__init__(self, e1, assoc, e2)


# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)
#   Exemplo:
#   s = Subtype('homem','mamifero')


# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)
#   Exemplo:
#   m = Member('socrates','homem')


# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)
#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)


# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl

    def __str__(self):
        return str(self.declarations)
    
    def insert(self,decl):
        self.declarations.append(decl)

    def query_local(self,user=None,e1=None,rel=None,e2=None, _type=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    

    def show_query_result(self):
        for d in self.query_result:
            print(str(d))


    def list_associations(self): # Ex1 - nomes das associações existentes
        association_names = []
        for declaration in self.declarations:
            if isinstance(declaration.relation, Association):
                association_names.append(declaration.relation.name)
        unique_association_names = sorted(set(association_names))
        return unique_association_names

    
    def list_objects(self): # Ex2 - lista das entidades declaradas como instâncias de tipos
        objects = []
        for declaration in self.declarations:
            if isinstance(declaration.relation, Member):
                objects.append(declaration.relation.entity1)
        return sorted(set(objects))


    def list_users(self): # Ex3 - lista de utilizadores existentes na rede
        user_names = []
        for declaration in self.declarations:
            user_names.append(declaration.user)
        
        unique_user_names = sorted(set(user_names))
        return unique_user_names
    

    def list_types(self): # Ex4 - lista de tipos existente na rede
        type_names = []
        for declaration in self.declarations:
            if isinstance(declaration.relation, Subtype):
                type_names.extend([declaration.relation.entity1, declaration.relation.entity2])
            if isinstance(declaration.relation, Member):
                type_names.append(declaration.relation.entity2)
        unique_type_names = sorted(set(type_names))
        return unique_type_names

    
    def list_local_associations(self, entity): # Ex5 - dada uma entidade, devolve a lista (dos nomes) das associações localmente declaradas
        local_associations = []
        for declaration in self.declarations:
            if isinstance(declaration.relation, Association) and entity in (declaration.relation.entity1, declaration.relation.entity2):
                local_associations.append(declaration.relation.name)
        return sorted(set(local_associations))
    

    def list_relations_by_user(self, user): # Ex6 - dado um utilizador, devolve a lista (dos nomes) das relações por ele declaradas
        user_relations = []
        for declaration in self.declarations:
            if declaration.user == user:
                user_relations.append(declaration.relation.name)
        return sorted(set(user_relations))
    

    def associations_by_user(self, user): # Ex7 - dado um utilizador, devolve o nº de associações diferentes por ele utilizadas nas relações que declarou
        user_associations = set()
        for declaration in self.declarations:
            if declaration.user == user and isinstance(declaration.relation, Association):
                user_associations.add(declaration.relation.name)
        return len(user_associations)
    

    def list_local_associations_by_entity(self, entity): # Ex8 - dada uma entidade, devolve uma lista que contém o nome de uma associação localmente declarada e o utilizador que a declarou.
        entity_associations = set()
        for declaration in self.declarations:
            if isinstance(declaration.relation, Association) and (declaration.relation.entity1 == entity or declaration.relation.entity2 == entity):
                entity_associations.add((declaration.relation.name, declaration.user))
        return list(entity_associations)
    

    def predecessor(self, type, entity): # Ex9 - checks if type is in entities predecessors
        pds = [d.relation.entity2 for d in self.query_local(e1=entity, _type=(Member, Subtype))]
        if pds == []:
            return False
        
        if type in pds:
            return True
        
        return any(self.predecessor(type, p) for p in pds)
    

    def predecessor_path(self, predecessor, entity): # Ex10
        if predecessor == entity:
            return [predecessor]

        relations = [d.relation.entity1 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity2 == predecessor]
        path = None

        for e in relations:
            path = self.predecessor_path(e, entity)
            if path:
                return [predecessor] + path

        return path
    

    def query(self, entity, association=None): # Ex11 a) - obter todas as declarações de associações locais ou herdadas por uma entidade.
        relations = [d.relation.entity2 for d in self.declarations if type(d.relation) in [Member, Subtype] and d.relation.entity1 == entity]
        
        declarations = [d for d in self.declarations if type(d.relation) == Association and d.relation.entity1 == entity] if association is None \
            else [d for d in self.declarations if type(d.relation) == Association and d.relation.name == association and d.relation.entity1 == entity]

        for super in relations:
            decl = self.query(super, association)
            if decl is not None:
                declarations += decl
        
        return declarations
    
    
    def query2(self, entity, association=None): # Ex11 b) - obter todas as declara ̧c ̃oes locais (incluindo Member e Subtype) ou herdadas (apenas Association) por uma entidade.
        local_declarations = [d for d in self.declarations if d.relation.entity1 == entity]
        
        if association is not None:
            local_declarations = [d for d in local_declarations if d.relation.name == association]

        inherited_declarations = []
        relations = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        
        for related_entity in relations:
            inherited_declarations += [d for d in self.query2(related_entity, association) if isinstance(d.relation, Association)]

        return local_declarations + inherited_declarations


    def query_cancel(self, entity, association): # Ex12 - similar a query(), mas existe cancelamento de herança. Neste caso, quando uma associação está declarada numa entidade, a entidade nao herdara essa associacao das entidades predecessoras.
        pds = [self.query_cancel(d.relation.entity2, association) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]

        local = self.query_local(e1=entity, rel=association, _type=Association)

        pds_query = [d for sublist in pds for d in sublist if d.relation.name not in [l.relation.name for l in local]]

        return pds_query + local
    

    def query_down(self, entity, assoc_name=None, first=True): # Ex13 - inferencia por induçao
        desc = [self.query_down(d.relation.entity1, assoc_name, first=False) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity2 == entity]

        desc_query = [ d for sublist in desc for d in sublist]

        if first:
            return desc_query

        local = self.query_local(e1=entity, rel=assoc_name)

        return desc_query + local
    

    def query_induce(self, entity, assoc_name): # Ex14 - inferencia por induçao
        desc = self.query_down(entity, assoc_name)

        for val, _ in Counter([d.relation.entity2 for d in desc]).most_common(1):
            return val
        
        return None
    

    def query_local_assoc(self, entity, assoc_name):
        local = self.query_local(e1=entity, rel=assoc_name)

        for l in local:
            if isinstance(l.relation, AssocNum):
                values = [d.relation.entity2 for d in local]
                return sum(values)/len(local)
            if isinstance(l.relation, AssocOne):
                val, count = Counter([d.relation.entity2 for d in local]).most_common(1)[0]
                return val, count/len(local)
            if isinstance(l.relation, Association):
                mc = []
                freq = 0
                for val, count in Counter([d.relation.entity2 for d in local]).most_common():
                    mc.append((val, count/len(local)))
                    freq += count/len(local)
                    if freq > 0.75:
                        return mc
                    

    def query_assoc_value(self, entity, association):
        local = self.query_local(e1=entity, rel=association)

        local_values = [l.relation.entity2 for l in local]

        if len(set(local_values)) == 1:
            return local_values[0]
        
        predecessor = [a for a in self.query(entity=entity, association=association) if a not in local]

        predecessor_values = [i.relation.entity2 for i in predecessor]

        def perc(lista, value):
            if lista == []:
                return 0

            return len([l for l in lista if l.relation.entity2 == value])/len(lista)
        
        return max(local_values + predecessor_values, key=lambda v: (perc(local, v)+perc(predecessor, v))/2)