# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 14:51:53 2014

@author: fernando
"""

from random import random, randint, sample
from sympy import symbols, Rational, latex, atan, asin, acos, sqrt, sin, cos, tan, cot, sec, csc, log, exp
from copy import copy

funciones = ['atan','asin','acos','sqrt','sin','cos','tan','cot','csc','sec','exp','ln','log']



#la cadena puede venir sin signos de multiplicación entre números y variables
#por ejemplo, 2xy debe transformarse a 2*x*y 
# 2x-->2*x
# 23x---> 23*x
# -5xy --> -5*x*y
# 3(xy+x^2) ---> 3*(x*y+x^2)
# x3 --> x*3 ?? o error?
# *  Recorrer la cadena de izquierda a derecha y buscar: (ir copiando los símbolos en el resultado al mismo tiempo) 
# **    Símbolo o número (iniciar un búfer vacío y llenarlo con el primer símbolo, o llenarlo mentras lea dígitos)
# **    Una vez que el búfer sea no vacío verificar que el carácter actual:
# ***      Si  caracter actual es un dígito, seguir leyendo
# ***      Si el caracter actual es un símbolo, insertar el signo de * y el símbolo, vaciar el búfer 
# ***      Si el caracter actual es un paréntesis insertar el * y el símbolo actual, vaciar el búfer    
# ***      Si el caracter actual es un operador, vaciar el búfer
# ***      Si es el  

# considerar las funciones!!
'''
def ajusta_cadena(cad, symbls):
    digs = [str(i) for i in range(10)]
    buf = {'tipo':'v', 'val':''}
    res = ''
    
    #el análsiis lo realiza excluyendo el inicio y final del nombre de una función
    
        
    for s in cad:
        #bufer vacío
        if buf['val'] == '':            
            if s in symbls:
                buf['val'] = s
                buf['tipo'] = 's'               
            elif s in digs:
                buf['val'] = s
                buf['tipo'] = 'd'                        
        #búfer no vacío
        else:
            if buf['tipo'] == 's':
                if s in symbls: #pareja de símbolos: xy
                    res += '*'
                    buf['val'] = s
                elif s in digs: #símbolo seguido de número: x300
                    res += '*'
                    buf['tipo'] = 'd'
                    buf['val'] = s
                elif s == '(': #símbolo seguido de paréntesis: x(3+x) 
                    res += '*' 
                    buf['tipo'] = 0
                    buf['val'] = ''
                elif s == ')':
                    buf['val'] = s
                    buf['tipo'] = 'p'                                
                else:
                    buf['tipo'] = 0
                    buf['val'] = ''
            elif buf['tipo'] == 'd':
                if s in symbls: #pareja número-símbolo: 3x
                    res += '*'       
                    buf['tipo'] = 's'
                    buf['val'] = s
                elif s in digs: #número seguido de número: 23
                    buf['val'] += s 
                elif s == '(': #número seguido de paréntesis: 3(x+5) 
                    res += '*' 
                    buf['tipo'] = 0
                    buf['val'] = ''
                elif s == ')':
                    buf['val'] = s
                    buf['tipo'] = 'p'            
                else:
                    buf['tipo'] = 0
                    buf['val'] = ''
            elif buf['tipo'] == 'p':
                if s in symbls: # )x
                    res += '*'       
                    buf['tipo'] = 's'
                    buf['val'] = s
                elif s in digs: #)3
                    res += '*'
                    buf['tipo'] = 'd'
                    buf['val'] = s
                elif s == '(':
                    res += '*'
                    buf['tipo'] = 0
                    buf['val'] = ''
                elif s == ')':
                    buf['val'] = s
                    buf['tipo'] = 'p' #paréntesis anidados            
                else:
                    buf['tipo'] = 0
                    buf['val'] = ''
        res += s    
    return res  
'''

def float_number(ltx):
    digs = ['0','1','2','3','4','5','6','7','8','9','.']
    
    if ltx.find('.')>=0:
        nc = ltx.count('.')
        if nc > 1:
            return False
    
    ind = ltx.find('-')
    if ind > 0:
        return False
    elif ind == 0:
        if ltx.count('-') > 1:
            return False
        ind = 1 
    else:
        ind = 0    
    for s in ltx[ind:]:
        if not s in digs:
            return False        
    return True


def ltxToE(ltx,symbs=['i']):
    '''
    if type(ltx) != unicode:
        ltx_nspxc = unicode(ltx, "utf-8")  
    else:
    '''
    ltx_nspxc = ltx
    ltx_nspxc = ltx_nspxc.replace(' ','')
    
    if ltx_nspxc.find('.')>=0:
        if float_number(ltx_nspxc):
            e = float(ltx)
            return e
    
    d = valida_ltx(ltx_nspxc,symbs,funciones)
    #la cadena no es válida (error de sintaxis)
    if not d['valida']:
        return None
    cad = d['cad']
    e = str2expr(cad,symbs)
    return e


def ajusta_cadena(cad, symbls):
    digs = [str(i) for i in range(10)]
    buf = {'tipo':'v', 'val':''}
    res = ''
    
    #funciones permitidas
    #funcs = ['sin','cos','tan','cot','csc','sec','exp','ln','log']
    ncad = cad
    for f in funciones:
        ncad = ncad.replace(f,'$'+f+'$')
    
    ncad = depura_funcion_potencia(ncad)
    
    #el análisis lo realiza excluyendo el inicio y final del nombre de una función
    in_func = False    
    for s in ncad:
        if s == '$':
            if not in_func:
                in_func = True
            else:
                in_func = False
                
        #bufer vacío
        if not in_func:
            if buf['val'] == '':            
                if s in symbls:
                    buf['val'] = s
                    buf['tipo'] = 's'               
                elif s in digs:
                    buf['val'] = s
                    buf['tipo'] = 'd'                        
            #búfer no vacío
            else:
                if buf['tipo'] == 's':
                    if s in symbls: #pareja de símbolos: xy
                        res += '*'
                        buf['val'] = s
                    elif s in digs: #símbolo seguido de número: x300
                        res += '*'
                        buf['tipo'] = 'd'
                        buf['val'] = s
                    elif s == '(': #símbolo seguido de paréntesis: x(3+x) 
                        res += '*' 
                        buf['tipo'] = 0
                        buf['val'] = ''
                    elif s == ')':
                        buf['val'] = s
                        buf['tipo'] = 'p'                                
                    else:
                        buf['tipo'] = 0
                        buf['val'] = ''
                elif buf['tipo'] == 'd':
                    if s in symbls: #pareja número-símbolo: 3x
                        res += '*'       
                        buf['tipo'] = 's'
                        buf['val'] = s
                    elif s in digs: #número seguido de número: 23
                        buf['val'] += s 
                    elif s == '(': #número seguido de paréntesis: 3(x+5) 
                        res += '*' 
                        buf['tipo'] = 0
                        buf['val'] = ''
                    elif s == ')':
                        buf['val'] = s
                        buf['tipo'] = 'p'            
                    else:
                        buf['tipo'] = 0
                        buf['val'] = ''
                elif buf['tipo'] == 'p':
                    if s in symbls: # )x
                        res += '*'       
                        buf['tipo'] = 's'
                        buf['val'] = s
                    elif s in digs: #)3
                        res += '*'
                        buf['tipo'] = 'd'
                        buf['val'] = s
                    elif s == '(':
                        res += '*'
                        buf['tipo'] = 0
                        buf['val'] = ''
                    elif s == ')':
                        buf['val'] = s
                        buf['tipo'] = 'p' #paréntesis anidados            
                    else:
                        buf['tipo'] = 0
                        buf['val'] = ''
            res += s    
        else:
            res += s
    res = res.replace('$','')
    return res
    
    
def depura_funcion_potencia(cad):
    #busca las subcadenas del tipo $^n
    cad_dep = cad
    ind = cad_dep.find('$^')#potencia de una función
    while ind > 0:
        #partiendo del índice donde se encontró la potencia, captura la potencia y la pasa al siguiente parénteis de cierre
        i0 = ind+1 #indice del exponente "^"
        e = cad_dep[i0] #guarda el exponente
        i1 = i0+1#apunta al inicio del exponete 
        s = cad_dep[i1] 
        #recorre hasta delimitar el exponente
        if s == '(': #el exponente está encerrado entre paréntesis (debe ser un exponente complicado)           
            lev = 1 #el nivel debe apagarse
            e = e+s #copio el caracter actual
            i1 = i1+1 #recorro al siguiente caracter
            s = cad_dep[i1] 
            while lev > 0:
                if s == '(':
                    lev = lev+1
                elif s == ')':
                    lev = lev-1
                e = e+s
                i1 = i1+1
                s = cad_dep[i1]
        else: #exponente simple
            e = e+s #copio el caracter actual
            i1 = i1+1 #recorro al siguiente caracter
            s = cad_dep[i1] 
            while s != '(':
                e = e+s
                i1 = i1+1
                s = cad_dep[i1]
        
        ipa = i1 #índice del inicio del argumento (paréntesis)
        #i1 = i1+1
        lev = 1 # se supone que inicia en un paréntesis abierto
        while lev > 0:
            i1 = i1+1
            s = cad_dep[i1]
            if s == '(':
                lev = lev+1
            elif s == ')':
                lev = lev-1
        ipc = i1
        func = cad_dep[:i0]
        arg = cad_dep[ipa:ipc+1]
        cad_rest = cad_dep[ipc+1:]
        cad_dep = func+arg+e+cad_rest
        ind = cad_dep.find('$^')    
    return cad_dep
                
        
def acomoda_exponente_latex(cad):
    
    #busca las subcadenas del tipo $^n
    cad_dep = cad
    
    for f in funciones:
        cad_dep = cad_dep.replace(f,'$'+f+'$')
        
    ind = cad_dep.find('$^')#potencia de una función
    while ind > 0:
        #partiendo del índice donde se encontró la potencia, captura la potencia y la pasa al siguiente parénteis de cierre
        i0 = ind+1 #indice del exponente "^"
        e = cad_dep[i0] #guarda el exponente
        i1 = i0+1#apunta al inicio del exponete 
        s = cad_dep[i1] 
        #recorre hasta delimitar el exponente
        if s == '(': #el exponente está encerrado entre paréntesis (debe ser un exponente complicado)           
            lev = 1 #el nivel debe apagarse
            e = e+s #copio el caracter actual
            i1 = i1+1 #recorro al siguiente caracter
            s = cad_dep[i1] 
            while lev > 0:
                if s == '{':
                    lev = lev+1
                elif s == '}':
                    lev = lev-1
                e = e+s
                i1 = i1+1
                s = cad_dep[i1]
        else: #exponente simple
            e = e+s #copio el caracter actual
            i1 = i1+1 #recorro al siguiente caracter
            s = cad_dep[i1] 
            while s != '{':
                e = e+s
                i1 = i1+1
                s = cad_dep[i1]
        
        ipa = i1 #índice del inicio del argumento (paréntesis)
        #i1 = i1+1
        lev = 1 # se supone que inicia en un paréntesis abierto
        while lev > 0:
            i1 = i1+1
            s = cad_dep[i1]
            if s == '{':
                lev = lev+1
            elif s == '}':
                lev = lev-1
        ipc = i1
        func = cad_dep[:i0]
        arg = cad_dep[ipa:ipc+1]
        cad_rest = cad_dep[ipc+1:]
        cad_dep = func+arg+e+cad_rest
        ind = cad_dep.find('$^')    
    return cad_dep.replace('$','')
    
    

#encuentra los límites de un ambiente de latex
# por ejemplo
# los límites de \frac{}{} debe indicar en donde inicia y terminan el denominador y el numerador
def ltx_find_amb_lims(n_args, nfun, i0, ltx):
    
    res = {}
    
    if n_args == 2: #ltx[i0] = es el inicio del ambiente \\frac
        l = 0
        arg1_ini = False
        arg1_fin = False
        arg2_ini = False
        arg2_fin = False
        shft = len(nfun)+1
        pos = i0+shft
        for s in ltx[i0+shft:]:
            #determina los límites del numeargor
            if s == '{':
                l += 1
                if not arg1_ini and l == 1: #inicio del numeargor
                    arg1_ini = True
                    res['arg1_ini'] = pos
                elif arg1_ini and not arg2_ini and l == 1:
                    arg2_ini = True
                    res['arg2_ini'] = pos                    
            elif s == '}':
                l -= 1
                if not arg1_fin and l == 0: #inicio del numeargor
                    arg1_fin = True
                    res['arg1_fin'] = pos
                elif arg1_fin and not arg2_fin and l == 0:
                    arg2_fin = True
                    res['arg2_fin'] = pos
                    break
                
            pos += 1
            
    else:
        l = 0
        arg_ini = False
        arg_fin = False
        shft = len(nfun)+1
        pos = i0+shft
        for s in ltx[i0+shft:]:
            #determina los límites del argumento
            if s == '{':
                l += 1
                if not arg_ini and l == 1: #inicio del numeargor
                    arg_ini = True
                    res['arg_ini'] = pos                
            elif s == '}':
                l -= 1
                if not arg_fin and l == 0: #inicio del numeargor
                    arg_fin = True
                    res['arg_fin'] = pos                
                    break
            pos += 1
            

    return res
     
#### reemplazar:
# '\\right)' por ')'
# '\\left(' por '('
# '\\frac{x}{y}' por 'x/y'

'''     
# 'x\\times y' por 'x*y'
# 'x\\div y' por 'x/y'     
'''
    
def ltx2cad(ltx):
    #reemplaza paréntesis
    res = ltx.replace('\\left(','(')
    res = res.replace('\\right)',')')
    res = res.replace('\\times','*')
    res = res.replace('\\cdot','*')
    res = res.replace('\\div','/')
    
    #reemplaza las fracciones
    ind = res.find('\\frac{')
    while ind >= 0: 
        
        pos = ltx_find_amb_lims(2,'frac',ind,res)
        #sustitución            
        num = res[pos['arg1_ini']+1:pos['arg1_fin']]
        den = res[pos['arg2_ini']+1:pos['arg2_fin']]
        res = res[:ind]+'(' + num + ')/(' + den + ')' + res[pos['arg2_fin']+1:]
        ind = res.find('\\frac{')
    
    
    res = ajusta_cad_latex(res,[])
        
    funcs = ['\\sqrt', '\\sin', '\\cos','\\tan', '\\cot', '\\log', '\\sec', '\\csc', '\\ln']
    
    for f in funcs:
        ind = res.find(f+'{')
        fr = f.replace('\\','')
        while ind >= 0:             
            pos = ltx_find_amb_lims(1,fr,ind,res)
            #sustitución            
            arg = res[pos['arg_ini']+1:pos['arg_fin']]
            res = res[:ind]+fr+'(' + arg + ')' + res[pos['arg_fin']+1:]
            ind = res.find(f+'{')
     
    return res
        
def evalua_arbol(t,pos):
    if len(t[pos][2]) == 0:
        return t[pos][1]
    else:
        nod = t[pos]
        h = nod[2]
        hd = evalua_arbol(t,h[0])
        hi = evalua_arbol(t,h[1])
        if nod[1] == '+':
            return hd+hi
        elif nod[1] == '-':
            return hd-hi
        elif nod[1] == '*':
            return hd*hi
        else:
            return hd/hi

def descompone(smbls):
    ops = ['+','-','*','/']    
    
    #selecciona aleatoriamente una operación aritmética
    op = ops[randint(0,3)]
    
    #guarda una expresión aleatoria (puede ser un símbolo o un dígito)
    digs = range(1,10)
    
    r = random()    
    if r < 0.3:
        li = sample(digs,1)
    else:
        li = sample(smbls,1)
    
    r = random()    
    if r < 0.3:
        ld = sample(digs,1)
    else:
        ld = sample(smbls,1)
                    
    res = [op,li[0],ld[0]]
    return res

#genera un árbol arbitrario y guarda en las hojas los lados derechos de las identidades
def genera_arbol(tot_oper,smbls):
    # inicia con un árbol sin hijos
    n_op = 0
    pend = []    
    a = [[None,0,[]]]
    pend.append(0)
    
    while n_op < tot_oper:
        #accede aleatoriamente a un nodo sin hijos
        nnod = sample(pend,1)
        #genera los hijos
        #pat = a[nnod[0]]
        d = descompone(smbls)
        #actualiza la información del padre (guarda el operando y apunta a los hijos)
        a[nnod[0]][1] = d[0]        
        pos = len(a)
        hij_pos = [pos,pos+1]        
        a[nnod[0]][2] = hij_pos        
        h1 = [nnod[0],d[1],[]]
        h2 = [nnod[0],d[2],[]]
        a.append(h1)
        a.append(h2)
        pend.append(pos)
        pend.append(pos+1)
        pend.remove(nnod[0])
        n_op = n_op+1
        
    return a
    
def hoja(h):
    if len(h[2]) == 0:
        return True
    else:
        return False
        
#regresa los índices de todas las hojas
def hojas(t):
    res = []
    for i in range(len(t)):
        if hoja(t[i]):
            res.append(i)
    return res
    
def jerarq(op1, op2):
    ops = ['/','*','-', '+']    
    return ops.index(op1) >= ops.index(op2)

#regresa los términos en paréntesis    
def terms_par(cad):
    trms = []
    n = 0
    buf = ''
    for s in cad:
        if s == '(':
            n += 1
        elif s == ')':
            n -= 1        
        
        if n > 0:
            buf += s    
        
        if s == ')': #si se acaba de cerrar un grupo
            if n == 0:
                trms.append(buf+')')
                buf = ''
        elif n == 0: # s!= ')' 
            trms.append(s)
    return trms


#recibe una cadena y separa los términos considerando la jerarquía de operaciones    
def Separa(cad):
    ops = ['+', '-', '*', '/']
    dat_op = {}
    n = 0
    in_prnts = True
    lc = len(cad)
    for i,s in enumerate(cad):
        if s == '(':
            n += 1
        elif s == ')':
            n -=1        
        if n == 0 and s in ops:
            if not 'op' in dat_op.keys():
                dat_op['op'] = s
                dat_op['ind'] = i
            elif jerarq(s,dat_op['op']):
                dat_op['op'] = s
                dat_op['ind'] = i
        
        if n == 0 and i < lc-1:
            in_prnts = False
    if in_prnts:
        return [cad]
        
    #si encuentra el operador de mayor jaraquía
    if 'op' in dat_op.keys():
        op = dat_op['op']
        i = dat_op['ind']
        return [op,cad[:i],cad[i+1:]]
    #si no tiene operadores es una función o una potencia (o ambas)
    else: #siempre y cuando no esté entre paréntesis
        #busca una potencia
        n = 0
        found = False
        for i,s in enumerate(cad):
            if s == '(':
                n += 1
            elif s == ')':
                n -= 1
            if s == '^' and n == 0:
                found = True                
                break
        if found:
            ex = cad[i:]
            return [ex,cad[:i]]
            
        #funcs = ['sqrt','sin','cos','tan','cot','sec','csc','log', 'ln','exp']
        #averigua si el término es una función
        ff =  ''
        findx = len(cad)+1
        for f in funciones:
            ind = cad.find(f)
            if ind >= 0 and ind < findx:
                ff = f
                findx = ind
        if ff in funciones:
            rad = ''
            #inicia en el paréntesis izquierdo
            i_izq = ind+len(ff)
            l = 1
            for s in cad[i_izq+1:]:                
                if s == '(':
                    l += 1
                elif s == ')':
                    l -= 1
                
                if l > 0:
                    rad += s
                else:
                    break
            return [ff,rad]
        else:
            return [cad]
            
        
    
#construye un subárbol que debe descender del vértice ind
#el índice puede modificarse, por lo cual se regresa el valor (actualizado o no)
def construye_arbol(cad,ind_root,arbol):
    
    #debe tener cuidado si la cadena viene con un signo negativo
    if cad[0] == '-':        
        n_ind_root = construye_arbol('0'+cad,ind_root,arbol)
        return n_ind_root
            
    else:        
        cad_terms = Separa(cad)
        nodo = arbol[ind_root]
        nt = len(cad_terms)
        n = len(arbol)                        
        if nt == 3:        
            
            nodo['val'] = cad_terms[0]            
            
            nod1 = {'ind_pat':ind_root, 'ind':n}
            nod2 = {'ind_pat':ind_root, 'ind':n+1}
            
            arbol.append(nod1)
            arbol.append(nod2)
            
            nh1 = construye_arbol(cad_terms[1],n,arbol)
            nh2 = construye_arbol(cad_terms[2],n+1,arbol)
            
            nodo['ind_h1'] = nh1
            nodo['ind_h2'] = nh2
            
            return ind_root
            
        elif nt == 2: #cuadrado o alguna función
            #guarda la función en el nodo y manda separar el término restante
            nodo['val'] = cad_terms[0]
            
            #genera el descendiente
            nod1 = {'ind':n, 'ind_pat':ind_root} #un solo descendiente
            arbol.append(nod1)
            
            n_ind_root = construye_arbol(cad_terms[1],n,arbol)
            nodo['ind_h1'] = n_ind_root
            
            return ind_root
            
        elif nt == 1:
            t = cad_terms[0]
            if t[0] == '(':
                n_cad = t[1:-1]
                n_ind_root = construye_arbol(n_cad,ind_root,arbol)
                return n_ind_root
            else:
                #probar si es un número convertir, si es un símbolo sustituir de un diccionario de símbolos
                nodo['val'] = t
                return ind_root
    
def cad2tree(cad):
    
    t = [] #guarda los nodos del árbol
    nodo = {'ind':0} #nodo raíz
    t.append(nodo)    
    
    construye_arbol(cad,0,t)
        
    return t

def cad2num(cad,digs):
    #la cadena puede estar envuelta entre paréntesis
    if cad.find('(') >= 0:
        ncad = unwrap_cad(cad)
    else:
        ncad = copy(cad)
    for i,c in enumerate(ncad):
        if i > 0 and not c in digs:
            return False        
        elif i == 0:
            if not c in digs and c != '-':
                return False        
    return eval(ncad)

def hoja2expr(h, digs, symbs): #recibe una hoja y regresa el valor en ella
    
    if h['val'][0] in digs:
        val = cad2num(h['val'],digs)
        return val
    elif h['val'][0] == '-' and h['val'][1] in digs:
        val = cad2num(h['val'][1:],digs)
        return -val        
    elif h['val'] in symbs:
        return symbols(h['val'])
    else:
        return False

def tree2expr(t,pos,symbs):
    digs = ['0','1','2','3','4','5','6','7','8','9','.']

    nod = t[pos]
    
    #si es una hoja (no tiene hijos)    
    if not 'ind_h1' in nod.keys():
        return hoja2expr(nod, digs, symbs)
    else:        
        h1 = t[nod['ind_h1']]
        e1 = tree2expr(t,h1['ind'],symbs)
        if not e1 and type(e1) == type(False):
            return False
        if not 'ind_h2' in nod.keys(): #nodo con un solo hijo asociado con una función
            
            #identifica la función guardada en el nodo
            ind = nod['val'].find('^') #potencia
            if ind >= 0:
                ex = nod['val'][1:]
                ex = str2expr(ex,symbs)
                #ex = cad2num(ex,digs)
                if not ex:
                    return False
                else:
                    return e1**ex #cuidar que el exponente no sea muy grande
            for f in funciones:
                ind = nod['val'].find(f) #raíz cuadrada
                if ind >= 0:
                    if f == 'sqrt':
                        return sqrt(e1) 
                    elif f == 'sin':
                        return sin(e1) 
                    elif f == 'cos':
                        return cos(e1) 
                    elif f == 'tan':
                        return tan(e1) 
                    elif f == 'cot':
                        return cot(e1) 
                    elif f == 'sec':
                        return sec(e1) 
                    elif f == 'csc':
                        return csc(e1) 
                    elif f == 'log':                        
                        return log(e1) 
                    elif f == 'acos':
                        return acos(e1)
                    elif f == 'asin':
                        return asin(e1)
                    elif f == 'atan':
                        return atan(e1)
                    elif f == 'exp':
                        return exp(e1)
                        
            #si el nodo tiene un solo hijo, debe ser una función 
            return False
        else:
            h2 = t[nod['ind_h2']]
            e2 = tree2expr(t,h2['ind'],symbs)
            if not e2 and type(e2) == type(False):
                return False
            
            if nod['val'] == '+':
                return e1+e2
            elif nod['val'] == '-':
                return e1-e2
            elif nod['val'] == '*':
                return e1*e2
            else:
                if e2 == 0:
                    return False
                else:
                    tp = type(0)
                    if type(e1) == tp and type(e2) == tp:
                        return Rational(e1,e2)
                    else:
                        return e1/e2

def root(arbol):
    for i,n in enumerate(arbol):
        if not 'ind_pat' in n:
            return i 

def str2expr(cad,symbs):
    a_cad = ajusta_cadena(cad,symbs)
    t = cad2tree(a_cad)
    
    #busca el nodo raíz del árbol
    pos = 0
    e = tree2expr(t,pos,symbs)
    return e
    
def sugiere_fact_com(e):
    fctrs = {}
    or_trms = e.as_ordered_terms() 
    for t in or_trms:
        ord_fctrs = t.as_ordered_factors()
        for f in ord_fctrs:
            sf = str(f)
            if not sf in fctrs.keys():
                fctrs[sf] = 1
            else:
                fctrs[sf] += 1
    for f in fctrs:
        print [f,fctrs[f]]
        
def factores(cad_in):
    
    cad = unwrap_cad(cad_in)
    
    n = 0
        
    #la expresión está factorizada?
    for i,s in enumerate(cad):
        if s == '(':
            n += 1
        elif s == ')':
            n -= 1
        
        ### si la cadena empieza con un signo menos?        
        if n == 0 and s in ['+','-']:
            if not (i == 0 and s == '-'):
                return [cad]    
    n = 0
    res = []    
    buff = '' #
    l = len(cad)
    
    for i,s in enumerate(cad):
        if s == '(':
            n += 1
        elif s == ')':
            n -= 1
        
        #el cambio se da si se cambia entre                
        if n == 0 and (s in ['*','/'] or i == l-1):
            if s != '*' and s!= '/':
                buff += s
            res.append(buff)
            buff = ''
        else:
            buff += s
    return res
    
#esta función toma una cadena y regresa la lista de factores
#por ejemplo
# a*x+b, regresa ax+b (un solo factor)
# a*x, regresa [a,b]   
# x/y, regresa [x,]    
    
#si la cadena llega "envuelta" en paréntesis, la desenvuelve 
def factores2(cad_in):
    
    cad = unwrap_cad(cad_in)
    
    n = 0
        
    #la expresión está factorizada?
    for i,s in enumerate(cad):
        if s == '(':
            n += 1
        elif s == ')':
            n -= 1
        
        ### si la cadena empieza con un signo menos?        
        if n == 0 and s in ['+','-']:
            if not (i == 0 and s == '-'):
                return [cad,[]]
    n = 0
    num_facts = []    
    den_facts = []        
    
    buff = '' #
    l = len(cad)
    
    in_num = True
    
    for i,s in enumerate(cad):
        if s == '(':
            n += 1
        elif s == ')':
            n -= 1
        
        #el cambio se da si se cambia entre                
        if n == 0 and (s in ['*','/'] or i == l-1):
            if s != '*' and s!= '/': #guarda el último carácter
                buff += s            
            if in_num:
                num_facts.append(buff)
            else:
                den_facts.append(buff)
                in_num = True 
            if s == '/':
                in_num = False
            buff = ''
        else:
            buff += s
    return [num_facts,den_facts]

#esta función toma una cadena y regresa la lista de factores
#por ejemplo
# a*x+b, regresa ax+b (un solo factor)
# a*x, regresa [a,b]   
# x/y, regresa [x,]    
    
#si la cadena llega "envuelta" en paréntesis, la desenvuelve 
def factores3(cad_in,in_num):
    
    in_num_in = in_num
    
    cad = unwrap_cad(cad_in)
    
    n = 0
        
    #la expresión está factorizada?
    for i,s in enumerate(cad):
        if s == '(':
            n += 1
        elif s == ')':
            n -= 1
        
        ### si la cadena empieza con un signo menos?        
        if n == 0 and s in ['+','-']:
            if not (i == 0 and s == '-'):
                return [{'c':cad,'in_num':in_num}]
    n = 0
    facts = []
    
    buff = '' #
    l = len(cad)
    
    for i,s in enumerate(cad):
        if s == '(':
            n += 1
        elif s == ')':
            n -= 1
        
        #el cambio se da si se cambia entre                
        if n == 0 and (s in ['*','/'] or i == l-1):
            if s != '*' and s!= '/': #guarda el último carácter
                buff += s            
                
            wpd = wrapped2(buff) 
            if wpd['wpd']:
                if not wpd['neg']:
                    ff = factores3(buff,in_num)
                else:
                    ff = factores3(buff[1:],in_num)
                    facts.append({'c':'-1','in_num':in_num})
                for f in ff:
                    facts.append(f)
            else:
                facts.append({'c':buff,'in_num':in_num})
            buff = ''
            if s == '/':
                in_num = not in_num
            elif s == '*' and in_num != in_num_in:
                in_num = in_num_in
        else:
            buff += s
    return facts
    
'''
def ajusta_cad_latex(cad_in,symbs):
    
    cad = cad_in.replace(' ','')
    cad = cad.replace('\\left(','(')
    cad = cad.replace('\\right)',')')
    
    excps = ['+','-','*','/','^','{','(']
    res = ''
    for i,s in enumerate(cad):
        if i > 0:
            if s == '\\': #inicio de una función
                sa = cad[i-1]
                if sa not in excps:
                    res += '*'                
        res += s
        
    res = res.replace('{','(')
    res = res.replace('}',')')
    
    #excepto en los exponentes
    
    res2 = ''
    #manejar el caso de un símbolo precedido por una variable
    in_name = False
    in_exp = False
    for i,s in enumerate(res):#identifica si está en el nombre de una función (entre '\\' y '{')
        #if i > 0:#y si inicia con una función?            
        if s == '\\':
            in_name = True
        elif in_name and s == '^' and not in_exp:
            in_exp = True        
        elif in_name and in_exp and s == ')':
            in_exp = False        
        elif in_name and s == '(' and not in_exp:
            in_name = False            
        elif i > 0 and not in_name and (s in symbs or s == '('):
            sa = res[i-1]
            if sa not in excps:
                res2 += '*'
        res2 += s
    
    res2 = res2.replace('\\','')
            
    return res2
'''

def ajusta_cad_latex(cad_in,symbs):
    
    cad = cad_in.replace(' ','')
    cad = cad.replace('\\left(','(')
    cad = cad.replace('\\right)',')')
    
    excps = ['+','-','*','/','^','{','(']
    res = ''
    for i,s in enumerate(cad):
        if i > 0:
            if s == '\\': #inicio de una función
                sa = cad[i-1]
                if sa not in excps:
                    res += '*'                
        res += s
        
    res = res.replace('{','(')
    res = res.replace('}',')')
    
    #excepto en los exponentes
    
    res2 = ''
    #manejar el caso de un símbolo precedido por una variable
    in_name = False
    in_exp = False
    for i,s in enumerate(res):#identifica si está en el nombre de una función (entre '\\' y '{')
        #if i > 0:#y si inicia con una función?            
        if s == '\\':
            in_name = True
        elif in_name and s == '^' and not in_exp:
            in_exp = True        
            lev_exp = 0
        elif in_name and in_exp and s == ')':
            lev_exp = lev_exp-1
            if lev_exp == 0:
                in_exp = False        
        elif in_name and in_exp and s == '(':
            lev_exp = lev_exp+1            
        elif in_name and s == '(' and not in_exp:
            in_name = False            
        elif i > 0 and not in_name and (s in symbs or s == '('):
            sa = res[i-1]
            if sa not in excps:
                res2 += '*'
        res2 += s
    
    res2 = res2.replace('\\','')
            
    return res2
    
'''
def ltx2cad_ajst(ltx,symbs):
    #return ajusta_cad_latex(ltx,symbs)
    cad = ltx2cad(ltx)        
    return cad
    #return ajusta_cad_latex(cad,symbs)
'''

def valida_ltx(ltx_in, symbols, funcs):
    #verifica que la cadena tenga contenido
    tmp = ltx_in.replace(' ','')
    if len(tmp) == 0:
        return {'cad':'','valida':False}
    
    ncad = tmp
    for f in funcs:
        if ncad.find('\\'+f) >=0:
            ncad = ncad.replace(f,'$'+f+'$')
    
    #tmp = depura_funcion_potencia(ncad)
    
    #revisa que el número de paréntesis de apertura iguale al número de paréntesis de cierre
    c = 0
    for s in ltx_in:
        if s == '{': #inicia un paréntesis
            c += 1
        elif s == '}':
            c -= 1
        if c < 0:
            return {'cad':ltx_in,'valida':False}
    if c != 0:
        return {'cad':ltx_in,'valida':False}
    
    cad_or = ltx2cad(ltx_in)
    cad = copy(cad_or)
    
    #borra cada una de las funciones
    for f in funcs:
        cad = cad.replace(f,'@')
    
        
    st_vals = ['0','1','2','3','4','5','6','7','8','9','+','-','*','/','^','(',')', '.', '@']
    for s in symbols: 
        st_vals.append(str(s))
    
    
    #revisa cada caracter de la cadena
    #si no es un carácter válido regresa Falso
    for s in cad:
        if not s in st_vals:
            return {'cad':cad,'valida':False}
    
    #revisa que el número de paréntesis de apertura iguale al número de paréntesis de cierre
    c = 0
    for s in cad:
        if s == '(': #inicia un paréntesis
            c += 1
        elif s == ')':
            c -= 1
        if c < 0:
            return {'cad':cad,'valida':False}
    if c != 0:
        return {'cad':cad,'valida':False}
    
    oprs = ['+','-','*','/','^']
    
    #busca errores de sintaxis
    #1- operador junto a operador: +-, *+, 
    #2- operador junto a paréntesis de cierre 
    #3- grupos de paréntesis vacíos ()
    l = len(cad)
    for i in range(l-1):
        sa = cad[i]
        sn = cad[i+1]
        if sa in oprs and sn in oprs:
            return {'cad':cad_or,'valida':False}
        if sa in oprs and sn == ')':
            return {'cad':cad_or,'valida':False}
        if sa == '(' and sn == ')':
            return {'cad':cad_or,'valida':False}
            
    if cad[-1] in oprs:
        return {'cad':ltx_in,'valida':False}
        
    return {'cad':cad_or,'valida':True}
    
def ltx_sympy2quill(ltx_sym):    
    res = ''
    #quita los corchetes que rodean los argumentos de una función
    buf = ''
    fn = False
    l = 0
    for s in ltx_sym:
        w = True
        if s == '\\':
            fn = True
        elif fn:                        
            if s == '{':
                fn = False
                if buf != 'frac':
                    w = False
                    l += 1
            else:
                buf += s
        if l > 0 and s == '}':
            w = False
            l -= 1            
        if w:
            res += s
            
    return res.replace(' ','')
    
#extrae los términos de una cadena de látex (supone que la cadena ya ha sido validada)
def ltx_terminos(ltx,symbs):
    trms = []
    trm = ''
    l = 0
    n = len(ltx)
    for i,s in enumerate(ltx):
        if s == '(':
            l += 1
            trm += s
        elif s == ')' and i < n-1:
            l -= 1
            trm += s
        elif (l == 0 and i > 0 and s in ['+','-']) or i == n-1:            
            if i == n-1:
                trm += s
            trms.append(trm)
            if s == '-':
                trm = '-'
            else:
                trm = ''
        else:
            trm += s
    #convierte cada término en una expresión
    e_trms = []
    for t in trms:
        cad = ajusta_cad_latex(t,symbs)
        trm = str2expr(cad,symbs)
        e_trms.append(trm)
    return e_trms
    
def ltx_terminos2(ltx,symbs):
    trms = []
    trm = ''
    l = 0
    n = len(ltx)
    for i,s in enumerate(ltx):
        if s == '(':
            l += 1
            trm += s
        elif s == ')' and i < n-1:
            l -= 1
            trm += s
        elif (l == 0 and i > 0 and s in ['+','-']) or i == n-1:            
            if i == n-1:
                trm += s
            trms.append(trm)
            if s == '-':
                trm = '-'
            else:
                trm = ''
        else:
            trm += s
    #convierte cada término en una expresión
    return trms
    
def ltx_terminos3(ltx_w,symbs=['a','b','c','x','y','x']):
    
    ltx = unwrap_cad(ltx_w)    
    
    trms = []
    trm = ''
    l = 0
    n = len(ltx)
    for i,s in enumerate(ltx):
        if s == '(':
            l += 1
            trm += s
        elif s == ')' and i < n-1:
            l -= 1
            trm += s
        elif (l == 0 and i > 0 and s in ['+','-']) or i == n-1:            
            if i == n-1:
                trm += s
            trms.append(trm)
            if s == '-':
                trm = '-'
            else:
                trm = ''
        else:
            trm += s
    #convierte cada término en una expresión
    return trms
    

#indica si la cadena está "envuelta" en paréntesis 
#y si el paréntesis inicial y el final corresponden
def wrapped(cad):
    l = 0
    for i,s in enumerate(cad):
        if i > 0 and l == 0:
            return False
        elif s == '(':
            l+=1
        elif s == ')':
            l -= 1
        elif l == 0:
            return False
    return True

#indica si la cadena está "envuelta" en paréntesis
#considera que la cadena puede iniciar con un signo menos
# por ejemplo -(3x+5) estaría envuelta
def wrapped2(cad):
    neg = False
    l = 0
    for i,s in enumerate(cad):
        if not (i == 0 and s == '-'):
            if s == '(':
                l+=1
            elif s == ')':
                l -= 1
            elif l == 0:
                return {'wpd':False,'neg':neg}
        else:
            neg = True
            
    return {'wpd':True,'neg':neg}

    
def unwrap_cad(cad):
    ncad = cad 
    while wrapped(ncad):        
        ncad = ncad[1:-1]
    return ncad

#extrae los términos de una cadena de látex (supone que la cadena ya ha sido validada)    
def str_terminos(cad_in,symbs,unwrap):
    
    if unwrap:
        cad = unwrap_cad(cad_in)
    else:
        cad = cad_in
    
    trms = []
    trm = ''
    l = 0
    n = len(cad)
    for i,s in enumerate(cad):
        if s == '(':
            l += 1
            trm += s
        elif s == ')' and i < n-1: #mientras no llegue al final
            l -= 1
            trm += s
        elif (l == 0 and i > 0 and s in ['+','-']) or i == n-1:            
            if i == n-1:
                trm += s
            trms.append(trm)
            if s == '-':
                trm = '-'
            else:
                trm = ''
        else:
            trm += s
    #convierte cada término en una expresión
    e_trms = []
    for t in trms:
        trm = str2expr(t,symbs)
        e_trms.append(trm)
    return e_trms
    
def varios_terminos(cad):
    l = 0
    for i,s in enumerate(cad):
        if s == '(':
            l += 1
        elif s == ')':
            l -= 1
        elif i > 0 and l == 0 and s in ['+','-']:
            return True
    return False
    
def varios_factores(cad,verify_trms):
    #estrictamente si existen varios términos, entonces la expresión no está factorizada    
    if verify_trms:
        trms = varios_terminos(cad)
        if trms:
            return False 
    
    #selecciona la subcadena a nivel cero de paréntesis
    subcad = ''
    l = 0
    for s in cad:
        if s == '(':
            l += 1
        elif s == ')':
            l -= 1        
        elif l == 0:
            subcad += s
        
    f = subcad.find('\\div')
    if f >= 0:
        return True
    f = subcad.find('\\times')
    if f >= 0:
        return True
    f = subcad.find('^')    
    if f >= 0:
        return True
    
    return False
    
#convierte un árbol en una expresión de latex
#que resume las operaciones representadas en el árbol
def tree2ltx(t,pos):
    nod = t[pos]
    #averigua si el nodo es una hoja
    if not ('ind_h1' in nod.keys()):
        return latex(nod['val'])
    elif not ('ind_h2' in nod.keys()): #función
        l1 = tree2ltx(t,nod['ind_h1'])
        #funcs = ['sqrt','sin','cos','tan','cot','sec','csc','log']
        if nod['val'] in funciones:
            if nod['val'] != 'sqrt':
                return '\\'+nod['val']+'\\left({'+l1+'}\\right)'
            else:
                return '\\'+nod['val']+'{'+l1+'}'
        elif '^' in nod['val']: #potencia
            if l1[0] == '-' or varios_terminos(l1) or varios_factores(l1,False):
                return '\\left(' + l1 + '\\right)^{'+nod['val'][1:]+'}'
            else:            
                return l1+'^{'+nod['val'][1:]+'}'
    else:
        l1 = tree2ltx(t,nod['ind_h1'])
        l2 = tree2ltx(t,nod['ind_h2'])
        if nod['val'] == '+': 
            if l2[0] == '-':
                return l1+'+\\left('+l2+'\\right)'
            else:
                return l1 + '+' + l2
        elif nod['val'] == '-':
            if l2[0] == '-' or varios_terminos(l2):
                return l1+'-\\left('+l2+'\\right)'
            else:
                return l1 + '-' + l2            
        elif nod['val'] == '*':
            if varios_terminos(l1):
                f1 = '\\left(' + l1 + '\\right)'                
            elif l1 == '-1':
                f1 = '-'
            elif l1 == '1':
                f1 = ''
            else:
                f1 = l1
            if l2[0] == '-' or varios_terminos(l2):
                f2 = '\\left(' + l2 + '\\right)'
            else:
                f2 = l2
            if l1 in ['-1','1']:
                return f1 + f2  
            else:
                return f1 + '\\times ' + f2  #verificar si los hijos son hojas, si las hojas son nega
        elif nod['val'] == '/':            
            if varios_terminos(l1) or varios_factores(l1,False):
                f1 = '\\left(' + l1 + '\\right)'
            else:
                f1 = l1
            if l2[0] == '-' or varios_terminos(l2) or varios_factores(l2,False):
                f2 = '\\left(' + l2 + '\\right)'
            else:
                f2 = l2
            return f1 + '\\div ' + f2 #verificar si los hijos son hojas o no
    

#separa los factores de numerador y denominador

def num_den_fact(cad):
    num = ''
    den = ''
    #identfica el ambiente de la fracción
    n = 0
    buff = ''
    in_num = False
    in_den = False
    in_f = False    
    for i,s in enumerate(cad):
        if not in_num and not in_den:
            if s == '\\':
                buff = ''
                in_f = True
            elif buff == 'frac' and s == '{': #empieza a buscar el numerador
                in_num = True
                buff = ''
                n = 1
            elif in_f and not in_num:
                buff += s            
        elif in_num:            
            if s == '{':
                n += 1
            elif s == '}':
                n -= 1            
            if n == 0:
                num = buff
                in_num = False
                in_den = True
                buff = ''
            else:
                buff += s 
        elif in_den:
            if s == '{':
                n += 1
            elif s == '}':
                n -= 1            
            if n == 0:
                den = buff
                in_den = False
            else:
                if not (n == 1 and s == '{'):
                    buff += s 
    return [num, den]
    
#una fracción puede aparecer como 3\\frac{1}{2}
#el 3 se debe agregar al numerador    
def num_den_fact2(cad):
    num = ''
    den = ''
    #identfica el ambiente de la fracción
    n = 0
    buff = ''
    in_num = False
    in_den = False
    in_f = False    
    for i,s in enumerate(cad):
        if not in_num and not in_den:
            if s == '\\':
                buff = ''
                in_f = True
            elif buff == 'frac' and s == '{': #empieza a buscar el numerador
                in_num = True
                buff = ''
                n = 1
            elif in_f and not in_num:
                buff += s            
        elif in_num:            
            if s == '{':
                n += 1
            elif s == '}':
                n -= 1            
            if n == 0:
                num = buff
                in_num = False
                in_den = True
                buff = ''
            else:
                buff += s 
        elif in_den:
            if s == '{':
                n += 1
            elif s == '}':
                n -= 1            
            if n == 0:
                den = buff
                in_den = False
            else:
                if not (n == 1 and s == '{'):
                    buff += s 
    return [num, den]   


if __name__ == '__main__':
    symbs = ['x']
    
    #ltx = "- \\frac{4 \\tan^{2}{\\left(x \\right)}}{3} - \\frac{4}{3}"
    ltx = "3(x+2)"
    #ltx = '\\sin{x}'
    d = valida_ltx(ltx, symbs, funciones)
    cad = d['cad']
    print(cad) #cadena de texto
    a_cad = ajusta_cadena(cad,symbs) #procesa la cadena
    print(a_cad)
    t = cad2tree(a_cad)
    print(t)
    
    pos = 0
    e = tree2expr(t,pos,symbs)
    print(e) #expresión de sympy
    
    
    