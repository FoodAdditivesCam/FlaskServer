# models.py
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, String, DateTime

db = SQLAlchemy()
basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')
engine = create_engine('sqlite:///'+dbfile, echo=False) # sqlite:///D:/2021/GradProject/FlaskServer/db.sqlite
table_name = 'Raw_material_info'

class Raw_material_info(db.Model):
    __tablename__ = 'Raw_material_info'

    id = db.Column(db.Integer, primary_key=True)#db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text(), default="")
    tag1 = db.Column(db.String(256), default="")
    tag2 = db.Column(db.String(256), default="")
    tag3 = db.Column(db.String(256), default="")
    tag4 = db.Column(db.String(256), default="")
    tag5 = db.Column(db.String(256), default="")
    reference = db.Column(db.String(256), default="")
    link = db.Column(db.Text(), default="")

    def __init__(self, id, name,description, tag1,tag2,tag3,tag4,tag5,reference,link):
        self.id =id
        self.name = name
        self.description = description
        self.tag1 = tag1
        self.tag2 = tag2
        self.tag3 = tag3
        self.tag4 = tag4
        self.tag5 = tag5
        self.reference = reference
        self.link = link

def data_update():
    data = pd.read_csv(r'D:\2021\GradProject\Data\db_0806_filter.csv', encoding='cp949')
    data.to_sql(
        'Raw_material_info',
        engine,
        if_exists='append', #'replace',
        index=False,
        chunksize=500,
        dtype={
            "id": Integer, #db.Column(db.String(256), primary_key=True),
            "name": String(256),
            "description": Text,
            "tag1": String(256),
            "tag2": String(256),
            "tag3": String(256),
            "tag4": String(256),
            "tag5": String(256),
            "reference": String(256),
            "link": Text,
        }
    )

def get_db_data(input):
    final_df=pd.DataFrame(columns=['id','name','description', 'tag1', 'tag2', 'tag3', 'tag4','tag5', 'reference', 'link'])
    for i in input:
        sql_df = pd.read_sql(
            "SELECT * FROM Raw_material_info WHERE name='"+i+"'",
            con=engine
        )
        final_df = pd.concat([final_df,sql_df])
    final_dic = final_df.to_dict('records')
    return final_dic