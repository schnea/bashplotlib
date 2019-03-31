"""
Plotting horizontal, terminal based histograms
"""

from __future__ import print_function

import math
from .utils.helpers import *
from .utils.commandhelp import hist


def plot_horiz_hist(f, width=20, bincount=None, binwidth=None, pch="o", title="", ylab=False, show_summary=False, regular=False):
    """
    Make a histogram

    Arguments:
        width -- the width of the histogram in # of lines
        bincount -- number of bins in the histogram
        binwidth -- width of bins in the histogram
        pch -- shape of the bars in the plot
        colour -- colour of the bars in the terminal
        title -- title at the top of the plot
        ylab -- boolen value for whether or not to display x-axis labels
        show_summary -- boolean value for whether or not to display a summary
        regular -- boolean value for whether or not to start y-labels at 0
    """
    if pch is None:
        pch = "o"

    if isinstance(f, str):
        with open(f) as fh:
            f = fh.readlines()

    min_val, max_val = None, None
    n, mean, sd = 0.0, 0.0, 0.0

    for number in read_numbers(f):
        n += 1
        if min_val is None or number < min_val:
            min_val = number
        if max_val is None or number > max_val:
            max_val = number
        mean += number

    mean /= n

    for number in read_numbers(f):
        sd += (mean - number)**2

    sd /= (n - 1)
    sd **= 0.5

    bins = list(calc_bins(n, min_val, max_val, bincount, binwidth))
    hist = dict((i, 0) for i in range(len(bins)))

    for number in read_numbers(f):
        for i, b in enumerate(bins):
            if number <= b:
                hist[i] += 1
                break
        if number == max_val and max_val > bins[len(bins) - 1]:
            hist[len(hist) - 1] += 1

    min_count = min(hist.values())
    max_count = max(hist.values())

    # `min_display_count` and `max_display_count` are the min/max
    # counts that will be displayed on the x-axis of our
    # graph. If the user sets the `regular` argument to True,
    # we use a `min_display_count` of 0.
    if regular:
        min_display_count = 0
    else:
        min_display_count = min_count
    max_display_count = max_count + 1

    if width is None:
        width = int(max_display_count - min_display_count)
        if width > 40:
            width = 40

    # Calculate how many counts each horizontal unit (square)
    # represents. This will be useful for knowing how long
    # each of our bars should be.
    counts_per_horizontal_unit = float(max_display_count - min_display_count) / width

    # If we need to display y-labels, use `bins` to generate
    # them. `ylabels_width` represents the width of the
    # y-labels "column" so that we can add the appropriate
    # amount of padding in the rest of our graph.
    if ylab:
        ylabels = [str(b) for b in bins]
        ylabels_width = max(len(l) for l in ylabels) + 1
    else:
        ylabels_width = 0

    # Print the title, as per usual
    if title:
        print(box_text(title, width*2 + ylabels_width))
    print()

    # Print the guts of the graph!
    for bin_n, count in hist.iteritems():
        line = ""
        if ylab:
            line += ylabels[bin_n].ljust(ylabels_width)
        line += "|"

        # This is why we calculated `counts_per_horizontal_unit`
        # earlier.
        n_squares = int((count - min_display_count) / counts_per_horizontal_unit) + 1
        line += (" " + pch) * n_squares
        print(line)

    print(" " * ylabels_width + "+" + "-" * width * 2)

    # Printing the x-labels is quite difficult. We only want to print
    # a label for a square if it different to the previous label. This
    # is because we don't want to print labels that look like
    # "1 1 1 1 2 2 2 2...".
    #
    # We therefore generate a list of "candidate" x-labels, which are
    # the labels we would show if we didn't care about repetition. We
    # use this list of candidates to generate a list of deduplicated
    # labels.
    #
    # First we generate the candidates
    candidate_xlabels = [str(int(l)) for l in list(drange(
        min_display_count,
        max_display_count,
        float(max_display_count - min_display_count) / width))]

    # Then we deduplicate `candidate_xlabels`
    xlabels = []
    for cand in candidate_xlabels:
        if cand not in xlabels:
            xlabels.append(cand)
        else:
            xlabels.append("")

    # Print the labels vertically by printing a row with all
    # the first characters in each label, then a row with all
    # the second characters, etc.
    max_xlabel_len = max(len(l) for l in xlabels)
    for row_n in range(0, max_xlabel_len):
        row = ""
        for label in xlabels:
            if len(label) > row_n:
                row += label[row_n]
            else:
                row += " "
            row += " "
        print(" " * (ylabels_width + 2) + row)

    # Finally, print the summary statistics, as per usual
    if show_summary:
        center = max(map(len, map(str, [n, min_val, mean, max_val])))
        center += 15

        print()
        print("-" * (2 + center))
        print("|" + "Summary".center(center) + "|")
        print("-" * (2 + center))
        summary = "|" + ("observations: %d" % n).center(center) + "|\n"
        summary += "|" + ("min value: %f" % min_val).center(center) + "|\n"
        summary += "|" + ("mean : %f" % mean).center(center) + "|\n"
        summary += "|" + ("std dev : %f" % sd).center(center) + "|\n"
        summary += "|" + ("max value: %f" % max_val).center(center) + "|\n"
        summary += "-" * (2 + center)
        print(summary)


def calc_bins(n, min_val, max_val, h=None, binwidth=None):
    """
    Calculate number of bins for the histogram
    """
    if not h:
        h = max(10, math.log(n + 1, 2))
    if binwidth == 0:
        binwidth = 0.1
    if binwidth is None:
        binwidth = (max_val - min_val) / h
    for b in drange(min_val, max_val, step=binwidth, include_stop=True):
        if b.is_integer():
            yield int(b)
        else:
            yield b


def read_numbers(numbers):
    """
    Read the input data in the most optimal way
    """
    if isiterable(numbers):
        for number in numbers:
            yield float(str(number).strip())
    else:
        with open(numbers) as fh:
            for number in fh:
                yield float(number.strip())


