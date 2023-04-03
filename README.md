# Burger-Recommender
This is a burger recommendation app, built and deployed using streamlit. App link: https://erik-02-burger-recommender-burger-recommender-no04nb.streamlit.app/

This is a 'Content based filtering' recommendation system. The goal is to recommend a burger to a user, asking only 4 questions.
In total there are 57 unique burgers each classified with 11 features.

Once a user answered the questions, a user vector will have formed, such as: "1,-1,-1,-1,1,1,-1,1,-1,1,1".
I then use 'Cosine similarity' to determine which 3 burgers are the closest to the input of the user.

The data is self collected.
