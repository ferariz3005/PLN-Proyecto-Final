'''

THIS PYTHON FILE INCLUDES EVERYTHING NEEDED TO CREATE A STREAMLIT INTERFACE WHERE THE USER WILL BE ABLE TO GET 
MOVIE RECOMMENDATIONS FROM A SPECIFIC GENRE THEY'VE CHOSEN. IT'S A SEARCH ENGINE INVOLVING TWO MAIN FUNCTIONS:

        1. Search By Genre. The user types in the genre they're intrested in, and will receive 10 random movie 
        suggestions from such genre. This movie titles exist within the dataset.

        2. AI Recommendations. Furthermore, the user has the option to receive aditional recommendations generated
        by AI using the OpenAI API. This extra feature allows the user to get movie suggestions even for movie 
        genre that do not exist within the dataset.

'''

# Import the libraries needed.
import streamlit as st
import pandas as pd
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
from PIL import Image


# Read the dataset.
df = pd.read_csv('final_movies.csv')


# 1. Search By Genre.

def search_by_genre(genre):
    available_genres = df['Genre'].unique().tolist()
    genre = genre.lower()

    # Error handling in case the genre does not exist within the dataset
    if genre not in available_genres:
        st.warning('''Please enter one of the categories listed below:
        \n1. Action/Adventure
        \n2. Comedy
        \n3. Drama
        \n4. Horror
        \n5. Romance
        \n6. Suspense/Thriller/Mystery
        ''')
    # Return a random sample of 10 movies from the selected genre
    else:
        filtered_movies = df[df['Genre'] == genre]
        return filtered_movies.sample(n=10)['Title'].tolist()



# 2. AI Recommendations.

def ai_recommendations(genre):    
        message = []
        llm = ChatOpenAI(model_name='gpt-3.5-turbo')

        query = genre

        # This program is directed to a movie review website, we want to encourage the users to leave their reviews.
        prompt = """
            You are a film expert providing movie recommendations based on the genre '{genre}'.
            Recommend 5 top movies in this genre. Be concise yet engaging. Also, remind the user
            to enjoy watching the movies and encourage them to write reviews on the website.
        """
        # The user is noted the following:
        st.write('''Be aware you could get movie recommendations for genres that do not
                 appear in our catalogue.''')
        
        if st.button('Continue'):
            with st.spinner('Here are some movies you might like ...'):
                response = llm.invoke([SystemMessage(content=prompt), 
                                        HumanMessage(content=query)])
                # Store the answer in a list 'message' defined at the beginning of the function.
                message.append(response.content)
        return message            


# MAIN. Calls the previous functions.

def main():
    # An OpenAI API key is needed to run the program (particularly for function 2.)
    with st.sidebar:
        api_key_file = st.file_uploader('Upload your key here', type=['txt'])

    if api_key_file is not None:
        key= str(api_key_file.readline().decode('utf-8'))
        os.environ['OPENAI_API_KEY'] = key
        
        # Set up the title and session state for the app
        st.title('Search Movie By Genre')
        
        session_state = st.session_state
        
        if 'genre' not in session_state:
            session_state.genre = ""

        genre = st.text_input('Type here:', value=session_state.genre)
        
        # Perform search when 'Search' button is clicked
        if st.button('Search'):
            if genre:
                # Retrieve and display movies by the entered genre
                genre_movies = search_by_genre(genre)
                st.subheader(f"Results for {genre}:")
                if genre_movies:
                    for i, title in enumerate(genre_movies, start=1):
                        st.write(f"{i}. {title}")
                session_state.genre = genre  # Save the genre in session state for future use

            else:
                st.warning('Please enter a genre!')

        # Provide AI recommendations if checkbox is selected and genre is entered
        extra_recom = st.checkbox('I would like to get further recommendations')
        
        if extra_recom and session_state.genre:
            new_recom = ai_recommendations(session_state.genre)
            st.subheader('AI Recommendations:')
            st.write(new_recom)

        # Allow user to reset genre and start over
        if st.button('Go back'):
            session_state.genre = ""

        image = Image.open('Letterboxd_logo_(2018).png')
        link_url = "https://letterboxd.com/"
        st.image(image, caption= 'Discover and share more wonderful films in: ', width=150,)
        link = st.markdown(f'<a href="{link_url}" target="_blank">https://letterboxd.com/</a>', unsafe_allow_html=True)


# Run the program
if __name__ == "__main__":
    main()


#After running the python file make sure to make sure you're in the folder/directory where 
# both the file and dataset are located. Once you've done this, you can launch the Streamlit 
# interface by using the command 'streamlit run search.py' .



