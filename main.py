#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Principal - Algoritmo de Dijkstra
Inicia a interface web Streamlit
"""

import sys
import subprocess


def main():
    print("Iniciando interface Streamlit...")
    print("Acesse http://localhost:8501 no navegador")
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app_dijkstra.py'])


if __name__ == "__main__":
    main()

