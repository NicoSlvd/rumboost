import biogeme.database as db
import biogeme.biogeme as bio
from biogeme.expressions import Beta
from biogeme.models import loglogit
import biogeme.logging as blog
import pandas as pd

def SwissMetro(dataset_train: pd.DataFrame):
    '''
    Create a MNL on the swissmetro dataset.

    Parameters
    ----------
    dataset_train : pandas DataFrame
        The training dataset.

    Returns
    -------
    biogeme : bio.BIOGEME
        The BIOGEME object containing the model.
    '''
    database_train = db.Database('swissmetro_train', dataset_train)

    globals().update(database_train.variables)

    #parameters to be estimated
    ASC_CAR   = Beta('ASC_CAR', 0, None, None, 0)
    ASC_SM    = Beta('ASC_SM',  0, None, None, 0)
    ASC_TRAIN = Beta('ASC_SBB', 0, None, None, 1)

    B_TIME = Beta('B_TIME', 0, None, 0, 0)
    B_COST = Beta('B_COST', 0, None, 0, 0)
    B_HE   = Beta('B_HE',   0, None, 0, 0)

    #utilities
    V_TRAIN = ASC_TRAIN + B_TIME * TRAIN_TT + B_COST * TRAIN_COST + B_HE * TRAIN_HE
    V_SM    = ASC_SM    + B_TIME * SM_TT    + B_COST * SM_COST    + B_HE * SM_HE
    V_CAR   = ASC_CAR   + B_TIME * CAR_TT   + B_COST * CAR_CO

    V = {0: V_TRAIN, 1: V_SM, 2: V_CAR}
    av = {0: 1, 1: 1, 2: 1}

    #choice model
    logprob = loglogit(V, av, CHOICE)
    biogeme = bio.BIOGEME(database_train, logprob)
    biogeme.modelName = "SwissmetroMNL"

    biogeme.generate_html = False
    biogeme.generate_pickle = False

    return biogeme

