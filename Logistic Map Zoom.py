'''
                                    CHAOS THEORY - LOGISTIC MAP
                                         & Zooming into it                                                        '''

import os
import numpy as np
import vispy
from numba import jit, prange
from vispy import app
import vispy.plot as vp
import vispy.io as io
from vispy.scene.visuals import Text
from pathlib import Path
from time import time

record_project = False

gens = 100
rates = 5000

rec_prefix = './frames'
project_name = 'Logistic Map'

frame_dir = Path(f'{rec_prefix}/{project_name}')

if not frame_dir.exists() and record_project:
    frame_dir.mkdir()

feigens = [
    1.0,
    3.0,
    3.4494897,
    3.5440903,
    3.5644073,
    3.5687594,
    3.5696916,
    3.5698913,
    3.569934067807427
]

feigenys = {
    1: 0.0,
    2: .67,
    4: .85,
    8: .884,
    16: .8907,
    32: .8921,
    64: .89214,
    128: .89224,
    256: .89215,
}


@jit(cache=True, nopython=True)
def simulate(num_gens=10, rate_min=0, rate_max=3.99, num_rates=10,
                  num_discard=100, initial_pop=0.5):

    pops = np.empty(shape=(num_gens*num_rates, 2), dtype=np.float64)
    rates = np.linspace(rate_min, rate_max, num_rates)

    for rate_num in prange(len(rates)):

        rate = rates[rate_num]

        pop = initial_pop

        for _ in range(num_discard):
            pop = pop * rate * (1 - pop)

        for gen_num in range(num_gens):
            row_num = gen_num + num_gens * rate_num
            pops[row_num] = [rate, pop]

            pop = pop * rate * (1 - pop)

    return pops


def feigen_ruler(plt, parent, color, x0, y0, x1, y1, x2=None, y2=None):

    serif = 0.1
    serif = serif * abs(y1-y0)

    verts = np.zeros((6, 2))

    verts[0, :] = [x0, y0 + serif]
    verts[1, :] = [x0, y0 - serif]
    verts[2, :] = [x0, y0 + serif*2]
    verts[3, :] = [x1, y0 + serif*2]
    verts[4, :] = [x1, y0 + serif]
    verts[5, :] = [x1, y1 - serif]

    ruler = plt.plot(verts, color=color)

    if x2 != None and y2 != None:
        f = x0-x1

        label = f""

        t = Text(label, face='Cambria Math', parent=parent, color=color)
        t.font_size = 18
        t.pos = (x1-x0)/2 + x0, y0 + serif
    else:
        t = None

    return {'plt': ruler, 'label': t, 'lims':(x1, x0)}


def feigen_lines(target, parent):
    cmap = vispy.color.get_colormap('prism')
    rulers = []

    for f, val in enumerate(feigens):

        if f == 0:
            continue

        c = f / len(feigens)
        c = c**4

        color = cmap[c]

        splits = lambda x: int((2)**(x))

        if f > 1:
            x0 = feigens[f]
            y0 = feigenys[splits(f)]

            x1 = feigens[f-1]
            y1 = feigenys[splits(f-1)]

            x2 = feigens[f-2]
            y2 = feigenys[splits(f-2)]

            d = feigens[f] - feigens[f-1]
            places = (abs(int(np.log10(d))) + 1)

            r = feigen_ruler(target, parent, color, x0, y0, x1, y1, x2, y2)

        else:
            x0 = feigens[f]
            y0 = feigenys[splits(f)]
            places = 1

        label = f"{splits(f)} →"

        t = Text(label, face='Cambria Math',
                    parent=parent, color=color, anchor_x='right')

        t.font_size = 16
        t.pos = x0, y0

        if f > 1:
            r['ptr'] = t
            rulers += [r]

    return rulers


def zoom_plot(target, RATES, ENDS, first=False):

    global gens, rates

    """  ---- CREATE DATA ---- """

    if not first and not 'labels' in project_name:
        start = time()
        print('... Simulating between', RATES, ENDS,'gens, rates', gens, rates)
        pops = simulate(num_gens=gens, num_rates=rates,

                                rate_min=RATES[0], rate_max=RATES[1],

                                num_discard = 1000, initial_pop=0.5)
        print('>>> DONE', round(time()-start,2),'s')

    elif first and 'labels' in project_name:

        mode = 0

        if mode==0:
            start = time()
            print('... Simulating between', RATES, ENDS, 'gens, rates', gens, rates)
            pops = simulate(num_gens=gens, num_rates=rates, rate_min=RATES[0], rate_max=RATES[1],
                            num_discard = 1000, initial_pop=0.5)
            print('>>> DONE', round(time()-start,2),'s')
        else:
            pops = np.zeros((1,2))

    else:
        pops = None
        pops = np.zeros((1, 2))

    """ ---- CREATE PLOT ---- """

    color = vispy.color.ColorArray("blue")
    color.alpha = 0.8
    size = 1

    if first:

        line = target[0,0].plot(pops, symbol='o', width=0, edge_width = 0, face_color=color,
                                edge_color=color, marker_size=size)
        line.set_gl_state(depth_test=False)

        if 'labels' in project_name:
            rulers = feigen_lines(target[0,0], line.parent)

            return line, rulers
        else:
            return line

    else:

        if pops is not None:
            target.set_data(pops, symbol='o', width=0, edge_width = 0,
                                      face_color=color, edge_color=color,
                                      marker_size=size)
            target.update()


