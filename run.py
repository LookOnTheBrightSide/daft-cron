"""
Flask application to serve json for consumption in vue
Application uses the Daftlistings module
"""
import json
import requests
import sqlite3
import time
import logging
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, render_template, jsonify, request, url_for, redirect
from daftlistings import Daft, CommercialType, RentType
from celery import Celery
from celery.task import task

app = Celery('app', broker='amqp://localhost//')
celery = Celery()
celery.config_from_object('celery_config')
scheduler = BackgroundScheduler()

conn = sqlite3.connect(":memory:", check_same_thread = False)
c = conn.cursor()

def create_table():
    conn.execute('CREATE TABLE IF NOT EXISTS listingsAppliedTo(listingID TEXT PRIMARY KEY UNIQUE, listingLink TEXT UNIQUE)')
    print('created table')


def data_entry(listingID,listingLink):
    print('SQL - inserting data into database')
    params = (listingID, listingLink)
    c.execute("INSERT INTO listingsAppliedTo VALUES(?,?)", params)
    conn.commit()


create_table()


def userSearchCriteria(county, rent_type, min_amount, max_amount):
    daft = Daft()
    daft.set_county(county)
    daft.set_listing_type(RentType[rent_type])
    daft.set_min_price(min_amount)
    daft.set_max_price(max_amount)
    print('running search ...')
    return daft.search()


def listing_mailer(listings, form_name, form_phone, form_email, form_message):
    
    for listing in listings:
        sql = "SELECT listingID FROM listingsAppliedTo"
        c.execute(sql)
        my_listings = c.fetchall()

        for entry in my_listings:
            if str(listing.id) != str(entry[0]):
                print(listing.id, listing.daft_link)
                data_entry(listing.id, listing.daft_link)
                # listing.contact_advertiser(
                #     name = form_name,
                #     contact_number = form_phone,
                #     email = form_email,
                #     message = form_message
                # )
                print('***  mailing contact   ***')

    print('exiting listing mailer ...')
    return

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'POST':
        form_name = request.form['name']
        form_email = request.form['email']
        form_phone = request.form['phone']
        min_amount = int(request.form['minAmount'])
        max_amount = int(request.form['maxAmount'])
        rent_type = request.form['accType']
        county = request.form['location']
        form_message = request.form['message']

        @task
        def job():
            print("Scheduler running ...")
            listings = userSearchCriteria(county, rent_type, min_amount, max_amount)
            listing_mailer(listings, form_name, form_phone, form_email, form_message)

        scheduler.start()   
        scheduler.add_job(
            func=job,
            trigger=IntervalTrigger(minutes=5),
            id='printing_job',
            name='check daft for new ads and email the contact',
            replace_existing=True)
        return render_template('success.html', name=form_name, email=form_email)

    return render_template('index.html')

atexit.register(lambda: scheduler.shutdown())


