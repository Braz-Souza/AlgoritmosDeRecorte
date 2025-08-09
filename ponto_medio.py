def ponto_medio(p1, p2, janela, tolerancia=1.0):
    """
    Algoritmo de corte de linha com ponto médio (Midpoint Subdivision)
    Usa sucessivas bisseções + testes "dentro/fora" pela janela
    """
    x_min, y_min, x_max, y_max = janela
    
    def esta_dentro(ponto):
        x, y = ponto
        return x_min <= x <= x_max and y_min <= y <= y_max
    
    def distancia(p1, p2):
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
    
    def ponto_medio_calc(p1, p2):
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    
    def encontrar_intersecao(p_dentro, p_fora):
        """Encontra interseção usando bisseção até a tolerância"""
        while distancia(p_dentro, p_fora) > tolerancia:
            meio = ponto_medio_calc(p_dentro, p_fora)
            
            if esta_dentro(meio):
                p_dentro = meio
            else:
                p_fora = meio
        
        return p_dentro
    
    # Verifica se os pontos estão dentro da janela
    p1_dentro = esta_dentro(p1)
    p2_dentro = esta_dentro(p2)
    
    # Caso 1: ambos pontos dentro
    if p1_dentro and p2_dentro:
        return p1, p2
    
    # Caso 2: ambos pontos fora
    if not p1_dentro and not p2_dentro:
        # Verifica se a linha pode intersectar a janela usando bisseção
        meio = ponto_medio_calc(p1, p2)
        if not esta_dentro(meio):
            # Tenta subdividir mais para encontrar possível interseção
            meio1 = ponto_medio_calc(p1, meio)
            meio2 = ponto_medio_calc(meio, p2)
            
            if not esta_dentro(meio1) and not esta_dentro(meio2):
                return None, None  # Linha completamente fora
        
        # Continua bisseção para encontrar interseções
        return encontrar_pontos_intersecao(p1, p2, janela)
    
    # Caso 3: um ponto dentro, um fora
    if p1_dentro and not p2_dentro:
        p2_clipped = encontrar_intersecao(p1, p2)
        return p1, p2_clipped
    else:  # p2_dentro and not p1_dentro
        p1_clipped = encontrar_intersecao(p2, p1)
        return p1_clipped, p2

def encontrar_pontos_intersecao(p1, p2, janela):
    """Encontra pontos de interseção quando ambos pontos estão fora"""
    x_min, y_min, x_max, y_max = janela
    
    def esta_dentro(ponto):
        x, y = ponto
        return x_min <= x <= x_max and y_min <= y <= y_max
    
    def ponto_medio_calc(p1, p2):
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    
    # Subdivide recursivamente para encontrar segmentos que cruzam a janela
    pontos_intersecao = []
    
    def bissecar_segmento(pa, pb, profundidade_max=20):
        if profundidade_max <= 0:
            return
        
        meio = ponto_medio_calc(pa, pb)
        
        pa_dentro = esta_dentro(pa)
        pb_dentro = esta_dentro(pb)
        meio_dentro = esta_dentro(meio)
        
        # Se encontrou mudança de estado, há interseção
        if pa_dentro != meio_dentro:
            bissecar_segmento(pa, meio, profundidade_max - 1)
            if meio_dentro:
                pontos_intersecao.append(meio)
        
        if meio_dentro != pb_dentro:
            if meio_dentro:
                pontos_intersecao.append(meio)
            bissecar_segmento(meio, pb, profundidade_max - 1)
    
    bissecar_segmento(p1, p2)
    
    if len(pontos_intersecao) >= 2:
        return pontos_intersecao[0], pontos_intersecao[-1]
    elif len(pontos_intersecao) == 1:
        return pontos_intersecao[0], pontos_intersecao[0]
    else:
        return None, None