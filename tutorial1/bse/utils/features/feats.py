'''
Created on Feb 13, 2014

@author: dimitar
'''

import mom 
import osc
import price
import volatility
import volume
import QSTK.qstkfeat as qstkfeat

def get_feats():
#lambda (dData): xxx(dData, lLookback = xx),
    lfc_TestFeatures = (
        lambda (dData): mom.featMomentum(dData, lLookback = 12),
        lambda (dData): mom.featMomentum(dData, lLookback = 18),
        lambda (dData): mom.featMomentum(dData, lLookback = 24), 
        lambda (dData): mom.featMomentum2Ema(dData, lLookback = 12),
        lambda (dData): mom.featMomentum2Ema(dData, lLookback = 18),
        lambda (dData): mom.featMomentum2Ema(dData, lLookback = 24), 
        lambda (dData): mom.featMomentumTradeRule(dData, lLookback = 12),
        lambda (dData): mom.featMomentumTradeRule(dData, lLookback = 18),
        lambda (dData): mom.featMomentumTradeRule(dData, lLookback = 24), 
        lambda (dData): mom.featAcceleration(dData, lLookback = 12),
        lambda (dData): mom.featAcceleration(dData, lLookback = 18),
        lambda (dData): mom.featAcceleration(dData, lLookback = 24), 
        lambda (dData): mom.featAccelerationTradingRule(dData, lLookback = 12),
        lambda (dData): mom.featAccelerationTradingRule(dData, lLookback = 18),
        lambda (dData): mom.featAccelerationTradingRule(dData, lLookback = 24), 
        lambda (dData): mom.featROC(dData, lLookback = 10),
        lambda (dData): mom.featROC(dData, lLookback = 16),
        lambda (dData): mom.featROC(dData, lLookback = 22), 
        lambda (dData): mom.featRateOfChangeTradingRule(dData, lLookback = 10),
        lambda (dData): mom.featRateOfChangeTradingRule(dData, lLookback = 16),
        lambda (dData): mom.featRateOfChangeTradingRule(dData, lLookback = 22),
        lambda (dData): mom.featMACD(dData, slow = 18, fast = 12),
        lambda (dData): mom.featMACD(dData, slow = 24, fast = 12),
        lambda (dData): mom.featMACD(dData, slow = 30, fast = 12),
        lambda (dData): mom.featMACDS(dData, lLookback = 9, fast = 12, slow = 18), 
        lambda (dData): mom.featMACDS(dData, lLookback = 9, fast = 12, slow = 24), 
        lambda (dData): mom.featMACDS(dData, lLookback = 9, fast = 12, slow = 30), 
        lambda (dData): mom.featMACDR(dData, lLookback = 9, fast = 12, slow = 18), 
        lambda (dData): mom.featMACDR(dData, lLookback = 9, fast = 12, slow = 24), 
        lambda (dData): mom.featMACDR(dData, lLookback = 9, fast = 12, slow = 30),
        lambda (dData): mom.featRSITradingRule(dData, lLookback = 9), 
        lambda (dData): mom.featRSITradingRule(dData, lLookback = 14), 
        lambda (dData): mom.featRSITradingRule(dData, lLookback = 25), 
        lambda (dData): qstkfeat.featRSI(dData, lLookback = 9, b_human = False), 
        lambda (dData): qstkfeat.featRSI(dData, lLookback = 14, b_human = False), 
        lambda (dData): qstkfeat.featRSI(dData, lLookback = 25, b_human = False), 
        lambda (dData): osc.featFASTK(dData, lLookback = 12),
        lambda (dData): osc.featFASTK(dData, lLookback = 18),
        lambda (dData): osc.featFASTK(dData, lLookback = 24),
        lambda (dData): osc.featFASTD(dData, lLookback = 12),
        lambda (dData): osc.featFASTD(dData, lLookback = 18),
        lambda (dData): osc.featFASTD(dData, lLookback = 24),
        lambda (dData): osc.featSLOWD(dData, lLookback = 12),
        lambda (dData): osc.featSLOWD(dData, lLookback = 18),
        lambda (dData): osc.featSLOWD(dData, lLookback = 24),
        lambda (dData): osc.featFASTTradingRule(dData, lLookback = 12),
        lambda (dData): osc.featFASTTradingRule(dData, lLookback = 18),
        lambda (dData): osc.featFASTTradingRule(dData, lLookback = 24),

        osc.featFastKFastD,
        osc.featWILL,
        osc.featWILLTradingRule,
        osc.featTypicalPrice,
        osc.featMFI,
        osc.featMFITradingRule,
        
        price.featEMAlambda,
        price.featBollinger,
        price.featBollingerUp,
        price.featBollingerDown,
        price.featPrice2BollingerUp,
        price.featPrice2BollingerDown,
        price.featBollingerTradeRule,
        
        volatility.featCHV,
#        volatility.featGK,
#        volatility.featSharpeRatio

        volume.featOBV,
        volume.featADL,
        volume.featCHO,
        volume.featChaikinTradeRule,
        volume.featNVI,
        volume.featPVI,
        volume.featNVITradeRule,
        volume.featPVITradeRule,
        volume.featNVI2SMA,
        volume.featPVI2SMA,
        volume.featPriceVolumeTrend)

    ld_FeatureParameters = {}
    for fc_feat in lfc_TestFeatures:
        ld_FeatureParameters[fc_feat] = {}

    return lfc_TestFeatures, ld_FeatureParameters