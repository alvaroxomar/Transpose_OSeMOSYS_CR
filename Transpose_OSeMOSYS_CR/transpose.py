# Este código está adaptado para transponer los datos de INPUT de OSeMOSYS-CR al formato matricial de entrada de datos de MoManI  

import pandas as pd
import numpy as np
# Los añosde inicio y horizonte de estudio del caso
ini_year = 2015
end_year = 2050
years = []
for i in range(ini_year, end_year+1):
    years.append(i)
print(years)
# Se definene los set según el código asignado en el repositorio OSeMOSYS-CR
tecnologias = 'BACKSTOP_PS BACKSTOP_TS DBIO_El DDSL_El DDSL_HF DDSL_LF DDSL_Pr DDSL_Pu DELE_HF DELE_LF DELE_Pr DELE_Pu DGSL_LF DGSL_Pr DGSL_Pu DHYD_HF DHYD_Pu DIST_DSL DIST_FOI DIST_FWO DIST_GSL DIST_HYD DIST_JFUEL DIST_LPG DIST_NG DIST_PCO DLPG_HF DLPG_LF DLPG_Pr DLPG_Pu ESRNBIO ESRNGEO ESRNSUN ESRNWAT ESRNWND PPBIO001 PPBIO002 PPDSL001 PPDSL002 PPFOB001 PPFOB002 PPGEO001 PPGEO002 PPHDAM001 PPHDAM002 PPHROR001 PPHROR002 PPPVD002 PPPVT001 PPPVT002 PPWND002 PPWNT001 PPWNT002 PROD_HYD_CH4 PROD_HYD_H20 TDDIST01 TDDIST02 TDTRANS01 TDTRANS02 Techs_4WD Techs_Buses Techs_He_Freight Techs_LD Techs_Li_Freight Techs_Microbuses Techs_Minivan Techs_Motos Techs_Taxis Techs_Trains TRANOMOTBike TRANOMOTWalk TRBUSDSL01 TRBUSDSL02 TRBUSELC02 TRBUSHYBD02 TRBUSHYD02 TRBUSLPG02 TRFWDDSL01 TRFWDDSL02 TRFWDELE02 TRFWDGAS01 TRFWDGAS02 TRFWDHYBD02 TRFWDLPG01 TRFWDLPG02 TRFWDPHYBD02 TRLDDSL01 TRLDDSL02 TRLDELE02 TRLDGAS01 TRLDGAS02 TRLDHYBG02 TRLDPHYBG02 TRMBUSDSL01 TRMBUSDSL02 TRMBUSELE02 TRMBUSHYBD02 TRMBUSHYD02 TRMBUSLPG02 TRMIVDSL02 TRMIVELE02 TRMIVGAS02 TRMIVHYBD02 TRMIVHYBG02 TRMIVLPG02 TRMOTELC02 TRMOTGAS01 TRMOTGAS02 TRTAXDSL01 TRTAXDSL02 TRTAXELC02 TRTAXGAS01 TRTAXGAS02 TRTAXHYBD02 TRTAXHYBG02 TRTAXLPG02 TRXTRAIELEFRE02 TRXTRAINDSL01 TRXTRAINDSL02 TRXTRAINELC02 TRYLFDSL01 TRYLFDSL02 TRYLFELE02 TRYLFGAS02 TRYLFHYBD02 TRYLFHYBG02 TRYLFLPG02 TRYTKDSL01 TRYTKDSL02 TRYTKELC02 TRYTKHYBD02 TRYTKHYD02 TRYTKLPG02'.split()
fuels = 'E1BIO E1DSL E1FOI E1FWO E1GAS E1GEO E1JEFU E1LPG E1METH E1PCO E1SOL E1WAT E1WIN E2ELC01 E2HYD E3ELC02 E3ELC03 E3ELC04 E6TDFREHEA E6TDFRELIG E6TDPASPRIV E6TDPASSPUB E6TRNOMOT E6TRRIDSHA E7DSL_HF E7DSL_LF E7DSL_Pr E7DSL_Pu E7ELE_HF E7ELE_LF E7ELE_Pr E7ELE_Pu E7GSL_LF E7GSL_Pr E7GSL_Pu E7HYD_HF E7HYD_Pu E7LPG_HF E7LPG_LF E7LPG_Pr E7LPG_Pu ETFREIGHT ETPASSENGER FHF_Trucks FLF_PickUpTrucks FPr_4WD FPr_LightDuty FPr_Minivan FPr_Moto FPu_Buses FPu_Micros FPu_Taxis FPu_Train HYDROGEN'.split()
emissions = 'Accidents CO2e_HeavyCargo C02e_Freigth CO2e_LightCargo CO2e_sources CO2e_Transport Congestion Health'.split()
timeslice = 'DRY RAIN'.split()
print(fuels)
print(len(fuels))
def csv_to_excel(input_csv, output_excel):
    # es para availabilityfactor (default value=1), capitalcost (default value=0.0001), fixedCost (dv=0), ResidualCapacity (dv=0)
    # para TotalAnnualMaxCapacity (dv=99999), TotalAnnualMinCapacity (dv=0), TotalTechnologyAnnualActivityLowerLimit (dv=0), VariableCost(dv=0.0001)
    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(input_csv)
    # Paso 2: Visualizar los datos originales
    # Especifica las columnas que deseas extraer
    #columnas_a_extraer = ['TECHNOLOGY', 'FUEL', 'YEAR']
    #columnas_a_extraer = ['TECHNOLOGY']
    # Crea un nuevo DataFrame con solo las columnas seleccionadas
    #df_seleccionado = df[columnas_a_extraer]
    # Especifica las condiciones para filtrar los datos
    filas = []
    default_value = 0.0001
    condicion_AÑO = df['YEAR'].isin(years) # busca los valores de la columna YEAR
    cont_row = 0
    for j in range(len(tecnologias)):
        condicion_TECH = df['TECHNOLOGY'] == tecnologias[j] # busca los valores de la columna TECHNOLOGY
        df_filtrado = df.loc[condicion_TECH & condicion_AÑO] # filtra entre tecnologia y año
        valores = df_filtrado.loc[:,'Value']
        if len(valores.values) == 0:
            val = [default_value for r in range(len(years))]
            # agrega el nombre de la tecnología como primer elemento de la fila y el valor por defecto como segundo elemento
            filas.append([tecnologias[j]]+val)
        else:
            filas.append([tecnologias[j]]+valores.values.tolist())
        cont_row += 1
    df_transpuesto = pd.DataFrame(filas, columns=['']+years, index=[x for x in range(cont_row)])
    df_transpuesto.to_excel(output_excel, index=False, header=False) # crea nueva archivo de excel con las nuevas filas
