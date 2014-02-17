# ----------------------------------------------------------------------
# openSAP32
# Copyright (c) 2014 Duken Marga Turnip
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of openSAP32 the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE        
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------

import numpy as np

class Restrain:
    ''' Define and manage restrain in node'''
    def __init__(self):
        self.list = np.array([])
        self.settlement = np.array([])
        self.spring = np.array([])
        pass
    def addRestrain(self, node, restrain, dimension=2):
        ''' Add restrain to node in structure
        
        Parameters
        ----------
        node : int
            Number of node
        restrain : {'fixed', 'pin', 'roller'}
            Type of restrain
        dimension : int, optional
            Dimension of structure (default: 2)
        
        Example
        -------
        This example shows how to add fixed restrain
        to node 2 and roller restrain to node 4
        
        >>> restrain = Restrain()
        >>> restrain.addRestrain(2, 'fixed')
        >>> restrain.addRestrain(4, 'roller')
        '''
        
        # The logic is to determine node which are
        # restrained based on the type
        # This algorithm still use translation
        # restrain without considering rotation
        totalDOF = dimension*node
        if restrain == 'fixed': # 1,1,1
            restrained = [totalDOF-dimension, totalDOF-dimension+1]
        elif restrain == 'pin': # 1,1,0
            restrained = [totalDOF-dimension, totalDOF-dimension+1]
        elif restrain == 'rollerX' or restrain == 'roller': # 0,1,0
            restrained = [totalDOF-dimension+1]
        elif restrain == 'rollerY': # 1,0,0
            restrained = [totalDOF-dimension]
        else:
            return
        if self.list.size == 0:
            self.list = np.array(restrained)
        else:
            self.list = np.append(self.list, restrained, axis=0)
    def addSettlement(self, node, (dx, dy), dimension=2):
        '''Add settlement to node'''
        if self.settlement.size == 0:
            self.settlement = np.array([[node, dx, dy]])
        else:
            self.settlement = np.append(self.settlement, [[node, dx, dy]], axis=0)
        pass
    def addSpring(self, node, k, direction='x', dimension=2):
        '''Add spring restrain to node'''
        if direction == 'x':
            angle = 180
        elif direction == '-x':
            angle = 0
        elif direction == 'y':
            angle = 270
        elif direction == '-y':
            angle = 90

        if self.spring.size == 0:
            self.spring = np.array([[node, k, angle]])
        else:
            self.spring = np.append(self.spring, [[node, k, angle]], axis=0)
        pass
        