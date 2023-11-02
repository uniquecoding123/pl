from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgress_2fvz_user:mSk50LgEYY0L3cffmy7sZ9Fetc9aKsps@dpg-cl1qd7gp2gis73fjje50-a.oregon-postgres.render.com/postgress_2fvz'

db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    goals = db.Column(db.Integer)

@app.route('/')
def index():
    players = Player.query.order_by(Player.goals.desc()).limit(5).all()

    return render_template('index.html', players=players)

@app.route('/add_player', methods=['POST'])
def add_player():
    name = request.form['name']

    goals = int(request.form['goals'])

    # Check if the player already exists in the database
    existing_player = Player.query.filter_by(name=name).first()

    if existing_player:
        # If the player already exists, update their goals
        existing_player.goals += goals
    else:
        # If the player doesn't exist, create a new entry
        player = Player(name=name, goals=goals)
        db.session.add(player)

    db.session.commit()

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
