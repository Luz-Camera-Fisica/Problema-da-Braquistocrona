from manim import *
import numpy as np

class BraquistocronaPrimeiroQuadrante(Scene):
    def construct(self):
        # Título
        title = Text("Problema da Braquistócrona", font_size=48, font="Liberation Serif").to_edge(UP)
        subtitle = Text("Comparação entre a linha reta e a cicloide", font_size=28, font="Liberation Serif").next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(2)

        # Eixos no primeiro quadrante
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 4, 1],
            x_length=7,
            y_length=4,
            axis_config={"color": WHITE},
        ).shift(DOWN)

        labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(labels))
        self.wait(1)

        r = 4 / np.pi
        y_offset = 0.6

        def reta(x):
            y_start = 2 + y_offset
            y_end = 2 - 2 * r + y_offset
            slope = (y_end - y_start) / 4
            return y_start + slope * x

        curva_reta = axes.plot(reta, color=BLUE, x_range=[0, 4])

        def cicloide_point(t):
            x = r * (t - np.sin(t))
            y = 2 - r * (1 - np.cos(t)) + y_offset
            return axes.c2p(x, y)

        curva_cicloide = ParametricFunction(cicloide_point, t_range=[0, np.pi], color=RED)

        self.play(Create(curva_reta), Create(curva_cicloide))

        label_reta = Text("Reta", font_size=24, color=BLUE, font="Liberation Serif").move_to(
            axes.c2p(2.8, reta(2.8)) + UP * 0.6 + LEFT * 0.5
        )
        label_cicloide = Text("Cicloide", font_size=24, color=RED, font="Liberation Serif").move_to(
            axes.c2p(1.2, 2 - r * (1 - np.cos(1.2 / r))) + DOWN * 0.4 + RIGHT * 0.5
        )
        self.play(Write(label_reta), Write(label_cicloide))
        self.wait(1)

        ponto_final = axes.c2p(4, reta(4))
        linha_pontilhada = DashedLine(start=ponto_final + UP * 1.5, end=ponto_final, color=YELLOW)
        self.play(Create(linha_pontilhada))

        bola_reta = Dot(axes.c2p(0, reta(0)), color=BLUE)
        bola_cicloide = Dot(axes.c2p(0, 2 + y_offset), color=RED)
        self.add(bola_reta, bola_cicloide)

        timer = ValueTracker(0)
        tempo_txt = Text("Tempo: ", font_size=24, font="Liberation Serif").to_corner(UL).shift(DOWN * 0.5)
        tempo_valor = DecimalNumber(0, num_decimal_places=2, font_size=24).next_to(tempo_txt, RIGHT)
        tempo_valor.add_updater(lambda m: m.set_value(timer.get_value()))
        self.add(tempo_txt, tempo_valor)

        def move_reta(m, alpha):
            x = 4 * alpha
            m.move_to(axes.c2p(x, reta(x)))

        def move_cicloide(m, alpha):
            t = alpha * np.pi
            m.move_to(cicloide_point(t))

        self.play(
            UpdateFromAlphaFunc(bola_reta, move_reta, run_time=4, rate_func=linear),
            UpdateFromAlphaFunc(bola_cicloide, move_cicloide, run_time=2, rate_func=linear),
            timer.animate.set_value(4)
        )
        timer.clear_updaters()
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

        titulo_eq = Text("Equações das Curvas", font_size=44, font="Liberation Serif").to_edge(UP)
        eq_reta = MathTex(r"\text{Reta: } y = 2 - \frac{x}{2}", color=BLUE).shift(UP * 1)
        eq_cicloide = MathTex(r"\text{Cicloide: } x = r(t - \sin t), \quad y = 2 - r(1 - \cos t)", color=RED)

        self.play(Write(titulo_eq))
        self.play(Write(eq_reta))
        self.play(Write(eq_cicloide))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

        title_exp = Text("Por que a cicloide é mais rápida?", font_size=44, font="Liberation Serif").to_edge(UP)

        texto1 = Text("A cicloide é a curva de descida mais rápida entre dois pontos,", font_size=28, font="Liberation Serif").next_to(title_exp, DOWN, buff=0.5)
        texto2 = Text("porque ela permite que o corpo ganhe velocidade mais rapidamente,", font_size=28, font="Liberation Serif").next_to(texto1, DOWN, aligned_edge=LEFT)
        texto3 = Text("graças à sua inclinação inicial mais acentuada.", font_size=28, font="Liberation Serif").next_to(texto2, DOWN, aligned_edge=LEFT)
        texto4 = Text("Mesmo com um caminho mais longo do que a reta,", font_size=28, font="Liberation Serif").next_to(texto3, DOWN, aligned_edge=LEFT)
        texto5 = Text("o tempo total de descida é menor.", font_size=28, font="Liberation Serif").next_to(texto4, DOWN, aligned_edge=LEFT)
        texto6 = Text("Esse problema foi proposto por Johann Bernoulli em 1696", font_size=28, font="Liberation Serif").next_to(texto5, DOWN, aligned_edge=LEFT)
        texto7 = Text("e sua solução marcou o nascimento do cálculo das variações.", font_size=28, font="Liberation Serif").next_to(texto6, DOWN, aligned_edge=LEFT)

        self.play(Write(title_exp))
        self.wait(0.5)
        self.play(Write(texto1))
        self.play(Write(texto2))
        self.play(Write(texto3))
        self.wait(0.5)
        self.play(Write(texto4))
        self.play(Write(texto5))
        self.wait(0.5)
        self.play(Write(texto6))
        self.play(Write(texto7))
        self.wait(5)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

        grafico = BarChart(
            values=[2, 4],
            bar_names=["Cicloide", "Reta"],
            y_range=[0, 5, 1],
            y_length=3,
            x_length=6,
            bar_colors=[RED, BLUE]
        )

        titulo_grafico = Text("Tempo de chegada", font_size=36, font="Liberation Serif").next_to(grafico, UP)

        self.play(Create(grafico), Write(titulo_grafico))
        self.wait(4)
