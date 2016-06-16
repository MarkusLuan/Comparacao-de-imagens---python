import os
import json
import math

def abrirSvg(arquivo):
    b = []
    f = open(arquivo, "r")
    for a in f.readline():
        linha = f.readline()
        if "<line" in linha:
            linha = linha.replace("<line ", "")
            linha = linha.replace("/>\n", "")
            b += [linha]
    f.close()
    return b

def pegarDistancia(x, y, X, Y):
    dist = math.sqrt(pow(x-X, 2) + pow(y-Y, 2))
    return dist

def calcularCentroide(ponto):
    centroideX = 0
    centroideY = 0
    for x, y in ponto:
        centroideX += x
        centroideY += y
    centroideX /= len(ponto[0])
    centroideY /= len(ponto[1])
    return [float(format(centroideX, '.1f')), float(format(centroideY, '.1f'))]

def pegaTag(tag, linha):
    tag += "=\""
    return linha[linha.index(tag)+4:linha.index(tag)+ 4 + linha[linha.index(tag)+ 4:].index("\"")];

def pegaPontos(img, ponto, menor):
    for linha in img:
        if [float(pegaTag("x1", linha)), float(pegaTag("y1", linha))] not in ponto:
            ponto += [[float(pegaTag("x1", linha)), float(pegaTag("y1", linha))]]
        if [float(pegaTag("x2", linha)), float(pegaTag("y2", linha))] not in ponto:
            ponto += [[float(pegaTag("x2", linha)), float(pegaTag("y2", linha))]]

    for x,y in ponto:
        if menor[0] is None or menor[0] > float(x):
            menor[0] = float(x)
        if menor[1] is None or menor[1] > float(y):
            menor[1] = float(y)

def aproximadeZero(ponto, menor):
    for P in ponto:
        P[0] -= menor[0]
        P[1] -= menor[1]

    for P in ponto:
        P[0] = float(format(P[0], '.1f'))
        P[1] = float(format(P[1], '.1f'))

def calculaDistancia(dist, ponto):
    j = 0
    while j < len(ponto)-1:
        i = j+1
        while i < len(ponto):
            dist += [pegarDistancia(ponto[j][0],ponto[j][1], ponto[i][0], ponto[i][1])]
            i+=1
        j+=1

def pegaPerimetro(dist):
    perimetroAux = 0
    for p in dist:
        perimetroAux += p
    return perimetroAux

def criarPontos(perimetro, ponto):
    distPontos = perimetro/quantidadePontos

    idx = 0
    somaDists = 0
    x0 = ponto[0][0]
    y0 = ponto[0][1]
    variosPontos = [[x0,y0]]
    for a in range(0, quantidadePontos):
        daux = distPontos
        while somaDists < perimetro :
            x1 = ponto[ (idx+1)%len(ponto)][0]
            y1 = ponto[ (idx+1)%len(ponto)][1]

            distSegmento = pegarDistancia(x0,y0,x1,y1)
            if (distSegmento > daux):
                t = daux/distSegmento
                proxx = x0 + t * (x1-x0)
                proxy = y0 + t * (y1-y0)
                variosPontos += [[float(format(proxx, '.1f')), float(format(proxy, '.1f'))]]
                x0 = proxx
                y0 = proxy
                somaDists += daux
                break
            else :
                daux = daux - distSegmento
                idx += 1
                x0 = ponto[idx % len(ponto)][0]
                y0 = ponto[idx % len(ponto)][1]
                somaDists += distSegmento
    return variosPontos

def criarJson(nome, qtIguais):
    data = []
    d = {}

    d['imagem'] = nome
    d['qtIguais'] = qtIguais
    data += [d]

    return data

def compararImagens(dist1, dist2):
    comp = 0
    a = 0
    while a<len(dist1):
        if dist1[a] in range(int(dist2[a]-500), int(dist2[a]+500)):
            comp += 1
        a+=1
    return comp

imagens = []

for files in os.listdir():
    if files[len(files)-4:] == ".svg" and files != "teste.svg":
        imagens += [files]

comp = []
v = 0
while v<len(imagens):
    ponto1 = []
    ponto2 = []
    menor1 = [None for a in range(2)]
    menor2 = [None for a in range(2)]

    img1 = []
    img2 = []

    img1 = abrirSvg("teste.svg")
    img2 = abrirSvg(imagens[v])

    pegaPontos(img1, ponto1, menor1)
    pegaPontos(img2, ponto2, menor2)

    print("<p style='color:red;'>Imprimindo pontos originais:</p>")
    print("Img1: " + str(ponto1))
    print("\n\nImg2: " + str(ponto2))

    print("\n\n<p style='color:red;'>Tornando pontos mais próximos do zero:</p>")

    aproximadeZero(ponto1, menor1)
    aproximadeZero(ponto2, menor2)

    print("Img1: " +str(ponto1))
    print("\n\nImg2: " + str(ponto2))

    dist1 = []
    dist2 = []
    
    calculaDistancia(dist1, ponto1)
    calculaDistancia(dist2, ponto2)

    perimetro1 = pegaPerimetro(dist1)
    perimetro2 = pegaPerimetro(dist2)
    
    quantidadePontos = 50
    
    variosPontos1 = criarPontos(perimetro1, ponto1)
    variosPontos2 = criarPontos(perimetro2, ponto2)

    print("\n\n<p style='color:red;'>Gerando novos pontos</p>")

    distC1 = []
    distC2 = []

    C1 = calcularCentroide(variosPontos1)
    C2 = calcularCentroide(variosPontos2)
    for x, y in variosPontos2:
        distC2 += [float(format(pegarDistancia(x, y, C2[0], C2[1]), '.1f'))]

    for x, y in variosPontos1:
        distC1 += [float(format(pegarDistancia(x, y, C1[0], C1[1]), '.1f'))]

    comp += [compararImagens(distC1, distC2)]
    v+=1

print("\n\n<p style='color:red;'>Comparando as imagens:</p>")
a = 0
maior = 0
while a<len(comp):
    print("\nImagem : " + imagens[a] + ", indice: " + str(a) + ", Nº * as distancias ao centroide se iguala: " + str(comp[a]))
    if comp[maior] < comp[a]:
        maior = a
    a+=1

print("\n\n\n\nA imagem %s é a mais semelhante a teste.svg" % imagens[maior])


f = open('Grafico.json', 'w')
jsonStr = {}
k = 0
while k<len(imagens):
    jsonStr[k] = criarJson(imagens[k], comp[k])
    k+=1
f.write(json.dumps(jsonStr))
f.close()
