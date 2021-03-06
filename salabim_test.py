import salabim as sim
import math
import random
import string
import time
import logging
import inspect

import platform
Pythonista=(platform.system()=='Darwin')


def test():
    test87()
    
def test87():
    def dump_an_objects():
        print('dump')
        for ao in env.an_objects:
            print(ao.type, ao.text(env.t) if ao.type=='text' else '')
            
    class X(sim.Component):
        def process(self):
            start = env.t
            an = sim.AnimateText('Hello', x=lambda t: (t - start) *100 , y=100)
            dump_an_objects()
            yield self.hold(5)
            an.remove()
            dump_an_objects()
            yield self.hold(6)

    env = sim.Environment(trace=False)
    env.animate(True)
    sim.AnimateText('abc', x=100,y=200)
    X()

    env.run(6)
    

def test86():

    class X(sim.Component):
        def setup(self, i):
            self.i = i

        def process(self):
            for i in range(2):
                yield self.hold(sim.Uniform(0,2)())
                self.enter(q)
                yield self.hold(sim.Uniform(0,2)())
                self.leave(q)

    env = sim.Environment(trace=False)
    q = sim.Queue('wachtrij' )
    qa0 = sim.AnimateQueue(q, x=500, y=300, direction='n')
    [X(i=i) for i in range(15)]
    env.animate(True)

    env.run()
    
def test85():
    env = sim.Environment(trace=True)
    q=sim.Queue(name='queue')
    with open('test.txt', 'w') as f:
        q.print_statistics(file=f)
    env.run()


def test84():
    def action():
        print(en.get())
        en.remove()
        
    class carAnimateCircle1(sim.Animate):

        def __init__(self, car):
            self.car = car
            sim.Animate.__init__(self,
                circle0=(car.R,), linecolor0='magenta', fillcolor0='white', linewidth0=1)

        def circle(self, t):
            if self.car.mode() == 'Driving':
                return (self.car.R,)
            else:
                return (0.1,)

        def fillcolor(self, t):
            if self.car.mode() == 'Driving':
                return ('yellow', 75)
            else:
                return ('white', 75) #'white'

    class carAnimateCircle(sim.Animate):

        def __init__(self, car):
            self.car = car
            sim.Animate.__init__(self,
                circle0=(car.R,), linecolor0='magenta', fillcolor0='white', linewidth0=1)

        def circle(self, t):
            if self.car.mode() == 'Driving':
                return (self.car.R,)
            else:
                return (0.1,)

        def fillcolor(self, t):
            if self.car.mode() == 'Driving':
                return ('yellow', 75)
            else:
                return ('white', 75) #'white'

    class Car(sim.Component):
        def setup(self, R):
            self.R = R
            sim.AnimateCircle(
                 linecolor='magenta',
                 radius=lambda car, t: self.R if car.mode() == 'Driving' else 0.1,
                 fillcolor=lambda car, t: ('yellow', 75) if car.mode() == 'Driving' else ('white', 75),
                 arg=self
                 )


        def process(self):
            while True:
                yield self.hold(1, mode='Driving')
                yield self.hold(1, mode='Stand still')
                

    env=sim.Environment()
    Car(R=100)
    env.animate(True)
    env.x0(-200)
    env.x1(200)
    env.y0(-150)
    sim.AnimateLine((0,0,100-3,100-3), screen_coordinates=True)


    en=sim.AnimateEntry(x=100, y=100, action=action)

    env.run()


    
def test83():
    l1 = []

    test_input = '''
    1   \t\t  {2 3 67} 4  12000
    4 5 6
    7
    '''
    with sim.ItemFile(test_input) as f:
        while True:
            try:
                print(f.read_item_int())
            except EOFError:
                break




def test82():
    env = sim.Environment()
    env.width(200)
    y = sim.AnimateCircle(radius=100, x=900, y=600, linewidth=1 / env.scale(), fillcolor=('red',100), linecolor='black', draw_arc=True)
#    x = sim.Animate(circle0=(100,100, 0, 60, False), x0=900, y0=600, linewidth0=3, fillcolor0='red', linecolor0='black')
    a = sim.Animate(circle0=(100,100, 0, 0, True), circle1=(100,None,0, 720, True), x0=200, y0=200, linewidth0=3, fillcolor0='blue', fillcolor1='green', t1=10)
    b = sim.Animate(rectangle0=(-100, -10, 100, 10), x0=300, y0=600, angle1=360, t1=10)
    b = sim.Animate(rectangle0=sim.centered_rectangle(10,10), x0=200, y0=200, fillcolor0='red')
#    b = sim.Animate(rectangle0=(-100,-10, 100, 10), x0=300, y0=600)
    sim.AnimateCircle(radius=100, radius1=300, x=lambda t: 700-t*10, y=200, fillcolor=lambda t: env.colorinterpolate(t,0,10,'yellow','blue'), arc_angle0=0, arc_angle1=lambda t: t * 10, draw_arc=True, linewidth=1, linecolor='red',
                      text='Piet', angle=lambda t: t * 10, textcolor='black', text_anchor='e')

    env.animate(True)
    env.run()

def test81():
    def mtally(x, n):
        for i in range(n):
            m.tally(x)
        mw.tally(x,n)

    class X(sim.Component):
        def process(self):
            mt.tally('abc')
            for i in range(10):
                yield self.hold(1)
                mt.tally(i)
            env.main().activate()

    sim.reset()
    env=sim.Environment()
    X()
    mt=sim.MonitorTimestamp(name='mt')
    mw = sim.Monitor(name='mw', weighted=True, weight_legend='de tijd')
    m = sim.Monitor(name='m')

    mtally(3,1)
    mtally(5,2)
    mtally(6,2)
    mtally('test',2)
    m.tally(3,1)

    print(m.mean())
    print(m.std())
    print(mw.mean())
    print(mw.std())
    env.run()
    m.monitor(False)
    mt.monitor(False)
    print(mt.mean(), mt.std())
    for values in (True, False):
        m.print_histogram(values=values)
        mw.print_histogram(values=values)
        mt.print_histogram(values=values)
    print(m.weight(ex0=True))
    print(mw.weight(ex0=True))
    print(mt.duration(ex0=True))
    print(mt.xt(exoff=True))

def test80():
    env=sim.Environment(trace=False)
    class X(sim.Component):
        def process(self):
            yield self.hold(1)
            env.snapshot('manual/source/Pic1.png')
    env.animate(True)
    env.background_color('20%gray')

    sim.AnimatePolygon(spec=(100, 100, 300, 100, 200,190), text='This is\na polygon')
    sim.AnimateLine(spec=(100, 200, 300, 300), text='This is a line')
    sim.AnimateRectangle(spec=(100, 10, 300, 30), text='This is a rectangle')
    sim.AnimateCircle(radius=60, x=100, y=400,text='This is a cicle')
    sim.AnimateCircle(radius=60, radius1=30, x=300, y=400,text='This is an ellipse')
    sim.AnimatePoints(spec=(100,500, 150, 550, 180, 570, 250, 500, 300, 500), text='These are points')
    sim.AnimateText(text='This is a one-line text', x=100, y=600)
    sim.AnimateText(text='''\
Multi line text
-----------------
Lorem ipsum dolor sit amet, consectetur
adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud
exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute
irure dolor in reprehenderit in voluptate
velit esse cillum dolore eu fugiat nulla
pariatur.

Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia
deserunt mollit anim id est laborum.
''', x=500, y=100)

    sim.AnimateImage('Pas un pipe.jpg', x=500, y=400)
    X()
    env.run(100)

def test79():
    env = sim.Environment(trace=True)
    class X(sim.Component):
        def process(self):
            yield self.hold(3)
            yield self.hold(5)


    env.reset_now(-1000)
    X(at=-500)
    env.run()

def test78():

    class X(sim.Component):

        def process(self):
            while True:
                yield self.hold(sim.Uniform(0,2)())
                self.enter(q)
                yield self.hold(sim.Uniform(0,2)())
                self.leave(q)

    env = sim.Environment(trace=False)
    for _ in range(15):
        x=X()
    q = sim.Queue('q')
    r=sim.Resource()
    s=sim.State()
    env.run(500)
    as_str=False
    f= open('test.txt', 'w')
    d=sim.Normal(4)
    d1=sim.Distribution('Normal(4)')
    q.print_histograms(as_str=as_str, file=f)
    q.print_statistics(as_str=as_str, file=f)
    q.print_info(as_str=as_str, file=f)
    env.print_info(as_str=as_str, file=f)
    x.print_info(as_str=as_str, file=f)
    s.print_info(as_str=as_str, file=f)
    r.print_info(as_str=as_str, file=f)
    d.print_info(as_str=as_str, file=f)
    d1.print_info(as_str=as_str,file=f)
    f.close()