def linear_interp(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def smooth(f, start, end):
    f = 0.5*(np.cos(np.pi*(f-1)) + 1) # assumes x between 0-1
    return linear_interp(f, 0,1, start, end)


keyframes = np.array([
    [
                -0.1,
                4.0,
                -.1,
                4/1.1,
    ],
    [
                3.56908,
                3.57056,
                .89206,
                4/1.1,
    ]
])


class Figure(vp.Fig):
    def __init__(self, *args, **kwargs):

        if 'record' in kwargs:
            self.rec = kwargs['record']
            del kwargs['record']
        else:
            self.rec = False

        super(Figure, self).__init__(*args, **kwargs)
        self.unfreeze()

        self.rec_fps = 24

        if self.rec:
            timer_spf = 'auto'
        else:
            timer_spf = 1 / self.rec_fps

        self.t = app.Timer(timer_spf, connect=self.on_timer, start=True)
        self.c_frames = 30 * self.rec_fps # frames per chapter
        self.f_max = self.c_frames * (len(keyframes)-1)
        self.f = 0
        self.on_timer(1)

    def on_key_press(self, event):
        if event.text ==' ':
            self.t.stop() if self.t.running else self.t.start()

        elif event.text == ',':
            self.f -= 2
            self.on_timer(1)

        elif event.text == '.':
            self.on_timer(1)

    def on_draw(self, event):

        # re-alpha the rulers based on zoom level
        rect = self.camera.rect
        rates = [rect.left, rect.right]

        for r, ruler in enumerate(self.rulers):

            b = ruler['lims']
            d = b[1] - b[0]
            a = abs(d) / abs(rates[1] - rates[0])
            a = min(a, 1)
            a = max(a, 0)

            if r < 5:
                peakx = 0.75
            elif r == 5:
                peakx = 0.1
            elif r == 6:
                peakx = 0.01

            a = np.interp(a, [0, peakx, 1], [0,1,1])

            if ruler['label'] != None:
                c = ruler['label'].color
                c.alpha = a
                ruler['label'].color = c

            c = ruler['ptr'].color
            c.alpha = a
            ruler['ptr'].color = c

            c = ruler['plt']._line._color
            c.alpha = a
            ruler['plt']._line._color = c

        super(Figure, self).on_draw(event)

    def on_timer(self, event):

        start = time()

        if not hasattr(self, 'plotted'):
            zoom_plot_ret = zoom_plot(self, [0,4], [0,1], first=True)
            if type(zoom_plot_ret) is tuple:
                self.plotted, self.rulers = zoom_plot_ret
            else:
                self.plotted = zoom_plot_ret
                self.rulers = []
            self.camera = self._plot_widgets[0].view.camera

        else:

            C = len(keyframes)
            c = self.f // self.c_frames
            z = (self.f/self.c_frames) % 1

            if c >= C-1:
                if self.rec:
                    self.close()
                self.done()

            else:
                LRBA = smooth(z, keyframes[c], keyframes[c+1])

                left = LRBA[0]
                bottom = LRBA[2]
                width = LRBA[1] - LRBA[0]
                height = width * 1/LRBA[3]

                rect = (left, bottom, width, height)

                self.camera.rect = tuple(rect)

            rect = self.camera.rect
            rates = [rect.left, rect.right]
            ends = [rect.bottom, rect.top]

            zoom_plot(self.plotted, rates, ends)

            if self.rec:
                rec_prefix = self.rec['pre']
                project_name = self.rec['name']

                image = self.render()
                io.write_png(f'{rec_prefix}/{project_name}/{project_name}_{self.f}.png', image)

                ETA = (time() - start) * (self.f_max-self.f)
                ETA = (ETA / 60) / 60 # seconds to hours
                ETA = np.modf(ETA)
                ETA = int(ETA[1]), int(round(ETA[0]*60))
                ETA = str(ETA[0]) + ":" + str(ETA[1]).zfill(2)

                print(f'>>> FRAME: {project_name}_{self.f}.png, ETA',
                        ETA,',', round(100*self.f/self.f_max,2),'% :', self.f, '/', self.f_max)


            self.f += 1

    def done(self):

        if self.rec:

            rec_prefix = self.rec['pre']
            project_name = self.rec['name']

            convert_cmd = (f"""ffmpeg -f image2 -framerate {self.rec_fps}"""
                               f""" -i {rec_prefix}/{project_name}/{project_name}_%d.png"""
                               f""" -c:v prores_ks -profile:v 3 {project_name}.mov""")

            print('CONVERTING >>>', convert_cmd)

            os.system(convert_cmd)

            dir = (f"./{rec_prefix}/{project_name}")
            filelist = [f for f in os.listdir(dir) if f.endswith(".png") ]
            for f in filelist:
                os.remove(os.path.join(dir, f))

            print("Logistic zoom is completed")
            exit()


if record_project:
    rec_dict = {'pre':rec_prefix, 'name':project_name}
else:
    rec_dict = None

fig = Figure(show=False, title="Logistic Map", size=(2538, 1080),
                record=rec_dict)

if __name__ == '__main__':
    fig.show(run=True)