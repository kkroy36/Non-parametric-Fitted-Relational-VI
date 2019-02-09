# -*- coding: utf-8 -*-
"""
Created on Sat Feb 02 15:46:30 2019

@author: Srijita
"""
traj=[(1, ['bOn(s1,b1,t1)', 'bOn(s1,b2,t1)', 'bOn(s1,b3,t1)', 'bOn(s1,b4,t1)', 'tIn(s1,t1,c1)', 'tIn(s1,t2,c1)', 'tIn(s1,t3,c1)', 'move(s1,t1,c3)']), (2, ['tIn(s2,t2,c1)', 'tIn(s2,t3,c1)', 'bOn(s2,b1,t1)', 'bOn(s2,b2,t1)', 'bOn(s2,b3,t1)', 'bOn(s2,b4,t1)', 'tIn(s2,t1,c3)', 'destination(s2,c3)', 'unload(s2,b1,t1)'])]
reversed_trajectory = traj[::-1]
print reversed_trajectory

