from datetime import datetime
from . import db
from config import HOME_FIRM

docAttributes = db.Table('docAttributes',
	db.Column('document_id', db.Integer, db.ForeignKey('documents.id')),
	db.Column('field_id', db.Integer, db.ForeignKey('fields.id')))
	
docTagging = db.Table('docTagging',
	db.Column('document_id', db.Integer, db.ForeignKey('documents.id')),
	db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))

userMessages = db.Table('userMessages',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('message_id', db.Integer, db.ForeignKey('messages.id')))

userMatters = db.Table('userMatters',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('matter_id', db.Integer, db.ForeignKey('matters.id')))

foundDocs = db.Table('foundDocs',
	db.Column('document_id', db.Integer, db.ForeignKey('documents.id')),
	db.Column('query_id', db.Integer, db.ForeignKey('queries.id')))
	
class Document(db.Model):
	__tablename__ = 'documents'
	id = db.Column(db.Integer, primary_key=True)
	fields = db.relationship('Field', secondary = docAttributes, backref=db.backref('documents', lazy='dynamic'), lazy='dynamic') 
	tags = db.relationship('Tag', secondary = docTagging, backref=db.backref('documents', lazy='dynamic'), lazy='dynamic')
	matter_id = db.Column(db.Integer, db.ForeignKey('matters.id'))
	messages = db.relationship('Message', backref='document', lazy='dynamic')
	metadata = db.relationship('Metadatum', backref='document', lazy='dynamic')
	queries = db.relationship('Query', secondary = foundDocs, backref=db.backref('documents', lazy='dynamic'), lazy='dynamic')
	
class Field(db.Model):
	__tablename__ = 'fields'
	id = db.Column(db.Integer, primary_key=True)
	documents = db.relationship('Document', secondary = docAttributes, backref=db.backref('fields', lazy='dynamic'), lazy='dynamic')
	name = db.Column(db.String(128))
	values = db.relationship('Metadatum', backref='field', lazy='dynamic')
	#consider a type attribute here
	
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	password_hash = db.Column(db.String(128))
	handle = db.Column(db.String(64), unique=True)
	firm = db.Column(db.String(128), default=HOME_FIRM)
	email = db.Column(db.String(64))
	permission = db.Column(db.Integer)
	queries = db.relationship('Query', backref='creator', lazy='dynamic')
	inMessages = db.relationship('Message', secondary = userMessages, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
	sentMessages = db.relationship('Message', backref='author', lazy='dynamic')
	matters = db.relationship('Matter', secondary = userMatters, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
	
class Tag(db.Model):
	__tablename__ = 'tags'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	description = db.Column(db.String(256))
	matter_id = db.Column(db.Integer, db.ForeignKey('matters.id'))
	documents = db.relationship('Document', secondary = docTagging, backref=db.backref('tags', lazy='dynamic'), lazy='dynamic')
	isParent = db.Column(db.Boolean)
	
class Message(db.Model):
	__tablename__ = 'messages'
	id = db.Column(db.Integer, primary_key=True)
	matter_id = db.Column(db.Integer, db.ForeignKey('matters.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	recipients = db.relationship('User', secondary = userMessages, backref=db.backref('recipients', lazy='dynamic'), lazy='dynamic')
	document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
	content = db.Column(db.String(256))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	
class Query(db.Model):
	__tablename__ = 'queries'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	matter_id = db.Column(db.Integer, db.ForeignKey('matters.id'))
	documents = db.relationship('Document', secondary = foundDocs, backref=db.backref('documents', lazy='dynamic'), lazy='dynamic')
	creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	isPrivate = db.Column(db.Boolean)
	
class Client(db.Model):
	__tablename__ = 'clients'
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Integer)
	name = db.Column(db.String(128))
	matters = db.relationship('Matter', backref='client', lazy='dynamic')

class Matter(db.Model):
	__tablename__ = 'matters'
	id = db.Column(db.Integer, primary_key=True)
	active = db.Column(db.Boolean)
	number = db.Column(db.Integer)
	name = db.Column(db.String(128))
	client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
	documents = db.relationship('Document', backref='matter', lazy='dynamic')
	users = db.relationship('User', seconary = userMatters, backref=db.backref('matters', lazy='dynamic'), lazy='dynamic')
	queries = db.relationship('Query', backref='matter', lazy=)
	messages = db.relationship('Message', backref='matter', lazy='dynamic')
	tags = db.relationship('Tag', backref='matter', lazy='dynamic')

class Metadatum(db.Model):
	__tablename__ = 'metadata'
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.Text)
	field_id = db.Column(db.Integer, db.ForeignKey('fields.id'))
	document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
	
	
	
	


	
