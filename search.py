import streamlit as st
import pandas as pd
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

df = pd.read_csv('final_movies.csv')

def search_by_genre(genre):

    available_genres = df['Genre'].unique().tolist()
    genre = genre.lower()

    if genre not in available_genres:
        st.warning('''Please enter one of the categories listed below:
        \n1. Action/Adventure
        \n2. Comedy
        \n3. Drama
        \n4. Horror
        \n5. Romance
        \n6. Suspense/Thriller/Mystery
        ''')
    else:
        filtered_movies = df[df['Genre'] == genre]
        return filtered_movies.sample(n=10)['Title'].tolist()

def ai_recommendations(genre):    
        
        message = []
        llm = ChatOpenAI(model_name='gpt-3.5-turbo')

        query = genre
        prompt = """
            You are a film expert providing movie recommendations based on the genre '{genre}'.
            Recommend 5 top movies in this genre. Be concise yet engaging. Also, remind the user
            to enjoy watching the movies and encourage them to write reviews on the website.
        """
        st.write('''Be aware you could get movie recommendations for genres that do not
                 appear in our catalogue.''')
        
        if st.button('Continue'):
            with st.spinner('Here are some movies you might like ...'):
                response = llm.invoke([SystemMessage(content=prompt), 
                                        HumanMessage(content=query)])
                message.append(response.content)
        return message            


def main():

    with st.sidebar:
        api_key_file = st.file_uploader('Upload your key here', type=['txt'])

    if api_key_file is not None:
        key= str(api_key_file.readline().decode('utf-8'))
        os.environ['OPENAI_API_KEY'] = key

        st.title('Search Movie By Genre')

        session_state = st.session_state
        
        if 'genre' not in session_state:
            session_state.genre = ""

        genre = st.text_input('Type here:', value=session_state.genre)

        if st.button('Search'):
            if genre:
                genre_movies = search_by_genre(genre)
                st.subheader(f"Results for {genre}:")
                if genre_movies:
                    for i, title in enumerate(genre_movies, start=1):
                        st.write(f"{i}. {title}")
                session_state.genre = genre  

            else:
                st.warning('Please enter a genre!')

        extra_recom = st.checkbox('I would like to get further recommendations')
        if extra_recom and session_state.genre:
            new_recom = ai_recommendations(session_state.genre)
            st.subheader('AI Recommendations:')
            st.write(new_recom)

        if st.button('Go back'):
            session_state.genre = ""
            session_state.genre = ""


if __name__ == "__main__":
    main()


