import psycopg2
import psycopg2.extras
import os
from flask import Flask, render_template, request
app = Flask(__name__)

# people=['Shane Chamberlain', 'Mad Max']
# p2=[{'person': 'Shane Chamberlain', 'major': 'Computer Science', 'year': 'Senior', 'gender': 'Male'}]

def connectToDB():
    # connectionString 
    connectionString = 'dbname=webpageusers user=shane password=Madmartigan host=localhost'
    print connectionString
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")
        

@app.route('/')
def mainIndex():
    eclipse = {'date': 'March 9th', 'time': '0200 UTC'}
    return render_template('index.html', selected='home', eclipse=eclipse)

@app.route('/blackHole')
def examples():
    isShowing = False
    eclipse = {'date': 'March 9th', 'time': '0200 UTC'}
    return render_template('blackHole.html', selected='blackHole', eclipse=eclipse, showing=isShowing)
	
@app.route('/eclipse')
def page():
    eclipse = {'date': 'March 9th', 'time': '0200 UTC'}
    return render_template('eclipse.html', selected='eclipse', eclipse=eclipse)
	
@app.route('/comet')
def another_page():
    videos = [{'title': 'Halleys Comet', 'vidLink': 'C8zV1xiGqf4', 'description': 'Halleys Comet or Comet Halley (officially designated 1P/Halley) is the most famous of the periodic comets.'},
    {'title': 'Comet Halley Returns-Voyager Uranus Flyby', 'vidLink': 'oBq3-ZqW4Ac', 'description': '"This videotape shows the five exploratory spacecraft, representing several countries, that will study Comet Halley: Giotto, Vega 1 and 2, Planet A, and Sakigaki."'}]
    eclipse = {'date': 'March 9th', 'time': '0200 UTC'}
    return render_template('comet.html', selected='comet', eclipse=eclipse, videos=videos)

# @app.route('/emailList', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         people.append(request.form['name'])
#     eclipse = {'date': 'March 9th', 'time': '0200 UTC'}
#     return render_template('emailList.html', selected='emailList', eclipse=eclipse, people=people)

# @app.route('/emailList2', methods=['GET', 'POST'])
# def register2():
#     if request.method == 'POST':
#         p2.append({'person': request.form['name'], 
#                   'major': request.form['major'],
#                   'year': request.form['year'],
#                   'gender': request.form['gender']})
#     eclipse = {'date': 'March 9th', 'time': '0200 UTC'}
#     return render_template('emailList2.html', selected='emailList2', eclipse=eclipse, people=p2)

@app.route('/contact')
def contact():
	return render_template('contact.php', selected='contact')

@app.route('/emailList2', methods=['GET', 'POST'])
def register2():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        try:
            cur.execute("""INSERT INTO wall (person, major, year, gender)
            VALUES (%s, %s, %s, %s);""",
            (request.form['person'], request.form['major'], request.form['year'], request.form['gender']) )
        except:
            print("ERROR inserting into wall")
            print("Tried: INSERT INTO wall (person, major, year, gender) VALUES (%s, %s, %s, %s);",
                (request.form['person'], request.form['major'], request.form['year'], request.form['gender']) )
            conn.rollback()
        conn.commit()
        
    try:
        cur.execute("select person, major, year, gender from wall")
    except:
        print("ERROR inserting from the wall")
        conn.rollback()
    conn.commit()
    eclipse = {'date': 'March 9th', 'time': '0200 UTC'}
    results = cur.fetchall()
    return render_template('emailList2.html', selected='emailList2', eclipse=eclipse, people=results)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', '8080')), debug=True)