#################
def csv_to_excel_de(input_csv, output_excel):
    # sirve para specifiedAnnualDemand (dv=0)
    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(input_csv)
    filas = []
    default_value = 0
    condicion_AÑO = df['YEAR'].isin(years) # filtra por año
    cont_row = 0
    for j in range(len(fuels)):
        condicion_FUEL = df['FUEL'] == fuels[j] # filtra por FUEL
        df_filtrado = df.loc[condicion_FUEL & condicion_AÑO]
        valores = df_filtrado.loc[:,'Value']
        if len(valores.values) == 0:
            print(valores.values)
            val = [default_value for r in range(len(years))]
            filas.append([fuels[j]]+val)
        else:
            filas.append([fuels[j]]+valores.values.tolist())
        cont_row += 1
    df_transpuesto = pd.DataFrame(filas, columns=['']+years, index=[x for x in range(cont_row)])
    df_transpuesto.to_excel(output_excel, index=False, header=False)

#################3
def csv_to_excel_o(input_csv, output_excel):
    # es para InputActivityRatio (dv=0) y es para OutputActivityRatio (dv=0)
    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(input_csv)
    # Especifica las condiciones para filtrar los datos
    filas = []
    default_value = 0
    condicion_AÑO = df['YEAR'].isin(years) # filtra por YEAR
    cont_row = 0
    for j in range(len(tecnologias)):
        condicion_TECH = df['TECHNOLOGY'] == tecnologias[j] # filtra por TECHNOLOGY
        for f in range(len(fuels)):
            condicion_FUEL = df['FUEL'] == fuels[f] # filtra por FUEL
            df_filtrado = df.loc[condicion_TECH & condicion_FUEL & condicion_AÑO]
            valores = df_filtrado.loc[:,'Value']
            if len(valores.values) == 0:
                val = [default_value for r in range(len(years))]
                filas.append([tecnologias[j]]+[fuels[f]]+val)
            else:
                filas.append([tecnologias[j]]+[fuels[f]]+valores.values.tolist())
            cont_row += 1
    print('#######################')
    df_transpuesto = pd.DataFrame(filas, columns=['','']+years, index=[x for x in range(cont_row)])
    df_transpuesto.to_excel(output_excel, index=False, header=False)

####################