def test77():

    def y(self,t):
        if self == qa0:
            return 50
        if self == qa1:
            return 100
        if self == qa2:
            return 150
        return 600

    class X(sim.Component):
        def setup(self, i):
            self.i = i

        def animation_objects1(self,id ):
            if id =='text':
                ao0 = sim.AnimateText(text=self.name(), textcolor='black')
                return 0, 20, ao0
            ao0 = sim.AnimateRectangle(spec=lambda c,t: (0,0,40 + 10 * t if c.index(q) <= 2 else 40,20), text=self.name(), fillcolor=id, textcolor='white', arg=self)
            return lambda c, t: 45 + 10 * t if c.index(q) <= 2 else 45, 0, ao0

        def process(self):
            while True:
                yield self.hold(sim.Uniform(0,2)())
                self.enter(q)
                yield self.hold(sim.Uniform(0,2)())
                self.leave(q)

    env = sim.Environment(trace=False)
    q = sim.Queue('q')
    qa0 = sim.AnimateQueue(q, x=lambda t: 100+t*10, y=y, direction='e', reverse=False, id='blue')
    qa1 = sim.AnimateQueue(q, x=100, y=y, direction='e', reverse=False, max_length=6, id='red')
    qa2 = sim.AnimateQueue(q, x=100, y=y, direction='e', reverse=True, max_length=6, id='green')
    qa3 = sim.AnimateQueue(q, x=100, y=200, direction='n', id='text', title='A very long title')
    [X(i=i) for i in range(15)]
    env.animate(True)
    env.run(5)
    qa1.remove()
    env.run(5)

def test76():
    class X(sim.Component):
        def process(self):
            for i in range(100):
                yield self.hold(0.3)
                testline = ['Line'+ str(i) for i in range(i)]
                testanim.line = testline

    env = sim.Environment()
    env.modelname('test many')
    env.background_color('10%gray')
#    an = sim.Rectangle(spec=(0,0,400,200),x=100, y=100, text='ABCabcopqxyz\nABCabcopqxyz              \nABCabcopqxyz\n', text_anchor='sw', font='narrow', fontsize=40, textcolor='blue')
#    an = sim.Rectangle(spec=(0,0,400,200),x=100, y=400, text='ABCabcopqxyz\nABCabcopqxyz           \nABCabcopqxyz\n', text_anchor='nw', font='narrow', fontsize=40, textcolor='blue')

#    an = sim.Text(x=600, y=100, text='ABCabcopqxyz', anchor='sw', font='', fontsize=40, textcolor='blue')
#    an = sim.Text(x=600, y=100, text='ABCabcopqxyz', anchor='nw', font='', fontsize=40, textcolor='blue')
#    an = sim.Text(x=600, y=100, text='ABCabcopqxyz', anchor='e', font='', fontsize=40, textcolor='blue')

    for dir in ('nw', 'w','sw','s','se','e','ne','n','c'):
        an = sim.AnimateRectangle(spec=(-250,-250,250,250), x=300,y =300,fillcolor='', linewidth=1, linecolor='white',text='A1y'+dir, text_anchor=dir, textcolor='white', angle=lambda t:t*5)

    x= 600
    for c in 'ABCabcopqxyz':
        sim.AnimateText(text=c, y=100, x=x, textcolor='white',text_anchor='s')
        x += 10

    an = sim.AnimateLine(spec=(0,0,1000,0), x=500, y=100, linecolor='red')
    an = sim.AnimateCircle(radius=100, fillcolor=('red',100), text='Hallo', textcolor='yellow', angle =45, x=500, y=500)

    an=sim.AnimateText(text=('cc\n\nx','abc','def','','ghi'), x=300, y=300, textcolor='white', text_anchor='c')

    testanim=sim.AnimateText(text=('Line1', 'Line2', 'Line3', 'Line4'), x=600, y=10, text_anchor='sw', max_lines=0)

    X()

    env.animate(True)
    env.run()


def test75():
    class MyText(sim.Text):
        def __init__(self, my='Abc', *args, **kwargs):
            sim.Text.__init__(self, text=None, *args, **kwargs)
            self.my=my

        def text(self,t):
            return self.my + str(env.now())

        def anchor(self, t):
            if t > 50:
                return 'w'
            else:
                return 'e'

    def xx(self,t):
        return self.sequence_number() * 75 + 600 + t

    class Comp(sim.Component):
        def setup(self):
            i = self.sequence_number()
            sim.Rectangle(spec=sim.centered_rectangle(50, 50), y=100 + i * 75,
                fillcolor='orange', x=xx, arg=self)

        def x(self, t):
            return self.sequence_number() * 75 + 600 + t

        def process(self):
            yield self.cancel()

    class CompGenerator(sim.Component):
        def process(self):
            while True:
                yield self.hold(sim.Uniform(20,20)())
                c=Comp()

    env = sim.Environment()
    env.modelname('test')
    env.background_color('10%gray')
    env.speed(16)
    CompGenerator()
    for s in ('a', 'b', 'p', 'A','A1yp'):
        print(s, env.getwidth(s, font='', fontsize=20), env.getheight(font='', fontsize=20))

    for text_anchor in ('s','sw','w','nw','n','ne','e','se','c'):
        sim.Text(x=200,y=200,text=text_anchor, text_anchor=text_anchor)

    anpanel = sim.Rectangle(spec=(0,0,400,200),x=lambda:50, y=500, text='This is a test with\ntwo lines\nline three ', text_anchor='sw', font='narrow', fontsize=40, textcolor='blue')
    anpanel1 = MyText(x=50, y=20, my='MY')
    anpanel2 = sim.Rectangle(x=0, y=200, text='abcde',
        spec=(0,0,500,100), angle=20, xy_anchor='n')
    sim.Circle(x=400,y=100,radius=100, text='Circle', fontsize=30, angle=45, xy_anchor='w')
    sim.Line(spec=(200,750,210,700,220,730,240,730,250,700,1000,0))
    sim.Points(spec=(200,750,210,700,220,730,240,730,250,700,1000,0))
    sim.Image(spec='Cogwheel.png', x=500, y=500, anchor='c', width=lambda t:t, text='cogwheel', angle=lambda t:t)
    angle = 0
    an = sim.Rectangle(spec=(-150, -25, 150, 25), x=300, y= 125, fillcolor='red', angle=lambda t: t * 360/200,
        text='test', textcolor='white', text_anchor='e')
    sim.Line(spec=(0,0,900,0), x=100, y=700, offsetx=0, offsety=0, text='hallo', text_anchor='nw', textcolor='white', text_offsetx=0, text_offsety=0, angle=lambda t: sim.interpolate(t, 0, 200, 0, 360))


    env.animate(True)
    env.run(100)

    env.run()

def test74():
    class Comp(sim.Component):
        def process(self):
            a.tally(env.now())
            self.enter(stage1)
            yield self.hold(sim.Uniform(10,20)())

            self.leave()
            b.tally(env.now())
            self.enter(stage2)
            yield self.hold(sim.Uniform(20,30)())
            self.leave()

    class CompGenerator(sim.Component):
        def process(self):
            while True:
                yield self.hold(sim.Uniform(2,6)())
                c=Comp()

    env = sim.Environment()
    env.modelname('test')
    env.background_color('10%gray')
    stage1=sim.Queue('stage1')
    stage2=sim.Queue('stage2')
    sim.aMonitor(monitor=stage2.length, x=100, y=100,as_points=True,as_level=True,linewidth=1, vertical_scale=5, fillcolor=('blue',100))
    s2 = sim.aMonitor(monitor=stage2.length, x=300, y=100, linewidth=2, horizontal_scale=2)
    s1 = sim.aMonitor(monitor=stage1.length_of_stay, x=100, y=400, as_points=False, height=200)
    sim.aMonitor(stage2.length_of_stay, x=300, y=400, height=200)
    a = sim.Monitor(name='a')
    b = sim.Monitor(name='')
    a1=sim.aMonitor(a, x=500, y=100, vertical_scale=1, horizontal_scale=10, height=200, as_points=True)
    sim.aMonitor(b, x=500, y=100, vertical_scale=1, linecolor='blue', height=200, as_points=True)

    CompGenerator()
    env.animate(True)
    env.speed(16)

    env.run(100)
#    s2.remove()
#    s1.remove()
    env.run()

def test73():
    class X(sim.Component):

        def process(self):
            while True:
                yield self.hold(1)
                mon.tally(sim.Uniform(-5,50)())


    env=sim.Environment(trace=False)
    X()
    mon=sim.Monitor('monitor')
    a=mon.animate(x=500, y=300, key_scale=10, point_size=4)
    env.animate(True)
    env.run(5)
    a.remove()
    env.run()

def test72():
    env=sim.Environment()
    p = sim.CumPdf((0, 0.5, 1,0.5))
    p.print_info()
    print(p.mean())
    r = sim.Resource(name='resource')
    s = sim.State(name='state')
    q=sim.Queue('rij')
    r.name('bron')
    s.name('staat')
    as_str=False
    print('---')
    r.print_histograms(as_str=as_str)
    s.print_histograms(as_str=as_str)
    q.print_histograms(as_str=as_str)
    r.print_statistics(as_str=as_str)
    s.print_statistics(as_str=as_str)
    q.print_statistics(as_str=as_str)
    print('---')


