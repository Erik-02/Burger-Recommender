import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load data from local file
#burgers_df = pd.read_csv('Burger data.csv')

# Load in Burger data
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

burgers_df = load_data("https://raw.githubusercontent.com/Erik-02/Burger-Recommender/main/Burger%20data.csv")
burgers_df.set_index('Burgers', inplace=True)

# Setting the global state of the page to go to
if 'pages' not in st.session_state: st.session_state.pages = 0
def home(): st.session_state.pages = 0
def meatPage(): st.session_state.pages = 1
def vegPage(): st.session_state.pages = 2
def predictionPage(): st.session_state.pages = 3

# Unknown variables of what the user would like, defaults
meat = 0
veggie = -1
vegan = -1
legume = -1
gourmet = -1
classical = 1
breakfast = -1
l_d = 0
beef = -1
chicken = -1
pork = -1
turkey = -1

# Background image
def set_bg_hack_url():
    """
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    """

    st.markdown(
        f"""
            <style>
            .stApp {{
                background: url("https://images.firstwefeast.com/complex/image/upload/c_limit,f_auto,fl_lossy,q_auto,w_1100/eijufgljsch1mfglymm2.jpg");
                background-size: cover
            }}
            </style>
            """,
        unsafe_allow_html=True
            )


# Start of APP
# Page 0
ph = st.empty()
if st.session_state.pages == 0:
    with ph.form('p0'):
        # set background image
        set_bg_hack_url()

        # Page layout/setup
        st.title("Burger Recommender")
        # Does a user want meat or not
        meat_yn = st.radio('Would you like meat on your burger?', ('Yes', 'No', 'none'), index=2)

        # Submit data, proceed to next page
        #submit = st.form_submit_button('Next', on_click=meatPage())


        if meat_yn == 'Yes':
            submit = st.form_submit_button('Next', on_click=meatPage())
        elif meat_yn == 'No':
            submit = st.form_submit_button('Next', on_click=vegPage())
        else:
            submit = st.form_submit_button('Next')



# Page 1
# Meat page
if st.session_state.pages == 1:
    with ph.form('meat burger'):
        # Background image
        set_bg_hack_url()

        # App text
        st.title('A MEATY BURGER')

        # Breakfast or Lunch/Dinner
        st.subheader('Would you like it for Breakfast or Lunch/Dinner?')
        select = '<p style="font-family:sans-serif; color:black; font-size: 12px;">You may select more than one option</p>'
        st.markdown(select, unsafe_allow_html=True)

        breakfast = st.checkbox('Breakfast')
        l_d = st.checkbox('Lunch/Dinner')

        # Gourmet or Classical
        st.header('Gourmet or Classical')
        st.subheader('Should your burger be gourmet or classical?')
        st.markdown(select, unsafe_allow_html=True)

        gourmet = st.checkbox('Gourmet')
        classical = st.checkbox('Classical')

        # Meat selection
        st.header('Meat selection')
        st.subheader('What type of meat would you like?')
        st.markdown(select, unsafe_allow_html=True)

        beef = st.checkbox('Beef')
        chicken = st.checkbox('Chicken')
        pork = st.checkbox('Pork')
        turkey = st.checkbox('Turkey')

        # Submit data, proceed to next page
        submit = st.form_submit_button('Recommend')
        if submit:
            # Clear forms
            ph.empty()

            # Go to recommendation page
            predictionPage()

            # Variable designation
            meat = 1

            if breakfast:
                breakfast = 1
            if l_d:
                l_d = 1
            else:
                l_d = -1
            if gourmet:
                gourmet = 1
            else:
                gourmet = -1
            if classical:
                classical = 1
            else:
                classical = -1
            if beef:
                beef = 1
            else:
                beef = -1
            if chicken:
                chicken = 1
            else:
                chicken = -1
            if pork:
                pork = 1
            else:
                pork = -1
            if turkey:
                turkey = 1
            else:
                turkey = -1


