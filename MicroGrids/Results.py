# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mtick
#.extract_values()
def Load_results1(instance):
    '''
    This function loads the results that depend of the periods in to a 
    dataframe and creates a excel file with it.
    
    :param instance: The instance of the project resolution created by PYOMO.
    
    :return: A dataframe called Time_series with the values of the variables 
    that depend of the periods.    
    '''

#      Creation of an index starting in the 'model.StartDate' value with a frequency step equal to 'model.Delta_Time'
   
    if instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1.0) : # if the step is in hours and minutes
        foo = str(instance.Delta_Time()) # trasform the number into a string
        hour = foo[0] # Extract the first character
        minutes = str(int(float(foo[1:3])*60)) # Extrac the last two character
        index_values = pd.DatetimeIndex(instance.StartDate(), 
                                        periods=instance.t(), freq=(hour + 
                                        'h'+ minutes + 'min')) # Creation of an index with a start date and a frequency
    elif instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1): # if the step is in hours
        index_values = pd.DatetimeIndex(start=instance.StartDate(), 
                                        periods=instance.Periods(), 
                                        freq=(str(instance.Delta_Time()) + 'h')) # Creation of an index with a start date and a frequency
    else: # if the step is in minutes
        index_values = pd.DatetimeIndex(start=instance.StartDate(), 
                                        periods=instance.t(), 
                                        freq=(str(int(instance.Delta_Time()*60)) 
                                        + 'min'))# Creation of an index with a start date and a frequency
    
    Columns = []
    for i in range(1,instance.Number_Generator.extract_values()[None]+1):
        Columns.append('Generator_'+str(i)+'_'+str(1))
        Columns.append('Generator_'+str(i)+'_'+str(2))
    # Load the variables that depend of the periods in python dyctionarys a
    L_L = instance.Lost_Load.get_values()
    Pv = instance.Total_Energy_PV.get_values()
    Cu = instance.Energy_Curtailment.get_values()
    B_O = instance.Energy_Battery_Flow_Out.get_values() 
    B_I = instance.Energy_Battery_Flow_In.get_values()
    G_E = instance.Generator_Total_Period_Energy.get_values()
    De = instance.Energy_Demand.extract_values()
    soc = instance.State_Of_Charge_Battery.get_values()
    G_C = instance.Period_Total_Cost_Generator.get_values()
    
    for s in range(1,instance.Scenarios.extract_values()[None]+1):
        Lost_Load = []
        Energy_PV = []
        Curtailment = []
        Discharge_Energy = []
        Charge_Energy = []
        Generator_Energy = []
        Demand=[]
        SoC = [] 
        Generator_Cost = []
        for t in range(1,instance.Periods.extract_values()[None]+1):