def csv_to_excel_em(input_csv, output_excel):
    # es para annualEmissionLimit (dv = 99999),  EmissionPenalty (dv=0)
    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(input_csv)
    # Especifica las condiciones para filtrar los datos
    filas = []
    default_value = 0
    condicion_AÑO = df['YEAR'].isin(years) # filtra por YEAR
    cont_row = 0
    for f in range(len(emissions)):
        condicion_EMISSION = df['EMISSION'] == emissions[f] # filtra por EMISSION
        df_filtrado = df.loc[condicion_EMISSION & condicion_AÑO]
        valores = df_filtrado.loc[:,'Value']
        if len(valores.values) == 0:
            val = [default_value for r in range(len(years))]
            filas.append([emissions[f]]+val)
        else:
            filas.append([emissions[f]]+valores.values.tolist())
        cont_row += 1
    print('#######################')
    print(len(filas))
    print(len(filas)==cont_row)
    df_transpuesto = pd.DataFrame(filas, columns=['']+years, index=[x for x in range(cont_row)])
    df_transpuesto.to_excel(output_excel, index=False, header=False)



####################
def csv_to_excel_e(input_csv, output_excel):
    # es para EmissionActvityRatio (dv=0),
    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(input_csv)
    # Especifica las condiciones para filtrar los datos
    filas = []
    default_value = 0
    condicion_AÑO = df['YEAR'].isin(years) # filtra por YEAR
    cont_row = 0
    for j in range(len(tecnologias)):
        condicion_TECH = df['TECHNOLOGY'] == tecnologias[j] # filtra por TECHNOLOGY
        for f in range(len(emissions)):
            condicion_EMISSION = df['EMISSION'] == emissions[f] #filtra por EMISSION
            df_filtrado = df.loc[condicion_TECH & condicion_EMISSION & condicion_AÑO]
            valores = df_filtrado.loc[:,'Value']
            if len(valores.values) == 0:
                val = [default_value for r in range(len(years))]
                filas.append([tecnologias[j]]+[emissions[f]]+val)
            else:
                filas.append([tecnologias[j]]+[emissions[f]]+valores.values.tolist())
            cont_row += 1
    print('#######################')
    df_transpuesto = pd.DataFrame(filas, columns=['','']+years, index=[x for x in range(cont_row)])
    df_transpuesto.to_excel(output_excel, index=False, header=False)

####################
def csv_to_excel_dr(input_csv, output_excel):
    # es para CapacityFactor (dEfault value 1)
    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(input_csv)
    # Especifica las condiciones para filtrar los datos
    filas = []
    default_value = 1
    condicion_AÑO = df['YEAR'].isin(years) # filtra por YEAR
    cont_row = 0
    for j in range(len(tecnologias)):
        condicion_TECH = df['TECHNOLOGY'] == tecnologias[j] # filtra por TECHNOLOGY
        for f in range(len(timeslice)):
            condicion_TIMESLICE = df['TIMESLICE'] == timeslice[f] # filtra por TIMESLICE
            df_filtrado = df.loc[condicion_TECH & condicion_TIMESLICE & condicion_AÑO]
            valores = df_filtrado.loc[:,'Value']
            if len(valores.values) == 0:
                #print(valores.values)
                val = [default_value for r in range(len(years))]
                #print(val)
                #print('largo: '+str(len(val)))
                filas.append([tecnologias[j]]+[timeslice[f]]+val)
            else:
                filas.append([tecnologias[j]]+[timeslice[f]]+valores.values.tolist())
            #print(filas[-1])
            cont_row += 1
    print('#######################')
    df_transpuesto = pd.DataFrame(filas, columns=['','']+years, index=[x for x in range(cont_row)])
    df_transpuesto.to_excel(output_excel, index=False, header=False)

##############
def csv_to_excel_dp(input_csv, output_excel):
    # sirve para SpecifiedDemandProfile (dv=0)
    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(input_csv)
    # Especifica las condiciones para filtrar los datos
    filas = []
    default_value = 0
    condicion_AÑO = df['YEAR'].isin(years) # filtra por YEAR
    cont_row = 0
    for j in range(len(fuels)):
        condicion_FUEL = df['FUEL'] == fuels[j] # filtra por FUEL 
        for f in range(len(timeslice)):
            condicion_TIMESLICE = df['TIMESLICE'] == timeslice[f] # filtra por TIMESLICE
            df_filtrado = df.loc[condicion_FUEL & condicion_TIMESLICE & condicion_AÑO]
            valores = df_filtrado.loc[:,'Value']
            if len(valores.values) == 0:
                #print(valores.values)
                val = [default_value for r in range(len(years))]
                filas.append([fuels[j]]+[timeslice[f]]+val)
            else:
                filas.append([fuels[j]]+[timeslice[f]]+valores.values.tolist())
            cont_row += 1
    print('#######################')
    df_transpuesto = pd.DataFrame(filas, columns=['','']+years, index=[x for x in range(cont_row)])
    df_transpuesto.to_excel(output_excel, index=False, header=False)
    
