import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
from zipfile import ZipFile

UPLOAD_FOLDER = "./uploaded_files"
ALLOWED_EXTENSIONS = {'csv'}

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
    
#configs
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#main api to upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        print(file.filename)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return "File uploaded"
        # with open(os.path.join(UPLOAD_FOLDER, file.filename), "wb") as fp:
        #     fp.write(request.data)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    
@app.route('/allprocess/<filename>')
def allprocess(filename):
    data_set = pd.read_csv(app.config['UPLOAD_FOLDER']+'/'+filename)

    #create child using type
    free_type = data_set[data_set['Type']=="Free"]
    paid_type = data_set[data_set['Type']=="Paid"]
    #save
    free_type.to_csv('./output/free_type.csv')
    paid_type.to_csv('./output/paid_type.csv')

    #filter data_set based on CR
    unique_content = []
    content_rating_names = data_set["Content Rating"].unique()
    index = 0
    for content_rating in content_rating_names:
        unique_content.append(data_set[data_set['Content Rating']==content_rating])
        index += 1
    #save them
    index = 0
    for content_rating in content_rating_names:
        unique_content[index].to_csv('./output/'+str(content_rating)+'.csv')
        index += 1

    #round off
    roundoff_data_set = data_set
    roundoff_data_set['Rating'] = roundoff_data_set['Rating'].fillna(0)    
    roundoff_data_set['Rating Roundoff'] = roundoff_data_set['Rating'].apply(lambda x: round(float(x)))
    roundoff_data_set.to_csv('./output/roundoff_data_set.csv')
    print(roundoff_data_set.head())

    # return send_from_directory(app.config['UPLOAD_FOLDER'],filename')
    return "all done"

@app.route('/type_split/<filename>')
def split_uploaded_file(filename):
    data_set = pd.read_csv(app.config['UPLOAD_FOLDER']+'/'+filename)

    #create child using type
    free_type = data_set[data_set['Type']=="Free"]
    paid_type = data_set[data_set['Type']=="Paid"]
    #save
    free_type.to_csv('./output/free_type.csv')
    paid_type.to_csv('./output/paid_type.csv')

    #send zipped files
    zipObj = ZipFile('./output/response_zip/type_split.zip', 'w')
    zipObj.write('./output/free_type.csv')
    zipObj.write('./output/paid_type.csv')
    zipObj.close()

    return send_from_directory('./output/response_zip/','type_split.zip')

@app.route('/filter/<filename>')
def filter_uploaded_file(filename):
    data_set = pd.read_csv(app.config['UPLOAD_FOLDER']+'/'+filename)

    #filter data_set based on CR
    unique_content = []
    content_rating_names = data_set["Content Rating"].unique()
    index = 0
    for content_rating in content_rating_names:
        unique_content.append(data_set[data_set['Content Rating']==content_rating])
        index += 1
    #save them
    zipObj = ZipFile('./output/response_zip/filter.zip', 'w')
    index = 0
    for content_rating in content_rating_names:
        unique_content[index].to_csv('./output/'+str(content_rating)+'.csv')
        zipObj.write('./output/'+str(content_rating)+'.csv')
        index += 1

    #send zipped files
    zipObj.close()

    return send_from_directory('./output/response_zip/','filter.zip')

@app.route('/roundoff/<filename>')
def roundoff_uploaded_file(filename):
    data_set = pd.read_csv(app.config['UPLOAD_FOLDER']+'/'+filename)

    #round off
    roundoff_data_set = data_set
    roundoff_data_set['Rating'] = roundoff_data_set['Rating'].fillna(0)    
    roundoff_data_set['Rating Roundoff'] = roundoff_data_set['Rating'].apply(lambda x: round(float(x)))
    roundoff_data_set.to_csv('./output/roundoff_data_set.csv')
    print(roundoff_data_set.head())

    return send_from_directory('./output/','roundoff_data_set.csv')

if __name__ == 'main':
    app.run(debug=True)