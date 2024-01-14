from flask import request, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


def login(get_db):
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']

        if not user_email or not user_password:
            flash('Both email and password are required.', 'error')
            return redirect(url_for('handle_login'))

        conn, cursor = get_db

        cursor.execute("SELECT email, password FROM users WHERE email=? AND password=?", (user_email, user_password))
        user = cursor.fetchone()

        if user:
            flash('Login successful!', 'success')
            return render_template('gen.html')
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('handle_login'))

    return render_template('login.html')


def signup(get_db,user_name,user_email,user_password):
    if request.method == 'POST':
        # user_name = request.form['name']
        # user_email = request.form['email']
        # user_password = request.form['password']

        if not user_name or not user_email or not user_password:
            flash('All fields are required.', 'error')
            return redirect(url_for('handle_signup'))

        conn, cursor = get_db

        # Check if the email is already registered
        cursor.execute("SELECT email FROM users WHERE email=?", (user_email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('handle_signup'))
        else:
            # Hash the password before storing it in the database
            
            #hashed_password = generate_password_hash(user_password, method='sha256')

            # Insert the new user into the database
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (user_name, user_email, user_password))
            conn.commit()

            flash('Signup successful! You can now log in.', 'success')
            return True

    return render_template('index.html')