def test71():
    env = sim.Environment()
    env.animate(True)
    p = (100,100, 300, 100, 300, 500)
    r=(400,400, 600,600)
    po =(800, 400, 1000, 400,1000,650)
    sim.Animate(line0=p, linecolor0='red', linewidth0=1)
    sim.Animate(line0=p, linecolor0='red', linewidth0=1, linewidth1=10, as_points=True, t1=10)
    sim.Animate(rectangle0=r, linecolor0='green', linewidth0=1, as_points=False, fillcolor0='', t1=10)
    sim.Animate(rectangle0=r, linecolor0='blue', linewidth0=10, linewidth1=10, as_points=True, t1=10)
    sim.Animate(polygon0=po, linecolor0='orange', as_points=False, t1=10)
    sim.Animate(polygon0=po, linecolor0='pink', linewidth1=10, as_points=True, t1=10)
    sim.Animate(rectangle0=(500,500,600,600))
    sim.Animate(circle0=100, x0=800,y0=300)
    env.run()

def test70():
    class X(sim.Component):
        def setup(self,start,durations,xs):
            self.start=start
            self.xs=xs
            self.durations = durations
            self.monitor = sim.MonitorTimestamp(name=self.name()+'.monitor',type='any', monitor=False)

        def process(self):
            yield self.hold(self.start)
            self.monitor.monitor(True)
            for x, duration in zip(self.xs, self.durations):
                self.monitor.tally(x)
                yield self.hold(duration)
            self.monitor.monitor(False)

    env=sim.Environment()
    x0= X(start=0, xs=(1,3,'a','7'), durations=(1,1,1,1))
    x1= X(start=0, xs=('a',2,5), durations=(3,3,8))
    env.run(20)
    x0.monitor.print_histograms()
    x1.monitor.print_histograms()
    m = sim.MonitorTimestamp(name='combined', merge=(x0.monitor,x1.monitor))
    m.print_histogram()

    a1=sim.Monitor(name='a1', type='int8')
    a1.tally(1)
    a1.tally(2)
    a1.tally(2)
    a1.tally(0)
    a2=sim.Monitor(name='a2', type='int8')
    a2.tally(1)
    a2.tally(20)
    a2.tally(18)
    a2.tally(0)
    a2.tally(2)
    a1.print_histogram()
    a2.print_histogram()
    a = sim.Monitor(name='combined', merge=(a1,a2), type='int8')
    a.print_histogram()




def test69():
    class X(sim.Component):
        pass

    sim.reset()
    env = sim.Environment()
    q=sim.Queue('q')
#    X().enter_sorted(q, (1,1))
#    X().enter_sorted(q, (0,2))
#    X().enter_sorted(q, (1,0))
#    X().enter_sorted(q, (1,3))
#    q.print_info()

    q=sim.Queue('q')
    X().enter_sorted(q, 'one')
    X().enter_sorted(q, 'two')
    X().enter_sorted(q, 'three')
    X().enter_sorted(q, 'four')
    q.print_info()

def test68():
    class X(sim.Component):

        def process(self):
            self.enter(q1).enter(q2)
            self.enter(q3)
            yield self.request(r)
            self.leave().enter(q2)
            self.leave(q2).leave().leave().enter(q1)

    env=sim.Environment(trace=True)
    q1=sim.Queue('q1')
    q2=sim.Queue('q2')
    q3=sim.Queue('q3')
    components = []
    somecomponents =[]
    x= [X().register(components).register(somecomponents) for _ in range(5)]

    r = sim.Resource().register(components)
    env.run()

    x[3].deregister(components)

    for c in components:
        print(c.name())
    for c in somecomponents:
        print(c.name())

def test67():
    env = sim.Environment()
    m = sim.Monitor('normal distribution')
    m.name('test')
    for i in range(100000):
        m.tally(sim.Normal(10,2)())
    m.print_histogram()

def test66():
    class Poly(sim.Animate):
        def __init__(self, radius, number_of_sides,*args, **kwargs):
            self.radius = radius
            self.number_of_sides = number_of_sides
            sim.Animate.__init__(self, polygon0=(), *args, **kwargs)

        def polygon(self,t):
            return sim.regular_polygon(radius=self.radius, number_of_sides=self.number_of_sides, initial_angle = t*1)

    env = sim.Environment()
    env.animate(True)
    for i in range(3,10):
#        sim.Animate(polygon0=sim.regular_polygon(radius=60, number_of_sides=i, initial_angle=90), x0=50+(i-3)*150, y0=300
        Poly(radius=60, number_of_sides=i, x0=50+(i-3)*150, y0=300)

    env.run()

def test65():
    class X(sim.Component):
        def process(self):
            while True:
                mt.tally('idle')
                yield self.hold(10)
                for i in range(6):
                    st = sim.Pdf(('produce A', 'produce B', 'produce C', 'produce D', 'transport', 'store'),1)()
                    mt.tally(st)
                    yield self.hold(sim.Uniform(6,6)())

    env = sim.Environment(trace=False)
    mt = sim.MonitorTimestamp('Status')

    X()
    env.run(300)
    mt.print_histogram(values=True)


def test64():
    class X(sim.Component):
        def process(self):
            for i in list(range(70)):
                mt.tally(i)
                yield self.hold(2)
            env.main().activate()

    env = sim.Environment(trace=False)
    m = sim.Monitor('m')
    mt = sim.MonitorTimestamp('mt')

    X()
    env.run()
    m.print_histograms()
    for i in (0,1,1,2,3,1,1,1,10,20,300):
        m.tally(i)
    m.print_histograms()
    mt.print_histograms(ex0=True)

def test63():
    class X(sim.Component):
        def process(self):
            for i in (1,2,3,1,1,1,'1','jan','a',1,2,'2'):
                mt.tally(i)
                try:
                    x = int(i)
                except:
                    x = 1.5
                yield self.hold(2.1 * x)
            env.main().activate()

    env = sim.Environment(trace=True)
    m = sim.Monitor('m')
    mt = sim.MonitorTimestamp('mt')

    X()
    env.run()
    m.print_histogram(values=True)
    for i in (1,2,3,1,1,1,1.1,1.2,'1.2',0,'',' ',' 1000 ',1000,600,6.8,5,'2','1','jan','piet','x','y','b','a',1,2,'2'):
        m.tally(i)
    m.print_histogram(values=True, ex0=False)
    mt.print_histogram(values=True)
    print(mt.xduration())

    mt.print_histogram()

def test62():
    class X1(sim.Component):
        def process(self):
            yield self.hold(100)

    class X2(sim.Component):
        def process(self):
            yield self.request(res, fail_at=100)
            yield self.hold(50)

    class X3(sim.Component):
        def process(self):
            yield self.passivate()

    class X4(sim.Component):
        def process(self):
            while True:
                yield self.standby()

    class X5(sim.Component):
        def process(self):
            yield self.wait(st, fail_at=100)
            yield self.hold(50)

    class Z(sim.Component):
        def process(self):
            for i in range(20):
                yield self.hold(1)

    class Y(sim.Component):
        def process(self):
            yield self.hold(4)
            x1.remaining_duration(100)
            yield self.hold(1)
            x1.interrupt()
            x2.interrupt()
            x2.interrupt()
            x3.interrupt()
            x4.interrupt()
            x5.interrupt()
            yield self.hold(2)
            res.set_capacity(0)
            st.set()
            yield self.hold(3)
            x1.resume()
            x2.resume()
            x3.resume()
            x4.resume()
            x5.resume()
            x2.resume()

    env = sim.Environment(trace=True)
    env.suppress_trace_standby(False)
    x1 = X1()
    x1.name('abc')
    x2 = X2()
    x3 = X3()
    x4 = X4()
    x5 = X5()

    y = Y()
    z = Z()
    res = sim.Resource('res', capacity=0)
    st = sim.State('st')

    env.run(urgent=True)

def test61():
    class X(sim.Component):
        def process(self):
            yield self.request(r)
            yield self.hold(1)

    class Y(sim.Component):
        def process(self):
            yield self.request(r)
            yield self.hold(1)
#            self.cancel()
            a=1

    env = sim.Environment(trace=True)
    r = sim.Resource('r', capacity=2)
    X()
    Y()
    env.run()
    print(r.claimed_quantity())

def test60():
    class X(sim.Component):
        def process(self):
            yield self.request(r)
            yield self.hold(sim.Uniform(0,2)())

    env = sim.Environment()
    r = sim.Resource(name='r',capacity=1)
    for i in range(5):
        X()
    env.trace(True)
    env.run(10)
    occupancy = r.claimed_quantity.mean() / r.capacity.mean()
    r.print_statistics()
    env.run(urgent=True)


