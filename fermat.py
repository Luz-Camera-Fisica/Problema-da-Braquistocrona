from manim import *
import numpy as np
from scipy.optimize import fsolve

class CicloideSequencial(Scene):
    def construct(self):
        # Abertura
        titulo = Text("Princípio de Fermat", font_size=48, font="Times").to_edge(UP)
        subtitulo = Text("A luz escolhe o caminho de menor tempo", font_size=28, font="Times").next_to(titulo, DOWN)
        self.play(Write(titulo), Write(subtitulo))
        self.wait(2)
        self.play(FadeOut(titulo), FadeOut(subtitulo))

        # ------------------- CENA DE REFLEXÃO -------------------
        titulo_reflexao = Text("Reflexão: o caminho mais rápido", font_size=30, font="Times").to_edge(UP)
        espelho = Line(start=LEFT * 5, end=RIGHT * 5, color=GRAY).shift(DOWN * 1.5)
        label_espelho = Text("Espelho", font_size=18, font="Times").next_to(espelho, DOWN)

        ponto_A2 = Dot([-4, 2, 0], color=YELLOW)
        ponto_B2 = Dot([4, 2, 0], color=YELLOW)
        imagem_B = Dot([4, -5, 0], color=BLUE).set_opacity(0.5)

        raio_inc = Line(ponto_A2.get_center(), [1, -1.5, 0], color=ORANGE)
        raio_ref = Line([1, -1.5, 0], ponto_B2.get_center(), color=ORANGE)

        linha_simetrica = Line(ponto_A2.get_center(), imagem_B.get_center(), color=WHITE).set_stroke(opacity=0.3)

        self.play(Write(titulo_reflexao), Create(espelho), Write(label_espelho))
        self.play(FadeIn(ponto_A2), FadeIn(ponto_B2), FadeIn(imagem_B))
        self.play(Create(raio_inc), Create(raio_ref), Create(linha_simetrica))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ------------------- FUNÇÃO GERAL -------------------
        def draw_cicloide(n_meios, n_start=1.0, n_end=1.5):
            cores = [PURPLE, ORANGE, TEAL, GOLD]
            largura = 10.0
            y_max_layer = 3.0
            y_min_layer = -3.5
            alturas = np.linspace(y_max_layer, y_min_layer, n_meios + 1)

            ponto_A_coords = np.array([-largura/2, alturas[0], 0])
            ponto_B_coords = np.array([largura/2, alturas[-1], 0])
            delta_x = ponto_B_coords[0] - ponto_A_coords[0]
            delta_y = ponto_A_coords[1] - ponto_B_coords[1]

            def sistema(vars):
                a, t = vars
                eq1 = a * (t - np.sin(t)) - delta_x
                eq2 = a * (1 - np.cos(t)) - delta_y
                return [eq1, eq2]

            chute_inicial = [delta_y / 2, np.pi]
            a, t_max = fsolve(sistema, chute_inicial)

            def cicloide(t):
                x = a * (t - np.sin(t)) + ponto_A_coords[0]
                y = ponto_A_coords[1] - a * (1 - np.cos(t))
                return np.array([x, y, 0])

            meios = VGroup()
            linhas_divisorias = VGroup()
            indices_ref = VGroup()

            for i in range(n_meios):
                cor_atual = cores[i % len(cores)]
                alt_sup = alturas[i]
                alt_inf = alturas[i + 1]

                retangulo = Rectangle(
                    width=largura,
                    height=abs(alt_sup - alt_inf),
                    fill_opacity=0.35,
                    stroke_width=1,
                    stroke_color=WHITE
                ).move_to(np.array([0, (alt_sup + alt_inf) / 2, 0]))
                retangulo.set_fill(cor_atual)
                meios.add(retangulo)

                linha_div = Line(
                    start=np.array([-largura/2, alt_inf, 0]),
                    end=np.array([largura/2, alt_inf, 0]),
                    color=WHITE,
                    stroke_width=1
                )
                linhas_divisorias.add(linha_div)

                if n_meios > 1:
                    n_val = n_start + (n_end - n_start) * i / (n_meios - 1)
                else:
                    n_val = n_start

                indice_texto = Text(f"n={n_val:.2f}", font_size=10, font="Times").set_color(WHITE).move_to(
                    np.array([largura/2 - 0.8, (alt_sup + alt_inf) / 2, 0])
                )
                indices_ref.add(indice_texto)

            self.play(*[FadeIn(m) for m in meios], Create(linhas_divisorias), *[Write(ind) for ind in indices_ref])

            dot_A = Dot(ponto_A_coords, color=YELLOW)
            label_A = Text("A", font_size=20, font="Times").next_to(dot_A, LEFT)
            dot_B = Dot(ponto_B_coords, color=YELLOW)
            label_B = Text("B", font_size=20, font="Times").next_to(dot_B, RIGHT)
            self.play(FadeIn(dot_A), FadeIn(dot_B), Write(label_A), Write(label_B))

            t_quebras = []
            for y_obj in alturas:
                cos_t = 1 - (ponto_A_coords[1] - y_obj) / a
                cos_t = np.clip(cos_t, -1, 1)
                t = np.arccos(cos_t)
                t_quebras.append(t)

            pontos_quebra = [cicloide(t) for t in t_quebras]

            caminho_segmentado = VMobject()
            caminho_segmentado.set_points_as_corners(pontos_quebra)
            caminho_segmentado.set_stroke(color=ORANGE, width=6, opacity=1.0)
            self.play(Create(caminho_segmentado), run_time=5)

            ponto_luz = Dot(pontos_quebra[0], radius=0.12, color=YELLOW)
            self.add(ponto_luz)

            def update_ponto(mob, alpha):
                total = len(pontos_quebra) - 1
                t = alpha * total
                i = int(np.floor(t))
                frac = t - i
                if i >= total:
                    pos = pontos_quebra[-1]
                else:
                    pos = pontos_quebra[i] * (1 - frac) + pontos_quebra[i + 1] * frac
                mob.move_to(pos)

            self.play(UpdateFromAlphaFunc(ponto_luz, update_ponto), run_time=5)
            self.wait(2)

            self.play(
                *[FadeOut(m) for m in meios],
                FadeOut(linhas_divisorias),
                *[FadeOut(ind) for ind in indices_ref],
                FadeOut(dot_A),
                FadeOut(label_A),
                FadeOut(dot_B),
                FadeOut(label_B),
                FadeOut(caminho_segmentado),
                FadeOut(ponto_luz)
            )

        # ---- CENA DE 3 MEIOS COM ÍNDICES MAIS PRÓXIMOS E TÍTULO ----
        titulo_meios_proximos = Text("Refração em 3 Meios Estratificados", font_size=28, font="Times").to_edge(UP)
        self.play(Write(titulo_meios_proximos))
        draw_cicloide(3, n_start=1.00, n_end=1.02)
        self.play(FadeOut(titulo_meios_proximos))

        # ---- CENAS COM MAIS MEIOS ----
        titulo_meios_proximos = Text("Aproximando-se de um Meio Contínuo", font_size=28, font="Times").to_edge(UP)
        self.play(Write(titulo_meios_proximos))
        draw_cicloide(10, n_start=1.0, n_end=1.1)
        self.play(FadeOut(titulo_meios_proximos))

        titulo_meios_proximos = Text("A Cicloide: Solução Natural do Princípio de Fermat", font_size=28, font="Times").to_edge(UP)
        self.play(Write(titulo_meios_proximos))
        draw_cicloide(30, n_start=1.0, n_end=1.3)
        self.play(FadeOut(titulo_meios_proximos))

        titulo_meios_proximos = Text("A Cicloide: Solução Natural do Princípio de Fermat", font_size=28, font="Times").to_edge(UP)
        self.play(Write(titulo_meios_proximos))
        draw_cicloide(50, n_start=1.0, n_end=1.5)
        self.play(FadeOut(titulo_meios_proximos))

        # Mensagem final
        fim = Text("A luz sempre segue o caminho mais rápido!", font_size=36, font="Times")
        self.play(Write(fim))
        self.wait(4)