if __name__ == "__main__":
    # Reemplaza 'input.csv' con el nombre de tu archivo CSV de entrada
    # Las siguientes direcciones son adaptadas para el PC local y segun el nombre del archivo .csv deseado
    #input_csv = 'input.csv'
    ################ CASO 2-SR15 #############
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\AnnualEmissionLimit.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\AvailabilityFactor.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\CapacityFactor.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\CapacityToActivityUnit.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\CapitalCost.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\EmissionActivityRatio.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\EmissionsPenalty.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\FixedCost.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\InputActivityRatio.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\OutputActivityRatio.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\ResidualCapacity.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\SpecifiedAnnualDemand.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\SpecifiedDemandProfile.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\TotalAnnualMaxCapacity.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\TotalAnnualMinCapacity.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\TotalAnnualMinCapacityInvestment.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\TotalTechnologyAnnualActivityLowerLimit.csv'
    input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\2_SR15\VariableCost.csv'
    ################ CASO 1-SR25 #############
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\AnnualEmissionLimit.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\AvailabilityFactor.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\CapacityFactor.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\CapacityToActivityUnit.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\CapitalCost.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\EmissionActivityRatio.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\EmissionsPenalty.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\FixedCost.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\InputActivityRatio.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\OutputActivityRatio.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\ResidualCapacity.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\SpecifiedAnnualDemand.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\SpecifiedDemandProfile.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\TotalAnnualMaxCapacity.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\TotalAnnualMinCapacity.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\TotalAnnualMinCapacityInvestment.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\TotalTechnologyAnnualActivityLowerLimit.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\1_SR20\VariableCost.csv'
    ################ CASO 0-BAU #############
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\AvailabilityFactor.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\CapitalCost.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\EmissionActivityRatio.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\InputActivityRatio.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\CapacityFactor.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\SpecifiedAnnualDemand.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\SpecifiedDemandProfile.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\FixedCost.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\OutputActivityRatio.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\ResidualCapacity.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\TotalAnnualMaxCapacity.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\TotalAnnualMinCapacityInvestment.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\TotalTechnologyAnnualActivityLowerLimit.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\TotalTechnologyModelPeriodActivityUpperLimit.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\TotalTechnologyModelPeriodActivityUpperLimit.csv'
    #input_csv = r'C:\Users\HITES\Desktop\la uwu\Practica 2\OSeMOSYS-CR-master\CODE\1_Scenarios_Inputs\0_BAU\VariableCost.csv'
    
    # Reemplaza 'output.xlsx' con el nombre que desees para el archivo Excel de salida
    #output_excel = 'AnnualEmissionLimit_tr.xlsx'
    #output_excel = 'FixedCost_Tr.xlsx'
    #output_excel = 'OutputActivityRatio_tr.xlsx'
    #output_excel = 'InputActivityRatio_tr.xlsx'
    #output_excel = 'ResidualCapacity_tr.xlsx'
    #output_excel = 'TotalAnnualMaxCapacity_tr.xlsx'
    #output_excel = 'TotalAnnualMinCapacity_tr.xlsx'
    #output_excel = 'TotalAnnualMinCapacityInvestment_tr.xlsx'
    #output_excel = 'TotalTechnologyAnnualActivityLowerLimit_tr.xlsx'
    #output_excel = 'TotalTechnologyModelPeriodActivityUpperLimit_tr.xlsx'
    output_excel = 'VariableCost_tr.xlsx'
    #output_excel = 'AvailabilityFactor_tr.xlsx'
    #output_excel = 'CapitalCost_tr.xlsx'
    #output_excel = 'EmissionActivityRatio_tr.xlsx'
    #output_excel = 'EmissionsPenalty_tr.xlsx'
    #output_excel = 'CapacityFactor_tr.xlsx'
    #output_excel = 'CapacityToActivityUnity_tr.xlsx'
    #output_excel = 'SpecifiedAnnualDemand_tr.xlsx'
    #output_excel = 'SpecifiedDemandProfile_tr.xlsx'

    # Escoge la función especifica según el tipo de parámetro escogido
    csv_to_excel(input_csv, output_excel)
    #csv_to_excel_o(input_csv, output_excel)
    #csv_to_excel_em(input_csv, output_excel)
    #csv_to_excel_e(input_csv, output_excel)
    #csv_to_excel_dr(input_csv, output_excel)
    #csv_to_excel_de(input_csv, output_excel)
    #csv_to_excel_dp(input_csv, output_excel)

    print(f"Se ha creado el archivo {output_excel} con los datos transpuestos.")