def test59():
    def do_next():
        global ans
        global min_n

        for an in ans:
            an.remove()
        ans = []

        x=10
        y=env.height() - 80
        sx= 230
        sy=14
        y -= 30
        fontnames = []
        n=0

        for fns, ifilename in sim.fonts():
            for fn in fns:
                fontnames.append(fn)
        fontnames.extend(sim.standardfonts().keys())
        last = ''
        any = False
        for font in sorted(fontnames, key=sim.normalize):
            if font != last:  # remove duplicates
                last = font
                n += 1
                if n >= min_n:
                    any = True
                    ans.append(sim.Animate(text=font, x0=x, y0=y, anchor='sw', fontsize0=15, font=font))
                    x += sx + 5
                    if x + sx > 1024:
                        y -= sy + 4
                        x = 10
                        if y<0:
                            break
        min_n = n + 1
        if not any:
            env.quit()

    global ans
    global min_n

    env = sim.Environment()
    sim.AnimateButton(x=500,y=-21, width=50, xy_anchor='nw', text='Next', fillcolor='red', action=do_next)
    ans = []
    min_n = 0
#    sim.Animate(text='Salabim fontnames', x0=x, y0=y, fontsize0=20, anchor='sw', textcolor0='white')

    do_next()
    env.background_color('20%gray')

    env.animate(True)
    env.run()

def test58():
    env = sim.Environment()
    names = sorted(sim.colornames().keys())
    x=10
    y=env.height() - 80
    sx= 155
    sy=23
    sim.Animate(text='Salabim colornames', x0=x, y0=y, fontsize0=20, anchor='sw', textcolor0='white')
    y -= 30
    for name in names:
        if env.is_dark(name):
            textcolor = 'white'
        else:
            textcolor = 'black'
        sim.Animate(rectangle0=(x, y, x + sx, y + sy), fillcolor0=name)
        sim.Animate(text='<null string>' if name =='' else name, x0=x + sx / 2, y0=y + sy /2, anchor='c', textcolor0=textcolor, fontsize0=15)
        x += sx + 5
        if x + sx > 1024:
            y -= sy + 4
            x = 10

    env.background_color('20%gray')
    env.animate(True)
    env.run()

def test57():
    class X(sim.Component):
        def process(self):
            while env.now()<run_length:
                an.update(text=str(run_length - env.now()))
                yield self.hold(1)
            env.animation_parameters(animate=False)
            print(self.env._animate)
#            yield self.hold(0)
            env.video('')
            env.main().activate()

    env = sim.Environment()
    env.animation_parameters(background_color='blue', modelname='test')
    env.video('test.gif')
    env.video_pingpong(False)
    env.video_repeat(2)

#    env.animation_parameters(video='test.avi+MP4V', speed=0.5)
    an = sim.Animate(text='', x0=100,y0=100, fontsize0=100)
    run_length = 1

    X()
    sim.Animate(line0=(0,50,None,None), line1=(0,50,1024,None), linewidth0=4,t1=run_length)
    sim.Animate(circle0=(40,), x0=200, y0=200)
    sim.Animate(circle0=40, x0=300, y0=200)
    env.run()
    print('done')
    env.quit()

def test56():
    env = sim.Environment()
    mon = sim.Monitor('number per second')
    for i in range(100):
        sample = sim.Normal(0.083,0.00166)()
        mon.tally(sample)

    mon = sim.Monitor('number per second')
    env.run(100)
    mon.print_histogram()


def test55():
    class X(sim.Component):
        def process(self):
            while True:
                yield self.hold(sim.Exponential(rate=0.83)())
                env.count += 1

    class Y(sim.Component):
        def process(self):
            while True:
                env.count=0
                yield self.hold(1)
                print(env.count)
                mon.tally(env.count)

    env = sim.Environment()
    env.count = 0
    X()
    Y()
    mon = sim.Monitor('number per second')
    env.run(100)
    mon.print_histogram()

def test54():
    import test_a
    import test_b
    env = sim.Environment(trace=True)
    test_a.X()
    test_b.X()


    env.run(10)

def test53():
    en =sim.Environment()
    d=sim.Normal(10, 3)
    d.print_info()
    d=sim.Normal(10, coefficient_of_variation=0.3)
    d.print_info()
    d=sim.Normal(0, standard_deviation=3)
    d.print_info()
    d=sim.Normal(0, coefficient_of_variation=4)
    d.print_info()

def test52():
    class X(sim.Component):
        def process(self):
#            env.animation_parameters(animate=False)
            while env.now()<=6:
                an.update(text=str(env.now()), x0=env.now()*10)
                yield self.hold(1)
            env.animate(True)
            while env.now()<=12:
                an.update(text=str(env.now()),x0=env.now()*10)
                yield self.hold(1)
            env.animation_parameters(animate=False)
            while env.now()<=20:
                an.update(text=str(env.now()),x0=env.now()*10)
                yield self.hold(1)
            env.animation_parameters(animate=True, modelname='something else', background_color='90%gray',x0=-100, width =500, height=500)
            env.x0(-100)
            while env.now()<=25:
                an.update(text=str(env.now()),x0=env.now()*10, textcolor0='red')
                yield self.hold(1)

    def printt(str2prn):
        return '['+str(env.now())+']',str2prn
    sim.reset()
    logging.basicConfig(filename='sim.log', filemode='w', level=logging.DEBUG)
    print('***can_animate',sim.can_animate(try_only=True))

    try:
        print('***can_animate',sim.can_animate(try_only=False))
    except:
        print('failed')
    print('***can_video',sim.can_video())
    print('passed.')
    env=sim.Environment(trace=True)
    logging.debug(printt('piet'))
    env.animation_parameters(animate=True, modelname='test52', video='')
    s = sim.AnimateSlider(x=300,y=-50,xy_anchor='nw')
    a=sim.Animate(line0=(0,-50,300,-50), xy_anchor='nw',screen_coordinates=True)
#    env.animate(True)

    X()
    an = sim.Animate(text='Test',x0=100, y0 =100)
    r = sim.Animate(rectangle0=(100,100,200,200),x0=0,y0=10)
    r = sim.Animate(circle0=(1.11,),x0=0,y0=10,fillcolor0='red')
    l = sim.Animate(polygon0=(10,10,20,20,10,20), fillcolor0='bg',linecolor0='fg',linewidth0=0.1)
    b = sim.AnimateButton(text='My button', x=-100, y=-20, xy_anchor='ne')
    env.run(10)
    env.run(20)
    env.quit()

def test51():
    env = sim.Environment()
    d = sim.Poisson(2)
    x = []
    m = sim.Monitor(name='samples')
    for i in range(10000):
        m.tally(d())
    m.print_histogram(15, 0, 1)

def test50():
    env=sim.Environment()
    for i, c in enumerate(string.printable):
        if i <= 94:
            print(i,c)
            sim.Animate(text=c,x0=10+i*10,y0=100,anchor='w')
    sim.Animate(line0=(0, 100, 1024, 100), linecolor0='red')

    env.animation_parameters(modelname='Test')
    env.animating = True
    env.trace(True)
    env.run(5)
    print (env.main()._scheduled_time)


def test49():
    l1 = []

    test_input = '''
    one two
    three four
    five
    '''
    with sim.ItemFile(test_input) as f:
        while True:
            try:
                print(f.read_item())
            except EOFError:
                break




    with sim.ItemFile('test.txt') as f:
        while True:
            try:
                l1.append(f.read_item_bool())
            except EOFError:
                break

        print('------------------------')

        f = sim.ItemFile('test.txt')
        l2 = []
        while True:
            try:
                l2.append(f.read_item())
            except EOFError:
                break

    for x1, x2 in zip(l1,l2):
        print(x1, x2)


def test48():

    class A(sim.Component):
        def myhold(self, t):
            print('**')
            yield self.hold(t)

        def process(self):
            while env.now()<5:
                if env.now()>30:
                    env.main().activate()
                print('aa')
                self.myhold(1)
                yield self.hold(1)


    class B(sim.Component):
        def process(self):
            while True:
                yield self.hold(1)
    env = sim.Environment(trace=True)
    env.suppress_trace_standby(True)
    A()
    B()
    env.run(8)
    print('ready')



def test47():
    class Dodo(sim.Component):
        pass

    class Car(sim.Component):
        def setup(self, color='unknown'):
            self.color=color
            print(self.name(),color)

        def process(self, duration):
            yield self.hold(duration)
            yield self.activate(process='process', duration=50)

        def other(self):
            yield self.hold(1)

    env=sim.Environment(trace=True)
    Car(process=None)
    Car(color='red', duration=12, mode='ABC')
    Car(color='blue',process='other')


    Dodo()

    env.run(100)


def test46():
    class Y(sim.Component):
        pass

    class X(sim.Component):
        def process(self):
            x=0

            for i in range(10):
                q.add(Y())
                print ('q.length=', q.length())
                if i==3:
                    monx.monitor(False)
                    monx.tally(x)
                if i==6:
                    monx.monitor(True)
                yield self.hold(1)
                x += 1

    env = sim.Environment()
    env.beep()
    monx = sim.MonitorTimestamp('monx')
    q = sim.Queue('q')
    X()

    env.run(20)
    print(monx.xt())
    print(q.length.xt())