#            for i in range(1, instance.Number_Generator.extract_values()[None]+1):
#                for j in range(1,3):
                    Lost_Load.append( L_L[s,t])
                    Energy_PV.append(Pv[s,t])
                    Curtailment.append(Cu[s,t])
                    Discharge_Energy.append(B_O[s,t])
                    Charge_Energy.append(B_I[s,t])
                    Generator_Energy.append(G_E[s,t])
                    Demand.append(De[s,t])
                    SoC.append(soc[s,t])
                    Generator_Cost.append(G_C[s,t])
        data = [Lost_Load,Energy_PV,Curtailment,Discharge_Energy,Charge_Energy,
                Generator_Energy, Demand, SoC,Generator_Cost] # Loading the values to a numpy array
        data = list(map(list, zip(*data)))
        Time_Series = pd.DataFrame(data ,columns=['Lost Load', 'Energy PV','Curtailment',
                                                  'Discharge energy from the Battery', 
                                                  'Charge energy to the Battery', 
                                                  'Energy Diesel',
                                                  'Energy_Demand',  
                                                  'State_Of_Charge_Battery',
                                                  'Generator Period Cost'],
                                                  index=index_values)
        
        Time_Series.to_excel('Results/Time_Series_+'+str(s) +'.xls') # Creating an excel file with the values of the variables that are in function of the periods
    
      
    Energy_Generator = instance.Generator_Energy_1.get_values()           
    Period_Cost_Generator= instance.Period_Cost_Generator_1.get_values() 
    
    Generator_Cost_Period = pd.DataFrame(index=index_values)
    Generator_Energy = pd.DataFrame(index=index_values)
    
    for s in range(1,instance.Scenarios.extract_values()[None]+1): 
        Generator_Cost_Period = pd.DataFrame(index=index_values)
        Generator_Energy = pd.DataFrame(index=index_values)
        
        for i in range(1, instance.Number_Generator.extract_values()[None]+1):
            for j in range(1, 3):
                Generator = []
                Period_Cost = []  
                for t in range(1,instance.Periods.extract_values()[None]+1):
                    Generator.append(Energy_Generator[(s,t,i,j)])
                    Period_Cost.append(Period_Cost_Generator[(s,t,i,j)])
                Generator_Cost_Period['S'+str(s) +' Gen '+str(i)+str(j)]=Generator
                Generator_Energy['S'+str(s) +' Gen '+str(i)+str(j)]=Period_Cost
    
    
        Generator_Cost_Period.to_excel('Results/Generator_Energy S'+str(s)+'.xls')
        Generator_Energy.to_excel('Results/Generators_Costs S'+str(s)+'.xls')
    
    index=[]
    for i in range(1, instance.Number_Generator.extract_values()[None]+1):
            for j in range(1, 3):
                index.append((i,j))
    
    
    cost_origins = instance.Cost_Origins.extract_values()
    Cost_Origins = pd.DataFrame(columns=['Origins'],index= index)
    for i in range(1, instance.Number_Generator.extract_values()[None]+1):
            for j in range(1, 3):
                Cost_Origins['Origins'][i,j]=cost_origins[i,j]
    Cost_Origins=Cost_Origins.transpose()
    Cost_Origins.to_excel('Results/Origins.xls')
     
    
    
    Percentage = instance.Scenario_Weight.extract_values()
    Scenario_Weight = pd.DataFrame(columns=['Scenario Weight'],index= range(1,
                                   instance.Scenarios.extract_values()[None]+1))
    for i in range(1,instance.Scenarios.extract_values()[None]+1):
        Scenario_Weight['Scenario Weight'][i] = Percentage[i]
    Scenario_Weight.to_excel('Results/Scenario Weight.xls')
    
    return Time_Series
    
    
    
    
def Load_results2(instance):
    '''
    This function extracts the unidimensional variables into a  data frame 
    and creates a excel file with this data
    
    :param instance: The instance of the project resolution created by PYOMO. 
    
    :return: Data frame called Size_variables with the variables values. 
    '''
    # Load the variables that doesnot depend of the periods in python dyctionarys
    ca = instance.Cost_Financial.get_values()
    cb = instance.PV_Units.get_values()
    cb = cb.values()
    cb=[list(cb)[0]*instance.PV_Nominal_Capacity.value]
    cc = instance.Battery_Nominal_Capacity.get_values()
    cd = [instance.Generator_Nominal_Capacity.value] 
    Number_Generators = instance.Integer_generator.get_values()
    Number_Generators = Number_Generators.values()
    Number_Generators=list(Number_Generators)
    cd= Number_Generators[0]*cd[0]
    NPC = instance.ObjectiveFuntion.expr()
    Mge_1 = instance.Marginal_Cost_Generator.extract_values()[1]
    Mge_2 = instance.Marginal_Cost_Generator.extract_values()[2]
    Funded= instance.Porcentage_Funded.value
    DiscountRate = instance.Discount_Rate.value
    InterestRate = instance.Interest_Rate_Loan.value
    PricePV = instance.PV_invesment_Cost.value
    PriceBatery= instance.Battery_Invesment_Cost.value
    PriceGenSet= instance.Generator_Invesment_Cost.value
    OM = instance.Maintenance_Operation_Cost_PV.value
    Years=instance.Years.value
    VOLL= instance.Value_Of_Lost_Load.value
    data3 = [ca[None], cb[0], cc[None], cd ,NPC,Mge_1 ,Mge_2,
            Funded,DiscountRate,InterestRate,PricePV,PriceBatery,
            PriceGenSet,OM,Years,VOLL] # Loading the values to a numpy array  
    Size_variables = pd.DataFrame(data3,index=['Amortization', 'Size of the solar panels', 
                                               'Size of the Battery',
                                               'Nominal Capacity Generator',
                                               'Net Present Cost','Marginal cost 1', 
                                               'Marginal cost 2', 'Funded Porcentage', 
                                               'Discount Rate', 'Interest Rate','Precio PV', 
                                               'Precio Bateria','Precio GenSet','OyM',
                                               'Project years','VOLL'])
    Size_variables.to_excel('Results/Size.xls') # Creating an excel file with the values of the variables that does not depend of the periods
    
    I_Inv = instance.Initial_Inversion.get_values()[None] 
    O_M = instance.Operation_Maintenance_Cost.get_values()[None] 
    Financial_Cost = instance.Total_Finalcial_Cost.get_values()[None] 
    Batt_Reposition = instance.Battery_Reposition_Cost.get_values()[None] 
    
    Data = [I_Inv, O_M, Financial_Cost,Batt_Reposition]
    Value_costs = pd.DataFrame(Data, index=['Initial Inversion', 'O & M',
                                            'Financial Cost', 'Battery reposition'])

    Value_costs.to_excel('Results/Partial Costs.xls')    


    VOLL = instance.Scenario_Lost_Load_Cost.get_values() 
    Scenario_Generator_Cost = instance.Sceneario_Generator_Total_Cost.get_values() 
    NPC_Scenario = instance.Scenario_Net_Present_Cost.get_values() 
    
    columns = ['VOLL', 'Scenario Generator Cost', 'NPC Scenario']
    scenarios= range(1,instance.Scenarios.extract_values()[None]+1)
    Scenario_Costs = pd.DataFrame(columns=columns, index=scenarios)
    
    
    for j in scenarios:
        Scenario_Costs['VOLL'][j]= VOLL[j] 
        Scenario_Costs['Scenario Generator Cost'][j]= Scenario_Generator_Cost[j]
        Scenario_Costs['NPC Scenario'][j]= NPC_Scenario[j]
    Scenario_Costs.to_excel('Results/Scenario Cost.xls')    
    
    return Size_variables

    