# Page 2
if st.session_state.pages == 2:
    with ph.form('veggie or vegan'):
        # Background Image
        set_bg_hack_url()



        # Page layout/setup
        st.title('Vegan / Veggie burger')

        # Vegan / Veggie
        st.subheader('Should your burger be Vegan or Veggie')
        select = '<p style="font-family:sans-serif; color:black; font-size: 12px;">You may select more than one option</p>'
        st.markdown(select, unsafe_allow_html=True)

        vegan = st.checkbox('Vegan')
        veggie = st.checkbox('Veggie')

        # Legume or not
        st.subheader('Legume or Non-Legume family')
        st.radio('Which do you prefer for your burger?', ('Legume  (Beans, Peas, Lentils, Peanuts)', 'Non-Legume  (Mushrooms, Tomato, Fruits)'))

        # Breakfast or Lunch/Dinner
        st.subheader('Would you like it for Breakfast or Lunch/Dinner?')
        st.markdown(select, unsafe_allow_html=True)

        breakfast = st.checkbox('Breakfast')
        l_d = st.checkbox('Lunch/Dinner')

        # Submit data, proceed to next page
        submit = st.form_submit_button('Recommend')
        if submit:
            # Clear form
            ph.empty()

            # Go to Recommendation page
            predictionPage()

            # Variable designation
            meat = -1

            if vegan:
                vegan = 1
            else:
                vegan = -1
            if veggie:
                veggie = 1
            else:
                veggie = -1
            if breakfast:
                breakfast = 1
            else:
                breakfast = -1
            if l_d:
                l_d = 1
            else:
                l_d = -1

# Function used to collect user input data and return top 3 recommendations
def recommendation():
    # User dictionary containing their input values
    user_dict = {'Meat_yn': meat, 'Veggie': veggie, 'Vegan': vegan, 'Legume_yn': legume, 'Gourmet_yn': gourmet,
                 'Classical': classical,
                 'Breakfast': breakfast, 'Lunch/Dinner': l_d, 'Beef': beef, 'Chicken': chicken, 'Pork': pork,
                 'Turkey': turkey}
    user_df = pd.DataFrame(user_dict, index=['user'])

    # Combine user input dataframe with burger dataframe imported at the top
    prediction_df = pd.concat([burgers_df.iloc[:,:-2], user_df], ignore_index=False)

    # get cosine similarity scores on the dataframe
    # It will calculate scores for a user in comparison to all of the burgers
    cosine_prediction_df = cosine_similarity(prediction_df)
    cosine_prediction_df = pd.DataFrame(cosine_prediction_df, index=prediction_df.index, columns=prediction_df.index)[:-1]

    # Create dataframe containing the 3 most similar burgers to our input parameters
    user_prediction_burgers = cosine_prediction_df.nlargest(3, 'user')

    # Get the pizza names and cosine similarity scores
    global burger_names, bl, pl
    # Names of recommended burgers
    burger_names = user_prediction_burgers.index.tolist()
    # Get link to recipe and image of burger
    bl = burgers_df['link'].loc[burger_names].values.ravel().tolist()
    pl = burgers_df['photo_link'].loc[burger_names].values.ravel().tolist()



# Recommendation page
ph = st.empty()
if st.session_state.pages == 3:
    recommendation()

    ph.empty()
    with ph.form('Recommendation page'):
        # Background Image
        set_bg_hack_url()

        # Page title
        st.title('Recommendations')

        # Create result columns
        col1,col2,col3 = st.columns(3)

        # Column 1 creation
        col1.header('1st Place')
        col1.image(pl[0])
        col1.subheader(burger_names[0])
        col1.write('Recipe link: ' + bl[0])

        # Column 2 creation
        col2.header('2nd Place')
        col2.image(pl[1])
        col2.subheader(burger_names[1])
        col2.write('Recipe link: ' + bl[1])

        # Column 3 creation
        col3.header('3rd Place')
        col3.image(pl[2])
        col3.subheader(burger_names[2])
        col3.write('Recipe link: ' + bl[2])

        # restart recommendation
        submit = st.form_submit_button('Restart recommendation', on_click=home())
