from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# fake_database = {
#     1: {'name': 'Clean car'},
#     2: {'name': 'Write blog'},
#     3: {'name': 'Start stream'},
# }

tasks_fields = {
    'id': fields.Integer,
    'name': fields.String
}


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return self.name


db.create_all()


class Items(Resource):
    @marshal_with(tasks_fields)
    def get(self):
        all_task = Task.query.all()
        return all_task

    @marshal_with(tasks_fields)
    def post(self):
        data = request.json
        # item_id = len(fake_database) + 1
        # fake_database[item_id] = {'name': data['name']}

        new_task = Task(name=data['name'])
        db.session.add(new_task)
        db.session.commit()

        all_task = Task.query.all()

        return all_task


api.add_resource(Items, '/')


class Item(Resource):
    @marshal_with(tasks_fields)
    def get(self, pk):
        task = Task.query.get(pk)
        return task

    @marshal_with(tasks_fields)
    def put(self, pk):
        data = request.json
        # fake_database[pk]['name'] = data['name']
        task = Task.query.get(pk)
        task.name = data['name']
        db.session.commit()

        all_task = Task.query.all()

        return all_task

    @marshal_with(tasks_fields)
    def delete(self, pk):
        # del fake_database[pk]
        task = Task.query.get(pk)
        db.session.delete(task)
        db.session.commit()

        all_task = Task.query.all()

        return all_task


api.add_resource(Item, '/<int:pk>')


if __name__ == '__main__':
    app.run(debug=True)