def test45():
    def test(d, lowerbound=-sim.inf, upperbound=sim.inf):
        d.print_info()
        print('mean=', d.mean())
        l=[d(lowerbound, upperbound) for i in range(10000)]
        print('one sample', d())
        print('mean sampled =', sum(l)/(len(l)+1))
        print('-'  * 79)

    env=sim.Environment()
    mon = sim.Monitor()
    d = sim.Cdf((5, 0, 10, 50, 15, 90, 30, 95, 60, 100))
    for _ in range(10000):
        mon.tally(d.bounded_sample(lowerbound=5, upperbound=sim.inf, number_of_retries=300))

    mon.print_histogram(30,-5,1)


def test44():
    import newqueue
    import newerqueue
    import newcomponent

    class X(sim.Component):
        def process(self):
            yield self.hold(10,mode='ok')
            if self == x1:
                yield self.passivate()
            yield self.hold(10,urgent=True)

    class Y(sim.Component):
        def setup(self, a='a'):
            print('a=',a)


        def process(self, text):
            print('-->',text)
            yield self.request((res, 4), fail_at=15)
            x1.activate(mode=5)


    env=sim.Environment(trace=True)
    res = sim.Resource()

    x0=X()
    x1=X(name='')
    x2=X(name=',')
    z=newcomponent.NewComponent()
    q0=sim.Queue()
    q1=newqueue.NewQueue()
    q2=newerqueue.NewerQueue()
    Y(process='process', text='Hello')
    q0.add(x1)
    q1.add(x1)
    q2.add(x1)

    env.run(50)
    env.print_trace_header()

def test43():
    def test(d):
        d.print_info()
        print('mean=', d.mean())
        l=[d() for i in range(10000)]
        print('one sample', d())
        print('mean sampled =', sum(l)/(len(l)+1))
        print('-'  * 79)

    env=sim.Environment()

    test(sim.IntUniform(1,6))
    test(sim.Weibull(2,1))
    test(sim.Gamma(5,9))
    test(sim.Erlang(2,scale=3))
    test(sim.Exponential(rate=2))
    test(sim.Beta(32,300))
    test(sim.Normal(5,7))
    test(sim.Normal(5,7,use_gauss=True))

    test(sim.Distribution('Exponential(rate=2)'))
    test(sim.Normal(5,5))

def test42():
    class Rij(sim.Queue):
        pass

    class Komponent(sim.Component):
        pass

    class Reg(sim.Monitor):
        pass

    env=sim.Environment(trace=True)

    q1=sim.Queue('q1')
    q2=sim.Queue('q2')
    for i in range(15):
        c = sim.Component(name='c.')
        if i < 10:
            q1.add_sorted(c, priority=20-i)
        if i > 5:
            q2.add_sorted(c, priority=i+100)
    env.run(1000)
    del q1[1]
    print('length',q1.length.number_of_entries())
    print('length_of_stay',q1.length_of_stay.number_of_entries())

    q1.print_info()
    q2.print_info()


    (q1 - q2).print_info()
    (q2 - q1).print_info()
    (q1 & q2).print_info()
    (q1 | q2).print_info()
    (q2 | q1).print_info()
    (q1 ^ q2).print_info()
    q3=sim.Queue(name='q3',fill=q1)
    q4=sim.Queue(name='q4',fill=q1)
    print('before')
    q3.print_info()
    del q3[-1:-4:-1]
    print('after')
    q3.print_info()
    q4.pop(3)
    for c in q3:
        print(c.name(),c.count(q2),c.count(),q4.count(c),c.queues())

def test41():
    class Airplane(sim.Component):
        pass

    class Boat(sim.Component):
        pass

    class Car(sim.Component):
        pass

    env=sim.Environment()
    for i in range(2):
        a = Airplane(name='airplane')
        b = Boat(name='boat,')
        c = Car()
        print(a.name(), b.name(), c.name())

def test40():
    class C(sim.Component):
        def process(self):
            yield self.hold(10)

    class Disturber(sim.Component):
        def process(self):
            yield self.hold(5)
            c.passivate()
            yield self.hold(2)
            c.hold(c.remaining_duration())


    env=sim.Environment(trace=True)
    c=C(name='c')
    Disturber(name='disturber')
    env.run()

def test39():
    class C(sim.Component):
        def process(self):
            yield self.request(r,s='y')

    env=sim.Environment(trace=True)
    x=sim.Uniform(4)
    r = sim.Resource()
    C()
    env.run(4)


def test38():
    def animation_objects(self, value):
        if value=='blue':
            an1=sim.Animate(circle0=(40,),fillcolor0=value, linewidth0=0)
        else:
            an1=sim.Animate(rectangle0=(-40,-20,40,20), fillcolor0=value,linewidth0=0)
        an2=sim.Animate(text=value,textcolor0='white')
        return (an1,an2)

    class X(sim.Component):
        def process(self):

            while True:
                for i in ('red','green','blue','yellow','red'):
                    letters.set(i[0])
                    light.set(i)
                    yield self.hold(1)

    class Q(sim.Queue):
        pass

    env=sim.Environment(trace=True)
    for i in range(3):
        q=Q(name='rij.')
    X()
    light=sim.State('light')
    light.animate()
    letters=sim.State('letters')
    letters.animate(x=100,y=100)

    env.animation_parameters(synced=False)
    env.run()

def test37():
    env=sim.Environment()
    s = sim.Monitor('s')

    s.tally(1)
    s.tally(2)
    s.tally(3)
    s.tally(0)
    s.tally(4)
    s.tally('a')

    print(s.x(ex0=False,force_numeric=True))


def test36():
    l=(1,2,3,4,5,5,'6','x','6.1')
    print(sim.list_to_array(l))

def test35():
    env=sim.Environment()
    sim.show_fonts()
    sim.fonts()


def test34():
    class X(sim.Component):
        def process(self):

            try:
                yield self.hold(-1)
            except sim.SalabimError:
                yield self.hold(1)
            s1.set(1)
            yield self.hold(1)
            s1.set(2)
            s2.set('red')
            yield self.hold(2)
            s1.set(30)

    class Y(sim.Component):
        def process(self):
            while True:
                yield self.wait((s1,'$==2'))
                yield self.hold(1.5)

    class Z(sim.Component):
        def process(self):
            while True:
                yield self.wait((s2,'"$" in ("red","yellow")'),all=True)
                yield self.hold(1.5)


    env=sim.Environment(trace=True)
    env.print_info()
    s1=sim.State(name='s.',value=0)
    s2=sim.State(name='s.',value='green')
    s3=sim.State(name='s.')
    s1.name('piet')
    q=sim.Queue('q.')
    x=X()
    y=Y()
    z=Z()
    env.run(10)
    s1.print_statistics()


def test33():
    class X(sim.Component):
        def process(self):

            yield self.hold(1)
            s1.set(1)
            yield self.hold(1)
            s1.set(2)
            s2.set('red')
            yield self.hold(2)
            s1.set(30)

    class Y(sim.Component):
        def process(self):
            while True:
                yield self.wait((s1,lambda x, component, state: x/2>self.env.now()))
                yield self.hold(1.5)

    class Z(sim.Component):
        def process(self):
            while True:
                yield self.wait((s2,lambda x, component, state: x in ("red","yellow")))
                yield self.hold(1.5)


    env=sim.Environment(trace=True)
    env.print_info()
    s1=sim.State(name='s.',value=0)
    s2=sim.State(name='s.',value='green')
    s3=sim.State(name='s.')
    q=sim.Queue('q.')
    x=X()
    y=Y()
    z=Z()
    env.run(10)


def test32():
    class X(sim.Component):
        def process(self):
            yield self.wait(go)
            print('X after wait')
            yield self.hold(10)

        def p1(self):
            print('X in p1')
            yield self.passivate()

    class Y(sim.Component):
        def process(self):
            yield self.hold(2)
            x.activate(keep_wait=True,at=20)




    env=sim.Environment(trace=True)
    go=sim.State()
    x=X()
    y=Y()
    env.run()


def test31():
    class X(sim.Component):
        def process(self):

            yield self.hold(1)
            s1.set()
            yield self.hold(2)
            s1.reset()
            yield self.hold(2)
            y.print_info()
            s1.trigger()

    class Y(sim.Component):
        def process(self):
            while True:
                yield self.wait(s1,(s2,'red'),(s2,'green'),s3)
                yield self.hold(1.5)


    env=sim.Environment(trace=True)
    env.print_info()
    s1=sim.State(name='s.')
    s2=sim.State(name='s.')
    s3=sim.State(name='s.')
    q=sim.Queue('q.')
    x=X()
    y=Y()
    env.run(10)
    print('value at ',env.now(),s1.get())
    print (s1.value.xduration())
    print(s1.value.tx())
    print(env)
    print(y)
    print(q)
    print(s1)
    s1.print_info()
    s2.print_info()

