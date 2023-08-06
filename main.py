from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
popular_df = pickle.load(open('pop.pkl','rb'))
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(np.round(popular_df['avg_ratings'].values, 2))
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend1.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    print("user_input ",user_input)
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:13]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print("data ",data)

    return render_template('recommend1.html',data=data)
    # return data

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')