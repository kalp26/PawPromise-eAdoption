import io
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, redirect, url_for,flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'pawpromise'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pawpromise'

IMAGE_FOLDER = "C:/Desktop/pawpromise/pawpromise/static/uploads"



mysql = MySQL(app)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# Users route
@app.route("/users")
def users():
    try:
        cursor = mysql.connection.cursor()

        # Fetch user details, concatenating first_name and last_name
        cursor.execute("""
            SELECT id, CONCAT(first_name, ' ', last_name) AS full_name, gender, phone, email, city, state FROM users
        """)
        users_data = cursor.fetchall()
        cursor.close()

        # Convert fetched data into a list of dictionaries
        users_list = []
        for user in users_data:
            users_list.append({
                "id": user[0],
                "name": user[1],
                "gender": user[2],
                "phone": user[3],
                "email": user[4],
                "city": user[5],
                "state": user[6]
            })

        return render_template("user.html", users=users_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE User Route
@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"success": True, "message": "User deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Fetch All Organizations
@app.route("/organizations")
def organizations():
    try:
        cursor = mysql.connection.cursor()

        # Fetch organization details
        cursor.execute("""
            SELECT id, org_name, org_type, phone, email, state, city, status, 
                   website, social_media, address, reg_number, years_operation, 
                   emergency_contact, reg_certificate, tax_certificate, 
                   rep_name, rep_id_proof, mission
            FROM organizations
        """)
        organizations_data = cursor.fetchall()
        cursor.close()

        # Convert fetched data into a list of dictionaries
        organizations_list = []
        for organization in organizations_data:
            organizations_list.append({
                "id": organization[0],
                "org_name": organization[1],
                "org_type": organization[2],
                "phone": organization[3],
                "email": organization[4],
                "state": organization[5],
                "city": organization[6],
                "status": organization[7],
                "website": organization[8],
                "social_media": organization[9],
                "address": organization[10],
                "reg_number": organization[11],
                "years_operation": organization[12],
                "emergency_contact": organization[13],
                "reg_certificate": organization[14],
                "tax_certificate": organization[15],
                "rep_name": organization[16],
                "rep_id_proof": organization[17],
                "mission": organization[18]
            })

        return render_template("organization.html", organizations=organizations_list)
    except Exception as e:
        return str(e)

def create_notification(recipient_id, recipient_type, message, notification_type, reference_id, reference_type):
    """
    Create a notification for a user or organization
    
    Args:
        recipient_id: ID of the recipient
        recipient_type: 'user' or 'organization'
        message: Notification message
        notification_type: Type of notification (status_change, etc)
        reference_id: ID of the referenced item (pet_id, event_id, etc)
        reference_type: Type of reference (pet, event, fundraiser, etc)
    """
    cur = mysql.connection.cursor()
    
    if recipient_type == 'user':
        cur.execute(
            "INSERT INTO notifications (user_id, message, type, reference_id, reference_type) VALUES (%s, %s, %s, %s, %s)",
            (recipient_id, message, notification_type, reference_id, reference_type)
        )
    else:  # organization
        cur.execute(
            "INSERT INTO notifications (org_id, message, type, reference_id, reference_type) VALUES (%s, %s, %s, %s, %s)",
            (recipient_id, message, notification_type, reference_id, reference_type)
        )
    
    mysql.connection.commit()
    cur.close()

@app.route("/update_organization_status/<int:org_id>/<status>", methods=["POST"])
def update_organization_status(org_id, status):
    try:
        # Validate status
        if status not in ['verified', 'pending', 'rejected']:
            return jsonify({"success": False, "message": "Invalid status"})
            
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE organizations 
            SET status = %s 
            WHERE id = %s
        """, (status, org_id))
        mysql.connection.commit()
        
        # Create notification for organization
        message = f"Your organization verification has been {status}"
        create_notification(org_id, 'organization', message, 'status_change', org_id, 'organization')
        
        cursor.close()
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# DELETE Organization Route
@app.route("/delete_organization/<int:organization_id>", methods=["POST"])
def delete_organization(organization_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM organizations WHERE id = %s", (organization_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"success": True, "message": "Organization deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/verified_organizations")
def verified_organizations():
    try:
        cursor = mysql.connection.cursor()
        
        # Fetch verified organization details
        cursor.execute("""
            SELECT id, org_name, org_type, phone, email, state, city, status,
                    website, social_media, address, reg_number, years_operation,
                    emergency_contact, reg_certificate, tax_certificate,
                    rep_name, rep_id_proof, mission
            FROM organizations
            WHERE status = 'verified'
        """)
        organizations_data = cursor.fetchall()
        cursor.close()
        
        # Convert fetched data into a list of dictionaries
        organizations_list = []
        for organization in organizations_data:
            organizations_list.append({
                "id": organization[0],
                "org_name": organization[1],
                "org_type": organization[2],
                "phone": organization[3],
                "email": organization[4],
                "state": organization[5],
                "city": organization[6],
                "status": organization[7],
                "website": organization[8],
                "social_media": organization[9],
                "address": organization[10],
                "reg_number": organization[11],
                "years_operation": organization[12],
                "emergency_contact": organization[13],
                "reg_certificate": organization[14],
                "tax_certificate": organization[15],
                "rep_name": organization[16],
                "rep_id_proof": organization[17],
                "mission": organization[18]
            })
        
        return render_template("verified_org.html", organizations=organizations_list)
    except Exception as e:
        return str(e)

@app.route("/pending_organizations")
def pending_organizations():
    try:
        cursor = mysql.connection.cursor()
        
        # Fetch pending organization details with non-null registration numbers
        cursor.execute("""
            SELECT id, org_name, org_type, phone, email, state, city, status,
                    website, social_media, address, reg_number, years_operation,
                    emergency_contact, reg_certificate, tax_certificate,
                    rep_name, rep_id_proof, mission
            FROM organizations
            WHERE status = 'pending' AND reg_number IS NOT NULL
        """)
        organizations_data = cursor.fetchall()
        cursor.close()
        
        # Convert fetched data into a list of dictionaries
        organizations_list = []
        for organization in organizations_data:
            organizations_list.append({
                "id": organization[0],
                "org_name": organization[1],
                "org_type": organization[2],
                "phone": organization[3],
                "email": organization[4],
                "state": organization[5],
                "city": organization[6],
                "status": organization[7],
                "website": organization[8],
                "social_media": organization[9],
                "address": organization[10],
                "reg_number": organization[11],
                "years_operation": organization[12],
                "emergency_contact": organization[13],
                "reg_certificate": organization[14],
                "tax_certificate": organization[15],
                "rep_name": organization[16],
                "rep_id_proof": organization[17],
                "mission": organization[18]
            })
        
        return render_template("pending_org.html", organizations=organizations_list)
    except Exception as e:
        return str(e)

@app.route('/uploads/<path:filename>')
def get_event_poster(filename):
    # Security check - only allow image files
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
        return "Invalid file type", 400
        
    return send_from_directory(IMAGE_FOLDER, filename)


@app.route("/pet-meetups")
def pet_meetups():
    try:
        # Get filter parameters
        event_type = request.args.get('event_type', '')
        status = request.args.get('status', '')
        date_range = request.args.get('date_range', '')
        
        # Build the base query
        query = """
            SELECT id, organizer_id, event_name, event_description, event_datetime, event_duration, event_location,
                   google_maps_link, event_type, allowed_pet_types, pet_limit, max_participants, event_poster,
                   organizer_name, organizer_type, email, phone, address, sponsors, rules, status, user_type
            FROM events
            WHERE 1=1
        """
        query_params = []
        
        # Add filters if provided
        if event_type:
            query += " AND event_type = %s"
            query_params.append(event_type)
            
        if status:
            query += " AND status = %s"
            query_params.append(status)
            
        if date_range:
            current_date = datetime.now().strftime('%Y-%m-%d')
            if date_range == 'today':
                query += " AND DATE(event_datetime) = %s"
                query_params.append(current_date)
            elif date_range == 'week':
                query += " AND YEARWEEK(event_datetime, 1) = YEARWEEK(%s, 1)"
                query_params.append(current_date)
            elif date_range == 'month':
                query += " AND YEAR(event_datetime) = YEAR(%s) AND MONTH(event_datetime) = MONTH(%s)"
                query_params.append(current_date)
                query_params.append(current_date)
        
        # Execute the query
        cursor = mysql.connection.cursor()
        cursor.execute(query, query_params)
        meetups_data = cursor.fetchall()
        cursor.close()

        # Process the data
        meetups_list = [
            {
                "id": meetup[0],
                "organizer_id": meetup[1],
                "event_name": meetup[2],
                "event_description": meetup[3],
                "event_datetime": meetup[4],
                "event_duration": meetup[5],
                "event_location": meetup[6],
                "google_maps_link": meetup[7],
                "event_type": meetup[8],
                "allowed_pet_types": meetup[9],
                "pet_limit": meetup[10],
                "max_participants": meetup[11],
                "event_poster": os.path.basename(meetup[12]) if meetup[12] else None, 
                "organizer_name": meetup[13],
                "organizer_type": meetup[14],
                "email": meetup[15],
                "phone": meetup[16],
                "address": meetup[17],
                "sponsors": meetup[18],
                "rules": meetup[19],
                "status": meetup[20],
                "user_type": meetup[21]
            }
            for meetup in meetups_data
        ]

        return render_template("pet-meetups.html", meetups=meetups_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update-meetup-status/<int:meetup_id>", methods=["POST"])
def update_meetup_status(meetup_id):
    if request.method == "POST":
        try:
            new_status = request.form.get("status")
            
            # Validate the status value
            if new_status not in ["approved", "rejected", "pending"]:
                return jsonify({"success": False, "message": "Invalid status value"}), 400
            
            cursor = mysql.connection.cursor()
            
            # First get the organizer details to send notification
            cursor.execute("SELECT organizer_id, user_type FROM events WHERE id = %s", (meetup_id,))
            event_info = cursor.fetchone()
            if not event_info:
                return jsonify({"success": False, "message": "Event not found"}), 404
                
            organizer_id = event_info[0]
            organizer_type = event_info[1]
            
            # Update the status in the database
            cursor.execute(
                "UPDATE events SET status = %s WHERE id = %s",
                (new_status, meetup_id)
            )
            mysql.connection.commit()
            
            # Create notification for event organizer
            message = f"Your meet-up event has been {new_status}"
            create_notification(organizer_id, organizer_type, message, 'status_change', meetup_id, 'event')
            
            cursor.close()
            
            # Return success response
            status_display = new_status.capitalize()
            return jsonify({
                "success": True, 
                "message": f"Meetup status updated to {status_display} successfully"
            })
            
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
        
@app.route("/meetup/<int:meetup_id>")
def meetup_detail(meetup_id):
    try:
        # Query to get the meetup details
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, organizer_id, event_name, event_description, event_datetime, event_duration, event_location,
                   google_maps_link, event_type, allowed_pet_types, pet_limit, max_participants, event_poster,
                   organizer_name, organizer_type, email, phone, address, sponsors, rules, status
            FROM events
            WHERE id = %s
        """, (meetup_id,))
        
        meetup_data = cursor.fetchone()
        cursor.close()
        
        if not meetup_data:
            flash("Meetup not found", "error")
            return redirect(url_for("pet_meetups"))
        
        # Transform to dictionary
        meetup = {
            "id": meetup_data[0],
            "organizer_id": meetup_data[1],
            "event_name": meetup_data[2],
            "event_description": meetup_data[3],
            "event_datetime": meetup_data[4],
            "event_duration": meetup_data[5],
            "event_location": meetup_data[6],
            "google_maps_link": meetup_data[7],
            "event_type": meetup_data[8],
            "allowed_pet_types": meetup_data[9],
            "pet_limit": meetup_data[10],
            "max_participants": meetup_data[11],
            "event_poster": os.path.basename(meetup_data[12]) if meetup_data[12] else None,
            "organizer_name": meetup_data[13],
            "organizer_type": meetup_data[14],
            "email": meetup_data[15],
            "phone": meetup_data[16],
            "address": meetup_data[17],
            "sponsors": meetup_data[18],
            "rules": meetup_data[19],
            "status": meetup_data[20]
        }
        
        return render_template("meetup-detail.html", meetup=meetup)
        
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("pet_meetups"))
        
