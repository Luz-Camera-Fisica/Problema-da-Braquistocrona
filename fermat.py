from manim import *
import numpy as np

class PrincipioDeFermat(Scene):
    def construct(self):
        # Títulos
        titulo = Text("Princípio de Fermat", font_size=48).to_edge(UP)
        subtitulo = Text("A luz escolhe o caminho de menor tempo", font_size=28).next_to(titulo, DOWN)
        self.play(Write(titulo), Write(subtitulo))
        self.wait(2)
        self.play(FadeOut(titulo), FadeOut(subtitulo))

        # Divisão dos meios
        linha_limite = Line(start=LEFT * 6 + DOWN, end=RIGHT * 6 + DOWN, color=WHITE)
        ar = Rectangle(width=12, height=3, color=BLUE, fill_opacity=0.2).next_to(linha_limite, UP, buff=0)
        agua = Rectangle(width=12, height=3, color=GREEN, fill_opacity=0.2).next_to(linha_limite, DOWN, buff=0)

        label_ar = Text("Ar (n = 1.0)", font_size=24).next_to(ar, UP)
        label_agua = Text("Água (n = 1.33)", font_size=24).next_to(agua, DOWN)

        self.play(FadeIn(ar), FadeIn(agua), Create(linha_limite))
        self.play(Write(label_ar), Write(label_agua))

        # Pontos iniciais e finais
        ponto_A = Dot([-5, 2, 0], color=YELLOW)
        ponto_B = Dot([5, -2, 0], color=YELLOW)
        label_A = Text("A", font_size=24).next_to(ponto_A, LEFT)
        label_B = Text("B", font_size=24).next_to(ponto_B, RIGHT)
        self.play(FadeIn(ponto_A), FadeIn(ponto_B), Write(label_A), Write(label_B))

        # Linha reta (comparação)
        linha_reta = Line(ponto_A.get_center(), ponto_B.get_center(), color=GRAY)
        self.play(Create(linha_reta))
        self.wait(1)

        # Ponto de quebra na interface
        ponto_quebra = Dot([0, -1, 0], color=RED)
        self.play(FadeIn(ponto_quebra))

        # Raios reais obedecendo à Lei de Snell
        raio1 = always_redraw(lambda: Line(ponto_A.get_center(), ponto_quebra.get_center(), color=ORANGE))
        raio2 = always_redraw(lambda: Line(ponto_quebra.get_center(), ponto_B.get_center(), color=ORANGE))
        self.play(Create(raio1), Create(raio2))
        self.wait(1)

        # Exibir ângulos com auxílio de linhas perpendiculares
        normal = Line(ponto_quebra.get_center() + UP * 2, ponto_quebra.get_center() + DOWN * 2, color=WHITE, stroke_opacity=0.3)
        self.play(FadeIn(normal))

        # Anima mover o ponto de quebra para ilustrar o princípio
        self.play(ponto_quebra.animate.move_to([1.5, -1, 0]), run_time=3)
        self.wait(1)
        self.play(ponto_quebra.animate.move_to([-1.5, -1, 0]), run_time=3)
        self.wait(1)

        # Fixar na posição correta da Lei de Snell para n1=1, n2=1.33
        self.play(ponto_quebra.animate.move_to([0.9, -1, 0]), run_time=2)
        self.wait(1)

        # Mostrar tempos
        tempo_texto = Text("Tempo total:", font_size=28).to_corner(UL)
        tempo_valor = DecimalNumber(0, num_decimal_places=2, font_size=28).next_to(tempo_texto, RIGHT)

        def atualizar_tempo(mob):
            A = ponto_A.get_center()
            P = ponto_quebra.get_center()
            B = ponto_B.get_center()
            d1 = np.linalg.norm(A - P) / 1     # velocidade na 1ª parte (n=1)
            d2 = np.linalg.norm(P - B) / 0.75  # velocidade na água (v = c/n, n=1.33)
            tempo = d1 + d2
            mob.set_value(tempo)

        tempo_valor.add_updater(atualizar_tempo)
        self.add(tempo_texto, tempo_valor)
        self.wait(3)
        tempo_valor.clear_updaters()

        # Apagar cena
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

        # Reflexão em espelho plano
        titulo_reflexao = Text("Reflexão: o caminho mais rápido", font_size=40).to_edge(UP)
        espelho = Line(start=LEFT * 5, end=RIGHT * 5, color=GRAY).shift(DOWN * 1.5)
        label_espelho = Text("Espelho", font_size=24).next_to(espelho, DOWN)

        ponto_A2 = Dot([-4, 2, 0], color=YELLOW)
        ponto_B2 = Dot([4, 2, 0], color=YELLOW)
        imagem_B = Dot([4, -5, 0], color=BLUE).set_opacity(0.5)

        raio_inc = Line(ponto_A2.get_center(), [1, -1.5, 0], color=ORANGE)
        raio_ref = Line([1, -1.5, 0], ponto_B2.get_center(), color=ORANGE)

        linha_simetrica = Line(ponto_A2.get_center(), imagem_B.get_center(), color=WHITE, stroke_opacity=0.3)

        self.play(Write(titulo_reflexao), Create(espelho), Write(label_espelho))
        self.play(FadeIn(ponto_A2), FadeIn(ponto_B2), FadeIn(imagem_B))
        self.play(Create(raio_inc), Create(raio_ref), Create(linha_simetrica))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])
        fim = Text("A luz sempre segue o caminho mais rápido!", font_size=36)
        self.play(Write(fim))
        self.wait(4)
