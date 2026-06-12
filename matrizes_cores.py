matriz_vermelho =  (
    1.0, 0.0, 0.0, 0,  # R recebe 100% do Vermelho original
    0.0, 0.0, 0.0, 0,  # G recebe nada
    0.0, 0.0, 0.0, 0   # B recebe nada
)

matriz_branca  = (
    0.5, 0.0, 0.0, 127,  # Mantém 50% do Vermelho original e soma 127 de luz branca
    0.0, 0.5, 0.0, 127,  # Mantém 50% do Verde original e soma 127 de luz branca
    0.0, 0.0, 0.5, 127   # Mantém 50% do Azul original e soma 127 de luz branca
)