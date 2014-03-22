'''
Created on Feb 13, 2014

@author: dimitar
'''

import mom 
import osc
import price
import volatility
import volume

def get_feats():
#lambda : KNeighborsClassifier(n_neighbors = 5)
    lfc_TestFeatures = (
        lambda (dData): mom.featMomentum(dData, lLookback = 12),
        lambda (dData): mom.featMomentum(dData, lLookback = 18),
        lambda (dData): mom.featMomentum(dData, lLookback = 24), 
        mom.featMomentum2Ema, 
        mom.featMomentumTradeRule, 
        mom.featAcceleration, 
        mom.featAccelerationTradingRule,
        mom.featROC, 
        mom.featRateOfChangeTradingRule, 
        mom.featMACD, 
        mom.featMACDS, 
        mom.featMACDR, 
        mom.featRSITradingRule,
        
        osc.featFASTK,
        osc.featFASTD,
        osc.featFASTTradingRule,
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