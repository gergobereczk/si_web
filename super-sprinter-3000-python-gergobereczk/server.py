from flask import Flask, render_template, request, redirect, url_for

import data_handler
import csv

app = Flask(__name__)



def get_table_from_file(file_name):
    table = []
    with open(file_name, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            table.append(line)
    return table

table = get_table_from_file("data.csv")

@app.route('/story/<thekey>')
def show_user_profile(thekey):
    print ("!!!!!!!!!!!!!!!megvan,az upddaet!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!44")
    table = get_table_from_file("data.csv")
    print(table[(int(thekey)+1)][1])

    return ("megvan",thekey)



@app.route('/')
def route_home():
    table = get_table_from_file("data.csv")
    del table[0]
    the_len = (len(table))
    print ("kkkk")
    print (the_len)
    return render_template("list.html", table=table,the_len=the_len)
@app.route('/list')
def route_list():
    user_stories = data_handler.get_all_user_story()

    return render_template('list.html', user_stories=user_stories)

@app.route("/story", methods=["GET", "POST"])
def route_story():
    if request.method == "POST":
        id_formax = []
        fieldnames = ["id", "story_title", "user_story", "acceptance_criteria", "bussiness_value", "estimation"]
        with open("data.csv", "r") as csv_file:
            csv_reader=csv.DictReader(csv_file)
            for line in csv_reader:
                id_formax.append(line["id"])
        if (len(id_formax)) == 0:
            temporary1 = request.form.to_dict()
            temporary1["id"] = (str(0))
            print(temporary1)
            with open("data.csv", "a") as csv_file:
                csv_reader = csv.DictWriter(csv_file, fieldnames)
                csv_reader.writerow(temporary1)
        else:
            actuel_id = ((int((max(id_formax))))+1)
            temporary1 = request.form.to_dict()
            temporary1["id"] = (str(actuel_id))
            print(temporary1)
            with open("data.csv", "a") as csv_file:
                csv_reader = csv.DictWriter(csv_file, fieldnames)
                csv_reader.writerow(temporary1)
        table = get_table_from_file("data.csv")
        del table[0]
        the_len = (len(table))
        return render_template("list.html", table=table,the_len=the_len)
    else:
        return  render_template("story.html")

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
