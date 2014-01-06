#!/usr/bin/env python
# coding: utf-8
# yc@2014/01/06

import signal
from threading import Condition


__all__ = ['EasyPauseResume', 'wait_if_paused']


class EasyPauseResume(object):
  '''
  '''
  cond = Condition()
  paused = False

  def __init__(self, sig_pause='SIGUSR1', sig_resume='SIGUSR2', debug=False):
    '''
    sig_pause: pause if received a sig_pause, default: SIGUSR1
    sig_resume: resume if received a sig_resume, default: SIGUSR2
    '''
    assert sig_pause != sig_resume, 'sig_pause cannot be equal to sig_resume'
    self.debug = debug
    try:
      signal.signal(getattr(signal, sig_pause), self._pause)
      signal.signal(getattr(signal, sig_resume), self._resume)
    except ValueError:
      print 'signal error, see `kill -l` for a list of signals'

  def wait_if_paused(self):
    '''
    If paused, wait to be wake up by outer resume, otherwise doing nothing
    '''
    with self.cond:
      if self.paused:
        self.log('Paused, waiting for resume signal...')
        while self.paused:
          self.cond.wait(1)
        self.log('Resumed, continue to run')

  def _resume(self, signum, frame):
    '''
    '''
    if self.paused:
      with self.cond:
        self.paused = False
        self.log('Resuming')
        self.cond.notify()

  def _pause(self, signum, frame):
    '''
    '''
    if not self.paused:
      with self.cond:
        self.paused = True
        self.log('Pausing')

  def log(self, msg):
    if self.debug:
      print msg

_epr = None
def wait_if_paused(**args):
  global _epr
  if not _epr:
    _epr = EasyPauseResume(**args)
  _epr.wait_if_paused()
