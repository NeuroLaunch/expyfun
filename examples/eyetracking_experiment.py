"""
============================
Experiment with eye-tracking
============================

Integration with Eyelink functionality makes programming experiments
using eye-tracking simpler.
"""
# Author: Eric Larson <larsoner@uw.edu>
#
# License: BSD (3-clause)

print __doc__

from expyfun import ExperimentController, EyelinkController
from psychopy import visual
import numpy as np

link = '100.1.1.1'  # or 'dummy' for fake operation


with ExperimentController('testExp', full_screen=True,
                          participant='foo', session='001') as ec:
    el = EyelinkController(ec, link=link)

    ec.init_trial()  # resets trial clock, clears keyboard buffer, etc
    ec.screen_prompt('Welcome to the experiment!\n\nFirst, we will '
                     'perform a screen calibration.1\n\nPress a button '
                     'to continue', live_keys=['1'])
    # do a calibration -- by default this automatically starts a
    # recording file on the EyeLink
    el.calibrate()

    # let's trace a circle on the screen
    ec.screen_prompt('Excellent! Now, follow the cursor around the '
                     'perimiter of a circle.\n\nPress a button '
                     'to continue', live_keys=['1'])
    ec.clear_screen()

    # initialize the circle
    rad = 10  # radius in degrees
    theta = np.linspace(np.pi / 2., 2.5 * np.pi, 200)
    x_pos, y_pos = rad * np.cos(theta), rad * np.sin(theta)
    # by default the circles are centered, which is what we want
    big_circ = visual.Circle(ec.win, 10, edges=100, units='deg')
    targ_circ = visual.Circle(ec.win, 0.2, edges=100, units='deg',
                              fillColor=(1., -1., -1.), lineColor=None)

    # let's stamp this trial ID to the file
    el.stamp_trial_id(1)
    # now let's make it so the SYNC message gets stamped when we flip
    ec.call_on_flip_and_play(el.stamp_trial_start)
    # start out by waiting for a 1 sec fixation at the start
    targ_circ.setPos((x_pos[0], y_pos[0]), units='deg')
    big_circ.draw()
    targ_circ.draw()
    fix_pos = ec.deg2pix((x_pos[0], y_pos[0]))
    ec.flip_and_play()
    if not el.wait_for_fix(fix_pos, 1., max_wait=5.):
        print 'Initial fixation failed'
    for ii, (x, y) in enumerate(zip(x_pos[1:], y_pos[1:])):
        targ_circ.setPos((x, y), units='deg')
        big_circ.draw()
        targ_circ.draw()
        ec._win.flip()
        fix_pos = ec.deg2pix((x, y))
        if not el.wait_for_fix(fix_pos, max_wait=5.):
            print 'Fixation {0} failed'.format(ii + 1)

    # eyelink auto-closes (el.close()) because it gets registered with EC