def Results_Analysis_3(instance):
    
    data_4 = instance.Generator_Nominal_Capacity.values()
    foo=instance.Binary_generator.get_values()
    for i in range(1,(len(instance.Generator_Nominal_Capacity.values()))+1):
        data_4.append(foo[i])
    data_5 = np.array(data_4)
    
    Generator_info = pd.DataFrame(data_5, index=['Cap 1', 'Cap 2', 'Cap 3', 'Bin 1', 'Bin 2', 'Bin 3'])
    Generator_info.to_excel('Results/Generator.xls')
    
    
def Plot_Energy_Total(instance, Time_Series):  
    '''
    This function creates a plot of the dispatch of energy of a defined number of days.
    
    :param instance: The instance of the project resolution created by PYOMO. 
    :param Time_series: The results of the optimization model that depend of the periods.
    
    
    '''
    Periods_Day = 24/instance.Delta_Time() # periods in a day
    for x in range(0, instance.Periods()): # Find the position form wich the plot will start in the Time_Series dataframe
        foo = pd.DatetimeIndex(start=instance.PlotDay(),periods=1,freq='1h') # Asign the start date of the graphic to a dumb variable
        if foo == Time_Series.index[x]: 
           Start_Plot = x # asign the value of x to the position where the plot will start 
    End_Plot = Start_Plot + instance.PlotTime()*Periods_Day # Create the end of the plot position inside the time_series
    Time_Series.index=range(1,8761)
    Plot_Data = Time_Series[Start_Plot:int(End_Plot)] # Extract the data between the start and end position from the Time_Series
    columns = pd.DatetimeIndex(start=instance.PlotDay(), periods=instance.PlotTime()*Periods_Day, freq=('1h'))    
    Plot_Data.index=columns
    
    
    Vec = pd.Series(Plot_Data['Energy PV'].values + Plot_Data['Energy Diesel'].values - Plot_Data['Curtailment'].values - Plot_Data['Charge energy to the Battery'].values , index=Plot_Data.index) # Create a vector with the sum of the diesel and solar energy
    Vec2 = pd.Series(Plot_Data['Energy_Demand'].values + Plot_Data['Curtailment'].values + Plot_Data['Charge energy to the Battery'].values, index=Plot_Data.index ) # Solar super plus of energy
    
    Vec3 = pd.Series(Vec.values + Plot_Data['Discharge energy from the Battery'].values, index=Plot_Data.index) # Substracction between the demand and energy discharge from the battery 
    Vec4 = -Plot_Data['Charge energy to the Battery'] # Creating a vector with the negative values of the energy going to the battery 
    Vec5 = pd.Series(Plot_Data['Energy_Demand'].values - Plot_Data['Lost Load'].values, index=Plot_Data.index)    
    
    ax1= Vec.plot(style='b-', linewidth=0.5) # Plot the line of the diesel energy plus the PV energy
    ax1.fill_between(Plot_Data.index, Plot_Data['Energy Diesel'].values, Vec.values,   alpha=0.3, color = 'b') # Fill the are of the energy produce by the energy of the PV
    ax2= Plot_Data['Energy Diesel'].plot(style='r', linewidth=0.5) # Plot the line of the diesel energy
    ax2.fill_between(Plot_Data.index, 0, Plot_Data['Energy Diesel'].values, alpha=0.2, color='r') # Fill the area of the energy produce by the diesel generator
    ax3= Plot_Data.Energy_Demand.plot(style='k-',linewidth=1) # Plot the line of the Energy_Demand
    ax3.fill_between(Plot_Data.index, Vec.values , Vec3.values, alpha=0.3, color='g') # Fill the area of the energy flowing out the battery
    ax5= Vec4.plot(style='m', linewidth=0.5) # Plot the line of the energy flowing into the battery
    ax5.fill_between(Plot_Data.index, 0, Vec4, alpha=0.3, color='m') # Fill the area of the energy flowing into the battery
    ax6= Plot_Data['State_Of_Charge_Battery'].plot(style='k--', secondary_y=True, linewidth=2, alpha=0.7 ) # Plot the line of the State of charge of the battery
    ax7= Vec2.plot(style='b-', linewidth=0.5) # Plot the line of PV energy that exceeds the demand
    ax7.fill_between(Plot_Data.index, Plot_Data['Energy_Demand'].values, Vec2.values,  alpha=0.3, color = 'b') # Fill the area between the demand and the curtailment energy
    ax3.fill_between(Plot_Data.index, Vec5 , Plot_Data['Energy_Demand'].values, alpha=0.3, color='y') 
    
    # Define name  and units of the axis
    ax1.set_ylabel('Power (W)')
    ax1.set_xlabel('Time (Hours)')
    ax6.set_ylabel('Battery State of charge (Wh)')
    
    # Define the legends of the plot
    From_PV = mpatches.Patch(color='blue',alpha=0.3, label='From PV')
    From_Generator = mpatches.Patch(color='red',alpha=0.3, label='From Generator')
    From_Battery = mpatches.Patch(color='green',alpha=0.5, label='From Battery')
    To_Battery = mpatches.Patch(color='magenta',alpha=0.5, label='To Battery')
    Lost_Load = mpatches.Patch(color='yellow', alpha= 0.3, label= 'Lost Load')
    Energy_Demand = mlines.Line2D([], [], color='black',label='Energy_Demand')
    State_Of_Charge_Battery = mlines.Line2D([], [], color='black',label='State_Of_Charge_Battery', linestyle='--',alpha=0.7)
    plt.legend(handles=[From_Generator, From_PV, From_Battery, To_Battery, Lost_Load, Energy_Demand, State_Of_Charge_Battery], bbox_to_anchor=(1.83, 1))
    plt.savefig('Results/Energy_Dispatch.png', bbox_inches='tight')    
    plt.show()    
    
