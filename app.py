from flask import Flask,request,render_template
import pickle
import numpy as np
import pandas
books =pickle.load(open('./assets/books.pkl','rb'))
books_table =pickle.load(open('./assets/books_table.pkl','rb'))
popular_books =pickle.load(open('./assets/popular_books.pkl','rb'))
similarities =pickle.load(open('./assets/similarities.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
    book_names=list(popular_books['Book-Title'].values),
    author=list(popular_books['Book-Author'].values),
    images=list(popular_books['Image-URL-M'].values),
    rating=list(popular_books['Book-Rating'].values),
    votes=list(popular_books['num_rating'].values),
    );

@app.route('/recommend')
def recommend():
     return render_template('recommend.html');

@app.route('/books',methods=['POST'])
def recommendation():
    input_=request.form.get('input')
    index=(np.where(books_table.index==input_))[0][0]
    book_indices=sorted(list(enumerate(similarities[index])),key=lambda x:x[1],reverse=True)[1:6]
    data=[]
    for book_index in book_indices:
        item=[]
        temp_table=books[books['Book-Title']==books_table.index[book_index[0]]]
        item.extend(list(temp_table.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_table.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_table.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return  render_template('recommend.html',data=data)

if __name__=="__main__":
    app.run(debug=True, port=3000)