def LPMC(dataset_train):
    '''
    Create a MNL on the LPMC dataset.
    The model is a slightly modified version from teh code that can be found here: https://github.com/JoseAngelMartinB/prediction-behavioural-analysis-ml-travel-mode-choice.

    Parameters
    ----------
    dataset_train : pandas DataFrame
        The training dataset.

    Returns
    -------
    biogeme : bio.BIOGEME
        The BIOGEME object containing the model.

    '''
    database_train = db.Database('LTDS_train', dataset_train)

    logger = blog.get_screen_logger(level=blog.DEBUG)
    logger.info('Model LTDS.py')

    globals().update(database_train.variables)

    #several model specifications are available below - the best one is the uncommented one.

    #best model until now, 0.6790 with lr = 0.3
    MNL_beta_params_positive = ['B_car_ownership_Car', 'B_driving_license_Car']
    MNL_beta_params_negative = ['B_dur_walking_Walk',  'B_dur_cycling_Bike', 'B_dur_pt_access_Public_Transport', 'B_dur_pt_rail_Public_Transport', 'B_dur_pt_bus_Public_Transport', 'B_dur_pt_int_waiting_Public_Transport', 'B_dur_pt_int_walking_Public_Transport', 'B_pt_n_interchanges_Public_Transport', 'B_cost_transit_Public_Transport', 'B_dur_driving_Car', 'B_cost_driving_total_Car', 'B_distance_Walk', 'B_distance_Bike', 'B_distance_Public_Transport', 'B_distance_Car']#, 'B_traffic_perc_Car']
    MNL_beta_params_neutral = ['ASC_Bike', 'ASC_Public_Transport', 'ASC_Car', 'B_car_ownership_Walk', 'B_car_ownership_Bike', 'B_car_ownership_Public_Transport', 'B_driving_license_Walk', 'B_driving_license_Bike', 'B_driving_license_Public_Transport', 'B_age_Walk', 'B_age_Bike', 'B_age_Public_Transport', 'B_age_Car', 'B_female_Walk', 'B_female_Bike', 'B_female_Public_Transport', 'B_female_Car', 'B_day_of_week_Walk', 'B_day_of_week_Bike', 'B_day_of_week_Public_Transport', 'B_day_of_week_Car', 'B_start_time_linear_Walk', 'B_start_time_linear_Bike', 'B_start_time_linear_Public_Transport', 'B_start_time_linear_Car', 'B_purpose_B_Walk', 'B_purpose_B_Bike', 'B_purpose_B_Public_Transport', 'B_purpose_B_Car', 'B_purpose_HBE_Walk', 'B_purpose_HBE_Bike', 'B_purpose_HBE_Public_Transport', 'B_purpose_HBE_Car', 'B_purpose_HBO_Walk', 'B_purpose_HBO_Bike', 'B_purpose_HBO_Public_Transport', 'B_purpose_HBO_Car', 'B_purpose_HBW_Walk', 'B_purpose_HBW_Bike', 'B_purpose_HBW_Public_Transport', 'B_purpose_HBW_Car', 'B_purpose_NHBO_Walk', 'B_purpose_NHBO_Bike', 'B_purpose_NHBO_Public_Transport', 'B_purpose_NHBO_Car', 'B_fueltype_Avrg_Walk', 'B_fueltype_Avrg_Bike', 'B_fueltype_Avrg_Public_Transport', 'B_fueltype_Avrg_Car', 'B_fueltype_Diesel_Walk', 'B_fueltype_Diesel_Bike', 'B_fueltype_Diesel_Public_Transport', 'B_fueltype_Diesel_Car', 'B_fueltype_Hybrid_Walk', 'B_fueltype_Hybrid_Bike', 'B_fueltype_Hybrid_Public_Transport', 'B_fueltype_Hybrid_Car', 'B_fueltype_Petrol_Walk', 'B_fueltype_Petrol_Bike', 'B_fueltype_Petrol_Public_Transport', 'B_fueltype_Petrol_Car'] 

    MNL_utilities = {0: 'B_age_Walk*age + B_female_Walk*female + B_day_of_week_Walk*day_of_week + B_start_time_linear_Walk*start_time_linear + B_car_ownership_Walk*car_ownership + B_driving_license_Walk*driving_license + B_purpose_B_Walk*purpose_B + B_purpose_HBE_Walk*purpose_HBE + B_purpose_HBO_Walk*purpose_HBO + B_purpose_HBW_Walk*purpose_HBW + B_purpose_NHBO_Walk*purpose_NHBO + B_fueltype_Avrg_Walk*fueltype_Average + B_fueltype_Diesel_Walk*fueltype_Diesel + B_fueltype_Hybrid_Walk*fueltype_Hybrid + B_fueltype_Petrol_Walk*fueltype_Petrol + B_distance_Walk*distance + B_dur_walking_Walk*dur_walking',
                        1: 'ASC_Bike + B_age_Bike*age + B_female_Bike*female + B_day_of_week_Bike*day_of_week + B_start_time_linear_Bike*start_time_linear + B_car_ownership_Bike*car_ownership + B_driving_license_Bike*driving_license + B_purpose_B_Bike*purpose_B + B_purpose_HBE_Bike*purpose_HBE + B_purpose_HBO_Bike*purpose_HBO + B_purpose_HBW_Bike*purpose_HBW + B_purpose_NHBO_Bike*purpose_NHBO + B_fueltype_Avrg_Bike*fueltype_Average + B_fueltype_Diesel_Bike*fueltype_Diesel + B_fueltype_Hybrid_Bike*fueltype_Hybrid + B_fueltype_Petrol_Bike*fueltype_Petrol + B_distance_Bike*distance + B_dur_cycling_Bike*dur_cycling',
                        2: 'ASC_Public_Transport + B_age_Public_Transport*age + B_female_Public_Transport*female + B_day_of_week_Public_Transport*day_of_week + B_start_time_linear_Public_Transport*start_time_linear + B_car_ownership_Public_Transport*car_ownership + B_driving_license_Public_Transport*driving_license + B_purpose_B_Public_Transport*purpose_B + B_purpose_HBE_Public_Transport*purpose_HBE + B_purpose_HBO_Public_Transport*purpose_HBO + B_purpose_HBW_Public_Transport*purpose_HBW + B_purpose_NHBO_Public_Transport*purpose_NHBO + B_fueltype_Avrg_Public_Transport*fueltype_Average + B_fueltype_Diesel_Public_Transport*fueltype_Diesel + B_fueltype_Hybrid_Public_Transport*fueltype_Hybrid + B_fueltype_Petrol_Public_Transport*fueltype_Petrol + B_distance_Public_Transport*distance + B_dur_pt_access_Public_Transport*dur_pt_access + B_dur_pt_rail_Public_Transport*dur_pt_rail + B_dur_pt_bus_Public_Transport*dur_pt_bus + B_dur_pt_int_waiting_Public_Transport*dur_pt_int_waiting + B_dur_pt_int_walking_Public_Transport*dur_pt_int_walking + B_pt_n_interchanges_Public_Transport*pt_n_interchanges + B_cost_transit_Public_Transport*cost_transit',
                        3: 'ASC_Car + B_age_Car*age + B_female_Car*female + B_day_of_week_Car*day_of_week + B_start_time_linear_Car*start_time_linear + B_car_ownership_Car*car_ownership + B_driving_license_Car*driving_license + B_purpose_B_Car*purpose_B + B_purpose_HBE_Car*purpose_HBE + B_purpose_HBO_Car*purpose_HBO + B_purpose_HBW_Car*purpose_HBW + B_purpose_NHBO_Car*purpose_NHBO + B_fueltype_Avrg_Car*fueltype_Average + B_fueltype_Diesel_Car*fueltype_Diesel + B_fueltype_Hybrid_Car*fueltype_Hybrid + B_fueltype_Petrol_Car*fueltype_Petrol + B_distance_Car*distance + B_dur_driving_Car*dur_driving + B_cost_driving_total_Car*cost_driving_total'}

    #0.6805
    # MNL_beta_params_positive = ['B_car_ownership_Car', 'B_driving_license_Car']
    # MNL_beta_params_negative = ['B_age_Bike', 'B_distance_Bike', 'B_distance_Public_Transport', 'B_distance_Car','B_driving_license_Public_Transport', 'B_car_ownership_Bike', 'B_car_ownership_Public_Transport', 'B_driving_license_Bike', 'B_dur_walking_Walk', 'B_dur_cycling_Bike', 'B_dur_pt_access_Public_Transport', 'B_dur_pt_rail_Public_Transport', 'B_dur_pt_bus_Public_Transport', 'B_dur_pt_int_waiting_Public_Transport', 'B_dur_pt_int_walking_Public_Transport', 'B_pt_n_interchanges_Public_Transport', 'B_cost_transit_Public_Transport', 'B_dur_driving_Car', 'B_cost_driving_total_Car']
    # MNL_beta_params_neutral = ['ASC_Bike', 'ASC_Public_Transport', 'ASC_Car', 'B_age_Public_Transport', 'B_age_Car', 'B_female_Bike', 'B_female_Public_Transport', 'B_female_Car', 'B_day_of_week_Bike', 'B_day_of_week_Public_Transport', 'B_day_of_week_Car', 'B_start_time_linear_Bike', 'B_start_time_linear_Public_Transport', 'B_start_time_linear_Car', 'B_purpose_B_Bike', 'B_purpose_B_Public_Transport', 'B_purpose_B_Car', 'B_purpose_HBE_Bike', 'B_purpose_HBE_Public_Transport', 'B_purpose_HBE_Car', 'B_purpose_HBO_Bike', 'B_purpose_HBO_Public_Transport', 'B_purpose_HBO_Car', 'B_purpose_HBW_Bike', 'B_purpose_HBW_Public_Transport', 'B_purpose_HBW_Car', 'B_purpose_NHBO_Bike', 'B_purpose_NHBO_Public_Transport', 'B_purpose_NHBO_Car','B_fueltype_Avrg_Bike', 'B_fueltype_Avrg_Public_Transport', 'B_fueltype_Avrg_Car', 'B_fueltype_Diesel_Bike', 'B_fueltype_Diesel_Public_Transport', 'B_fueltype_Diesel_Car', 'B_fueltype_Hybrid_Bike', 'B_fueltype_Hybrid_Public_Transport', 'B_fueltype_Hybrid_Car', 'B_fueltype_Petrol_Bike', 'B_fueltype_Petrol_Public_Transport', 'B_fueltype_Petrol_Car']

    # MNL_utilities = {0: 'B_dur_walking_Walk*dur_walking',
    #                  1: 'ASC_Bike + B_age_Bike*age + B_female_Bike*female + B_day_of_week_Bike*day_of_week + B_start_time_linear_Bike*start_time_linear + B_car_ownership_Bike*car_ownership + B_driving_license_Bike*driving_license + B_purpose_B_Bike*purpose_B + B_purpose_HBE_Bike*purpose_HBE + B_purpose_HBO_Bike*purpose_HBO + B_purpose_HBW_Bike*purpose_HBW + B_purpose_NHBO_Bike*purpose_NHBO + B_fueltype_Avrg_Bike*fueltype_Average + B_fueltype_Diesel_Bike*fueltype_Diesel + B_fueltype_Hybrid_Bike*fueltype_Hybrid + B_fueltype_Petrol_Bike*fueltype_Petrol + B_distance_Bike*distance + B_dur_cycling_Bike*dur_cycling',
    #                  2: 'ASC_Public_Transport + B_age_Public_Transport*age + B_female_Public_Transport*female + B_day_of_week_Public_Transport*day_of_week + B_start_time_linear_Public_Transport*start_time_linear + B_car_ownership_Public_Transport*car_ownership + B_driving_license_Public_Transport*driving_license + B_purpose_B_Public_Transport*purpose_B + B_purpose_HBE_Public_Transport*purpose_HBE + B_purpose_HBO_Public_Transport*purpose_HBO + B_purpose_HBW_Public_Transport*purpose_HBW + B_purpose_NHBO_Public_Transport*purpose_NHBO + B_fueltype_Avrg_Public_Transport*fueltype_Average + B_fueltype_Diesel_Public_Transport*fueltype_Diesel + B_fueltype_Hybrid_Public_Transport*fueltype_Hybrid + B_fueltype_Petrol_Public_Transport*fueltype_Petrol + B_dur_pt_access_Public_Transport*dur_pt_access + B_dur_pt_rail_Public_Transport*dur_pt_rail + B_dur_pt_bus_Public_Transport*dur_pt_bus + B_dur_pt_int_waiting_Public_Transport*dur_pt_int_waiting + B_dur_pt_int_walking_Public_Transport*dur_pt_int_walking + B_pt_n_interchanges_Public_Transport*pt_n_interchanges + B_cost_transit_Public_Transport*cost_transit + B_distance_Public_Transport*distance',
    #                  3: 'ASC_Car + B_age_Car*age + B_female_Car*female + B_day_of_week_Car*day_of_week + B_start_time_linear_Car*start_time_linear + B_car_ownership_Car*car_ownership + B_driving_license_Car*driving_license + B_purpose_B_Car*purpose_B + B_purpose_HBE_Car*purpose_HBE + B_purpose_HBO_Car*purpose_HBO + B_purpose_HBW_Car*purpose_HBW + B_purpose_NHBO_Car*purpose_NHBO + B_fueltype_Avrg_Car*fueltype_Average + B_fueltype_Diesel_Car*fueltype_Diesel + B_fueltype_Hybrid_Car*fueltype_Hybrid + B_fueltype_Petrol_Car*fueltype_Petrol + B_dur_driving_Car*dur_driving + B_cost_driving_total_Car*cost_driving_total + B_distance_Car*distance'}

    # 0.6791 but misspecification
    # MNL_beta_params_positive = ['B_car_ownership_Car', 'B_driving_license_Car']
    # MNL_beta_params_negative = ['B_dur_walking_Walk',  'B_dur_cycling_Bike', 'B_dur_pt_access_Public_Transport', 'B_dur_pt_rail_Public_Transport', 'B_dur_pt_bus_Public_Transport', 'B_dur_pt_int_waiting_Public_Transport', 'B_dur_pt_int_walking_Public_Transport', 'B_pt_n_interchanges_Public_Transport', 'B_cost_transit_Public_Transport', 'B_dur_driving_Car', 'B_cost_driving_total_Car']#, 'B_traffic_perc_Car']
    # MNL_beta_params_neutral = ['ASC_Bike', 'ASC_Public_Transport', 'ASC_Car', 'B_car_ownership_Walk', 'B_car_ownership_Bike', 'B_car_ownership_Public_Transport', 'B_driving_license_Walk', 'B_driving_license_Bike', 'B_driving_license_Public_Transport', 'B_age_Walk', 'B_age_Bike', 'B_age_Public_Transport', 'B_age_Car', 'B_female_Walk', 'B_female_Bike', 'B_female_Public_Transport', 'B_female_Car', 'B_distance_Walk', 'B_distance_Bike', 'B_day_of_week_Walk', 'B_day_of_week_Bike', 'B_day_of_week_Public_Transport', 'B_day_of_week_Car', 'B_start_time_linear_Walk', 'B_start_time_linear_Bike', 'B_start_time_linear_Public_Transport', 'B_start_time_linear_Car', 'B_purpose_B_Walk', 'B_purpose_B_Bike', 'B_purpose_B_Public_Transport', 'B_purpose_B_Car', 'B_purpose_HBE_Walk', 'B_purpose_HBE_Bike', 'B_purpose_HBE_Public_Transport', 'B_purpose_HBE_Car', 'B_purpose_HBO_Walk', 'B_purpose_HBO_Bike', 'B_purpose_HBO_Public_Transport', 'B_purpose_HBO_Car', 'B_purpose_HBW_Walk', 'B_purpose_HBW_Bike', 'B_purpose_HBW_Public_Transport', 'B_purpose_HBW_Car', 'B_purpose_NHBO_Walk', 'B_purpose_NHBO_Bike', 'B_purpose_NHBO_Public_Transport', 'B_purpose_NHBO_Car', 'B_fueltype_Avrg_Walk', 'B_fueltype_Avrg_Bike', 'B_fueltype_Avrg_Public_Transport', 'B_fueltype_Avrg_Car', 'B_fueltype_Diesel_Walk', 'B_fueltype_Diesel_Bike', 'B_fueltype_Diesel_Public_Transport', 'B_fueltype_Diesel_Car', 'B_fueltype_Hybrid_Walk', 'B_fueltype_Hybrid_Bike', 'B_fueltype_Hybrid_Public_Transport', 'B_fueltype_Hybrid_Car', 'B_fueltype_Petrol_Walk', 'B_fueltype_Petrol_Bike', 'B_fueltype_Petrol_Public_Transport', 'B_fueltype_Petrol_Car'] 

    # MNL_utilities = {0: 'B_age_Walk*age + B_female_Walk*female + B_day_of_week_Walk*day_of_week + B_start_time_linear_Walk*start_time_linear + B_car_ownership_Walk*car_ownership + B_driving_license_Walk*driving_license + B_purpose_B_Walk*purpose_B + B_purpose_HBE_Walk*purpose_HBE + B_purpose_HBO_Walk*purpose_HBO + B_purpose_HBW_Walk*purpose_HBW + B_purpose_NHBO_Walk*purpose_NHBO + B_fueltype_Avrg_Walk*fueltype_Average + B_fueltype_Diesel_Walk*fueltype_Diesel + B_fueltype_Hybrid_Walk*fueltype_Hybrid + B_fueltype_Petrol_Walk*fueltype_Petrol + B_distance_Walk*distance + B_dur_walking_Walk*dur_walking',
    #                  1: 'ASC_Bike + B_age_Bike*age + B_female_Bike*female + B_day_of_week_Bike*day_of_week + B_start_time_linear_Bike*start_time_linear + B_car_ownership_Bike*car_ownership + B_driving_license_Bike*driving_license + B_purpose_B_Bike*purpose_B + B_purpose_HBE_Bike*purpose_HBE + B_purpose_HBO_Bike*purpose_HBO + B_purpose_HBW_Bike*purpose_HBW + B_purpose_NHBO_Bike*purpose_NHBO + B_fueltype_Avrg_Bike*fueltype_Average + B_fueltype_Diesel_Bike*fueltype_Diesel + B_fueltype_Hybrid_Bike*fueltype_Hybrid + B_fueltype_Petrol_Bike*fueltype_Petrol + B_distance_Bike*distance + B_dur_cycling_Bike*dur_cycling',
    #                  2: 'ASC_Public_Transport + B_age_Public_Transport*age + B_female_Public_Transport*female + B_day_of_week_Public_Transport*day_of_week + B_start_time_linear_Public_Transport*start_time_linear + B_car_ownership_Public_Transport*car_ownership + B_driving_license_Public_Transport*driving_license + B_purpose_B_Public_Transport*purpose_B + B_purpose_HBE_Public_Transport*purpose_HBE + B_purpose_HBO_Public_Transport*purpose_HBO + B_purpose_HBW_Public_Transport*purpose_HBW + B_purpose_NHBO_Public_Transport*purpose_NHBO + B_fueltype_Avrg_Public_Transport*fueltype_Average + B_fueltype_Diesel_Public_Transport*fueltype_Diesel + B_fueltype_Hybrid_Public_Transport*fueltype_Hybrid + B_fueltype_Petrol_Public_Transport*fueltype_Petrol + B_dur_pt_access_Public_Transport*dur_pt_access + B_dur_pt_rail_Public_Transport*dur_pt_rail + B_dur_pt_bus_Public_Transport*dur_pt_bus + B_dur_pt_int_waiting_Public_Transport*dur_pt_int_waiting + B_dur_pt_int_walking_Public_Transport*dur_pt_int_walking + B_pt_n_interchanges_Public_Transport*pt_n_interchanges + B_cost_transit_Public_Transport*cost_transit',
    #                  3: 'ASC_Car + B_age_Car*age + B_female_Car*female + B_day_of_week_Car*day_of_week + B_start_time_linear_Car*start_time_linear + B_car_ownership_Car*car_ownership + B_driving_license_Car*driving_license + B_purpose_B_Car*purpose_B + B_purpose_HBE_Car*purpose_HBE + B_purpose_HBO_Car*purpose_HBO + B_purpose_HBW_Car*purpose_HBW + B_purpose_NHBO_Car*purpose_NHBO + B_fueltype_Avrg_Car*fueltype_Average + B_fueltype_Diesel_Car*fueltype_Diesel + B_fueltype_Hybrid_Car*fueltype_Hybrid + B_fueltype_Petrol_Car*fueltype_Petrol + B_dur_driving_Car*dur_driving + B_cost_driving_total_Car*cost_driving_total'}

    # 0.6796
    # MNL_beta_params_positive = ['B_car_ownership_Car', 'B_driving_license_Car']
    # MNL_beta_params_negative = ['B_dur_walking_Walk',  'B_dur_cycling_Bike', 'B_dur_pt_access_Public_Transport', 'B_dur_pt_rail_Public_Transport', 'B_dur_pt_bus_Public_Transport', 'B_dur_pt_int_waiting_Public_Transport', 'B_dur_pt_int_walking_Public_Transport', 'B_pt_n_interchanges_Public_Transport', 'B_cost_transit_Public_Transport', 'B_dur_driving_Car', 'B_cost_driving_total_Car']#, 'B_traffic_perc_Car']
    # MNL_beta_params_neutral = ['ASC_Bike', 'ASC_Public_Transport', 'ASC_Car', 'B_car_ownership_Walk', 'B_car_ownership_Bike', 'B_car_ownership_Public_Transport', 'B_driving_license_Walk', 'B_driving_license_Bike', 'B_driving_license_Public_Transport', 'B_age_Walk', 'B_age_Bike', 'B_age_Public_Transport', 'B_age_Car', 'B_female_Walk', 'B_female_Bike', 'B_female_Public_Transport', 'B_female_Car', 'B_distance_Walk', 'B_distance_Bike', 'B_distance_Public_Transport', 'B_distance_Car', 'B_day_of_week_Walk', 'B_day_of_week_Bike', 'B_day_of_week_Public_Transport', 'B_day_of_week_Car', 'B_start_time_linear_Walk', 'B_start_time_linear_Bike', 'B_start_time_linear_Public_Transport', 'B_start_time_linear_Car', 'B_purpose_B_Walk', 'B_purpose_B_Bike', 'B_purpose_B_Public_Transport', 'B_purpose_B_Car', 'B_purpose_HBE_Walk', 'B_purpose_HBE_Bike', 'B_purpose_HBE_Public_Transport', 'B_purpose_HBE_Car', 'B_purpose_HBO_Walk', 'B_purpose_HBO_Bike', 'B_purpose_HBO_Public_Transport', 'B_purpose_HBO_Car', 'B_purpose_HBW_Walk', 'B_purpose_HBW_Bike', 'B_purpose_HBW_Public_Transport', 'B_purpose_HBW_Car', 'B_purpose_NHBO_Walk', 'B_purpose_NHBO_Bike', 'B_purpose_NHBO_Public_Transport', 'B_purpose_NHBO_Car', 'B_fueltype_Avrg_Walk', 'B_fueltype_Avrg_Bike', 'B_fueltype_Avrg_Public_Transport', 'B_fueltype_Avrg_Car', 'B_fueltype_Diesel_Walk', 'B_fueltype_Diesel_Bike', 'B_fueltype_Diesel_Public_Transport', 'B_fueltype_Diesel_Car', 'B_fueltype_Hybrid_Walk', 'B_fueltype_Hybrid_Bike', 'B_fueltype_Hybrid_Public_Transport', 'B_fueltype_Hybrid_Car', 'B_fueltype_Petrol_Walk', 'B_fueltype_Petrol_Bike', 'B_fueltype_Petrol_Public_Transport', 'B_fueltype_Petrol_Car'] 

    # MNL_utilities = {0: 'B_age_Walk*age + B_female_Walk*female + B_day_of_week_Walk*day_of_week + B_start_time_linear_Walk*start_time_linear + B_car_ownership_Walk*car_ownership + B_driving_license_Walk*driving_license + B_purpose_B_Walk*purpose_B + B_purpose_HBE_Walk*purpose_HBE + B_purpose_HBO_Walk*purpose_HBO + B_purpose_HBW_Walk*purpose_HBW + B_purpose_NHBO_Walk*purpose_NHBO + B_fueltype_Avrg_Walk*fueltype_Average + B_fueltype_Diesel_Walk*fueltype_Diesel + B_fueltype_Hybrid_Walk*fueltype_Hybrid + B_fueltype_Petrol_Walk*fueltype_Petrol + B_distance_Walk*distance + B_dur_walking_Walk*dur_walking',
    #                  1: 'ASC_Bike + B_age_Bike*age + B_female_Bike*female + B_day_of_week_Bike*day_of_week + B_start_time_linear_Bike*start_time_linear + B_car_ownership_Bike*car_ownership + B_driving_license_Bike*driving_license + B_purpose_B_Bike*purpose_B + B_purpose_HBE_Bike*purpose_HBE + B_purpose_HBO_Bike*purpose_HBO + B_purpose_HBW_Bike*purpose_HBW + B_purpose_NHBO_Bike*purpose_NHBO + B_fueltype_Avrg_Bike*fueltype_Average + B_fueltype_Diesel_Bike*fueltype_Diesel + B_fueltype_Hybrid_Bike*fueltype_Hybrid + B_fueltype_Petrol_Bike*fueltype_Petrol + B_distance_Bike*distance + B_dur_cycling_Bike*dur_cycling',
    #                  2: 'ASC_Public_Transport + B_age_Public_Transport*age + B_female_Public_Transport*female + B_day_of_week_Public_Transport*day_of_week + B_start_time_linear_Public_Transport*start_time_linear + B_car_ownership_Public_Transport*car_ownership + B_driving_license_Public_Transport*driving_license + B_purpose_B_Public_Transport*purpose_B + B_purpose_HBE_Public_Transport*purpose_HBE + B_purpose_HBO_Public_Transport*purpose_HBO + B_purpose_HBW_Public_Transport*purpose_HBW + B_purpose_NHBO_Public_Transport*purpose_NHBO + B_fueltype_Avrg_Public_Transport*fueltype_Average + B_fueltype_Diesel_Public_Transport*fueltype_Diesel + B_fueltype_Hybrid_Public_Transport*fueltype_Hybrid + B_fueltype_Petrol_Public_Transport*fueltype_Petrol + B_distance_Public_Transport*distance + B_dur_pt_access_Public_Transport*dur_pt_access + B_dur_pt_rail_Public_Transport*dur_pt_rail + B_dur_pt_bus_Public_Transport*dur_pt_bus + B_dur_pt_int_waiting_Public_Transport*dur_pt_int_waiting + B_dur_pt_int_walking_Public_Transport*dur_pt_int_walking + B_pt_n_interchanges_Public_Transport*pt_n_interchanges + B_cost_transit_Public_Transport*cost_transit',
    #                  3: 'ASC_Car + B_age_Car*age + B_female_Car*female + B_day_of_week_Car*day_of_week + B_start_time_linear_Car*start_time_linear + B_car_ownership_Car*car_ownership + B_driving_license_Car*driving_license + B_purpose_B_Car*purpose_B + B_purpose_HBE_Car*purpose_HBE + B_purpose_HBO_Car*purpose_HBO + B_purpose_HBW_Car*purpose_HBW + B_purpose_NHBO_Car*purpose_NHBO + B_fueltype_Avrg_Car*fueltype_Average + B_fueltype_Diesel_Car*fueltype_Diesel + B_fueltype_Hybrid_Car*fueltype_Hybrid + B_fueltype_Petrol_Car*fueltype_Petrol + B_distance_Car*distance + B_dur_driving_Car*dur_driving + B_cost_driving_total_Car*cost_driving_total'}

    # 0.6789 with lr 0.3 --- change with above model; B_age_Bike and B_age_Walk in negative mono, got rid of driving license in cycling, got rid of fueltype in other features than car, got rid of car ownership in walk
    # MNL_beta_params_positive = ['B_car_ownership_Car', 'B_driving_license_Car']
    # MNL_beta_params_negative = ['B_age_Walk', 'B_age_Bike', 'B_dur_walking_Walk',  'B_dur_cycling_Bike', 'B_dur_pt_access_Public_Transport', 'B_dur_pt_rail_Public_Transport', 'B_dur_pt_bus_Public_Transport', 'B_dur_pt_int_waiting_Public_Transport', 'B_dur_pt_int_walking_Public_Transport', 'B_pt_n_interchanges_Public_Transport', 'B_cost_transit_Public_Transport', 'B_dur_driving_Car', 'B_cost_driving_total_Car', 'B_distance_Walk', 'B_distance_Bike', 'B_distance_Public_Transport', 'B_distance_Car']#, 'B_traffic_perc_Car']
    # MNL_beta_params_neutral = ['ASC_Bike', 'ASC_Public_Transport', 'ASC_Car', 'B_car_ownership_Bike', 'B_car_ownership_Public_Transport', 'B_driving_license_Walk', 'B_driving_license_Public_Transport', 'B_age_Public_Transport', 'B_age_Car', 'B_female_Walk', 'B_female_Bike', 'B_female_Public_Transport', 'B_female_Car', 'B_day_of_week_Walk', 'B_day_of_week_Bike', 'B_day_of_week_Public_Transport', 'B_day_of_week_Car', 'B_start_time_linear_Walk', 'B_start_time_linear_Bike', 'B_start_time_linear_Public_Transport', 'B_start_time_linear_Car', 'B_purpose_B_Walk', 'B_purpose_B_Bike', 'B_purpose_B_Public_Transport', 'B_purpose_B_Car', 'B_purpose_HBE_Walk', 'B_purpose_HBE_Bike', 'B_purpose_HBE_Public_Transport', 'B_purpose_HBE_Car', 'B_purpose_HBO_Walk', 'B_purpose_HBO_Bike', 'B_purpose_HBO_Public_Transport', 'B_purpose_HBO_Car', 'B_purpose_HBW_Walk', 'B_purpose_HBW_Bike', 'B_purpose_HBW_Public_Transport', 'B_purpose_HBW_Car', 'B_purpose_NHBO_Walk', 'B_purpose_NHBO_Bike', 'B_purpose_NHBO_Public_Transport', 'B_purpose_NHBO_Car', 'B_fueltype_Avrg_Car', 'B_fueltype_Diesel_Car', 'B_fueltype_Hybrid_Car', 'B_fueltype_Petrol_Car'] 

    # MNL_utilities = {0: 'B_age_Walk*age + B_female_Walk*female + B_day_of_week_Walk*day_of_week + B_start_time_linear_Walk*start_time_linear + B_driving_license_Walk*driving_license + B_purpose_B_Walk*purpose_B + B_purpose_HBE_Walk*purpose_HBE + B_purpose_HBO_Walk*purpose_HBO + B_purpose_HBW_Walk*purpose_HBW + B_purpose_NHBO_Walk*purpose_NHBO + B_distance_Walk*distance + B_dur_walking_Walk*dur_walking',
    #                  1: 'ASC_Bike + B_age_Bike*age + B_female_Bike*female + B_day_of_week_Bike*day_of_week + B_start_time_linear_Bike*start_time_linear + B_car_ownership_Bike*car_ownership + B_purpose_B_Bike*purpose_B + B_purpose_HBE_Bike*purpose_HBE + B_purpose_HBO_Bike*purpose_HBO + B_purpose_HBW_Bike*purpose_HBW + B_purpose_NHBO_Bike*purpose_NHBO + B_distance_Bike*distance + B_dur_cycling_Bike*dur_cycling',
    #                  2: 'ASC_Public_Transport + B_age_Public_Transport*age + B_female_Public_Transport*female + B_day_of_week_Public_Transport*day_of_week + B_start_time_linear_Public_Transport*start_time_linear + B_car_ownership_Public_Transport*car_ownership + B_driving_license_Public_Transport*driving_license + B_purpose_B_Public_Transport*purpose_B + B_purpose_HBE_Public_Transport*purpose_HBE + B_purpose_HBO_Public_Transport*purpose_HBO + B_purpose_HBW_Public_Transport*purpose_HBW + B_purpose_NHBO_Public_Transport*purpose_NHBO + B_distance_Public_Transport*distance + B_dur_pt_access_Public_Transport*dur_pt_access + B_dur_pt_rail_Public_Transport*dur_pt_rail + B_dur_pt_bus_Public_Transport*dur_pt_bus + B_dur_pt_int_waiting_Public_Transport*dur_pt_int_waiting + B_dur_pt_int_walking_Public_Transport*dur_pt_int_walking + B_pt_n_interchanges_Public_Transport*pt_n_interchanges + B_cost_transit_Public_Transport*cost_transit',
    #                  3: 'ASC_Car + B_age_Car*age + B_female_Car*female + B_day_of_week_Car*day_of_week + B_start_time_linear_Car*start_time_linear + B_car_ownership_Car*car_ownership + B_driving_license_Car*driving_license + B_purpose_B_Car*purpose_B + B_purpose_HBE_Car*purpose_HBE + B_purpose_HBO_Car*purpose_HBO + B_purpose_HBW_Car*purpose_HBW + B_purpose_NHBO_Car*purpose_NHBO + B_fueltype_Avrg_Car*fueltype_Average + B_fueltype_Diesel_Car*fueltype_Diesel + B_fueltype_Hybrid_Car*fueltype_Hybrid + B_fueltype_Petrol_Car*fueltype_Petrol + B_distance_Car*distance + B_dur_driving_Car*dur_driving + B_cost_driving_total_Car*cost_driving_total'}

    # 0.6789 with lr 0.3 --- change with above model; got rid of start time linear
    # MNL_beta_params_positive = ['B_car_ownership_Car', 'B_driving_license_Car']
    # MNL_beta_params_negative = ['B_age_Walk', 'B_age_Bike', 'B_dur_walking_Walk',  'B_dur_cycling_Bike', 'B_dur_pt_access_Public_Transport', 'B_dur_pt_rail_Public_Transport', 'B_dur_pt_bus_Public_Transport', 'B_dur_pt_int_waiting_Public_Transport', 'B_dur_pt_int_walking_Public_Transport', 'B_pt_n_interchanges_Public_Transport', 'B_cost_transit_Public_Transport', 'B_dur_driving_Car', 'B_cost_driving_total_Car', 'B_distance_Walk', 'B_distance_Bike', 'B_distance_Public_Transport', 'B_distance_Car']#, 'B_traffic_perc_Car']
    # MNL_beta_params_neutral = ['ASC_Bike', 'ASC_Public_Transport', 'ASC_Car', 'B_car_ownership_Bike', 'B_car_ownership_Public_Transport', 'B_driving_license_Walk', 'B_driving_license_Public_Transport', 'B_age_Public_Transport', 'B_age_Car', 'B_female_Walk', 'B_female_Bike', 'B_female_Public_Transport', 'B_female_Car', 'B_day_of_week_Walk', 'B_day_of_week_Bike', 'B_day_of_week_Public_Transport', 'B_day_of_week_Car', 'B_purpose_B_Walk', 'B_purpose_B_Bike', 'B_purpose_B_Public_Transport', 'B_purpose_B_Car', 'B_purpose_HBE_Walk', 'B_purpose_HBE_Bike', 'B_purpose_HBE_Public_Transport', 'B_purpose_HBE_Car', 'B_purpose_HBO_Walk', 'B_purpose_HBO_Bike', 'B_purpose_HBO_Public_Transport', 'B_purpose_HBO_Car', 'B_purpose_HBW_Walk', 'B_purpose_HBW_Bike', 'B_purpose_HBW_Public_Transport', 'B_purpose_HBW_Car', 'B_purpose_NHBO_Walk', 'B_purpose_NHBO_Bike', 'B_purpose_NHBO_Public_Transport', 'B_purpose_NHBO_Car', 'B_fueltype_Avrg_Car', 'B_fueltype_Diesel_Car', 'B_fueltype_Hybrid_Car', 'B_fueltype_Petrol_Car'] 

    # MNL_utilities = {0: 'B_age_Walk*age + B_female_Walk*female + B_day_of_week_Walk*day_of_week + B_driving_license_Walk*driving_license + B_purpose_B_Walk*purpose_B + B_purpose_HBE_Walk*purpose_HBE + B_purpose_HBO_Walk*purpose_HBO + B_purpose_HBW_Walk*purpose_HBW + B_purpose_NHBO_Walk*purpose_NHBO + B_distance_Walk*distance + B_dur_walking_Walk*dur_walking',
    #                  1: 'ASC_Bike + B_age_Bike*age + B_female_Bike*female + B_day_of_week_Bike*day_of_week + B_car_ownership_Bike*car_ownership + B_purpose_B_Bike*purpose_B + B_purpose_HBE_Bike*purpose_HBE + B_purpose_HBO_Bike*purpose_HBO + B_purpose_HBW_Bike*purpose_HBW + B_purpose_NHBO_Bike*purpose_NHBO + B_distance_Bike*distance + B_dur_cycling_Bike*dur_cycling',
    #                  2: 'ASC_Public_Transport + B_age_Public_Transport*age + B_female_Public_Transport*female + B_day_of_week_Public_Transport*day_of_week + B_car_ownership_Public_Transport*car_ownership + B_driving_license_Public_Transport*driving_license + B_purpose_B_Public_Transport*purpose_B + B_purpose_HBE_Public_Transport*purpose_HBE + B_purpose_HBO_Public_Transport*purpose_HBO + B_purpose_HBW_Public_Transport*purpose_HBW + B_purpose_NHBO_Public_Transport*purpose_NHBO + B_distance_Public_Transport*distance + B_dur_pt_access_Public_Transport*dur_pt_access + B_dur_pt_rail_Public_Transport*dur_pt_rail + B_dur_pt_bus_Public_Transport*dur_pt_bus + B_dur_pt_int_waiting_Public_Transport*dur_pt_int_waiting + B_dur_pt_int_walking_Public_Transport*dur_pt_int_walking + B_pt_n_interchanges_Public_Transport*pt_n_interchanges + B_cost_transit_Public_Transport*cost_transit',
    #                  3: 'ASC_Car + B_age_Car*age + B_female_Car*female + B_day_of_week_Car*day_of_week + B_car_ownership_Car*car_ownership + B_driving_license_Car*driving_license + B_purpose_B_Car*purpose_B + B_purpose_HBE_Car*purpose_HBE + B_purpose_HBO_Car*purpose_HBO + B_purpose_HBW_Car*purpose_HBW + B_purpose_NHBO_Car*purpose_NHBO + B_fueltype_Avrg_Car*fueltype_Average + B_fueltype_Diesel_Car*fueltype_Diesel + B_fueltype_Hybrid_Car*fueltype_Hybrid + B_fueltype_Petrol_Car*fueltype_Petrol + B_distance_Car*distance + B_dur_driving_Car*dur_driving + B_cost_driving_total_Car*cost_driving_total'}


    #with travel month and traffic percentage
    # MNL_beta_params_positive = ['B_car_ownership_Car', 'B_driving_license_Car']
    # MNL_beta_params_negative = ['B_dur_walking_Walk',  'B_dur_cycling_Bike', 'B_dur_pt_access_Public_Transport', 'B_dur_pt_rail_Public_Transport', 'B_dur_pt_bus_Public_Transport', 'B_dur_pt_int_waiting_Public_Transport', 'B_dur_pt_int_walking_Public_Transport', 'B_pt_n_interchanges_Public_Transport', 'B_cost_transit_Public_Transport', 'B_dur_driving_Car', 'B_cost_driving_total_Car', 'B_traffic_perc_Car']
    # MNL_beta_params_neutral = ['ASC_Bike', 'ASC_Public_Transport', 'ASC_Car', 'B_car_ownership_Walk', 'B_car_ownership_Bike', 'B_car_ownership_Public_Transport', 'B_driving_license_Walk', 'B_driving_license_Bike', 'B_driving_license_Public_Transport', 'B_age_Walk', 'B_age_Bike', 'B_age_Public_Transport', 'B_age_Car', 'B_female_Walk', 'B_female_Bike', 'B_female_Public_Transport', 'B_female_Car', 'B_distance_Walk', 'B_distance_Bike', 'B_distance_Public_Transport', 'B_distance_Car', 'B_day_of_week_Walk', 'B_day_of_week_Bike', 'B_day_of_week_Public_Transport', 'B_day_of_week_Car', 'B_start_time_linear_Walk', 'B_start_time_linear_Bike', 'B_start_time_linear_Public_Transport', 'B_start_time_linear_Car', 'B_purpose_B_Walk', 'B_purpose_B_Bike', 'B_purpose_B_Public_Transport', 'B_purpose_B_Car', 'B_purpose_HBE_Walk', 'B_purpose_HBE_Bike', 'B_purpose_HBE_Public_Transport', 'B_purpose_HBE_Car', 'B_purpose_HBO_Walk', 'B_purpose_HBO_Bike', 'B_purpose_HBO_Public_Transport', 'B_purpose_HBO_Car', 'B_purpose_HBW_Walk', 'B_purpose_HBW_Bike', 'B_purpose_HBW_Public_Transport', 'B_purpose_HBW_Car', 'B_purpose_NHBO_Walk', 'B_purpose_NHBO_Bike', 'B_purpose_NHBO_Public_Transport', 'B_purpose_NHBO_Car', 'B_fueltype_Avrg_Walk', 'B_fueltype_Avrg_Bike', 'B_fueltype_Avrg_Public_Transport', 'B_fueltype_Avrg_Car', 'B_fueltype_Diesel_Walk', 'B_fueltype_Diesel_Bike', 'B_fueltype_Diesel_Public_Transport', 'B_fueltype_Diesel_Car', 'B_fueltype_Hybrid_Walk', 'B_fueltype_Hybrid_Bike', 'B_fueltype_Hybrid_Public_Transport', 'B_fueltype_Hybrid_Car', 'B_fueltype_Petrol_Walk', 'B_fueltype_Petrol_Bike', 'B_fueltype_Petrol_Public_Transport', 'B_fueltype_Petrol_Car', 'B_travel_month_Walk', 'B_travel_month_Bike', 'B_travel_month_Public_Transport', 'B_travel_month_Car']

    # MNL_utilities = {0: 'B_travel_month_Walk*travel_month + B_age_Walk*age + B_female_Walk*female + B_day_of_week_Walk*day_of_week + B_start_time_linear_Walk*start_time_linear + B_car_ownership_Walk*car_ownership + B_driving_license_Walk*driving_license + B_purpose_B_Walk*purpose_B + B_purpose_HBE_Walk*purpose_HBE + B_purpose_HBO_Walk*purpose_HBO + B_purpose_HBW_Walk*purpose_HBW + B_purpose_NHBO_Walk*purpose_NHBO + B_fueltype_Avrg_Walk*fueltype_Average + B_fueltype_Diesel_Walk*fueltype_Diesel + B_fueltype_Hybrid_Walk*fueltype_Hybrid + B_fueltype_Petrol_Walk*fueltype_Petrol + B_distance_Walk*distance + B_dur_walking_Walk*dur_walking',
    #                  1: 'ASC_Bike + B_travel_month_Bike*travel_month + B_age_Bike*age + B_female_Bike*female + B_day_of_week_Bike*day_of_week + B_start_time_linear_Bike*start_time_linear + B_car_ownership_Bike*car_ownership + B_driving_license_Bike*driving_license + B_purpose_B_Bike*purpose_B + B_purpose_HBE_Bike*purpose_HBE + B_purpose_HBO_Bike*purpose_HBO + B_purpose_HBW_Bike*purpose_HBW + B_purpose_NHBO_Bike*purpose_NHBO + B_fueltype_Avrg_Bike*fueltype_Average + B_fueltype_Diesel_Bike*fueltype_Diesel + B_fueltype_Hybrid_Bike*fueltype_Hybrid + B_fueltype_Petrol_Bike*fueltype_Petrol + B_distance_Bike*distance + B_dur_cycling_Bike*dur_cycling',
    #                  2: 'ASC_Public_Transport + B_travel_month_Public_Transport*travel_month + B_age_Public_Transport*age + B_female_Public_Transport*female + B_day_of_week_Public_Transport*day_of_week + B_start_time_linear_Public_Transport*start_time_linear + B_car_ownership_Public_Transport*car_ownership + B_driving_license_Public_Transport*driving_license + B_purpose_B_Public_Transport*purpose_B + B_purpose_HBE_Public_Transport*purpose_HBE + B_purpose_HBO_Public_Transport*purpose_HBO + B_purpose_HBW_Public_Transport*purpose_HBW + B_purpose_NHBO_Public_Transport*purpose_NHBO + B_fueltype_Avrg_Public_Transport*fueltype_Average + B_fueltype_Diesel_Public_Transport*fueltype_Diesel + B_fueltype_Hybrid_Public_Transport*fueltype_Hybrid + B_fueltype_Petrol_Public_Transport*fueltype_Petrol + B_distance_Public_Transport*distance + B_dur_pt_access_Public_Transport*dur_pt_access + B_dur_pt_rail_Public_Transport*dur_pt_rail + B_dur_pt_bus_Public_Transport*dur_pt_bus + B_dur_pt_int_waiting_Public_Transport*dur_pt_int_waiting + B_dur_pt_int_walking_Public_Transport*dur_pt_int_walking + B_pt_n_interchanges_Public_Transport*pt_n_interchanges + B_cost_transit_Public_Transport*cost_transit',
    #                  3: 'ASC_Car + B_travel_month_Car*travel_month + B_traffic_perc_Car*driving_traffic_percent + B_age_Car*age + B_female_Car*female + B_day_of_week_Car*day_of_week + B_start_time_linear_Car*start_time_linear + B_car_ownership_Car*car_ownership + B_driving_license_Car*driving_license + B_purpose_B_Car*purpose_B + B_purpose_HBE_Car*purpose_HBE + B_purpose_HBO_Car*purpose_HBO + B_purpose_HBW_Car*purpose_HBW + B_purpose_NHBO_Car*purpose_NHBO + B_fueltype_Avrg_Car*fueltype_Average + B_fueltype_Diesel_Car*fueltype_Diesel + B_fueltype_Hybrid_Car*fueltype_Hybrid + B_fueltype_Petrol_Car*fueltype_Petrol + B_distance_Car*distance + B_dur_driving_Car*dur_driving + B_cost_driving_total_Car*cost_driving_total'}

    #market segmentation with weekend
    # MNL_beta_params_positive = ['B_car_ownership_Car', 'B_driving_license_Car']
    # MNL_beta_params_negative = ['B_dur_walking_Walk',  'B_dur_cycling_Bike', 'B_dur_pt_access_Public_Transport', 'B_dur_pt_rail_Public_Transport', 'B_dur_pt_bus_Public_Transport', 'B_dur_pt_int_waiting_Public_Transport', 'B_dur_pt_int_walking_Public_Transport', 'B_pt_n_interchanges_Public_Transport', 'B_cost_transit_Public_Transport', 'B_dur_driving_Car', 'B_cost_driving_total_Car', 'B_distance_Walk', 'B_distance_Bike', 'B_distance_Public_Transport', 'B_distance_Car']#, 'B_traffic_perc_Car']
    # MNL_beta_params_neutral = ['ASC_Bike', 'ASC_Public_Transport', 'ASC_Car', 'B_car_ownership_Walk', 'B_car_ownership_Bike', 'B_car_ownership_Public_Transport', 'B_driving_license_Walk', 'B_driving_license_Bike', 'B_driving_license_Public_Transport', 'B_age_Walk', 'B_age_Bike', 'B_age_Public_Transport', 'B_age_Car', 'B_female_Walk', 'B_female_Bike', 'B_female_Public_Transport', 'B_female_Car', 'B_weekend_Walk', 'B_weekend_Bike', 'B_weekend_Public_Transport', 'B_weekend_Car', 'B_start_time_linear_Walk', 'B_start_time_linear_Bike', 'B_start_time_linear_Public_Transport', 'B_start_time_linear_Car', 'B_purpose_B_Walk', 'B_purpose_B_Bike', 'B_purpose_B_Public_Transport', 'B_purpose_B_Car', 'B_purpose_HBE_Walk', 'B_purpose_HBE_Bike', 'B_purpose_HBE_Public_Transport', 'B_purpose_HBE_Car', 'B_purpose_HBO_Walk', 'B_purpose_HBO_Bike', 'B_purpose_HBO_Public_Transport', 'B_purpose_HBO_Car', 'B_purpose_HBW_Walk', 'B_purpose_HBW_Bike', 'B_purpose_HBW_Public_Transport', 'B_purpose_HBW_Car', 'B_purpose_NHBO_Walk', 'B_purpose_NHBO_Bike', 'B_purpose_NHBO_Public_Transport', 'B_purpose_NHBO_Car', 'B_fueltype_Avrg_Walk', 'B_fueltype_Avrg_Bike', 'B_fueltype_Avrg_Public_Transport', 'B_fueltype_Avrg_Car', 'B_fueltype_Diesel_Walk', 'B_fueltype_Diesel_Bike', 'B_fueltype_Diesel_Public_Transport', 'B_fueltype_Diesel_Car', 'B_fueltype_Hybrid_Walk', 'B_fueltype_Hybrid_Bike', 'B_fueltype_Hybrid_Public_Transport', 'B_fueltype_Hybrid_Car', 'B_fueltype_Petrol_Walk', 'B_fueltype_Petrol_Bike', 'B_fueltype_Petrol_Public_Transport', 'B_fueltype_Petrol_Car'] 

    # MNL_utilities = {0: 'B_age_Walk*age + B_female_Walk*female + B_weekend_Walk*weekend + B_start_time_linear_Walk*start_time_linear + B_car_ownership_Walk*car_ownership + B_driving_license_Walk*driving_license + B_purpose_B_Walk*purpose_B + B_purpose_HBE_Walk*purpose_HBE + B_purpose_HBO_Walk*purpose_HBO + B_purpose_HBW_Walk*purpose_HBW + B_purpose_NHBO_Walk*purpose_NHBO + B_fueltype_Avrg_Walk*fueltype_Average + B_fueltype_Diesel_Walk*fueltype_Diesel + B_fueltype_Hybrid_Walk*fueltype_Hybrid + B_fueltype_Petrol_Walk*fueltype_Petrol + B_distance_Walk*distance + B_dur_walking_Walk*dur_walking',
    #                  1: 'ASC_Bike + B_age_Bike*age + B_female_Bike*female + B_weekend_Bike*weekend + B_start_time_linear_Bike*start_time_linear + B_car_ownership_Bike*car_ownership + B_driving_license_Bike*driving_license + B_purpose_B_Bike*purpose_B + B_purpose_HBE_Bike*purpose_HBE + B_purpose_HBO_Bike*purpose_HBO + B_purpose_HBW_Bike*purpose_HBW + B_purpose_NHBO_Bike*purpose_NHBO + B_fueltype_Avrg_Bike*fueltype_Average + B_fueltype_Diesel_Bike*fueltype_Diesel + B_fueltype_Hybrid_Bike*fueltype_Hybrid + B_fueltype_Petrol_Bike*fueltype_Petrol + B_distance_Bike*distance + B_dur_cycling_Bike*dur_cycling',
    #                  2: 'ASC_Public_Transport + B_age_Public_Transport*age + B_female_Public_Transport*female + B_weekend_Public_Transport*weekend + B_start_time_linear_Public_Transport*start_time_linear + B_car_ownership_Public_Transport*car_ownership + B_driving_license_Public_Transport*driving_license + B_purpose_B_Public_Transport*purpose_B + B_purpose_HBE_Public_Transport*purpose_HBE + B_purpose_HBO_Public_Transport*purpose_HBO + B_purpose_HBW_Public_Transport*purpose_HBW + B_purpose_NHBO_Public_Transport*purpose_NHBO + B_fueltype_Avrg_Public_Transport*fueltype_Average + B_fueltype_Diesel_Public_Transport*fueltype_Diesel + B_fueltype_Hybrid_Public_Transport*fueltype_Hybrid + B_fueltype_Petrol_Public_Transport*fueltype_Petrol + B_distance_Public_Transport*distance + B_dur_pt_access_Public_Transport*dur_pt_access + B_dur_pt_rail_Public_Transport*dur_pt_rail + B_dur_pt_bus_Public_Transport*dur_pt_bus + B_dur_pt_int_waiting_Public_Transport*dur_pt_int_waiting + B_dur_pt_int_walking_Public_Transport*dur_pt_int_walking + B_pt_n_interchanges_Public_Transport*pt_n_interchanges + B_cost_transit_Public_Transport*cost_transit',
    #                  3: 'ASC_Car + B_age_Car*age + B_female_Car*female + B_weekend_Car*weekend + B_start_time_linear_Car*start_time_linear + B_car_ownership_Car*car_ownership + B_driving_license_Car*driving_license + B_purpose_B_Car*purpose_B + B_purpose_HBE_Car*purpose_HBE + B_purpose_HBO_Car*purpose_HBO + B_purpose_HBW_Car*purpose_HBW + B_purpose_NHBO_Car*purpose_NHBO + B_fueltype_Avrg_Car*fueltype_Average + B_fueltype_Diesel_Car*fueltype_Diesel + B_fueltype_Hybrid_Car*fueltype_Hybrid + B_fueltype_Petrol_Car*fueltype_Petrol + B_distance_Car*distance + B_dur_driving_Car*dur_driving + B_cost_driving_total_Car*cost_driving_total'}

    #construct the model parameters
    for beta in MNL_beta_params_positive:
        exec("{} = Beta('{}', 0, 0, None, 0)".format(beta, beta), globals())
    for beta in MNL_beta_params_negative:
        exec("{} = Beta('{}', 0, None, 0, 0)".format(beta, beta), globals())
    for beta in MNL_beta_params_neutral:
        exec("{} = Beta('{}', 0, None, None, 0)".format(beta, beta), globals())

    #define utility functions
    for utility_idx in MNL_utilities.keys():
        exec("V_{} = {}".format(utility_idx, MNL_utilities[utility_idx]), globals())

    #assign utility functions to utility indices
    exec("V_dict = {}", globals())
    for utility_idx in MNL_utilities.keys():
        exec("V_dict[{}] = V_{}".format(utility_idx, utility_idx), globals())

    #associate the availability conditions with the alternatives
    exec("av = {}", globals())
    for utility_idx in MNL_utilities.keys():
        exec("av[{}] = 1".format(utility_idx), globals())
    
    #definition of the model
    logprob = loglogit(V_dict, av, choice)

    #create the Biogeme object
    biogeme = bio.BIOGEME(database_train, logprob)
    biogeme.modelName = 'Biogeme-model'

    biogeme.generate_html = False
    biogeme.generate_pickle = False

    return biogeme

