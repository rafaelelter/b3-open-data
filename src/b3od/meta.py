"""Meta information from the services used by the scrapper"""

from numpy import dtype

SERVICES_DTYPES = {
    "TradeInformationConsolidated": {
        "RptDt": dtype("O"),
        "TckrSymb": dtype("O"),
        "ISIN": dtype("O"),
        "SgmtNm": dtype("O"),
        "MinPric": dtype("float64"),
        "MaxPric": dtype("float64"),
        "TradAvrgPric": dtype("float64"),
        "LastPric": dtype("float64"),
        "OscnPctg": dtype("float64"),
        "AdjstdQt": dtype("float64"),
        "AdjstdQtTax": dtype("float64"),
        "RefPric": dtype("float64"),
        "TradQty": dtype("float64"),
        "FinInstrmQty": dtype("float64"),
        "NtlFinVol": dtype("float64"),
    },
    "OTCTradeInformationConsolidated": {
        "RptDt": dtype("O"),
        "TckrSymb": dtype("O"),
        "ISIN": dtype("O"),
        "MinPric": dtype("float64"),
        "MaxPric": dtype("float64"),
        "TradAvrgPric": dtype("float64"),
        "LastPric": dtype("float64"),
        "AdjstdQt": dtype("float64"),
        "RefPric": dtype("float64"),
        "TradQty": dtype("int64"),
        "FinInstrmQty": dtype("float64"),
        "NtlFinVol": dtype("float64"),
        "OprnClssfctnTpCd": dtype("O"),
        "OprnClssfctnTpNm": dtype("O"),
    },
    "TradeInformationConsolidatedAfterHours": {
        "RptDt": dtype("O"),
        "TckrSymb": dtype("O"),
        "ISIN": dtype("O"),
        "SgmtNm": dtype("O"),
        "MinPric": dtype("float64"),
        "MaxPric": dtype("float64"),
        "TradAvrgPric": dtype("float64"),
        "LastPric": dtype("float64"),
        "OscnPctg": dtype("float64"),
        "AdjstdQt": dtype("float64"),
        "AdjstdQtTax": dtype("float64"),
        "RefPric": dtype("float64"),
        "TradQty": dtype("float64"),
        "FinInstrmQty": dtype("float64"),
        "NtlFinVol": dtype("float64"),
    },
    "DerivativesOpenPosition": {
        "RptDt": dtype("O"),
        "TckrSymb": dtype("O"),
        "ISIN": dtype("O"),
        "Asst": dtype("O"),
        "XprtnCd": dtype("O"),
        "SgmtNm": dtype("O"),
        "OpnIntrst": dtype("float64"),
        "VartnOpnIntrst": dtype("float64"),
        "DstrbtnId": dtype("float64"),
        "CvrdQty": dtype("float64"),
        "TtlBlckdPos": dtype("float64"),
        "UcvrdQty": dtype("float64"),
        "TtlPos": dtype("float64"),
        "BrrwrQty": dtype("float64"),
        "LndrQty": dtype("float64"),
        "CurQty": dtype("float64"),
        "FwdPric": dtype("float64"),
    },
    "EconomicIndicatorPrice": {
        "RptDt": dtype("O"),
        "Asst": dtype("O"),
        "TckrSymb": dtype("O"),
        "EcncIndDesc": dtype("O"),
        "PricVal": dtype("float64"),
    },
    "InstrumentsConsolidated": {
        "RptDt": dtype("O"),
        "TckrSymb": dtype("O"),
        "Asst": dtype("O"),
        "AsstDesc": dtype("O"),
        "SgmtNm": dtype("O"),
        "MktNm": dtype("O"),
        "SctyCtgyNm": dtype("O"),
        "XprtnDt": dtype("O"),
        "XprtnCd": dtype("O"),
        "TradgStartDt": dtype("O"),
        "TradgEndDt": dtype("O"),
        "BaseCd": dtype("float64"),
        "ConvsCritNm": dtype("O"),
        "MtrtyDtTrgtPt": dtype("float64"),
        "ReqrdConvsInd": dtype("O"),
        "ISIN": dtype("O"),
        "CFICd": dtype("O"),
        "DlvryNtceStartDt": dtype("O"),
        "DlvryNtceEndDt": dtype("O"),
        "OptnTp": dtype("O"),
        "CtrctMltplr": dtype("float64"),
        "AsstQtnQty": dtype("float64"),
        "AllcnRndLot": dtype("float64"),
        "TradgCcy": dtype("O"),
        "DlvryTpNm": dtype("O"),
        "WdrwlDays": dtype("float64"),
        "WrkgDays": dtype("float64"),
        "ClnrDays": dtype("float64"),
        "RlvrBasePricNm": dtype("O"),
        "OpngFutrPosDay": dtype("float64"),
        "SdTpCd1": dtype("O"),
        "UndrlygTckrSymb1": dtype("O"),
        "SdTpCd2": dtype("O"),
        "UndrlygTckrSymb2": dtype("O"),
        "PureGoldWght": dtype("float64"),
        "ExrcPric": dtype("float64"),
        "OptnStyle": dtype("O"),
        "ValTpNm": dtype("O"),
        "PrmUpfrntInd": dtype("O"),
        "OpngPosLmtDt": dtype("O"),
        "DstrbtnId": dtype("float64"),
        "PricFctr": dtype("float64"),
        "DaysToSttlm": dtype("float64"),
        "SrsTpNm": dtype("O"),
        "PrtcnFlg": dtype("O"),
        "AutomtcExrcInd": dtype("O"),
        "SpcfctnCd": dtype("O"),
        "CrpnNm": dtype("O"),
        "CorpActnStartDt": dtype("O"),
        "CtdyTrtmntTpNm": dtype("O"),
        "MktCptlstn": dtype("float64"),
        "CorpGovnLvlNm": dtype("O"),
    },
    "OTCInstrumentsConsolidated": {
        "RptDt": dtype("O"),
        "CrpnCd": dtype("O"),
        "TckrSymb": dtype("O"),
        "ISIN": dtype("O"),
        "CrpnNm": dtype("O"),
        "OTCSgmtNm": dtype("O"),
        "MktNm": dtype("O"),
        "Law12431SpprtInd": dtype("bool"),
        "SrsIdCd": dtype("O"),
        "IsseNb": dtype("int64"),
        "InstrmRmnrtnTp": dtype("O"),
        "IntrstParamsPctg": dtype("float64"),
        "IntrstPctgRate": dtype("float64"),
        "BaseIntrstRate": dtype("float64"),
        "XprtnDt": dtype("O"),
        "IssdQty": dtype("float64"),
        "IsseUnitPric": dtype("float64"),
        "EmssnRstrctdWorkInd": dtype("bool"),
    },
    "MarginScenarioLiquidAssets": {
        "RptDt": dtype("O"),
        "PRFNm": dtype("O"),
        "VrtxCd": dtype("int64"),
        "ScnroId": dtype("int64"),
        "PRFVal": dtype("float64"),
        "TpShck": dtype("O"),
    },
    "LendingOpenPosition": {
        "RptDt": dtype("O"),
        "TckrSymb": dtype("O"),
        "ISIN": dtype("O"),
        "Asst": dtype("O"),
        "BalQty": dtype("int64"),
        "TradAvrgPric": dtype("float64"),
        "PricFctr": dtype("int64"),
        "BalVal": dtype("float64"),
    },
    "LoanBalance": {
        "RptDt": dtype("O"),
        "TckrSymb": dtype("O"),
        "ISIN": dtype("O"),
        "Asst": dtype("O"),
        "QtyCtrctsDay": dtype("int64"),
        "QtyShrDay": dtype("int64"),
        "ValCtrctsDay": dtype("float64"),
        "DnrMinRate": dtype("O"),
        "DnrAvrgRate": dtype("O"),
        "DnrMaxRate": dtype("O"),
        "TakrMinRate": dtype("O"),
        "TakrAvrgRate": dtype("O"),
        "TakrMaxRate": dtype("O"),
        "MktNm": dtype("O"),
    },
    "PositionLimits": {
        "PosLmtTpCd": dtype("O"),
        "TickerSymbol": dtype("O"),
        "XprtnDt": dtype("O"),
        "PosLmtDesc": dtype("O"),
        "AggrLvlCd": dtype("O"),
        "L1LmtQty": dtype("int64"),
        "L2LmtQty": dtype("int64"),
        "FreeFloatQty": dtype("O"),
    },
}

SERVICES_DATE_COLUMNS = {
    "TradeInformationConsolidated": ["RptDt"],
    "OTCTradeInformationConsolidated": ["RptDt"],
    "TradeInformationConsolidatedAfterHours": ["RptDt"],
    "DerivativesOpenPosition": ["RptDt"],
    "EconomicIndicatorPrice": ["RptDt"],
    "InstrumentsConsolidated": [
        "RptDt",
        "XprtnDt",
        "TradgStartDt",
        "TradgEndDt",
        "DlvryNtceStartDt",
        "DlvryNtceEndDt",
        "OpngPosLmtDt",
        "CorpActnStartDt",
    ],
    "OTCInstrumentsConsolidated": ["RptDt", "XprtnDt"],
    "MarginScenarioLiquidAssets": ["RptDt"],
    "LendingOpenPosition": ["RptDt"],
    "LoanBalance": ["RptDt"],
    "PositionLimits": ["XprtnDt"],
}