def test30():
    env=sim.Environment()
    m=sim.Monitor('m')
    print (m.x(ex0=True))
    m.tally(1)
    m.tally(2)
    m.tally(3)
    m.tally(0)
    m.tally('0')
    m.tally('12')
    m.tally('abc')
    print (m.x(ex0=True))


def test29():
    global light
    class Light(sim.Component):
        def setup(self):
            self.green=sim.State(name='green')

        def process(self):
            while True:
                yield self.hold(1)
                self.green.trigger(max=2)
                yield self.hold(1)
                self.green.reset()

    class Car(sim.Component):
        def process(self):
            while True:
                yield self.wait((light.green,True,1),(light.green,True,1),fail_delay=8,all=True)
                yield self.hold(sim.Uniform(1,3).sample())

    de=sim.Environment(trace=True)
    for i in range(10):
        car=Car()
    light=Light()
    de.run(10)
    light.green.print_statistics()
    print(light.green.value.xt())
    print(light.green.waiters())


def test28():
    de=sim.Environment(trace=True)
    wait={}
    for i in range(3):
        wait[i]=sim.Queue('wait.')


def test27():
    m1=sim.Monitor('m1')
    print (m1.mean(),m1.std(),m1.percentile(50),m1.histogram())
    m1.tally(10)
    print (m1.mean(),m1.std(),m1.percentile(50),m1.histogram())


def test26():
    global de
    class X(sim.Component):
        def _get_a(self):
            return self.a

        def _now(self):
            return self.env._now

        def process(self):
            m2.tally()
            yield self.hold(1)
            self.a=4
            m2.tally()
            m2.monitor(True)
            print('3',m2.xt())
            yield self.hold(1)
            self.a=20
            m2.tally()
            yield self.hold(1)
            self.a=0
            m2.tally()
            yield self.hold(1)
            m3.tally()
            m2.monitor(True)




    de=sim.Environment()
    m1=sim.Monitor('m1',type='uint8')
    print (m1.mean())
    m1.tally(10)
    m1.tally(15)
    m1.tally(20)
    m1.tally(92)
    m1.tally(0)
    m1.tally(12)
    m1.tally(0)
    print ('m1.x()',m1.x(force_numeric=False))

    print ('m1',m1.mean(),m1.std(),m1.percentile(50))
    print ('m1 ex0',m1.mean(ex0=True),m1.std(ex0=True),m1.percentile(50,ex0=True))
    x=X()
    x.a=10
    m2=sim.MonitorTimestamp('m2',getter=x._get_a,type='int8')
    print('1',m2.xt())
    m2.monitor(True)
    m2.tally()
    print('a',m2.xt())
#    m2.monitor(True)
    m2.tally()
    print('2',m2.xt())


    m3=sim.MonitorTimestamp('m3',getter=x._now)
    print(m3())

    de.run(10)
    print('4',m2.xt())
    print('5',m2.xduration())
    print(m2.mean(),m2.std(),m2.percentile(50))
    m1.print_histogram(10,0,10)
    m2.print_histogram(10,0,10)
    print(m3.xduration())

    m3.print_histogram(10,0,10)
    print('done')

#    for i in range(101):
#        print(i,m1.percentile(i),m2.percentile(i))
    m3=sim.Monitor('m3')
    m3.tally(1)
    m3.tally(3)
    print('xx')

def test25():
    de=sim.Environment()
    q=sim.Queue('q')
    c={}
    for i in range(8):
        c[i]=sim.Component(name='c.')
        c[i].enter(q)
    print(q)
    for c in q:
        c.priority(q,-c.sequence_number())
    print(q)

def test24():
    class X1(sim.Component):
        def process(self):
            print('**x1 active')
            yield self.request((r,2))
            yield self.hold(100)
            yield self.passivate()
        def p1(self):
            yield self.hold(0.5)
            yield self.activate(process=self.process())
            yield self.hold(100)
            yield self.passivate()

    class X2(sim.Component):
        def process(self):
            yield self.hold(1)
            x1.activate(at=3,keep_request=True)
            yield self.hold(5)
            x1.request(r)
            yield self.hold(1)
            x1.passivate()
            de.main().passivate()
            yield self.hold(5)
            x1.activate(at=20)

    class X3(sim.Component):
        def process(self):
            a=1
            yield self.hold(1)
        pass

    de=sim.Environment(trace=True)
    x1=X1(process='p1')
    x1.activate(at=0.5,process='process',urgent=True,mode='blabla')
    x2=X2()
    x3=X3()
    print('***name=',x3.running_process())
    x4=sim.Component()
    x3.activate(process='process')
    r=sim.Resource('resource')
    de.run(till=sim.inf)

def test1():
    print('test1')

    class X(sim.Component):
        def __init__(self,extra=1,*args,**kwargs):
            sim.Component.__init__(self,*args,**kwargs)
            self.extra=extra


        def process(self):
            while True:
                yield self.hold(1)
                pass

        def action2(self):
            for i in range(5):
                yield self.hold(25)

            yield self.hold(1)

        def actionx(self):
            pass

    class Y(sim.Component):

        def process(self):
            x[3].reactivate(process=x[3].action2(),at=30)
            x[4].cancel()
            yield self.hold(0.5)
            yield self.standby()
            yield self.activate(process=self.action2(0.3))


        def action2(self,param):
            yield self.hold(param)

    class Monitor(sim.Component):
        def process(self):
            while env.now()<30:
                yield self.standby()

    de=sim.Environment(trace=True)
    q=sim.Queue()

    x=[0]
    for i in range(10):
        x.append(X(name='x.',at=i*5))
#        x[i+1].activate(at=i*5,proc=x[i+1].action())
        x[i+1].enter(q)

    x[6].suppress_trace(True)
    i=0
    for c in q:
        print (c._name)
        i=i+1
        if i==4:
            x[1].leave(q)
            x[5].leave(q)
            x[6].leave(q)

    y=Y(name='y')
#    y.activate(at=20)
    env.run(till=35)

#    env.run(4)

def test2():
    de=sim.Environment()
    print('test2')
    x=[None]
    q=[None]
    for i in range(5):
        x.append(sim.Component(name='x.'))
        q.append(sim.Queue(name='q.'))
    y=sim.Component(name='y')
    x[1].enter(q[1])
    y.enter(q[1])
    x[1].enter(q[2])
    x[2].enter(q[2])
    x[2].enter(q[1])
    x[3].enter(q[2])
    q[1].print_statistics()

    q[2].print_statistics()
    q[1].union(q[2],'my union').print_statistics()

    q[1].difference(q[2],'my difference').print_statistics()
    q[1].intersect(q[2],'my intersect').print_statistics()
    q[1].copy('my copy').print_statistics()
#    q[1].move('my move').print_statistics()
    q[1].print_statistics()

    print (q[1])

    yy=q[1].component_with_name('y')
    ii=q[1].index(y)
    print(yy,ii)


def sample_and_print(dist,n):
    s=[]

    for i in range(n):
        s.append(dist.sample())
    print ('mean=',dist.mean(),'samples', s)

def test3():
    print('test3')

    sim.Environment(random_seed=1234567)
    print('string')
    d=sim.Distribution('Exponential (1000)')
    sample_and_print(d,5)
    sim.random_seed(1234567)
    sample_and_print(d,5)
    sim.random_seed(None)
    sample_and_print(d,5)

    print('triangular')
    tr=sim.Triangular(1,5,3)
    sample_and_print(tr,5)

    print('uniform')
    u=sim.Uniform(1,1.1)
    sample_and_print(u,5)
    print('constant')
    c=sim.Constant(10)
    sample_and_print(c,5)

    print('normal')
    n=sim.Normal(1,2)
    sample_and_print(n,5)
    sample_and_print(n,5)

    print('poisson')
    n=sim.Poisson(2)
    sample_and_print(n,5)
    sample_and_print(n,5)

    print('cdf')
    cdf=sim.Cdf((1,0,2,25,2,75,3,100))
    sample_and_print(cdf,5)
    sample_and_print(cdf,5)

    print('pdf list')
    pdf=sim.Pdf((1,2),1)
    sample_and_print(pdf,5)

    print('pdf dict')
    d = {1:'een', 2:'twee'}
    pdf=sim.Pdf(d,1)
    sample_and_print(pdf,5)

    print('pdf x')
    pdf=sim.Pdf((1,1,2,1))
    sample_and_print(pdf,5)

    print('pdf 1')
    pdf=sim.Pdf((sim.Uniform(10,20),10,sim.Uniform(20,30),80,sim.Uniform(30,40),10))
    sample_and_print(pdf,5)

    print('pdf 2')
    pdf=sim.Pdf((sim.Uniform(10,20),sim.Uniform(20,30),sim.Uniform(30,40)),(10,80,10))
    sample_and_print(pdf,5)

    print('pdf 3')
    pdf=sim.Pdf(('red','green',1000),(10,1,10))
    sample_and_print(pdf,5)

    print('pdf 4')
    pdf=sim.Pdf(('red',10,'green',1,1000,10))
    sample_and_print(pdf,5)

