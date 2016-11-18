from datetime import datetime
from . import db

class Document(db.Model):
	__tablename__ = 'documents'
	id 
	fields
	tags
	matter
	messages
	
class Field(db.Model):
	__tablename__ = 'fields'
	id
	documents
	name
	values
	type
	
class User(db.Model):
	__tablename__ = 'users'
	id
	name
	handle
	firm
	email
	permission
	messages
	matters
	
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
	sender
	recipients #search string for handles and add?
	document
	content
	timestamp
	
class Query(db.Model):
	__tablename__ = 'queries'
	id
	matter
	documents
	


	
