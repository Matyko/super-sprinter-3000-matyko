from peewee import *
from connect import ConnectDatabase
from models import Stories
from flask import Flask, request,  g, redirect, url_for, \
    render_template, flash


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key'
))
app.config.from_envvar('SPRINTER_SETTINGS', silent=True)


def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.create_tables([Stories], safe=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route('/')
@app.route('/list')
def show_list():
    stories = Stories.select().order_by(Stories.id.asc())
    return render_template('list.html', stories=stories)


@app.route('/story', methods=['GET', 'POST'])
def show_form():
    return render_template('form.html', mode='save', story=0)


@app.route('/add', methods=['GET', 'POST'])
def add_story():
    print(request.form)
    if request.form['submit_type'] == 'save':
        new_story = Stories.create(story_name=request.form.get('story_name'),
                                   user_story=request.form.get('user_story'),
                                   acceptance_criteria=request.form.get('acceptance_criteria'),
                                   business_value=request.form.get('business_value'),
                                   estimation=request.form.get('estimation'),
                                   status=request.form.get('status')
                                   )
        new_story.save()
        flash('New story saved')
    elif request.form['submit_type'] == 'update':
        story_to_modify = Stories.select().where(Stories.id == request.form['story_id'])
        for story in story_to_modify:
            story.story_name = request.form.get('story_name')
            story.user_story = request.form.get('user_story')
            story.acceptance_criteria = request.form.get('acceptance_criteria')
            story.business_value = request.form.get('business_value')
            story.estimation = request.form.get('estimation')
            story.status = request.form.get('status')
            story.save()
            flash('Story modified')
    return redirect(url_for('show_list'))


@app.route('/story/<story_id>', methods=['GET', 'POST'])
def show_update_form(story_id):
    stories = Stories.select().where(Stories.id == story_id)
    for story in stories:
        return render_template('form.html', story=story, mode='update')


@app.route('/del/<story_id>', methods=['GET', 'POST'])
def delete_story(story_id):
    stories = Stories.select().where(Stories.id == story_id)
    for story in stories:
        story.delete_instance()
    return redirect(url_for('show_list'))


if __name__ == '__main__':
    init_db()
    app.run()
