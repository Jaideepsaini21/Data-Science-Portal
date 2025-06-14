from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 

## 
app = Flask(__name__)
main_data = pd.read_csv("cleaned_glassdoor_data.csv")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/searchjob/")
def jobsearch():
    return render_template("searchjobform.html")


@app.route("/aftersubmit/", methods=['GET', 'POST'])
def aftersubmit():
    if request.method == "POST":
        # extract data from form and search into dataset 
        # return the final result 
        # html --> python --> jinja 
        jobprofile = request.form.get("jobprofile")
        location = request.form.get("location")
        rating = request.form.get("rating")
        sector = request.form.get("sector")
        company_name = request.form.get("companyname")
        data = main_data.copy()
        if rating:
            if rating.isnumeric():
                rating = eval(rating)
                if not rating<=5:
                    error = "Please Enter Rating 1 to 5"
                    return render_template("searchjobform.html", err=error)
            else:
                error = "Invalid Rating"
                return render_template("searchjobform.html", err=error)
        if jobprofile:
            data = data[data['job_title'].apply(lambda x:True if "data analyst" in x.lower() else False)]
        if location:
            data = data[data['location'].str.lower() == str(location).lower()]
        if rating:
            data = data[data['company_rating']>=rating]
        if sector:
            data = data[data['sector'].apply(lambda x: True if str(sector) in str(x).lower() else False)]
        if company_name:
            data = data[data['company'].str.lower().str.strip() == company_name.strip().lower()]               
        return render_template("job-detail.html", data= data.to_dict(orient='records'))
    else:
        return render_template("searchjobform.html")
    

@app.route("/showplot/", methods=['GET', 'POST'])
def showplot():
    if request.method == "GET":
        return render_template("index.html")
    else:
        category = request.form.get("category")
        column_name = request.form.get("column")
        if category == "bar":
            count = main_data[column_name].value_counts()[:10]
            index = count.index 
            values = count.values 
            file_name = f"static/img/{column_name}_{category}.jpg"
            plt.figure(figsize=(10, 5), dpi=100)
            sns.barplot(index, values)
            plt.xticks(rotation=90)
            plt.title(f"TOP 10 {column_name.upper()}", color='green')
            plt.savefig(file_name, bbox_inches='tight')
        elif category == "piechart":
            count = main_data[column_name].value_counts()[:10]
            index = count.index 
            values = count.values 
            file_name = f"static/img/{column_name}_{category}.jpg"
            plt.figure(figsize=(10, 5), dpi=100)
            plt.pie(values, labels=index)
            plt.title(f"TOP 10 {column_name.upper()}", color='green')
            plt.savefig(file_name, bbox_inches='tight')
        elif category == "histogram":
            file_name = f"static/img/{column_name}_{category}.jpg"
            plt.figure(figsize=(10, 5), dpi=100)
            sns.histplot(main_data[column_name])
            plt.xticks(rotation=90)
            plt.title(f"DISTRIBUTION OF {column_name.upper()}", color='green')
            plt.savefig(file_name, bbox_inches='tight')
        return render_template("index.html", img="../"+file_name)
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)


# main.py --> static/
# static
# templates --> index.html --> ../static/img/