def test4():
    print('test4')
    class X(sim.Component):
        def process(self):
            yield self.hold(10)
            yield self.request(res,4)
            yield self.hold(20)
            res.requesters().print_statistics()
            res.claimers().print_statistics()
            for i in range(1):
                self.release(res,4)

    class Y(sim.Component):
        def process(self):
            yield self.hold(11)
            yield self.request(res,1,priority=1-self.i)
            if self.request_failed():
                pass
            else:
                yield self.hold(1)
                self.release(res)

    class Z(sim.Component):
        def process(self):
            yield self.hold(20)
            y[4].reschedule()
            res.capacity(2)

    de=sim.Environment()
    res=sim.Resource(name='res.',capacity=4)
    res.x=0
    x=X(name='x')
    y=[0]
    for i in range(6):
        c=Y(name='y.')
        c.i=i
        y.append(c)

    z=Z(name='z')
    env.run(till=1000)

def test5():
    print('test5')

    class X1(sim.Component):

        def process(self):
            while True:
                while True:
                    yield self.request(r1,2,5,r2,greedy=True,fail_at=de.now()+6)
                    if not self.request_failed()():
                        break
                yield self.hold(1)
                self.release(r1,r2)
                yield self.passivate()
    class X2(sim.Component):

        def process(self):
            while True:
                yield self.request((r1,3),(r2,1,1))
                yield self.hold(1)
                self.release(r1)
                yield self.passivate()
    class X3(sim.Component):

        def process(self):
            while True:
                yield self.request(r1,r2)
                yield self.hold(1)
                self.release(r1,r2)
                yield self.passivate()

    class Y(sim.Component):

#        def __init__(self,*args,**kwargs):
#            sim.Component.__init__(self,*args,**kwargs)

        def process(self):
            yield self.hold(3)
            x1.cancel()
            yield self.hold(10)
            r2.capacity(1)
            pass



    de=sim.Environment(trace=True)
    q=sim.Queue(name='q')
    r1=sim.Resource(name='r1',capacity=3)
    r2=sim.Resource(name='r2',capacity=0)
    r3=sim.Resource(name='r3',capacity=1)

    x1=X1()
    x2=X2()
    x3=X3()


    y=Y(name='y')
    env.run(till=21)

def test6():
    print('test6')
    class X(sim.Component):
        def process(self):
            yield self.passivate()
            yield self.hold(1)

    de=sim.Environment(trace=True)
    x=X()
    print (x.status()())
    q=sim.Queue(name='Queue.')
    q.name('Rij.')
    print (q.name())
    q.clear()
    env.run(till=10)
    x.reactivate()
    env.run()

def test7():
    print('test7')

    class X1(sim.Component):
        def process(self):
            yield self.request(r1,5,r2,2,greedy=True,fail_at=5)
            yield self.passivate()


    class X2(sim.Component):
        def process(self):
            yield self.request(r1,8,r2)
            yield self.passivate()

    class X3(sim.Component):
        def process(self):
            yield self.request(r1,7)
            yield self.passivate()


    de=sim.Environment(trace=True)

    x1=X1()
    x2=X2()
    x3=X3()

    X4=sim.Component()

    r1=sim.Resource(capacity=10,anonymous=True)
    r2=sim.Resource()
    r3=sim.Resource()

    q={}
    for i in range(1,5):
        q[i]=sim.Queue()

    x1.enter(q[1])
    x1.enter(q[2])
    x1.enter(q[3])

    x2.enter(q[1])
    x3.enter(q[1])



    env.run(10)
    r2.capacity(2)
    env.run(20)

    print(sim.default_env)

    print(x1)
    print(x2)
    print(x3)

    print (q[1])
    print (q[2])
    print (q[3])
    print (q[4])

    print(r1)
    print(r2)
    print(r3)

    d=sim.Exponential(10)
    print(d)
    print(sim.Uniform(1,2))
    print(sim.Triangular(40,150,55))
    print(sim.Distribution('Constant(5)'))



def test8():
    print('test8')

    class AnimatePolar(sim.Animate):
        def __init__(self,r,*args,**kwargs):
            self.r=r
            super().__init__(*args,**kwargs)

        def x(self,t):
            tangle=sim.interpolate(t,self.t0,self.t1,0,2*math.pi)
            sint=math.sin(tangle)
            cost=math.cos(tangle)
            x,y=(100+self.r*cost-0*sint,100+self.r*sint+0*cost)
            return x

        def y(self,t):
            tangle=sim.interpolate(t,self.t0,self.t1,0,2*math.pi)
            sint=math.sin(tangle)
            cost=math.cos(tangle)
            x,y=(100+self.r*cost-0*sint,100+self.r*sint+0*cost)
            return y

        def angle(self,t):
            return sim.interpolate(t,self.t0,self.t1,0,360)

        def fillcolor(self,t):
            f=sim.interpolate(t,self.t0,self.t1,0,1)
            if f<0.5:
                return sim.colorinterpolate(f,0,0.5,sim.colorspec_to_tuple('red'),sim.colorspec_to_tuple('blue'))
            else:
                return sim.colorinterpolate(f,0.5,1,sim.colorspec_to_tuple('blue'),sim.colorspec_to_tuple('green'))

        def text(self,t):
            angle=sim.interpolate(t,self.t0,self.t1,0,360)
            return '{:3.0f}'.format(angle)


    class X(sim.Component):
        def slideraction(self):
            print ('value='+str(self.myslider.v))

        def process(self):

            AnimatePolar(r=100,text='A',t1=10)

            x=0
            for fontsize in range(8,30):
                sim.Animate(x0=x,y0=height-100,text='aA1',font=('Calibri,calibri'),fontsize0=fontsize)
                x+=fontsize*2
            x=0
            for fontsize in range(8,30):
                sim.Animate(x0=x,y0=height-200,text='aA1',font='CabinSketch-Bold',fontsize0=fontsize)
                x+=fontsize*2


            self.rx=sim.Animate(x0=600,y0=300,linewidth0=1,
                            rectangle0=(-200,-200,200,200),t1=10,fillcolor0='green#7f',angle1=0)
            self.rx=sim.Animate(x0=500,y0=500,linewidth0=1,line0=(-500,0,500,0),t1=10,fillcolor0='black')
            self.rx=sim.Animate(x0=500,y0=500,linewidth0=1,line0=(0,-500,0,500),t1=10,fillcolor0='black')

            self.rx=sim.Animate(x0=500,y0=500,linewidth0=10,polygon0=(0,0,100,0,100,100,50,50,0,100),offsetx1=100,offsety1=100,t1=10,fillcolor0='red#7f',angle1=360)
            self.rx=sim.Animate(x0=600,y0=300,linewidth0=1,rectangle0=(-200,-200,200,200),t1=10,fillcolor0='blue#7f',angle1=360)

#            self.t1=sim.Animate(x0=500,y0=500,fillcolor0='black',
#                text='Test text',x1=500,y1=500,t1=25,font='CabinSketch-#Bold',fontsize0=20,anchor='ne',angle1=0,fontsize1=50)


            self.i1=sim.Animate(x0=250,y0=250,offsetx0=100,offsety0=100,angle0=0,angle1=360,circle0=(20,),fillcolor0=('red',0),linewidth0=2,linecolor0='blue',circle1=(20,),t1=15)

#            self.ry=sim.Animate(x0=500,y0=300,linewidth0=1,polygon0=(-100,-100,100,-100,0,100),t1=10,fillcolor0='blue',angle1=90)

            self.i1=sim.Animate(x0=500,y0=500,angle0=0,layer=1,image='salabim.png',width0=300,x1=500,y1=500,angle1=360,t1=20,anchor='center')

            yield self.hold(3)
            self.i1.update(image='Upward Systems.jpg',angle1=self.i1.angle1,t1=self.i1.t1,width0=self.i1.width0)
            return
            self.myslider=sim.AnimateSlider(x=600,y=height,width=100,height=20,vmin=5,vmax=10,v=23,resolution=1,label='Test slider',action=self.slideraction)

            return


            self.p1=sim.AnimatePolygon(
            x0=200,y0=200,polygon0=(-100,-100,100,-100,100,100,-100,100),
            t1=25,x1=100,y1=100,fillcolor1='red',linecolor0='blue',linewidth0=3)
            self.p2=sim.Animate(linewidth0=2,linecolor0='black',linecolor1='white',
                x0=100,y0=600,fillcolor0='green',polygon0=(-50,-50,50,-50,0,0),angle1=720,t1=8)
            self.r1=sim.Animate(layer=1,x0=500,y0=500,rectangle0=(0,0,100,100),fillcolor0='yellow',linecolor0='red',linewidth0=2,angle1=180,t1=10)
            self.t1=sim.Animate(x0=200,y0=200,fillcolor0='black',
                text='Test text',x1=100,y1=100,anchor='center',t1=25,font='courier',fontsize1=50)
            self.r2=sim.Animate(rectangle0=(-5,-5,5,5))

            i=0
            for s in ['ne','n','nw','e','center','w','se','s','sw']:
                sim.Animate(x0=200,y0=200,text=s,t0=i,t1=i+1,anchor=s,keep=False,fillcolor0='red')
                i=i+1

            self.p2=sim.Animate(x0=500,y0=500,line0=(0,0,100,100),angle1=360,t1=10,linecolor0='red',linewidth0=5)
            self.r2=sim.Animate(x0=300,y0=700,rectangle0=(-300,-300,300,300),fillcolor0='',linecolor0='black', linewidth0=2)
            self.c1=sim.Animate(x0=300,y0=700,circle0=(0,),fillcolor0='blue',circle1=(60,),t1=20)
            self.i1=sim.Animate(x0=500,y0=500,angle0=0,layer=1,image='BOA.png',width0=300,x1=500,y1=500,angle1=360,t1=20,anchor='center')
