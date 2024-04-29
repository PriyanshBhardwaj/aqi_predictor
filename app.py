'''
    it will take inputs like station name, date, etc. and call the downloader fn, downloads the data and then create the input sample
    for aqi predictor and then feed that data into the aqi predictor fn, predicts the aqi and outputs it.
'''
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import ast
import pytz

from helper.aqi_ip_sample import create_aqi_input_sample
from helper.predict_aqi import predict_aqi



@st.cache_data(ttl=1200, show_spinner=False)
def find_aqi(state, city, station_id, station_name):
    ''' main function which will automatically predict the aqi: [curr-1, curr, +1, +2, +3, +4, +5, +6]'''
    # from_date : previous date, time: 1hr before
    # to_date: current date, time: 2hrs before

    from_date = (datetime.now(pytz.timezone('Asia/Kolkata')).replace(second=0,minute=0) - timedelta(days=1, hours=1)).strftime("%d-%m-%Y T%H:%M:%SZ")
    to_date = (datetime.now(pytz.timezone('Asia/Kolkata')).replace(second=0,minute=0) - timedelta(hours=2)).strftime("%d-%m-%Y T%H:%M:%SZ")

    # print(from_date, to_date, sep='\n')

    try:
        ## creating aqi input sample
        aqi_input, pollutants_data_list = create_aqi_input_sample(from_date = from_date, to_date = to_date, state = state, city = city, criteria = '1 Hours', station_id = station_id, p_id = ['parameter_193', 'parameter_215', 'parameter_194', 'parameter_311', "parameter_312", "parameter_203", "parameter_222"], parameters = ['PM2.5', 'PM10', 'NO2', 'NH3', 'SO2', 'CO', 'Ozone'], station_name=station_name)
    
    except Exception as e:
        # print("error: ", e)
        status = False
        errorMsg = "Currently there is not sufficient data to predict AQI for this station. You can check for other stations."
        return errorMsg, status, None

    # print(aqi_input)
    # print(pollutants_data_list)
    ## predicting aqi
    predicted_aqi, polls = predict_aqi(aqi_input, pollutants_data_list)
    status = True

    # aqi: curr-1, curr, curr+1, +2, +3, +4, +5, +6
    # print(predicted_aqi)

    return predicted_aqi, status, polls

# find_aqi()



@st.cache_data(show_spinner=False)          #caching will make it faster
def read_states_cities_station_csv():
    state_cities = pd.read_csv('states_cities.csv', converters={'cities': ast.literal_eval})
    city_stations = pd.read_csv('city_stations.csv', converters={'station_ids':pd.eval,'station_names': ast.literal_eval})
    
    return state_cities, city_stations


