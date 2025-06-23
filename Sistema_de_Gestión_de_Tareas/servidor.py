from flask import Flask, request, jsonify, make_response, render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    completada = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Login required', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
        user = Usuario.query.filter_by(usuario=auth.username).first()
        if not user or not check_password_hash(user.contraseña, auth.password):
            return make_response('Credenciales inválidas', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
        return f(user, *args, **kwargs)
    return decorated

@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    if not data or not data.get('usuario') or not data.get('contraseña'):
        return jsonify({'mensaje': 'Faltan datos'}), 400
    if Usuario.query.filter_by(usuario=data['usuario']).first():
        return jsonify({'mensaje': 'Usuario ya existe'}), 400
    hashed = generate_password_hash(data['contraseña'], method='pbkdf2:sha256')
    nuevo = Usuario(usuario=data['usuario'], contraseña=hashed)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario registrado correctamente'})

@app.route('/login', methods=['POST'])
@token_required
def login(current_user):
    return jsonify({'mensaje': f'Bienvenido {current_user.usuario}'})

@app.route('/tareas', methods=['GET'])
@token_required
def tareas_welcome(current_user):
    html = f"""
    <h1>Bienvenido, {current_user.usuario}</h1>
    <p>Usa POST, GET, PUT y DELETE en /tareas y /tareas/list para gestionar tareas.</p>
    """
    return render_template_string(html)

@app.route('/tareas', methods=['POST'])
@token_required
def crear_tarea(current_user):
    data = request.get_json()
    nueva = Tarea(descripcion=data['descripcion'], user_id=current_user.id)
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'mensaje': 'Tarea creada', 'tarea': {'id': nueva.id, 'descripcion': nueva.descripcion}})

@app.route('/tareas/list', methods=['GET'])
@token_required
def listar_tareas(current_user):
    tareas = Tarea.query.filter_by(user_id=current_user.id).all()
    salida = [{'id': t.id, 'descripcion': t.descripcion, 'completada': t.completada} for t in tareas]
    return jsonify({'tareas': salida})

@app.route('/tareas/<int:id>', methods=['PUT'])
@token_required
def actualizar_tarea(current_user, id):
    tarea = Tarea.query.filter_by(id=id, user_id=current_user.id).first()
    if not tarea:
        return jsonify({'mensaje': 'Tarea no encontrada'}), 404
    datos = request.get_json()
    tarea.descripcion = datos.get('descripcion', tarea.descripcion)
    tarea.completada = datos.get('completada', tarea.completada)
    db.session.commit()
    return jsonify({'mensaje': 'Tarea actualizada'})

@app.route('/tareas/<int:id>', methods=['DELETE'])
@token_required
def eliminar_tarea(current_user, id):
    tarea = Tarea.query.filter_by(id=id, user_id=current_user.id).first()
    if not tarea:
        return jsonify({'mensaje': 'Tarea no encontrada'}), 404
    db.session.delete(tarea)
    db.session.commit()
    return jsonify({'mensaje': 'Tarea eliminada'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False)