def Percentage_Of_Use(Time_Series):
    '''
    This model creates a plot with the percentage of the time that each technologies is activate during the analized 
    time.
    :param Time_series: The results of the optimization model that depend of the periods.
    '''    
    
    # Creation of the technolgy dictonary    
    PercentageOfUse= {'Lost Load':0, 'Energy PV':0,'Curtailment':0, 'Energy Diesel':0, 'Discharge energy from the Battery':0, 'Charge energy to the Battery':0}
    
    # Count the quantity of times each technology has energy production
    for v in PercentageOfUse.keys():
        foo = 0
        for i in range(len(Time_Series)):
            if Time_Series[v][i]>0: 
                foo = foo + 1      
            PercentageOfUse[v] = (round((foo/float(len(Time_Series))), 3))*100 
    
    # Create the names in the plot
    c = ['From Generator', 'Curtailment', 'To Battery', 'From PV', 'From Battery', 'Lost Load']       
    
#     Create the bar plot  
    plt.figure()
    plt.bar((1,2,3,4,5,6), PercentageOfUse.values(), color= 'b', alpha=0.5, align='center')
   
    plt.xticks((1.2,2.2,3.2,4.2,5.2,6.2), c) # Put the names and position for the ticks in the x axis 
    plt.xticks(rotation=-30) # Rotate the ticks
    plt.xlabel('Technology') # Create a label for the x axis
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='on')
    plt.ylabel('Percentage of use (%)') # Create a label for the y axis
    plt.savefig('Results/Percentge_of_Use.png', bbox_inches='tight') # Save the plot 
    plt.show() 
    
    return PercentageOfUse
    