def app():
    st.set_page_config(page_title='AQI Predictor', page_icon='💨', layout='wide')
    # emoji shortcut: CTRL + CMD + Space

    #Removing the Menu Button and Streamlit Icon
    hide_default_format = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_default_format, unsafe_allow_html=True)

    cola, colb = st.columns([5,2])
    cola.title("AQI Predictor")

    with colb:
        colb.write('#')
        with st.expander("**About me**"):
            st.write("**Priyansh Bhardwaj**")
            st.write("[Website](https://priyansh-portfolio.streamlit.app/)")
            st.write("[LinkedIn](https://www.linkedin.com/in/priyansh-bhardwaj-25964317a)")


    st.subheader("Welcome to AQI Predictor!", anchor=False)
    st.subheader("Air Quality Index is a scientifically calculated value which tells the quality of air for a particular location.\
                It takes into accout several pollutants like PM2.5, PM10, NO2, NH3, SO2, CO and Ozone.\
                Different countries takes into account different pollutants in different range but in India these pollutants are considered and in the range of 0-500 and the AQI is also calculated in the range of 0-500.", anchor=False)
    st.subheader("**It will predict current hour AQI along with the last hour AQI and next 6 hours AQI**. It also shows the variations of above mentioned pollutants with time.", anchor=False)

    st.write('#')
    st.markdown("Predict AQI in just 3 simple steps: \
                \n - First: select the state from the list\
                \n - Second: select any city of that state\
                \n - Third: select the station\
                \n - Click the \"Predict AQI\" button.")
    st.write('#')
    

    ##user input parameters ====> state, city, station
    col1, col2, col3 = st.columns([1,1,1])
    
    ## creating list of states, cities and stations
    state_cities, city_stations = read_states_cities_station_csv()

    #state
    state_list = state_cities['states']   
    state =  col1.selectbox('**State**', options=state_list, index=None, placeholder='select state')
    # col1.write(state)

    #city
    st.session_state.disabled = True
    city_list = ['']
    if state:
        st.session_state.disabled = False
        state_ix = state_cities.loc[state_cities['states'] == state].index[0]

        city_list = state_cities.at[state_ix, 'cities']
        # print((city_list))
        # print(type(city_list))
    city =  col2.selectbox('**City**', index=None, placeholder='select city', disabled=st.session_state.disabled, options=city_list)
    # col2.write(city)

    #station
    disabled = True
    station_list = ['']
    if city:
        disabled = False
        city_ix = city_stations.loc[city_stations['city'] == city].index[0]
        # print(city_ix)
        station_list = city_stations.at[city_ix, 'station_names']

        station_id_list = city_stations.at[city_ix, 'station_ids']
        # print(station_id_list)
    station =  col3.selectbox('**Station**', index=None, placeholder='select station', disabled=disabled, options=station_list)
    # col3.write(station)

    if station:
        station_id = station_id_list[station_list.index(station)]

        #aqi calculation
        st.write('#')
        aqi_button = st.button('Predict AQI', type='primary')

        if aqi_button:
            with st.spinner(''):

                ##calling aqi function
                aqi, status, polls = find_aqi(state, city, station_id, station)
            # print(aqi)

            if status == False:
                st.write('#')
                st.write(f'**{aqi}**')

            else:
                time_list = []
                aqi_time = {}
                pm25 = {}; pm10 = {}; NO2 = {}; NH3 = {}; SO2 = {}; CO = {}; Ozone = {}
                i = 1
                while i>=(2-len(aqi)):
                    time_list.append((datetime.now(pytz.timezone('Asia/Kolkata')).replace(second=0,minute=0) - timedelta(hours=i)).strftime("%d-%m-%Y %H:%M:%S"))    
                    i-=1

                for i in range(len(time_list)):
                    aqi_time[time_list[i]] = aqi[i]

                    pm25[time_list[i]] = polls[0][i]
                    pm10[time_list[i]] = polls[1][i]
                    NO2[time_list[i]] = polls[2][i]
                    NH3[time_list[i]] = polls[3][i]
                    SO2[time_list[i]] = polls[4][i]
                    CO[time_list[i]] = polls[5][i]
                    Ozone[time_list[i]] = polls[6][i]
                    

                ## writting aqi
                col1, col2 = st.columns([1,5])
                # col1.write("")

                #current hour aqi
                col1.write('#')
                col1.write(f"**Current AQI: {aqi[1]}**")

                ##AQI Remark
                aqi_remark = ''
                if 0 < aqi[1] < 50:
                    aqi_remark = 'Good'
                if 51 < aqi[1] < 100:
                    aqi_remark = 'Satisfactory'
                if 101 < aqi[1] < 200:
                    aqi_remark = 'Moderate'
                if 201 < aqi[1] < 300:
                    aqi_remark = 'Poor'
                if 301 < aqi[1] < 400:
                    aqi_remark = 'Very poor'
                if 401 < aqi[1] < 500:
                    aqi_remark = 'Severe'

                col1.write('#')
                col1.write(f"**AQI Remark: {aqi_remark}**")

                #prev hour aqi
                col2.write('#')
                col2.write(f'**{time_list[0]}: {aqi[0]}**')

                #next hours aqi
                col2.write('#')
                col3, col4, col5, col6, col7, col8 = col2.columns([1,1,1,1,1,1])
                col3.write(f'**{time_list[2]}: {aqi[2]}**')
                col4.write(f'**{time_list[3]}: {aqi[3]}**')
                col5.write(f'**{time_list[4]}: {aqi[4]}**')
                col6.write(f'**{time_list[5]}: {aqi[5]}**')
                col7.write(f'**{time_list[6]}: {aqi[6]}**')
                col8.write(f'**{time_list[7]}: {aqi[7]}**')


                ## plotting aqi chart and aqi against time
                col1, col2 = st.columns([5,5])
                col1.write("")  #creates gap between both columns

                col1.write('#')
                col1.image('AQI_Chart.png', caption='AQI Chart', use_column_width=True)

                col2.write('#')
                col2.subheader('**AQI vs Time plot**')
                col2.write('#')
                col2.line_chart(aqi_time)


                ## plotting each pollutants predicted values against time
                st.subheader("**Pollutants vs Time plots**")
                col1, col2, col3 = st.columns([1,1,1])

                ## col1
                col1.write('#')
                col1.write('**PM2.5**')
                col1.bar_chart(pm25)

                col1.write('#')
                col1.write('**NH3**')
                col1.bar_chart(NH3)

                col1.write('#')
                col1.write('**Ozone**')
                col1.bar_chart(Ozone)

                ##col2
                col2.write('#')
                col2.write('**PM10**')
                col2.bar_chart(pm10)

                col2.write('#')
                col2.write('**SO2**')
                col2.bar_chart(SO2)

                ##col3
                col3.write('#')
                col3.write('**NO2**')
                col3.bar_chart(NO2)

                col3.write('#')
                col3.write('**CO**')
                col3.bar_chart(CO)
                    


if __name__ == '__main__':
    # pred_aqi,_,_ = find_aqi('Haryana', 'Gurugram', 'site_5345','Teri Gram, Gurugram - HSPCB')
    # print(pred_aqi)
    app()