# Contact Messages Route
@app.route("/contact-messages")
def contact_messages():
    try:
        cursor = mysql.connection.cursor()

        # Fetch contact messages
        cursor.execute("SELECT id, name, phone, email, message, created_at FROM contact_messages")
        messages_data = cursor.fetchall()
        cursor.close()

        messages_list = [
            {
                "id": message[0],
                "name": message[1],
                "phone": message[2],
                "email": message[3],
                "message": message[4],
                "created_at": message[5]
            }
            for message in messages_data
        ]

        return render_template("message.html", messages=messages_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_data')
def get_data():
    try:
        cursor = mysql.connection.cursor()
        
        # Get users count
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        # Get organizations count
        cursor.execute("SELECT COUNT(*) FROM organizations")
        orgs_count = cursor.fetchone()[0]
        
        # Get verified organizations count
        cursor.execute("SELECT COUNT(*) FROM organizations WHERE status = 'verified'")
        verified_orgs_count = cursor.fetchone()[0]
        
        # Get pending organizations count
        cursor.execute("SELECT COUNT(*) FROM organizations WHERE status = 'pending' AND reg_number IS NOT NULL")
        pending_orgs_count = cursor.fetchone()[0]
        
        # Get pet adoption/selling count
        cursor.execute("SELECT COUNT(*) FROM pets")
        pets_count = cursor.fetchone()[0]
        
        # Get pet meetup count
        cursor.execute("SELECT COUNT(*) FROM events")
        events_count = cursor.fetchone()[0]
        
        # Get messages count
        cursor.execute("SELECT COUNT(*) FROM contact_messages")
        messages_count = cursor.fetchone()[0]
        
        # Get donations count
        try:
            cursor.execute("SELECT COUNT(*) FROM fundraisers")
            donations_count = cursor.fetchone()[0]
        except:
            donations_count = 0
        
        cursor.close()
        
        data = {
            "users": users_count,
            "organizations": orgs_count,
            "verified_organizations": verified_orgs_count,
            "pending_organizations": pending_orgs_count,
            "pet_adoption_sell": pets_count,
            "pet_meetup": events_count,
            "messages": messages_count,
            "donations": donations_count
        }
        
        return jsonify(data)
    except Exception as e:
        import traceback
        print(f"Error in get_data route: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/static/uploads/<path:filename>')
def serve_uploads(filename):
    # Use the actual IMAGE_FOLDER path
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route("/pet-selling")
def pet_listings():
    try:
        cursor = mysql.connection.cursor()
        
        # Get filter parameters
        species = request.args.get('species', '')
        status = request.args.get('status', '')
        date_range = request.args.get('date', '')
        
        # Build query based on filters
        query = """
            SELECT p.id, p.pet_name, p.species, p.breed, p.age, p.gender, 
                   p.reason, p.pet_image, p.location, p.status, p.created_at,
                   p.reg_certificate, p.vaccination_records,
                   COALESCE(CONCAT(u.first_name, ' ', u.last_name), '') AS full_name
            FROM pets p
            LEFT JOIN users u ON p.owner_id = u.id AND p.owner_type = 'user'
            WHERE 1=1
        """
        
        params = []
        
        # Add filters if provided
        if species:
            query += " AND p.species = %s"
            params.append(species)
            
        if status:
            query += " AND p.status = %s"
            params.append(status)
            
        if date_range:
            today = datetime.now().date()
            if date_range == 'today':
                query += " AND DATE(p.created_at) = %s"
                params.append(today)
            elif date_range == 'week':
                week_ago = today - timedelta(days=7)
                query += " AND p.created_at >= %s"
                params.append(week_ago)
            elif date_range == 'month':
                month_ago = today - timedelta(days=30)
                query += " AND p.created_at >= %s"
                params.append(month_ago)
        
        # Order by most recent first
        query += " ORDER BY p.created_at DESC"
        
        cursor.execute(query, params)
        pets_data = cursor.fetchall()
        cursor.close()
        
        # Convert to list of dictionaries
        pets_list = []
        for pet in pets_data:
            pets_list.append({
                "id": pet[0],
                "pet_name": pet[1],
                "species": pet[2],
                "breed": pet[3],
                "age": pet[4],
                "gender": pet[5],
                "reason": pet[6],
                "pet_image": pet[7],
                "location": pet[8],
                "status": pet[9],
                "created_at": pet[10],
                "reg_certificate": pet[11],
                "vaccination_records": pet[12],
                "full_name": pet[13]
            })
        
        return render_template("pet-selling.html", pets=pets_list, request=request)
    
    except Exception as e:
        print(f"Error in pet_listings: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# Pet detail route
@app.route("/pet/<int:pet_id>")
def pet_detail(pet_id):
    try:
        cursor = mysql.connection.cursor()
        
        # Get pet details
        cursor.execute("""
            SELECT * FROM pets WHERE id = %s
        """, (pet_id,))
        
        pet_data = cursor.fetchone()
        
        if not pet_data:
            flash("Pet not found", "error")
            return redirect(url_for('pet_listings'))
        
        # Convert to dictionary
        column_names = [desc[0] for desc in cursor.description]
        pet_dict = dict(zip(column_names, pet_data))
        
        cursor.close()
        return render_template("pet-detail.html", pet=pet_dict)
    
    except Exception as e:
        print(f"Error in pet_detail: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Update pet status route
@app.route("/update_pet_status", methods=["POST"])
def update_pet_status():
    try:
        pet_id = request.form.get('pet_id')
        status = request.form.get('status')
        
        # Validate input
        if not pet_id or not status:
            return jsonify({"success": False, "message": "Missing required parameters"}), 400
            
        # Validate status
        if status not in ['pending', 'approved', 'rejected']:
            return jsonify({"success": False, "message": "Invalid status"}), 400
            
        cursor = mysql.connection.cursor()
        
        # First get the pet owner details to send notification
        cursor.execute("SELECT owner_id, owner_type FROM pets WHERE id = %s", (pet_id,))
        pet_info = cursor.fetchone()
        if not pet_info:
            return jsonify({"success": False, "message": "Pet not found"}), 404
            
        owner_id = pet_info[0]
        owner_type = pet_info[1]
        
        cursor.execute("UPDATE pets SET status = %s WHERE id = %s", (status, pet_id))
        mysql.connection.commit()
        
        # Create notification for pet owner
        message = f"Your pet listing status has been {status}"
        create_notification(owner_id, owner_type, message, 'status_change', pet_id, 'pet')
        
        # Confirm the update was successful
        rows_affected = cursor.rowcount
        cursor.close()
        
        if rows_affected > 0:
            # Return success response
            return jsonify({
                "success": True, 
                "message": f"Pet status updated to {status.capitalize()}"
            })
        else:
            return jsonify({
                "success": False,
                "message": "No records were updated. Pet may not exist."
            })
        
    except Exception as e:
        print(f"Error in admin_update_pet_status: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route("/pet-statistics")
def pet_statistics():
    try:
        cursor = mysql.connection.cursor()
        
        # Get counts by status
        cursor.execute("""
            SELECT status, COUNT(*) as count FROM pets GROUP BY status
        """)
        status_data = cursor.fetchall()
        status_counts = {row[0]: row[1] for row in status_data}
        
        # Get counts by species
        cursor.execute("""
            SELECT species, COUNT(*) as count FROM pets GROUP BY species
        """)
        species_data = cursor.fetchall()
        species_counts = {row[0]: row[1] for row in species_data}
        
        # Get counts by month (last 6 months)
        cursor.execute("""
            SELECT DATE_FORMAT(created_at, '%Y-%m') as month, COUNT(*) 
            FROM pets 
            GROUP BY DATE_FORMAT(created_at, '%Y-%m')
            ORDER BY month DESC
            LIMIT 6
        """)
        monthly_data = cursor.fetchall()
        monthly_counts = {}
        for row in monthly_data:
            # Format the month for display (e.g., "2023-03" to "Mar 2023")
            month_date = datetime.strptime(row[0], '%Y-%m')
            formatted_month = month_date.strftime('%b %Y')
            monthly_counts[formatted_month] = row[1]
        
        # Get counts by breed (top 5)
        cursor.execute("""
            SELECT breed, COUNT(*) as count 
            FROM pets 
            GROUP BY breed
            ORDER BY count DESC
            LIMIT 5
        """)
        breed_data = cursor.fetchall()
        breed_counts = {row[0]: row[1] for row in breed_data}
        
        # Get average age by species
        cursor.execute("""
            SELECT species, AVG(age) as avg_age 
            FROM pets 
            GROUP BY species
        """)
        age_data = cursor.fetchall()
        avg_age = {row[0]: round(row[1], 1) for row in age_data}
        
        cursor.close()
        
        return render_template(
            "/pet-statistics.html",
            status_counts=status_counts,
            species_counts=species_counts,
            monthly_counts=monthly_counts,
            breed_counts=breed_counts,
            avg_age=avg_age
        )
        
    except Exception as e:
        print(f"Error in pet_statistics: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/fundraiser-Listings")
def fundraiser_listings():
    try:
        cursor = mysql.connection.cursor()
        
        # Get filter parameters
        creator_type = request.args.get('creator_type', '')
        status = request.args.get('status', '')
        date_range = request.args.get('date', '')
        
        # Build query based on filters
        query = """
            SELECT f.id, f.title, f.brief_description, f.start_date, f.end_date, 
                   f.funds_usage, f.beneficiaries, f.animals_helped, f.proof_document, 
                   f.status, f.created_at, f.creator_type, f.creator_id,
                   CASE
                       WHEN f.creator_type = 'user' THEN CONCAT(u.first_name, ' ', u.last_name)
                       WHEN f.creator_type = 'organization' THEN o.org_name
                       ELSE ''
                   END AS creator_name
            FROM fundraisers f
            LEFT JOIN users u ON f.creator_id = u.id AND f.creator_type = 'user'
            LEFT JOIN organizations o ON f.creator_id = o.id AND f.creator_type = 'organization'
            WHERE 1=1
        """
        
        params = []
        
        # Add filters if provided
        if creator_type:
            query += " AND f.creator_type = %s"
            params.append(creator_type)
            
        if status:
            query += " AND f.status = %s"
            params.append(status)
            
        if date_range:
            today = datetime.now().date()
            if date_range == 'today':
                query += " AND DATE(f.created_at) = %s"
                params.append(today)
            elif date_range == 'week':
                week_ago = today - timedelta(days=7)
                query += " AND f.created_at >= %s"
                params.append(week_ago)
            elif date_range == 'month':
                month_ago = today - timedelta(days=30)
                query += " AND f.created_at >= %s"
                params.append(month_ago)
        
        # Order by most recent first
        query += " ORDER BY f.created_at DESC"
        
        cursor.execute(query, params)
        fundraisers_data = cursor.fetchall()
        cursor.close()
        
        # Convert to list of dictionaries
        fundraisers_list = []
        for fundraiser in fundraisers_data:
            fundraisers_list.append({
                "id": fundraiser[0],
                "title": fundraiser[1],
                "brief_description": fundraiser[2],
                "start_date": fundraiser[3],
                "end_date": fundraiser[4],
                "funds_usage": fundraiser[5],
                "beneficiaries": fundraiser[6],
                "animals_helped": fundraiser[7],
                "proof_document": fundraiser[8],
                "status": fundraiser[9],
                "created_at": fundraiser[10],
                "creator_type": fundraiser[11],
                "creator_id": fundraiser[12],
                "creator_name": fundraiser[13]
            })
        
        return render_template("fundraiser-Listings.html", fundraisers=fundraisers_list, request=request)
    
    except Exception as e:
        print(f"Error in fundraiser_listings: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/update_fundraiser_status", methods=["POST"])
def update_fundraiser_status():
    try:
        fundraiser_id = request.form.get('fundraiser_id')
        status = request.form.get('status')
        
        # Validate inputs
        if not fundraiser_id or not status:
            return jsonify({"success": False, "message": "Missing required parameters"}), 400
            
        if status not in ['pending', 'approved', 'rejected']:
            return jsonify({"success": False, "message": "Invalid status value"}), 400
        
        cursor = mysql.connection.cursor()
        
        # First get the fundraiser creator details to send notification
        cursor.execute("SELECT creator_id, creator_type FROM fundraisers WHERE id = %s", (fundraiser_id,))
        fundraiser_info = cursor.fetchone()
        if not fundraiser_info:
            return jsonify({"success": False, "message": "Fundraiser not found"}), 404
            
        creator_id = fundraiser_info[0]
        creator_type = fundraiser_info[1]
        
        # Update status in database
        cursor.execute(
            "UPDATE fundraisers SET status = %s WHERE id = %s",
            (status, fundraiser_id)
        )
        mysql.connection.commit()
        
        # Create notification for fundraiser creator
        message = f"Your fundraiser request has been {status}"
        create_notification(creator_id, creator_type, message, 'status_change', fundraiser_id, 'fundraiser')
        
        # Check if update was successful
        if cursor.rowcount > 0:
            cursor.close()
            return jsonify({
                "success": True, 
                "message": f"Fundraiser status updated to {status} successfully"
            })
        else:
            cursor.close()
            return jsonify({
                "success": False, 
                "message": "Fundraiser not found or status already set"
            }), 404
            
    except Exception as e:
        print(f"Error in update_fundraiser_status: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route('/fundraiser-detail/<int:fundraiser_id>')
def fundraiser_details(fundraiser_id):
    try:
        cursor = mysql.connection.cursor()

        # Query that matches exactly with your database schema
        query = """
            SELECT 
                f.id, f.creator_id, f.creator_type, f.title, f.brief_description, 
                f.start_date, f.end_date, f.funds_usage, f.beneficiaries, 
                f.animals_helped, f.previous_efforts, f.proof_document, 
                f.donation_qr, f.upi_id, f.donor_message, f.social_media, 
                f.website, f.endorsements, f.volunteer_info, f.emergency_contact, 
                f.status, f.created_at,
                CASE
                    WHEN f.creator_type = 'user' THEN CONCAT(u.first_name, ' ', u.last_name)
                    WHEN f.creator_type = 'organization' THEN o.org_name
                    ELSE ''
                END AS creator_name,
                CASE
                    WHEN f.creator_type = 'user' THEN u.email
                    WHEN f.creator_type = 'organization' THEN o.email
                    ELSE ''
                END AS creator_email
            FROM fundraisers f
            LEFT JOIN users u ON f.creator_id = u.id AND f.creator_type = 'user'
            LEFT JOIN organizations o ON f.creator_id = o.id AND f.creator_type = 'organization'
            WHERE f.id = %s
        """
        
        cursor.execute(query, (fundraiser_id,))
        fundraiser = cursor.fetchone()
        cursor.close()
        
        if not fundraiser:
            return render_template("404.html", message="Fundraiser not found"), 404
            
        # Create dictionary using list of column names that match your query results
        fundraiser_data = {
            "id": fundraiser[0],
            "creator_id": fundraiser[1],
            "creator_type": fundraiser[2],
            "title": fundraiser[3],
            "brief_description": fundraiser[4],
            "start_date": fundraiser[5],
            "end_date": fundraiser[6],
            "funds_usage": fundraiser[7],
            "beneficiaries": fundraiser[8],
            "animals_helped": fundraiser[9],
            "previous_efforts": fundraiser[10],
            "proof_document": fundraiser[11],
            "donation_qr": fundraiser[12],
            "upi_id": fundraiser[13],
            "donor_message": fundraiser[14],
            "social_media": fundraiser[15],
            "website": fundraiser[16],
            "endorsements": fundraiser[17],
            "volunteer_info": fundraiser[18],
            "emergency_contact": fundraiser[19],
            "status": fundraiser[20],
            "created_at": fundraiser[21],
            "creator_name": fundraiser[22],
            "creator_email": fundraiser[23]
        }
        
        return render_template("fundraiser-detail.html", fundraiser=fundraiser_data)
        
    except Exception as e:
        print(f"Error in fundraiser_details: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(port=5002, debug=True)

