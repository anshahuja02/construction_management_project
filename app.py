from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Database Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3306,
    password="ANSH9900",
    database="construction_project_management"
)

cursor = db.cursor()

# Route for displaying all projects


@app.route('/')
def index():
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    return render_template('index.html', projects=projects)

# Route for creating a new project


@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        budget = float(request.form['budget'])
        status = request.form['status']

        sql = "INSERT INTO projects (name, location, start_date, end_date, budget, status) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (name, location, start_date,
                       end_date, budget, status))
        db.commit()
        return redirect(url_for('index'))

    return render_template('create_project.html')

# Route for displaying tasks of a project


@app.route('/project/<int:project_id>')
def project(project_id):
    sql = "SELECT * FROM projects WHERE id=%s"
    cursor.execute(sql, (project_id,))
    project = cursor.fetchone()

    sql = "SELECT * FROM tasks WHERE project_id=%s"
    cursor.execute(sql, (project_id,))
    tasks = cursor.fetchall()

    return render_template('project.html', project=project, tasks=tasks)

# Route for creating a new task for a project


@app.route('/project/<int:project_id>/create_task', methods=['GET', 'POST'])
def create_task(project_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        status = request.form['status']

        sql = "INSERT INTO tasks (project_id, name, description, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (project_id, name, description,
                       start_date, end_date, status))
        db.commit()
        return redirect(url_for('project', project_id=project_id))

    return render_template('create_task.html', project_id=project_id)

# Route for editing a task


@app.route('/project/<int:project_id>/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(project_id, task_id):
    sql = "SELECT * FROM tasks WHERE id=%s AND project_id=%s"
    cursor.execute(sql, (task_id, project_id))
    task = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        status = request.form['status']

        sql = "UPDATE tasks SET name=%s, description=%s, start_date=%s, end_date=%s, status=%s WHERE id=%s AND project_id=%s"
        cursor.execute(sql, (name, description, start_date,
                       end_date, status, task_id, project_id))
        db.commit()
        return redirect(url_for('project', project_id=project_id))

    return render_template('edit_task.html', project_id=project_id, task_id=task_id, task=task)


@app.route('/project/<int:project_id>/delete_task/<int:task_id>', methods=['GET', 'POST'])
def delete_task(project_id, task_id):
    sql = "SELECT * FROM tasks WHERE id=%s AND project_id=%s"
    cursor.execute(sql, (task_id, project_id))
    task = cursor.fetchone()

    if request.method == 'POST':
        sql = "DELETE FROM tasks WHERE id=%s AND project_id=%s"
        cursor.execute(sql, (task_id, project_id))
        db.commit()
        return redirect(url_for('project', project_id=project_id))

    return render_template('delete_task.html', project_id=project_id, task_id=task_id, task=task)

# ... Other imports and code ...

# Route for deleting a project


@app.route('/project/<int:project_id>/delete_project', methods=['GET', 'POST'])
def delete_project(project_id):
    sql = "SELECT * FROM projects WHERE id=%s"
    cursor.execute(sql, (project_id,))
    project = cursor.fetchone()

    if request.method == 'POST':
        # Delete all tasks associated with the project
        sql = "DELETE FROM tasks WHERE project_id=%s"
        cursor.execute(sql, (project_id,))
        # Delete the project
        sql = "DELETE FROM projects WHERE id=%s"
        cursor.execute(sql, (project_id,))
        db.commit()
        return redirect(url_for('index'))

    return render_template('delete_project.html', project=project)


if __name__ == '__main__':
    app.run(debug=True)
