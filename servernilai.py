from flask import Flask, render_template, request
import urllib.request, json

from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# Format: mysql://[username]:[password]@[host]:[port]/[database]'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/seluruh_nilai'

db = SQLAlchemy(app)

class Score(db.Model):
    __tablename__ = "hasil"

    id = db.Column(db.Integer, primary_key=True)
    id_siswa = db.Column(db.Integer,  nullable=False)
    nama = db.Column(db.String(255), nullable=False)
    nrp = db.Column(db.String(30),  nullable=False)
    Fisika = db.Column(db.String(255),  nullable=False)
    Kimia = db.Column(db.String(255),  nullable=False)
    Matematika = db.Column(db.String(255),  nullable=False)
    Biologi = db.Column(db.String(255),  nullable=False)
    Agama = db.Column(db.String(255),  nullable=False)
    BahasaInd = db.Column("Bahasa Indonesia", db.String(255),  nullable=False)
    BahasaIng = db.Column("Bahasa Inggris", db.String(255),  nullable=False)

score_fields = {
    'id': fields.Integer,
    'id_siswa': fields.Integer,
    'nrp': fields.String,
    'nama': fields.String,
    'Fisika': fields.String,
    'Kimia': fields.String,
    'Matematika': fields.String,
    'Biologi': fields.String,
    'Agama': fields.String,
    'BahasaInd': fields.String,
    'BahasaIng': fields.String
}

score_post_args = reqparse.RequestParser()
score_post_args.add_argument("id", type=int, required=True)
score_post_args.add_argument("nama", type=str, required=True)
score_post_args.add_argument("id_siswa", type=int, required=True)
score_post_args.add_argument("Fisika", type=str, required=True)
score_post_args.add_argument("Kimia", type=str, required=True)
score_post_args.add_argument("Matematika", type=str, required=True)
score_post_args.add_argument("Biologi", type=str, required=True)
score_post_args.add_argument("Agama", type=str, required=True)
score_post_args.add_argument("BahasaInd", type=str, required=True)
score_post_args.add_argument("BahasaIng", type=str, required=True)
score_post_args.add_argument("nrp", type=str, required=True)

score_put_args = reqparse.RequestParser()
score_put_args.add_argument("id", type=int, required=True)
score_put_args.add_argument("nama", type=str, required=True)
score_put_args.add_argument("id_siswa", type=int, required=True)
score_put_args.add_argument("Fisika", type=str, required=True)
score_put_args.add_argument("Kimia", type=str, required=True)
score_put_args.add_argument("Matematika", type=str, required=True)
score_put_args.add_argument("Biologi", type=str, required=True)
score_put_args.add_argument("Agama", type=str, required=True)
score_put_args.add_argument("BahasaInd", type=str, required=True)
score_put_args.add_argument("BahasaIng", type=str, required=True)
score_put_args.add_argument("nrp", type=str, required=True)


@api.resource('/hasil_nilai/', '/hasil_nilai/<int:siswa_id>', '/hasil_nilai/<string:search>')
# @api.resource('/hasil_nilai/', '/hasil_nilai/<int:siswa_id>')
class Result_Resource(Resource):
    @marshal_with(score_fields)
    def get(self, siswa_id=None, search=None):
    # def get(self, siswa_id=None):
        if search:
            # result = Score.query.filter(Score.nama.like(f"%{search}%")).first()
            result = Score.query.filter(Score.nama.like(f"%{search}%")).limit(70).all()
            print(result)
            return result

        if not siswa_id:
            return Score.query.limit(20).all()

        result = Score.query.filter_by(id_siswa=siswa_id).first()

        if not result:
            abort(404, message=f"Siswa dengan ID {siswa_id} tidak ditemukan")

        return result

    @marshal_with(score_fields)
    def post(self, siswa_id=None):
        if siswa_id:
            abort(400, message="Bad Request")

        args = score_post_args.parse_args()

        result = Score(nama=args['nama'], id_siswa=args['id_siswa'], nrp=args['nrp'], id_mapel=args['id_mapel'], score=args['score'])

        db.session.add(result)
        db.session.commit()
        return result, 201

    @marshal_with(score_fields)
    def put(self, siswa_id=None):
        if not siswa_id:
            abort(400, message=f"ID siswa tidak boleh kosong")

        args = score_put_args.parse_args()

        result = Score.query.filter_by(id_siswa=siswa_id).first()

        if not result:
            abort(404, message=f"Siswa dengan ID {siswa_id} tidak ditemukan")

        db.session.commit()

        return result

    @marshal_with(score_fields)
    def delete(self, siswa_id=None):
        if not siswa_id:
            abort(400, message=f"ID siswa tidak boleh kosong")

        deleted = Score.query.filter_by(id_siswa=siswa_id).delete()

        if not deleted:
            abort(404, message=f"Siswa dengan ID {siswa_id} gagal dihapus, cek apa ID sudah benar")

        db.session.commit()
        return None, 204
    
@app.route("/cbt/") #endpoint browser
def get_results():
    args = request.args
    search = args.get("search")

    url = "http://localhost:5000/hasil_nilai/" #api

    if search:
        url = f"http://localhost:5000/hasil_nilai/{search}"

    response = urllib.request.urlopen(url) #request yang dikirim ke server
    data = response.read() #isi dari responnya
    dict = json.loads(data)
    # print(dict)
    return render_template ("index.html", tampilans=dict)

@app.route("/cbt/<string:search>") #endpoint browser
def search_results(search):
    print (search)
    url = f"http://localhost:5000/hasil_nilai/{search}"

    response = urllib.request.urlopen(url) #request yang dikirim ke server
    data = response.read() #isi dari responnya
    dict = json.loads(data)
    # print(dict)
    return render_template ("index.html", tampilans=dict)

@app.route("/cbt/<int:siswa_id>") #endpoint browser
def get_result(siswa_id=None):
    url = f"http://localhost:5000/hasil_nilai/{siswa_id}" #api

    response = urllib.request.urlopen(url) #request yang dikirim ke server
    data = response.read() #isi dari responnya
    dict = json.loads(data)
    # print(dict)
    return render_template ("index2.html", tampilan=dict)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
