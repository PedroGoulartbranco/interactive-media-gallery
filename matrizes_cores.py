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

matriz_verde = (
    0.0, 0.0, 0.0, 0,  # Canal Vermelho (R) zerado
    0.0, 1.0, 0.0, 0,  # Canal Verde (G) em 100%
    0.0, 0.0, 0.0, 0   # Canal Azul (B) zerado
)

matriz_azul = (
    0.0, 0.0, 0.0, 0,  # Canal Vermelho (R) zerado
    0.0, 0.0, 0.0, 0,  # Canal Verde (G) zerado
    0.0, 0.0, 1.0, 0   # Canal Azul (B) em 100%
)

matriz_amarela = (
    1.0, 0.0, 0.0, 0,  # Canal Vermelho (R) em 100%
    0.0, 1.0, 0.0, 0,  # Canal Verde (G) em 100%
    0.0, 0.0, 0.0, 0   # Canal Azul (B) zerado
)

matriz_colorida = (
    1.5, -0.2, -0.2, 0,  # Aumenta o Vermelho e diminui a interferência de G e B
   -0.2,  1.5, -0.2, 0,  # Aumenta o Verde e diminui a interferência de R e B
   -0.2, -0.2,  1.5, 0   # Aumenta o Azul e diminui a interferência de R e G
)

matriz_roxa = (
    1.0, 0.0, 0.0, 0,  # Canal Vermelho (R) em 100%
    0.0, 0.0, 0.0, 0,  # Canal Verde (G) zerado
    0.0, 0.0, 1.0, 0   # Canal Azul (B) em 100%
)

matriz_raiox = (
            0.0, 0.0, 0.0, 0,    # Remove totalmente o Vermelho (R)
            0.0, 0.5, 0.3, 0,    # Deixa o Verde (G) mais suave
            0.0, 0.4, 1.0, 0     # Dá foco total no Azul (B)
        )