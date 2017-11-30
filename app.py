from flask import Flask, render_template, request, redirect, session, g, url_for
import pymongo

app = Flask(__name__)
app.secret_key = 'lbnkgdjfgh98hgskjd'



@app.route('/', methods=['GET', 'POST'])
def index():
    m = pymongo.MongoClient()
    list_all = m.phonebook.item.find()
    if request.method == 'POST':
        if 'delete' in request.form:
            phone = request.form.get('phone', '')
            m.phonebook.item.remove({
                'phone': phone
            })
        if 'update' in request.form:
            name = request.form.get('name', '')
            new_name = request.form.get('newname', '')
            phone = request.form.get('phone', '')
            new_phone = request.form.get('newphone', '')
            m.phonebook.item.update({'name': name, 'phone': phone}, {'$set': {
                'phone': new_phone,
                'name': new_name}})

    return render_template('index.html',
                           all=list_all)

@app.route('/create', methods=['GET', 'POST'])
def create():
    name = phone = ''
    if request.method == 'POST':
        name = request.form.get('name', '')
        phone = request.form.get('phone', '')
        if name and phone:
            m = pymongo.MongoClient()
            m.phonebook.item.insert({'name': name, 'phone': phone})
            return redirect('/')
    return render_template('items.html',
                           name = name,
                           phone = phone)


if __name__ == '__main__':
    app.run(debug=True)