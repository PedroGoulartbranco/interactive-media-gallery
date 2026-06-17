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

matriz_rosa = (
    0.5, 0.0, 0.0, 127,  # Mantém 50% do R e soma 127 de luz vermelha
    0.0, 0.5, 0.0, 0,    # Mantém 50% do G (sem alterar o fundo)
    0.0, 0.0, 0.5, 127   # Mantém 50% do B e soma 127 de luz azul
)

matriz_preta = (
    0.4, 0.0, 0.0, 0,  # Reduz o Vermelho original para apenas 40% da força
    0.0, 0.4, 0.0, 0,  # Reduz o Verde original para apenas 40% da força
    0.0, 0.0, 0.4, 0   # Reduz o Azul original para apenas 40% da força
)

matriz_laranja = (
    1.0, 0.0, 0.0, 0,  # Vermelho no máximo
    0.0, 0.5, 0.0, 0,  # Verde pela metade
    0.0, 0.0, 0.0, 0   # Sem Azul
)

matriz_verde_menta = (
    0.4, 0.0, 0.0, 0,    # Reduz o Vermelho original
    0.0, 0.6, 0.0, 120,  # Mantém o Verde e injeta +120 de névoa verde
    0.0, 0.0, 0.6, 100   # Mantém o Azul e injeta +100 de névoa azul
)

matriz_preto_e_branco = (
    0.35, 0.65, 0.15, -30,  # Aumenta os fatores e puxa o offset para o negativo
    0.35, 0.65, 0.15, -30,  # (Isso "esmaga" as sombras, deixando-as bem pretas)
    0.35, 0.65, 0.15, -30
)

matriz_psicodelica = (
    1.2, 0.0, 0.3, 40,  # Força o Vermelho e injeta luz rosa
    0.0, 0.9, 0.0, 0,   # Segura um pouco o Verde
    0.3, 0.0, 1.4, 20   # Força o Azul e cria os tons cianos
)

matriz_polaroid = (
    1.3, 0.0, 0.0, 20,   # Dá um ganho no Vermelho e aquece a imagem
    0.0, 1.1, 0.0, 15,   # Ajusta o Verde suavemente
    -0.1, 0.0, 0.8, -10  # Reduz o Azul nas sombras para criar o tom amarelado
)