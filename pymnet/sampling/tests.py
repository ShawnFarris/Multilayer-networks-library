# -*- coding: utf-8 -*-
"""
@author: T. Nurmi
"""

import sys
import unittest
from pymnet import net,models
import reqs
import dumb
import esu
import creators

class TestSampling(unittest.TestCase):

    def test_required_lengths(self):
        self.assertEqual((reqs.calculate_required_lengths([4,3,4,2],[3,2,2,1,2,1,1,2,1,1,1])),(6,4))
        self.assertEqual((reqs.calculate_required_lengths([1,2,1],[1,0,1,0])),(2,3))
        self.assertEqual((reqs.calculate_required_lengths([2,2,1],[1,0,1,0])),(3,3))
        self.assertEqual((reqs.calculate_required_lengths([1],[])),(1,1))
        self.assertEqual((reqs.calculate_required_lengths([9999],[])),(9999,1))
        
        self.assertNotEqual((reqs.calculate_required_lengths([5,3,4,2],[3,2,2,1,2,1,1,2,1,1,1])),(6,4))
        
        with self.assertRaises(AssertionError):
            reqs.calculate_required_lengths([49,999],[])
        with self.assertRaises(AssertionError):
            reqs.calculate_required_lengths([],[])
        with self.assertRaises(AssertionError):
            reqs.calculate_required_lengths([1],[1,2,3,4])
        with self.assertRaises(AssertionError):
            reqs.calculate_required_lengths([0,-1,1],[1,2,3,4])
        with self.assertRaises(AssertionError):
            reqs.calculate_required_lengths([0,0,0],[1,2,3,4])
        with self.assertRaises(AssertionError):
            reqs.calculate_required_lengths([0,0,0],[0,0,0,0])
        with self.assertRaises(AssertionError):
            reqs.calculate_required_lengths([1,1],[-1])
        with self.assertRaises(AssertionError):
            reqs.calculate_required_lengths([1,1],[0.5])
        with self.assertRaises(AssertionError):
            reqs.calculate_required_lengths([1,0.5],[1])
            
    def test_dumb_enumeration(self):
        net1 = net.MultilayerNetwork(aspects=1,fullyInterconnected=False)
        net2 = net.MultilayerNetwork(aspects=1,fullyInterconnected=False)
        net2[1,'X'][1,'Y'] = 1
        net2[1,'X'][2,'X'] = 1
        net3 = net.MultilayerNetwork(aspects=1,fullyInterconnected=False)
        net3[1,'X'][1,'Y'] = 1
        net3[1,'X'][3,'X'] = 1
        net3[1,'Y'][1,'Z'] = 1
        net3[1,'Y'][2,'Z'] = 1
        net4 = net.MultilayerNetwork(aspects=1,fullyInterconnected=True)
        net4[1,'X'][1,'Y'] = 1
        net4[1,'X'][2,'X'] = 1
        net5 = models.full_multilayer(2,['X','Y','Z'])
        net6 = net.MultilayerNetwork(aspects=1,fullyInterconnected=True)
        net6[1,'X'][2,'X'] = 1
        net6[1,'X'][1,'Y'] = 1
        net6[1,'Y'][1,'Z'] = 1
        net6[1,'Z'][2,'Z'] = 1
        net6[2,'Z'][2,'Y'] = 1
        resultlist = []
        dumb.dumbEnumeration(net1,[1,2],[1],resultlist)
        self.assertEqual(resultlist,[])
        resultlist = []
        dumb.dumbEnumeration(net2,[1,2],[1],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1,2],['X','Y'])])
        resultlist = []
        dumb.dumbEnumeration(net2,[2,1],[1],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1,2],['X','Y'])])
        resultlist = []
        dumb.dumbEnumeration(net3,[1,1],[1],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1],['X','Y']),([1],['Y','Z'])])
        resultlist = []
        dumb.dumbEnumeration(net3,[2,1],[1],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1,2],['Y','Z']),([1,3],['X','Y'])])
        resultlist = []
        dumb.dumbEnumeration(net3,[2,2],[1],resultlist)
        self.assertEqual(resultlist,[])
        resultlist = []
        dumb.dumbEnumeration(net3,[2,1,1],[1,0,0,0],resultlist)
        self.assertEqual(resultlist,[])
        resultlist = []
        dumb.dumbEnumeration(net3,[2,1,2],[1,1,1,1],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1,2,3],['X','Y','Z'])])
        resultlist = []
        dumb.dumbEnumeration(net4,[1,2],[1],resultlist)
        self.assertEqual(resultlist,[])
        resultlist =  []
        dumb.dumbEnumeration(net5,[2,2,2],[2,2,2,2],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([0,1],['X','Y','Z'])])
        resultlist =  []
        dumb.dumbEnumeration(net5,[2,2],[2],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([0, 1], ['X', 'Y']), ([0, 1], ['X', 'Z']), ([0, 1], ['Y', 'Z'])])
        resultlist = []
        dumb.dumbEnumeration(net6,[2,2,2],[2,2,2,2],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1,2],['X','Y','Z'])])
        
    def test_esu_concise(self):
        net1 = net.MultilayerNetwork(aspects=1,fullyInterconnected=False)
        net2 = net.MultilayerNetwork(aspects=1,fullyInterconnected=False)
        net2[1,'X'][1,'Y'] = 1
        net2[1,'X'][2,'X'] = 1
        net3 = net.MultilayerNetwork(aspects=1,fullyInterconnected=False)
        net3[1,'X'][1,'Y'] = 1
        net3[1,'X'][3,'X'] = 1
        net3[1,'Y'][1,'Z'] = 1
        net3[1,'Y'][2,'Z'] = 1
        net4 = net.MultilayerNetwork(aspects=1,fullyInterconnected=True)
        net4[1,'X'][1,'Y'] = 1
        net4[1,'X'][2,'X'] = 1
        net5 = models.full_multilayer(2,['X','Y','Z'])
        net6 = net.MultilayerNetwork(aspects=1,fullyInterconnected=True)
        net6[1,'X'][2,'X'] = 1
        net6[1,'X'][1,'Y'] = 1
        net6[1,'Y'][1,'Z'] = 1
        net6[1,'Z'][2,'Z'] = 1
        net6[2,'Z'][2,'Y'] = 1
        resultlist = []
        esu.enumerateSubgraphs_v3(net1,[1,2],[1],resultlist)
        self.assertEqual(resultlist,[])
        resultlist = []
        esu.enumerateSubgraphs_v3(net2,[1,2],[1],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1,2],['X','Y'])])
        resultlist = []
        esu.enumerateSubgraphs_v3(net2,[2,1],[1],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1,2],['X','Y'])])
        resultlist = []
        esu.enumerateSubgraphs_v3(net3,[1,1],[1],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1],['X','Y']),([1],['Y','Z'])])
        resultlist = []
        esu.enumerateSubgraphs_v3(net3,[2,1],[1],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1,2],['Y','Z']),([1,3],['X','Y'])])
        resultlist = []
        esu.enumerateSubgraphs_v3(net3,[2,2],[1],resultlist)
        self.assertEqual(resultlist,[])
        resultlist = []
        esu.enumerateSubgraphs_v3(net3,[2,1,1],[1,0,0,0],resultlist)
        self.assertEqual(resultlist,[])
        resultlist = []
        esu.enumerateSubgraphs_v3(net3,[2,1,2],[1,1,1,1],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1,2,3],['X','Y','Z'])])
        resultlist = []
        esu.enumerateSubgraphs_v3(net4,[1,2],[1],resultlist)
        self.assertEqual(resultlist,[])
        resultlist =  []
        esu.enumerateSubgraphs_v3(net5,[2,2,2],[2,2,2,2],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([0,1],['X','Y','Z'])])
        resultlist =  []
        esu.enumerateSubgraphs_v3(net5,[2,2],[2],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([0, 1], ['X', 'Y']), ([0, 1], ['X', 'Z']), ([0, 1], ['Y', 'Z'])])
        resultlist = []
        esu.enumerateSubgraphs_v3(net6,[2,2,2],[2,2,2,2],resultlist)
        for result in resultlist:
            result[0].sort()
            result[1].sort()
        resultlist.sort()
        self.assertEqual(resultlist,[([1,2],['X','Y','Z'])])
        
    def test_esu_exhaustive(self):
        # Will take approx. 45 min
        reqlist = [([1,1],[0]),([1,2],[0]),([1,2],[1]),([2,3],[1]),([2,1,1],[1,0,0,0])]
        for requirement in reqlist:
            for _ in range(30):
                network = creators.multilayer_partially_interconnected(creators.random_nodelists(30,10,5),0.05)
                resultlist_dumb = []
                resultlist_esu = []
                dumb.dumbEnumeration(network,requirement[0],requirement[1],resultlist_dumb)
                esu.enumerateSubgraphs_v3(network,requirement[0],requirement[1],resultlist_esu)
                for result in resultlist_dumb:
                    result[0].sort()
                    result[1].sort()
                resultlist_dumb.sort()
                for result in resultlist_esu:
                    result[0].sort()
                    result[1].sort()
                resultlist_esu.sort()
                self.assertEqual(resultlist_dumb,resultlist_esu)
                

                
        
def makesuite(exhaustive=False):
    suite = unittest.TestSuite()
    suite.addTest(TestSampling("test_required_lengths"))
    suite.addTest(TestSampling("test_dumb_enumeration"))
    suite.addTest(TestSampling("test_esu_concise"))
    if exhaustive:
        suite.addTest(TestSampling("test_esu_exhaustive"))
    return suite

if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestSampling)
    unittest.TextTestRunner(stream=sys.stdout,verbosity=2).run(makesuite())
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    