def Energy_Flow(Time_Series):


    Energy_Flow = {'Energy_Demand':0, 'Lost Load':0, 'Energy PV':0,'Curtailment':0, 'Energy Diesel':0, 'Discharge energy from the Battery':0, 'Charge energy to the Battery':0}

    for v in Energy_Flow.keys():
        if v == 'Energy PV':
            Energy_Flow[v] = round((Time_Series[v].sum() - Time_Series['Curtailment'].sum()- Time_Series['Charge energy to the Battery'].sum())/1000000, 2)
        else:
            Energy_Flow[v] = round((Time_Series[v].sum())/1000000, 2)
          
    
    c = ['From Generator', 'To Battery', 'Demand', 'From PV', 'From Battery', 'Curtailment', 'Lost Load']       
    plt.figure()    
    plt.bar((1,2,3,4,5,6,7), Energy_Flow.values(), color= 'b', alpha=0.3, align='center')
    
    plt.xticks((1.2,2.2,3.2,4.2,5.2,6.2,7.2), c)
    plt.xlabel('Technology')
    plt.ylabel('Energy Flow (MWh)')
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='on')
    plt.xticks(rotation=-30)
    plt.savefig('Results/Energy_Flow.png', bbox_inches='tight')
    plt.show()    
    
    return Energy_Flow

def Energy_Participation(Energy_Flow):
    
    Energy_Participation = {'Energy PV':0, 'Energy Diesel':0, 'Discharge energy from the Battery':0, 'Lost Load':0}
    c = {'Energy Diesel':'Diesel Generator', 'Discharge energy from the Battery':'Battery', 'Energy PV':'From PV', 'Lost Load':'Lost Load'}       
    labels=[]
    
    for v in Energy_Participation.keys():
        if Energy_Flow[v]/Energy_Flow['Energy_Demand'] >= 0.001:
            Energy_Participation[v] = Energy_Flow[v]/Energy_Flow['Energy_Demand']
            labels.append(c[v])
        else:
            del Energy_Participation[v]
    Colors=['r','c','b','k']
    
    plt.figure()                     
    plt.pie(Energy_Participation.values(), autopct='%1.1f%%', colors=Colors)
    
    Handles = []
    for t in range(len(labels)):
        Handles.append(mpatches.Patch(color=Colors[t], alpha=1, label=labels[t]))
    
    plt.legend(handles=Handles, bbox_to_anchor=(1.4, 1))   
    plt.savefig('Results/Energy_Participation.png', bbox_inches='tight')
    plt.show()
    
    return Energy_Participation

def LDR(Time_Series):

    columns=['Consume diesel', 'Lost Load', 'Energy PV','Curtailment','Energy Diesel', 
             'Discharge energy from the Battery', 'Charge energy to the Battery', 
             'Energy_Demand',  'State_Of_Charge_Battery'  ]
    Sort_Values = Time_Series.sort('Energy_Demand', ascending=False)
    
    index_values = []
    
    for i in range(len(Time_Series)):
        index_values.append((i+1)/float(len(Time_Series))*100)
    
    Sort_Values = pd.DataFrame(Sort_Values.values/1000, columns=columns, index=index_values)
    
    plt.figure() 
    ax = Sort_Values['Energy_Demand'].plot(style='k-',linewidth=1)
    
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    xticks = mtick.FormatStrFormatter(fmt)
    ax.xaxis.set_major_formatter(xticks)
    ax.set_ylabel('Load (kWh)')
    ax.set_xlabel('Percentage (%)')
    
    plt.savefig('Results/LDR.png', bbox_inches='tight')
    plt.show()    
    
