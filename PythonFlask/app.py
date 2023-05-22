from flask import Flask,render_template, request, redirect,url_for,flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

registros =[]
userRegistros =[]

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cursos.db"
db.init_app(app)

class cursos(db.Model):
     
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)
    
    def __init__(self, nome, descricao,ch):
         self.nome=nome
         self.descricao =descricao
         self.ch =ch
         

@app.route('/', methods= ["POST", "GET"])
def cadastroLogin(): 
     
     if request.method =='POST':
          
          if request.form.get("email") and request.form.get("senha"):
               
               userRegistros.append({"email": request.form.get('email'),"senha": request.form.get("senha")})

     return render_template('index.html',userRegistros=userRegistros)


@app.route('/sobre', methods=["POST","GET"])

def sobre(): 
     if request.method =='POST':
          if request.form.get("aluno") and request.form.get("nota"):
             
             registros.append({"aluno": request.form.get("aluno"),"nota": request.form.get("nota") })  
          
     return render_template('sobre.html',  registros =registros)


@app.route('/filmes')

def filmes(): 
     url = 'https://api.themoviedb.org/3/movie/550?api_key=0e7423b403e951fb10ace6e5b54d06c9'
     response = urllib.request.urlopen(url)
     data = response.read()
     jsondata =json.loads(data)
          
     # return jsondata
     return render_template('filmes.html',  filmes=jsondata["production_companies"])

@app.route('/cursos')
def listaCursos():
     page = request.args.get('page', 1, type=int)
     per_page =4
     todos_cursos = cursos.query.paginate(page=page, per_page=per_page)
     
     return render_template('cursos.html', cursos=todos_cursos)

@app.route('/cria_curso', methods=['POST', 'GET'])
def cria_curso():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    ch = request.form.get('ch')

    if request.method == "POST":
        if not nome or not descricao or not ch:
            flash('Preencha todos os campos do formulario')
        else:
            
            curso_existente = cursos.query.filter_by(nome=nome).first()
            if curso_existente:
               
                flash('O nome do curso já está cadastrado')
            else:
                
                curso = cursos(nome, descricao, ch)
                db.session.add(curso)
                db.session.commit()
                return redirect(url_for('listaCursos'))
           
    return render_template('cadastro_curso.html')


@app.route('/<int:id>/atualiza_curso', methods=["POST", "GET"])
def atualiza_curso(id):
     curso = cursos.query.filter_by(id=id).first()
     if request.method =='POST':
          nome = request.form["nome"]
          descricao = request.form["descricao"]
          ch = request.form["ch"]
     
          cursos.query.filter_by(id=id).update({"nome":nome,"descricao": descricao, "ch":ch})
          db.session.commit()
          return redirect(url_for('listaCursos'))
          
     return render_template('atualiza_curso.html', curso=curso)

@app.route('/<int:id>/excluir')
def excluir(id):
     
     curso = cursos.query.filter_by(id=id).first()
     db.session.delete(curso)
     db.session.commit()
     
     return redirect(url_for('listaCursos'))     
     
if (__name__ == "__main__"):
     
     with app.app_context():
          db.create_all()
     
     app.run(debug=True)
     

