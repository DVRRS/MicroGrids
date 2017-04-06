
from pyomo.opt import SolverFactory

from pyomo.environ import Objective, minimize, Constraint
from Constraints import  Net_Present_Cost, Solar_Energy, State_of_Charge,\
Maximun_Charge, Minimun_Charge, Max_Power_Battery_Charge, Max_Power_Battery_Discharge, Max_Bat_in, Max_Bat_out,  \
Financial_Cost, Energy_balance, Maximun_Lost_Load, Generators_Binary_Constraint, \
Generator_Cost_1, Energy_Genarator_Energy_Max, Generator_Total_Period_Energy, \
Period_Total_Cost_Generator,Total_Cost_Generator,Generator_Bounds_Min,\
Generator_Bounds_Max, Initial_Inversion, Operation_Maintenance_Cost,Total_Finalcial_Cost,\
Battery_Reposition_Cost, Scenario_Lost_Load_Cost, Sceneario_Generator_Total_Cost,Scenario_Net_Present_Cost, Generator_rampling_limits_down, Generator_rampling_limits_up


def Model_Resolution(model):   
    '''
    This function creates the model and call Pyomo to solve the instance of the proyect 
    
    :param model: Pyomo model as defined in the Model_creation library
    
    :return: The solution inside an object call instance.
    '''
    # OBJETIVE FUNTION:
    model.ObjectiveFuntion = Objective(rule=Net_Present_Cost, sense=minimize)  
    
    # CONSTRAINTS
    #Energy constraints
    model.EnergyBalance = Constraint(model.scenario,model.periods, rule=Energy_balance)  # Energy balance
    model.MaximunLostLoad = Constraint(model.scenario,rule=Maximun_Lost_Load) # Maximum permissible lost load
    # PV constraints
    model.SolarEnergy = Constraint(model.scenario,model.periods, rule=Solar_Energy)  # Energy output of the solar panels
    # Battery constraints
    model.StateOfCharge = Constraint(model.scenario,model.periods, rule=State_of_Charge) # State of Charge of the battery
    model.MaximunCharge = Constraint(model.scenario,model.periods, rule=Maximun_Charge) # Maximun state of charge of the Battery
    model.MinimunCharge = Constraint(model.scenario,model.periods, rule=Minimun_Charge) # Minimun state of charge
#    model.MaxPowerBatteryCharge = Constraint(rule=Max_Power_Battery_Charge)  # Max power battery charge constraint
#    model.MaxPowerBatteryDischarge = Constraint(rule=Max_Power_Battery_Discharge)    # Max power battery discharge constraint
#    model.MaxBatIn = Constraint(model.scenario,model.periods, rule=Max_Bat_in) # Minimun flow of energy for the charge fase
#    model.Maxbatout = Constraint(model.scenario,model.periods, rule=Max_Bat_out) #minimun flow of energy for the discharge fase
    # Diesel Generator constraints
    model.PeriodTotalCostGenerator = Constraint(model.scenario,model.periods, rule=Period_Total_Cost_Generator)
    
    model.GeneratorsBinaryConstraint = Constraint(model.scenario,model.periods, rule=Generators_Binary_Constraint)
    
    model.GeneratorBoundsMin = Constraint(model.scenario,model.periods, model.Generators, model.Slops, rule=Generator_Bounds_Min)
    model.GeneratorBoundsMax = Constraint(model.scenario,model.periods, model.Generators, model.Slops, rule=Generator_Bounds_Max)
    
    model.GeneratorCost1 = Constraint(model.scenario,model.periods, model.Generators, model.Slops, rule=Generator_Cost_1)

    model.EnergyGenaratorEnergyMax = Constraint(model.scenario,model.periods, rule=Energy_Genarator_Energy_Max)
    model.TotalCostGenerator = Constraint(model.scenario,rule=Total_Cost_Generator)
    model.GeneratorTotalPeriodEnergy = Constraint(model.scenario,model.periods, rule=Generator_Total_Period_Energy)
#    model.Generatorramplinglimitsdown =  Constraint(model.scenario,model.periods, rule=Generator_rampling_limits_down)  
#    model.Generatorramplinglimitsup = Constraint(model.scenario,model.periods, rule=Generator_rampling_limits_up) 
#    
#    
    # Financial Constraints
    model.FinancialCost = Constraint(rule=Financial_Cost) # Financial cost
    model.InitialInversion = Constraint(rule=Initial_Inversion)
    model.OperationMaintenanceCost = Constraint(rule=Operation_Maintenance_Cost)
    model.TotalFinalcialCost = Constraint(rule=Total_Finalcial_Cost)
    model.BatteryRepositionCost = Constraint(rule=Battery_Reposition_Cost) 
    model.ScenarioLostLoadCost = Constraint(model.scenario, rule=Scenario_Lost_Load_Cost)
    model.ScenearioGeneratorTotalCost = Constraint(model.scenario, rule=Sceneario_Generator_Total_Cost)
    model.ScenarioNetPresentCost = Constraint(model.scenario, rule=Scenario_Net_Present_Cost) 
    
    
    instance = model.create_instance("Example/data.dat") # load parameters       
    opt = SolverFactory('cplex') # Solver use during the optimization    
    opt.options['emphasis_memory'] = 'y'
#    opt.options['node_select'] = 3
    results = opt.solve(instance, tee=True,options_string="mipgap=0.15") # Solving a model instance 

    #    instance.write(io_options={'emphasis_memory':True})
    #options_string="mipgap=0.03", timelimit=1200
    instance.solutions.load_from(results) # Loading solution into instance
    return instance