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

@app.route('/story/<thekey>', methods=["GET", "POST"])
def show_user_profile(thekey):
    if request.method == "POST":
        table = get_table_from_file("data.csv")
        table[((int(thekey))+1)][1]= request.form["story_title"]
        table[((int(thekey)) + 1)][2] = request.form["user_story"]
        table[((int(thekey)) + 1)][3] = request.form["acceptance_criteria"]
        table[((int(thekey)) + 1)][4] = request.form["bussiness_value"]
        table[((int(thekey)) + 1)][5] = request.form["estimation"]
        table[((int(thekey)) + 1)][6] = request.form["status"]


        with open("data.csv", "w") as csv_file:
            csv_writer=csv.writer(csv_file, delimiter=",")

            for line in table:
                csv_writer.writerow(line)

        return redirect('/')
    else:
        table = get_table_from_file("data.csv")
        update_number = (int(thekey)+1)

        return render_template('story1.html', table=table, update_number=update_number)



@app.route('/')
def route_home():
    table = get_table_from_file("data.csv")
    del table[0]
    the_len = (len(table))
    return render_template("list.html", table=table,the_len=the_len)


@app.route('/list')
def route_list():
    user_stories = data_handler.get_all_user_story()

    return render_template('list.html', user_stories=user_stories)

@app.route("/story", methods=["GET", "POST"])
def route_story():
    if request.method == "POST":
        id_formax = []
        fieldnames = ["id", "story_title", "user_story", "acceptance_criteria", "bussiness_value", "estimation", "status"]
        with open("data.csv", "r") as csv_file:
            csv_reader=csv.DictReader(csv_file)
            for line in csv_reader:
                id_formax.append (int(line["id"]))
        if (len(id_formax)) == 0:
            temporary1 = request.form.to_dict()
            temporary1["id"] = (str(0))
            with open("data.csv", "a") as csv_file:
                csv_reader = csv.DictWriter(csv_file, fieldnames)
                csv_reader.writerow(temporary1)
        else:
            actuel_id = (((max(id_formax)))+1)
            temporary1 = request.form.to_dict()
            temporary1["id"] = (str(actuel_id))
            with open("data.csv", "a") as csv_file:
                csv_reader = csv.DictWriter(csv_file, fieldnames)
                csv_reader.writerow(temporary1)
        table = get_table_from_file("data.csv")
        del table[0]
        the_len = (len(table))
        return redirect('/')
    else:
        return  render_template("story.html")

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