def Optima(dataset_train):
    '''
    Create a MNL on the OPTIMA dataset.
    The model is a slightly modified version from the code that can be found here: https://github.com/JoseAngelMartinB/prediction-behavioural-analysis-ml-travel-mode-choice.

    Parameters
    ----------
    dataset_train : pandas DataFrame
        The training dataset.

    Returns
    -------
    biogeme : bio.BIOGEME
        The BIOGEME object containing the model.

    '''
    database_train = db.Database('OP', dataset_train)

    logger = blog.get_screen_logger(level=blog.DEBUG)
    logger.info('Model Optima.py')

    globals().update(database_train.variables)

    #model
    MNL_beta_params_negative = ['B_TimePT_PT', 'B_MarginalCostPT_PT', 'B_distance_km_PT', 'B_TimeCar_PM', 'B_CostCarCHF_PM', 'B_distance_km_PM', 'B_distance_km_SM']
    MNL_beta_params_neutral = ['ASC_PM', 'ASC_SM', 'B_age_PT', 'B_age_PM', 'B_age_SM', 'B_NbChild_PT', 'B_NbChild_PM', 'B_NbChild_SM', 'B_NbCar_PT', 'B_NbCar_PM', 'B_NbCar_SM', 'B_NbMoto_PT', 'B_NbMoto_PM', 'B_NbMoto_SM', 'B_NbBicy_PT', 'B_NbBicy_PM', 'B_NbBicy_SM', 'B_OccupStat_fulltime_PT', 'B_OccupStat_fulltime_PM', 'B_OccupStat_fulltime_SM', 'B_Gender_man_PT', 'B_Gender_man_PM', 'B_Gender_man_SM', 'B_Gender_woman_PT', 'B_Gender_woman_PM', 'B_Gender_woman_SM', 'B_Gender_unreported_PT', 'B_Gender_unreported_PM', 'B_Gender_unreported_SM']
    MNL_utilities = {0: 'B_age_PT*age + B_NbChild_PT*NbChild + B_NbCar_PT*NbCar + B_NbMoto_PT*NbMoto + B_NbBicy_PT*NbBicy + B_OccupStat_fulltime_PT*OccupStat_fulltime + B_Gender_man_PT*Gender_man + B_Gender_woman_PT*Gender_woman + B_Gender_unreported_PT*Gender_unreported + B_TimePT_PT*TimePT + B_MarginalCostPT_PT*MarginalCostPT + B_distance_km_PT*distance_km',
                     1: 'ASC_PM + B_age_PM*age + B_NbChild_PM*NbChild + B_NbCar_PM*NbCar + B_NbMoto_PM*NbMoto + B_NbBicy_PM*NbBicy + B_OccupStat_fulltime_PM*OccupStat_fulltime + B_Gender_man_PM*Gender_man + B_Gender_woman_PM*Gender_woman + B_Gender_unreported_PM*Gender_unreported + B_TimeCar_PM*TimeCar + B_CostCarCHF_PM*CostCarCHF + B_distance_km_PM*distance_km',
                     2: 'ASC_SM + B_age_SM*age + B_NbChild_SM*NbChild + B_NbCar_SM*NbCar + B_NbMoto_SM*NbMoto + B_NbBicy_SM*NbBicy + B_OccupStat_fulltime_SM*OccupStat_fulltime + B_Gender_man_SM*Gender_man + B_Gender_woman_SM*Gender_woman + B_Gender_unreported_SM*Gender_unreported + B_distance_km_SM*distance_km'}

    #construct the model parameters
    for beta in MNL_beta_params_negative:
        exec("{} = Beta('{}', 0, None, 0, 0)".format(beta, beta), globals())
    for beta in MNL_beta_params_neutral:
        exec("{} = Beta('{}', 0, None, None, 0)".format(beta, beta), globals())

    #define utility functions
    for utility_idx in MNL_utilities.keys():
        exec("V_{} = {}".format(utility_idx, MNL_utilities[utility_idx]), globals())

    #assign utility functions to utility indices
    exec("V_dict = {}", globals())
    for utility_idx in MNL_utilities.keys():
        exec("V_dict[{}] = V_{}".format(utility_idx, utility_idx), globals())

    #associate the availability conditions with the alternatives
    exec("av = {}", globals())
    for utility_idx in MNL_utilities.keys():
        exec("av[{}] = 1".format(utility_idx), globals())
    
    #definition of the model
    logprob = loglogit(V_dict, av, choice)

    #create the Biogeme object
    biogeme = bio.BIOGEME(database_train, logprob)
    biogeme.modelName = 'Biogeme-model'

    biogeme.generate_html = False
    biogeme.generate_pickle = False

    return biogeme