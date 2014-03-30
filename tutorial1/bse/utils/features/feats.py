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
#lambda (dFullData): xxx(dFullData, lLookback = xx),
    lfc_TestFeatures = (
        lambda (dFullData): mom.featMomentum(dFullData, lLookback = 12),
        lambda (dFullData): mom.featMomentum(dFullData, lLookback = 18),
        lambda (dFullData): mom.featMomentum(dFullData, lLookback = 24), 
        lambda (dFullData): mom.featMomentum2Ema(dFullData, lLookback = 12),
        lambda (dFullData): mom.featMomentum2Ema(dFullData, lLookback = 18),
        lambda (dFullData): mom.featMomentum2Ema(dFullData, lLookback = 24), 
        lambda (dFullData): mom.featMomentumTradeRule(dFullData, lLookback = 12),
        lambda (dFullData): mom.featMomentumTradeRule(dFullData, lLookback = 18),
        lambda (dFullData): mom.featMomentumTradeRule(dFullData, lLookback = 24), 
        lambda (dFullData): mom.featAcceleration(dFullData, lLookback = 12),
        lambda (dFullData): mom.featAcceleration(dFullData, lLookback = 18),
        lambda (dFullData): mom.featAcceleration(dFullData, lLookback = 24), 
        lambda (dFullData): mom.featAccelerationTradingRule(dFullData, lLookback = 12),
        lambda (dFullData): mom.featAccelerationTradingRule(dFullData, lLookback = 18),
        lambda (dFullData): mom.featAccelerationTradingRule(dFullData, lLookback = 24), 
        lambda (dFullData): mom.featROC(dFullData, lLookback = 10),
        lambda (dFullData): mom.featROC(dFullData, lLookback = 16),
        lambda (dFullData): mom.featROC(dFullData, lLookback = 22), 
        lambda (dFullData): mom.featRateOfChangeTradingRule(dFullData, lLookback = 10),
        lambda (dFullData): mom.featRateOfChangeTradingRule(dFullData, lLookback = 16),
        lambda (dFullData): mom.featRateOfChangeTradingRule(dFullData, lLookback = 22),
        lambda (dFullData): mom.featMACD(dFullData, slow = 18, fast = 12),
        lambda (dFullData): mom.featMACD(dFullData, slow = 24, fast = 12),
        lambda (dFullData): mom.featMACD(dFullData, slow = 30, fast = 12),
        lambda (dFullData): mom.featMACDS(dFullData, lLookback = 9, fast = 12, slow = 18), 
        lambda (dFullData): mom.featMACDS(dFullData, lLookback = 9, fast = 12, slow = 24), 
        lambda (dFullData): mom.featMACDS(dFullData, lLookback = 9, fast = 12, slow = 30), 
        lambda (dFullData): mom.featMACDR(dFullData, lLookback = 9, fast = 12, slow = 18), 
        lambda (dFullData): mom.featMACDR(dFullData, lLookback = 9, fast = 12, slow = 24), 
        lambda (dFullData): mom.featMACDR(dFullData, lLookback = 9, fast = 12, slow = 30),
        lambda (dFullData): mom.featRSITradingRule(dFullData, lLookback = 9), 
        lambda (dFullData): mom.featRSITradingRule(dFullData, lLookback = 14), 
        lambda (dFullData): mom.featRSITradingRule(dFullData, lLookback = 25), 
        lambda (dFullData): qstkfeat.featRSI(dFullData, lLookback = 9, b_human = False), 
        lambda (dFullData): qstkfeat.featRSI(dFullData, lLookback = 14, b_human = False), 
        lambda (dFullData): qstkfeat.featRSI(dFullData, lLookback = 25, b_human = False), 
        lambda (dFullData): osc.featFASTK(dFullData, lLookback = 12),
        lambda (dFullData): osc.featFASTK(dFullData, lLookback = 18),
        lambda (dFullData): osc.featFASTK(dFullData, lLookback = 24),
        lambda (dFullData): osc.featFASTD(dFullData, lLookback = 12),
        lambda (dFullData): osc.featFASTD(dFullData, lLookback = 18),
        lambda (dFullData): osc.featFASTD(dFullData, lLookback = 24),
        lambda (dFullData): osc.featSLOWD(dFullData, lLookback = 12),
        lambda (dFullData): osc.featSLOWD(dFullData, lLookback = 18),
        lambda (dFullData): osc.featSLOWD(dFullData, lLookback = 24),
        lambda (dFullData): osc.featFASTTradingRule(dFullData, lLookback = 12),
        lambda (dFullData): osc.featFASTTradingRule(dFullData, lLookback = 18),
        lambda (dFullData): osc.featFASTTradingRule(dFullData, lLookback = 24),
        lambda (dFullData): osc.featSLOWTradingRule(dFullData, lLookback = 12),
        lambda (dFullData): osc.featSLOWTradingRule(dFullData, lLookback = 18),
        lambda (dFullData): osc.featSLOWTradingRule(dFullData, lLookback = 24),
        lambda (dFullData): osc.featFastKFastD(dFullData, lLookback = 12),
        lambda (dFullData): osc.featFastKFastD(dFullData, lLookback = 18),
        lambda (dFullData): osc.featFastKFastD(dFullData, lLookback = 24),
        lambda (dFullData): osc.featSlowKSlowD(dFullData, lLookback = 12),
        lambda (dFullData): osc.featSlowKSlowD(dFullData, lLookback = 18),
        lambda (dFullData): osc.featSlowKSlowD(dFullData, lLookback = 24),
        lambda (dFullData): osc.featWILL(dFullData, lLookback = 14),
        lambda (dFullData): osc.featWILLTradingRule(dFullData, lLookback = 14),
        lambda (dFullData): osc.featTypicalPrice(dFullData),
        lambda (dFullData): osc.featMFI(dFullData, lLookback = 14),
        lambda (dFullData): osc.featMFITradingRule(dFullData, lLookback = 14),

        lambda (dFullData): price.featEMAlambda(dFullData, lambd = 0.9),
        lambda (dFullData): price.featEMAlambda(dFullData, lambd = 0.84),
        lambda (dFullData): price.featEMAlambda(dFullData, lambd = 0.78),
        lambda (dFullData): price.featBollingerUp(dFullData, lLookback = 20),
        lambda (dFullData): price.featBollingerUp(dFullData, lLookback = 26),
        lambda (dFullData): price.featBollingerUp(dFullData, lLookback = 32),
        lambda (dFullData): price.featBollingerDown(dFullData, lLookback = 20),
        lambda (dFullData): price.featBollingerDown(dFullData, lLookback = 26),
        lambda (dFullData): price.featBollingerDown(dFullData, lLookback = 32),
        lambda (dFullData): price.featPrice2BollingerUp(dFullData, lLookback = 20),
        lambda (dFullData): price.featPrice2BollingerUp(dFullData, lLookback = 26),
        lambda (dFullData): price.featPrice2BollingerUp(dFullData, lLookback = 32),
        lambda (dFullData): price.featPrice2BollingerDown(dFullData, lLookback = 20),
        lambda (dFullData): price.featPrice2BollingerDown(dFullData, lLookback = 26),
        lambda (dFullData): price.featPrice2BollingerDown(dFullData, lLookback = 32),
        lambda (dFullData): price.featBollingerTradeRule(dFullData, lLookback = 20),
        lambda (dFullData): price.featBollingerTradeRule(dFullData, lLookback = 26),
        lambda (dFullData): price.featBollingerTradeRule(dFullData, lLookback = 32),

        lambda (dFullData): volatility.featCHV(dFullData, lLookback = 10),

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
        #volume.featNVI2SMA,
        #volume.featPVI2SMA,
        volume.featPriceVolumeTrend)

    ld_FeatureParameters = {}
    for fc_feat in lfc_TestFeatures:
        ld_FeatureParameters[fc_feat] = {}

    return lfc_TestFeatures, ld_FeatureParameters