#            self.i1=sim.AnimateText(text='ABCDEF',x0=500,y0=200,angle0=0,layer=1,angle1=360,t1=20,anchor='center')
            yield self.hold(10)
#            self.t1.update(color0='white',x1=100,y1=100,t1=25)
            self.r1.update()
            self.c1.update(t1=20,radius1=0)

    import os

    de=sim.Environment(trace=True)
    x=X()
#    s='abcdefghijk'

#    size=getfontsize_to_fit(s,10000)
#    print ('--fontsize_to_fit',size)
#    print('--width-1=', getwidth(s,'',size-1))
#    print('--width  =', getwidth(s,'',size))
#    print('--width+1=', getwidth(s,'',size+1))
#    assert False

    height=768
    env.animation_parameters(modelname='Salabim test')
    env.run(15)
    env.run(till=30)
    print('THE END')


def test9():
    print('test9')
    class X(sim.Component):
        def process(self):
            yield self.passivate(mode='One')
            yield self.passivate(mode='Two')
            yield self.passivate()
            yield self.hold(1)

    class Y(sim.Component):
        def process(self):
            while True:
                print('de.now()=',de.now())
                yield self.hold(1)
                print(x.mode())
                if self.ispassive():
                    x.reactivate()


    de=sim.Environment(trace=True)
    x=X()
    y=Y()
    env.run(till=6)


def test10():
    print('test10')
    for s in ('blue','','black#23','#123456','#12345678',(1,2,3),(4,5,6,7),('blue',8),('blue#67',1),('#123456',23)):
        t=sim.colorspec_to_tuple(s)
        print(s,'==>',t)

def test11():
    class Do1(sim.Component):
        def process(self):
            while True:
                if q1.length()==0:
                    yield self.passivate()
                print('------')
                for cc in q1:
                    print(de.now(),cc.name())
                    yield self.hold(1)

    class Do2(sim.Component):
        def process(self):

            c[1].enter(q1)
            c[2].enter(q1)
            if d1.ispassive():
                d1.reactivate()
            yield self.hold(till=1.5)

            c[3].enter(q1)
            c[4].enter_at_head(q1)
            if d1.ispassive():
                d1.reactivate()

            yield self.hold(till=20.5)
            for cc in q1:
                cc.leave(q1)
            if d1.ispassive():
                d1.reactivate()

    class X(sim.Component):
        pass

    de=sim.Environment(trace=True)
    d2=Do2()
    d1=Do1()

    q1=sim.Queue('q1')
    q2=sim.Queue('q2')
    c={}
    for i in range(10):
        c[i]=sim.Component(name='c'+str(i))
        c[i].enter(q2)
    x=q2.pop()
    print('x=',x)
    print('head of q1',q1.head())
    print('q1[0]',q1[0])
    print('tail of q1',q1.tail())
    print('q1[-1]',q1[-1])

    print('head of q2',q2.head())
    print('q2[0]',q2[0])
    print('tail of q2',q2.tail())
    print('q2[-1]',q2[-1])




    print('**c[0]=',c[0])
    c[0].enter(q1)
    c[0].set_priority(q1,10)
    print(q1)

    c[3].set_priority(q2,10)

    c[1].set_priority(q2,-1)
    c[5].set_priority(q2,10)
    for cx in q2:
        print(cx.name())
    for cx in reversed(q2):
        print(cx.name(),cx in q1)

    print ('--')
    print(q2[-1])
    print('---')


    env.run(till=100)

def test12():

    class X(sim.Component):
        def process(self):
            sim.Animate(text='Piet' ,x0=100,y0=100,x1=500,y1=500,t1=10)
            while True:
                print(sim.default_env())
                yield self.hold(1)

    de=sim.Environment(trace=True)
    env.animation_parameters(speed=1)
    a=sim.Environment(name='piet.')
    b=sim.Environment(name='piet.')
    c=sim.Environment(name='piet.')
    print(a)
    print(b)
    print(c)

    X(auto_start=False)
    X(auto_start=False)
    X(auto_start=False)
    X()
    env.animation_parameters(speed=0.1,video='x.mp4')
    env.run(4)
    env.run(2)
    env.run(4)


def test13():
    de=sim.Environment()
    q=sim.Queue()
    for i in range(10):
        c=sim.Component(name='c.')
        q.add(c)

    print(q)
    for c in q:
        print (c.name())

    for i in range(20):
        print(i,q[i].name())


def test14():
    class X(sim.Component):
        def process(self):
            yield self.request(*r)
            print(self.claimed_resources())

    de=sim.Environment()
    X()
    r=[sim.Resource() for i in range(10)]
    de.run(till=10)

def test15():
    d=sim.Pdf(('r',1,'c',1))
    d=sim.Pdf((1,2,3,4) ,1)
    print(d.mean())
    s=''
    for i in range(100):
        x=d.sample()
        s=s+str(x)
    print(s)


def test16():
    de=sim.Environment()
    env.animation_parameters()
    a=sim.Animate(text='Test',x0=100,y0=100,fontsize0=30,fillcolor0='red')
    a=sim.Animate(line0=(0,0,500,500),linecolor0='white',linewidth0=6)
    env.run()


def test17():
    def actiona():
        bb.remove()
        sl.remove()
    def actionb():
        ba.remove()

    de=sim.Environment()

    for x in range(10):
        for y in range(10):
            a=sim.Animate(rectangle0=(0,0,95,65),x0=5+x*100,y0=5+y*70,fillcolor0='blue',linewidth0=0)
    ba=sim.AnimateButton(x=100,y=700,text='A',action=actiona)
    bb=sim.AnimateButton(x=200,y=700,text='B',action=actionb)
    sl=sim.AnimateSlider(x=300,y=700,width=300)
    sim.Animate(text='Text',x0=700,y0=750,font='Times NEWRomian Italic',fontsize0=30)
    de.animation_parameters(animate=True)
    env.run(5)
    env.animation_parameters(animate=False)
    env.run(100)
    env.animation_parameters(animate=True,background_color='yellow')
    env.run(10)

def test18():
    for j in range(2):
        print('---')
        r=random.Random(-1)
        r1=random.Random(-1)
        d=sim.Exponential(3,r1)
        sim.Environment(random_seed=-1)
        for i in range(3):
            print(sim.Exponential(3,r).sample())
            print(sim.Exponential(3).sample())
            print(d.sample())

def test19():
    sim.show_fonts()

def test20():
    de=sim.Environment()
    y=650
    if Pythonista:
        for t in ('TimesNewRomanPSItalic-MT','Times.NewRoman. PSItalic-MT',
          'TimesNewRomanPSITALIC-MT','TimesNoRomanPSItalic-MT'):
            sim.Animate(text=t,x0=100,y0=y,font=t,fontsize0=30,anchor='w')
            y=y-50
    else:
        for t in ('Times New Roman Italic','TimesNEWRoman   Italic','Times No Roman Italic','timesi','TIMESI'):
            sim.Animate(text=t,x0=100,y0=y,font=t,fontsize0=30,anchor='w')
            y=y-50

    de.animation_parameters(animate=True)
    env.run()


def test21():
#    d=sim.Pdf((sim.Uniform(10,20),10,sim.Uniform(20,30),80,sim.Uniform(30,40),10))
    d=sim.Pdf((sim.Uniform(10,20),sim.Uniform(20,30),sim.Uniform(30,40)),(10,80,10))


    for i in range(20):
        print (d.sample())

def test22():

    class X(sim.Component):
        def process(self):
            yield self.hold(10)

    class Y(sim.Component):
        def process(self):
            while True:
                yield self.hold(1)
                print('status of x=',env.now(),x.status()())

    de=sim.Environment()
    x=X()
    Y()

    env.run(12)

def test23():
    sim.a=100
    for d in ('uni(12,30)','n(12)','exponentia(a)','TRI(1)','(12)','12','  (  12,  30)  ','a'):
        print(d)
        print(sim.Distribution(d))


if __name__ == '__main__':
    test()
