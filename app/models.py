from datetime import datetime
from . import db

docAttributes = db.Table('docAttributes',
	db.Column('document_id', db.Integer, db.ForeignKey('documents.id')),
	db.Column('field_id', db.Integer, db.ForeignKey('fields.id')))
	
docTagging = db.Table('docTagging',
	db.Column('document_id', db.Integer, db.ForeignKey('documents.id')),
	db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))

userMessages = db.Table('userMessages',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('message_id', db.Integer, db.ForeignKey('messages.id')))

userMatters - db.Table('userMatters',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('matter_id', db.Integer, db.ForeignKey('matters.id')))

class Document(db.Model):
	__tablename__ = 'documents'
	id = db.Column(db.Integer, primary_key=True)
	fields = db.relationship('Field', secondary = docAttributes, backref=db.backref('documents', lazy='dynamic'), lazy='dynamic') 
	tags = db.relationship('Tag', secondary = docTagging, backref=db.backref('documents', lazy='dynamic'), lazy='dynamic')
	matter_id = db.Column(db.Integer, db.ForeignKey('matters.id'))
	messages = db.relationship('Message', backref='document', lazy='dynamic')
	metadata = db.relationship('Metadatum', backref='document', lazy='dynamic')
	
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
	inMessages = db.relationship('Message', secondary = userMessages, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
	sentMessages = db.relationship('Message', backref='author', lazy='dynamic')
	matters = db.relationship('Matter', secondary = userMatters, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
	
class Tag(db.Model):
	__tablename__ = 'tags'
	id
	name
	description
	matter
	documents
	
class Message(db.Model):
	__tablename__ = 'messages'
	id
	matter
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	recipients = db.relationship('User', secondary = userMessages, backref=db.backref('recipients', lazy='dynamic'), lazy='dynamic')
	document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
	content
	timestamp
	
class Query(db.Model):
	__tablename__ = 'queries'
	id
	name
	matter
	documents
	
class Client(db.Model):
	__tablename__ = 'clients'
	id
	number
	name
	matters

class Matter(db.Model):
	__tablename__ = 'matters'
	id
	active
	number
	name
	client
	documents = db.relationship('Document', backref='matter', lazy='dynamic')
	users = db.relationship('User', seconary = userMatters, backref=db.backref('matters', lazy='dynamic'), lazy='dynamic')
	queries
	messages
	tags

class Metadatum(db.Model):
	__tablename__ = 'metadata'
	id
	value
	field_id = db.Column(db.Integer, db.ForeignKey('fields.id'))
	document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
	
	
	
	


	
