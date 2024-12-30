import pandas as pd
import numpy as np

def aegis_dcf_model():
    wacc = 0.12
    perpetual_growth = 0.04
    years_projection = 5
    
    historical = {
        'revenue': [7000, 8200, 9500],
        'ebit_margin': [0.11, 0.12, 0.13],
        'depreciation': [150, 170, 190],
        'capex': [250, 270, 290],
        'working_capital_change': [50, 60, 70]
    }
    
    def project_financials():
        projections = pd.DataFrame()
        revenue_growth = 0.15
        revenues = []
        base_revenue = historical['revenue'][-1]
        
        for i in range(years_projection):
            base_revenue *= (1 + revenue_growth)
            revenues.append(base_revenue)
            
        projections['Revenue'] = revenues
        projections['EBIT'] = projections['Revenue'] * historical['ebit_margin'][-1]
        
        dep_growth = 0.10
        base_dep = historical['depreciation'][-1]
        depreciation = []
        
        for i in range(years_projection):
            base_dep *= (1 + dep_growth)
            depreciation.append(base_dep)
            
        projections['Depreciation'] = depreciation
        projections['CAPEX'] = projections['Revenue'] * 0.05
        projections['WC_Change'] = projections['Revenue'] * 0.02
        
        projections['FCF'] = (
            projections['EBIT'] * 0.75
            + projections['Depreciation']
            - projections['CAPEX']
            - projections['WC_Change']
        )
        
        return projections
    
    def calculate_terminal_value(final_fcf):
        return final_fcf * (1 + perpetual_growth) / (wacc - perpetual_growth)
    
    def discount_cash_flows(projections):
        dcf_values = []
        
        for i in range(len(projections)):
            dcf = projections['FCF'].iloc[i] / ((1 + wacc) ** (i + 1))
            dcf_values.append(dcf)
            
        terminal_value = calculate_terminal_value(projections['FCF'].iloc[-1])
        discounted_terminal_value = terminal_value / ((1 + wacc) ** years_projection)
        
        enterprise_value = sum(dcf_values) + discounted_terminal_value
        
        return {
            'dcf_values': dcf_values,
            'terminal_value': terminal_value,
            'discounted_terminal_value': discounted_terminal_value,
            'enterprise_value': enterprise_value
        }
    
    projections = project_financials()
    valuation = discount_cash_flows(projections)
    
    net_debt = 1000
    equity_value = valuation['enterprise_value'] - net_debt
    shares_outstanding = 350
    price_per_share = equity_value / shares_outstanding
    
    return {
        'projections': projections,
        'valuation_metrics': valuation,
        'equity_value': equity_value,
        'price_per_share': price_per_share
    }

results = aegis_dcf_model()


print("\nFinancial Projections:")
print(results['projections'])

print("\nValuation Metrics:")
print("Enterprise Value: Rs", round(results['valuation_metrics']['enterprise_value'], 2), "Crores")
print("Equity Value: Rs", round(results['equity_value'], 2), "Crores")
print("Price per Share: Rs", round(results['price_per_share'], 2))