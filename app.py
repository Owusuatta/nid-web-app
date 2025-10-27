from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import verify_admin, create_admin, init_admin_table, save_citizen
from blockchain import Blockchain
from flask import make_response


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # You can change this to something more secure
init_admin_table()
bc = Blockchain()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if verify_admin(email, password):
            session['admin'] = email
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'admin' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = {
            "full_name": request.form['full_name'],
            "dob": request.form['dob'],
            "gender": request.form['gender'],
            "address": request.form['address'],
            "national_id": request.form['national_id']
        }
        bc.add_block(data)
        last_block = bc.chain[-1]
        save_citizen(last_block.data, last_block.timestamp)
        flash('Citizen registered successfully')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))
    import sqlite3
    conn = sqlite3.connect("nid_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, dob, gender, address, national_id, timestamp FROM citizens")
    citizens = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', citizens=citizens)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    result = None
    if request.method == 'POST':
        query = request.form['query']
        field = request.form['field']
        import sqlite3
        conn = sqlite3.connect("nid_system.db")
        cursor = conn.cursor()
        if field == 'national_id':
            cursor.execute("SELECT * FROM citizens WHERE national_id = ?", (query,))
        else:
            cursor.execute("SELECT * FROM citizens WHERE full_name LIKE ?", ('%' + query + '%',))
        result = cursor.fetchone()
        conn.close()
    return render_template('verify.html', result=result)

@app.route('/edit/<nid>', methods=['GET', 'POST'])
def edit_citizen(nid):
    import sqlite3
    conn = sqlite3.connect("nid_system.db")
    cursor = conn.cursor()
    if request.method == 'POST':
        full_name = request.form['full_name']
        dob = request.form['dob']
        gender = request.form['gender']
        address = request.form['address']
        cursor.execute("""
            UPDATE citizens SET full_name=?, dob=?, gender=?, address=?
            WHERE national_id=?
        """, (full_name, dob, gender, address, nid))
        conn.commit()
        conn.close()
        flash('Citizen updated successfully')
        return redirect(url_for('dashboard'))
    else:
        cursor.execute("SELECT full_name, dob, gender, address FROM citizens WHERE national_id=?", (nid,))
        citizen = cursor.fetchone()
        conn.close()
        return render_template('edit.html', citizen=citizen, nid=nid)
@app.route('/delete/<nid>')
def delete_citizen(nid):
    import sqlite3
    conn = sqlite3.connect("nid_system.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM citizens WHERE national_id = ?", (nid,))
    conn.commit()
    conn.close()
    flash("Citizen deleted successfully.")
    return redirect(url_for('dashboard'))
@app.route('/export_csv')
def export_csv():
    import csv, io, sqlite3
    conn = sqlite3.connect("nid_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM citizens")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Full Name', 'DOB', 'Gender', 'Address', 'National ID', 'Timestamp'])
    writer.writerows(rows)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=citizens.csv"
    response.headers["Content-type"] = "text/csv"
    return response
@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():
    if 'admin' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_email = request.form['new_email']
        new_password = request.form['new_password']
        old_email = session['admin']
        import sqlite3
        conn = sqlite3.connect("nid_system.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE admins SET email=?, password=? WHERE email=?", (new_email, new_password, old_email))
        conn.commit()
        conn.close()
        session['admin'] = new_email  # update session
        flash("Admin profile updated successfully.")
        return redirect(url_for('dashboard'))
    return render_template('admin_profile.html', current_email=session['admin'])



@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
