//= Use pipenv for python packaging

//* Schema
// Pydantic Schema's are used for validating data along with serializing (JSON -> Python) and de-serializing (Python -> JSON). It does not serve as a Mongo schema validator, in other words.

//= create schemas with Config meta class
// Config meta class may contain extra informations
//! read pydantic docs for more detail

//= create updateModel differently from the real model, update model can be used everytime

//* Setting up mongodb
//? for async support we have to use motor, pymongo is synchronous
//! motor does contain pymongo as a dependency library
// When the first I/O operation is made, both the database and collection will be created if they don't already exist.

//* creating CRUD api
//= step 1: create models for your application
// use pydantic docs for better models

//= step 2: create functions that will do CRUD operations, inside database.py
// create all the important functions that will be used for doing CRUD

//= step 3: use this utility function inside routes of your app
// inside routes folder create route for each work
