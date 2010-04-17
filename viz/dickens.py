import os
import json

url ='http://austgate.co.uk/dickens/js/index_json.php?author=Dickens'
OUTDIR = 'out'
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

def retrieve_json():
    localpath = 'dickens.json'
    if not os.path.exists(localpath):
        urllib.retrieve(url, localpath)
    return localpath

DICKENS = 'Mr Charles Dickens'
def load_json():
    '''Load and clean json.
    
    Just load into memory since pretty small ...

    @return: a dictionary of letters keyed by 
    '''
    out = json.load(open(retrieve_json()))
    letters = {}
    for count,letter in enumerate(out['items']):
        name = letter['label'].strip()
        year = int(letter['date'])
        id = letter['letter_id']
        # some tests for weird data
        if year != 0 and letter['date'] == '0':
            print letter
        # skip bad data ...
        if year == 0 or 'The same' in letter['label']:
            continue 
        yield (name, year)

import math
PI = math.pi
import matplotlib.pyplot as plt
class Analyzer(object):
    '''Analyze the Dickens letter data.
    '''
    @property
    def letters(self):
        if not hasattr(self, '_letters'):
            self._letters = [ letter for letter in load_json() ]
        return self._letters

    def plot_counts(self, dates=None):
        if dates is None:
            dates = [ x[1] for x in self.letters ]
        bins = range(min(dates), max(dates)+1)
        plt.hist(dates, bins, fc='blue', alpha=0.8)
        plt.savefig('letter_dates.png')

    def plot_letter_network(self, names=None, fn='dickens_letter_network.png'):
        if names is None:
            names = list(set([ x[0] for x in self.letters]))
        import networkx as nx
        dgr = nx.Graph()
        labels = { -1: u'Charles Dickens' } 
        for count,name in enumerate(names):
            # dgr.add_edge(u'Charles Dickens', name)
            dgr.add_edge(-1, count)
            labels[count] = name
        pos = nx.graphviz_layout(dgr, prog='twopi')
        fig = plt.figure(1, figsize=(15,15))
        nx.draw(dgr, pos, node_size=15, labels=labels, font_size=10)
        plt.savefig(self._fn(fn))

    def _clock_data(self, letters):
        counts = {}
        starts = {}
        ends = {}
        maxyear = 100000
        minyear = -100000
        for name,year in letters:
            counts[name] = counts.get(name, 0) + 1
            starts[name] = min(year, starts.get(name, maxyear))
            ends[name] = max(year+1, ends.get(name, minyear))
        return counts,starts,ends
    
    def _clock_data_in_polar(self, counts, starts, ends, start_radius=0.1):
        maxcount = float(max(counts.values()))
        first = min(starts.values())
        last = max(ends.values())
        def angle_start(year):
            return 2*PI * float(year - first) / (last-first)
        def angle_end(year):
            return 2*PI - 2*PI * float(last - year) / (last-first)

        # width of 
        # sum(width) = 1 - start_radius
        # width(x) = alpha * count(x)
        # => alpha = 1-start_radius/sum(count)
        alpha = (1.0-start_radius)/sum(counts.values())

        orderedcounts = [ (y,x) for x,y in
            sorted([(y,x) for x,y in counts.items()]) ]

        # dictionary of (starttheta, startr)
        results = {}
        radius = start_radius
        for name,count in orderedcounts:
            astart = angle_start(starts[name])
            aend = angle_end(ends[name])
            results[name] = [(astart,radius), aend-astart, alpha*count]
            radius += alpha*count
        return results

    def clock_plot(self, letters=None, fn='clock.png', annotate=True):
        '''Do a "clock" plot.
        
        1. Count number of letters per person and start and end date.
            * Find first and last dates
        2. Rank people in order of the number of letters they received.
        3. Plot segments whose width is proportional to number of letters and
        start and end of segment corresponds to start and end date.

        Use polar coordinates. (If not using polar you would need to use
        matplotlib.patches.Wedge)
        '''
        if letters is None:
            letters = self.letters
        counts, starts, ends = self._clock_data(letters)
        out = self._clock_data_in_polar(counts,starts,ends)
        import pylab
        from matplotlib.patches import Rectangle
        from matplotlib.collections import PatchCollection
        fig=pylab.figure()
        ax=fig.add_subplot(111, polar=True)
        patches = []
        for name in out:
            anglestart,radius = out[name][0]
            radius_width = out[name][2]
            # draw line out to segment
            # pylab.polar([anglestart,anglestart], [0,radius], 'k-')
            w = Rectangle(*out[name], facecolor='black', ec='black')
            patches.append(w)

            wedge_centre = (anglestart,radius+radius_width)
            if annotate:
                 pylab.annotate(name, wedge_centre,
                     (anglestart,1.2+2*radius_width),
                     arrowprops={'width':0.05, 'headwidth': 0.05, 'frac': 0.01},
                     size='xx-small'
                     )

        p = PatchCollection(patches)
        ax.add_collection(p)
        pylab.polar([0,0], [0,0.0])

        # hack to get rid of axes ...
        # ax = pylab.gca()
        # ax.set_frame_on(False)
        # pylab.yticks([],[])
        # pylab.xticks([],[])
        first = min(starts.values())
        last = max(ends.values())
        numticks = 10
        increment = int(float(last-first)/numticks)
        increment_angle = (2*PI*increment)/(last-first)
        pylab.xticks([idx*increment_angle for idx in range(numticks)],
            [ first + increment * idx for idx in range(numticks) ]
            )
        # play around with where outside is relative to annotations and data
        pylab.ylim(0, 1.0)
        pylab.yticks([],[])
        # pylab.title('Who Dickens Wrote To (width~num letters)')
        pylab.savefig(self._fn(fn))
    
    def _fn(self, fn):
        return os.path.join(OUTDIR, fn)


if __name__ == '__main__':
    a = Analyzer()
    a.plot_letter_network()
    a.clock_plot(fn='clock_labels.png', annotate=True)
    a.clock_plot(fn='clock_no_labels.png', annotate=False)
    print
    print('** New visualizations in: %s' % OUTDIR)

