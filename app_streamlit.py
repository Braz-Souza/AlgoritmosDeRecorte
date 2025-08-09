import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from cohen_sutherland import cohen_sutherland
from ponto_medio import ponto_medio
from sutherland_hodgman import sutherland_hodgman

def plot_result(title, fig, ax):
    st.subheader(title)
    st.pyplot(fig)
    plt.close(fig)

def main():
    st.title("Algoritmos de Recorte")
    
    tab1, tab2, tab3 = st.tabs(["Cohen-Sutherland", "Ponto Médio", "Sutherland-Hodgman"])
    
    with tab1:
        st.header("Clipping de Linhas - Cohen-Sutherland")
        
        col1, col2 = st.columns(2)
        with col1:
            x1 = st.number_input("P1 - X:", value=5)
            y1 = st.number_input("P1 - Y:", value=5)
        with col2:
            x2 = st.number_input("P2 - X:", value=25)
            y2 = st.number_input("P2 - Y:", value=25)
        
        col3, col4, col5, col6 = st.columns(4)
        with col3:
            x_min = st.number_input("X min:", value=10)
        with col4:
            y_min = st.number_input("Y min:", value=10)
        with col5:
            x_max = st.number_input("X max:", value=20)
        with col6:
            y_max = st.number_input("Y max:", value=20)
        
        if st.button("Executar Cohen-Sutherland"):
            fig, ax = plt.subplots(figsize=(8, 8))
            
            ax.plot([x1, x2], [y1, y2], 'b-', linewidth=2, label='Linha original')
            
            rect = plt.Rectangle((x_min, y_min), x_max-x_min, y_max-y_min, 
                               fill=False, color='red', linewidth=2, label='Janela de clipping')
            ax.add_patch(rect)
            
            p1_clipped, p2_clipped = cohen_sutherland([x1, y1], [x2, y2], [x_min, y_min, x_max, y_max])
            
            if p1_clipped is not None:
                ax.plot([p1_clipped[0], p2_clipped[0]], [p1_clipped[1], p2_clipped[1]], 
                       'g-', linewidth=3, label='Linha recortada')
            
            ax.set_xlim(0, 30)
            ax.set_ylim(0, 30)
            ax.grid(True)
            ax.legend()
            ax.set_title("Cohen-Sutherland Line Clipping")
            
            plot_result("Resultado", fig, ax)
    
    with tab2:
        st.header("Clipping de Linha - Midpoint Subdivision")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Ponto Inicial")
            x1 = st.number_input("X1:", value=5, key="pm_x1")
            y1 = st.number_input("Y1:", value=5, key="pm_y1")
        with col2:
            st.subheader("Ponto Final")
            x2 = st.number_input("X2:", value=25, key="pm_x2")
            y2 = st.number_input("Y2:", value=25, key="pm_y2")
        
        st.subheader("Janela de Clipping")
        col3, col4, col5, col6 = st.columns(4)
        with col3:
            pm_x_min = st.number_input("X min:", value=10, key="pm_x_min")
        with col4:
            pm_y_min = st.number_input("Y min:", value=10, key="pm_y_min")
        with col5:
            pm_x_max = st.number_input("X max:", value=20, key="pm_x_max")
        with col6:
            pm_y_max = st.number_input("Y max:", value=20, key="pm_y_max")
        
        tolerancia = st.slider("Tolerância (pixels):", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
        
        if st.button("Executar Midpoint Subdivision"):
            fig, ax = plt.subplots(figsize=(8, 8))
            
            # Linha original
            ax.plot([x1, x2], [y1, y2], 'b-', linewidth=2, alpha=0.7, label='Linha original')
            
            # Janela de clipping
            rect = plt.Rectangle((pm_x_min, pm_y_min), pm_x_max-pm_x_min, pm_y_max-pm_y_min, 
                               fill=False, color='red', linewidth=2, label='Janela de clipping')
            ax.add_patch(rect)
            
            # Aplicar algoritmo Midpoint Subdivision
            janela = [pm_x_min, pm_y_min, pm_x_max, pm_y_max]
            p1_clipped, p2_clipped = ponto_medio([x1, y1], [x2, y2], janela, tolerancia)
            
            if p1_clipped is not None and p2_clipped is not None:
                ax.plot([p1_clipped[0], p2_clipped[0]], [p1_clipped[1], p2_clipped[1]], 
                       'g-', linewidth=4, label='Linha cortada')
                ax.scatter([p1_clipped[0], p2_clipped[0]], [p1_clipped[1], p2_clipped[1]], 
                          c='green', s=80, zorder=5, label='Pontos de interseção')
            else:
                st.info("Linha completamente fora da janela de clipping")
            
            # Pontos originais
            ax.scatter([x1, x2], [y1, y2], c='blue', s=80, marker='o', 
                      label='Pontos originais', zorder=6)
            
            ax.set_xlim(0, 30)
            ax.set_ylim(0, 30)
            ax.grid(True, alpha=0.3)
            ax.legend()
            ax.set_title("Midpoint Subdivision Line Clipping")
            ax.set_aspect('equal')
            
            plot_result("Resultado", fig, ax)
    
    with tab3:
        st.header("Clipping de Polígonos - Sutherland-Hodgman")
        
        st.subheader("Definir Polígono")
        num_vertices = st.number_input("Número de vértices:", min_value=3, max_value=8, value=4)
        
        polygon = []
        cols = st.columns(2)
        for i in range(num_vertices):
            with cols[i % 2]:
                x = st.number_input(f"Vértice {i+1} - X:", value=5 + i*5, key=f"poly_x_{i}")
                y = st.number_input(f"Vértice {i+1} - Y:", value=5 + (i%2)*10, key=f"poly_y_{i}")
                polygon.append([x, y])
        
        st.subheader("Janela de Clipping")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            clip_x_min = st.number_input("X min janela:", value=8)
        with col2:
            clip_y_min = st.number_input("Y min janela:", value=8)
        with col3:
            clip_x_max = st.number_input("X max janela:", value=18)
        with col4:
            clip_y_max = st.number_input("Y max janela:", value=18)
        
        if st.button("Executar Sutherland-Hodgman"):
            fig, ax = plt.subplots(figsize=(8, 8))
            
            if polygon:
                poly_x = [p[0] for p in polygon] + [polygon[0][0]]
                poly_y = [p[1] for p in polygon] + [polygon[0][1]]
                ax.plot(poly_x, poly_y, 'b-', linewidth=2, label='Polígono original')
            
            rect = plt.Rectangle((clip_x_min, clip_y_min), 
                               clip_x_max-clip_x_min, clip_y_max-clip_y_min, 
                               fill=False, color='red', linewidth=2, label='Janela de clipping')
            ax.add_patch(rect)
            
            clipped_polygon = sutherland_hodgman(polygon, [clip_x_min, clip_y_min, clip_x_max, clip_y_max])
            
            if clipped_polygon:
                clipped_x = [p[0] for p in clipped_polygon] + [clipped_polygon[0][0]]
                clipped_y = [p[1] for p in clipped_polygon] + [clipped_polygon[0][1]]
                ax.fill(clipped_x, clipped_y, alpha=0.3, color='green', label='Polígono recortado')
                ax.plot(clipped_x, clipped_y, 'g-', linewidth=3)
            
            ax.set_xlim(0, 25)
            ax.set_ylim(0, 25)
            ax.grid(True)
            ax.legend()
            ax.set_title("Sutherland-Hodgman Polygon Clipping")
            
            plot_result("Resultado", fig, ax)

if __name__ == "__main__":
    main()