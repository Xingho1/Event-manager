import mysql.connector as ms
from mysql.connector import Error
from fpdf import FPDF
import bcrypt
import random

# Database connection
mydb = ms.connect(host='localhost', user='root', passwd='2419jonak@', database='EventMS')
cursor = mydb.cursor()

def generate_unique_user_id():
    while True:
        user_id = random.randint(1000, 9999)  # Generate a random user ID
        cursor.execute("SELECT COUNT(*) FROM users WHERE id = %s", (user_id,))
        if cursor.fetchone()[0] == 0:  # Check if the ID is unique
            return user_id

def sign_up(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_id = generate_unique_user_id()  # Generate a unique user ID

    try:
        cursor.execute("INSERT INTO users (id, username, password) VALUES (%s, %s, %s)", 
                       (user_id, username, hashed_password))
        mydb.commit()
        print("User registered successfully!")

        # User inputs for the default event
        event_name = input("Enter the event name for your default event: ")
        event_date = input("Enter the event date (YYYY-MM-DD) for your default event: ")
        event_location = input("Enter the event location for your default event: ")
        description = input("Enter the event description for your default event: ")

        # Create the user-defined event
        event_id = create_event_for_user(user_id, event_name, event_date, event_location, description)
        print(f"Default event created with ID: {event_id}")

    except Error as e:
        if e.errno == 1062:  # Duplicate entry
            print("Username already exists.")
        else:
            print(f"The error '{e}' occurred")

def create_event_for_user(user_id, event_name, event_date, event_location, description):
    try:
        cursor.execute(
            "INSERT INTO events (user_id, event_name, event_date, event_location, description) VALUES (%s, %s, %s, %s, %s)", 
            (user_id, event_name, event_date, event_location, description)
        )
        mydb.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def create_event(event_name, event_date, location, description):
    try:
        cursor.execute("INSERT INTO events (event_name, event_date, event_location, description) VALUES (%s, %s, %s, %s)", 
                       (event_name, event_date, location, description))
        mydb.commit()
        print("Event created successfully!")
    except Error as e:
        print(f"The error '{e}' occurred")

def view_events():
    try:
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        for event in events:
            print(f"ID: {event[0]}, Name: {event[1]}, Date: {event[2]}, Location: {event[3]}, Description: {event[4]}")
    except Error as e:
        print(f"The error '{e}' occurred")

def delete_event(event_id):
    try:
        cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        mydb.commit()
        print(f"Event ID {event_id} deleted successfully!")
    except Error as e:
        print(f"The error '{e}' occurred")

def update_event(event_id, event_name=None, event_date=None, location=None, description=None):
    updates = []
    if event_name:
        updates.append(f"event_name = '{event_name}'")
    if event_date:
        updates.append(f"event_date = '{event_date}'")
    if location:
        updates.append(f"event_location = '{location}'")
    if description:
        updates.append(f"description = '{description}'")

    if updates:
        try:
            updates_str = ", ".join(updates)
            cursor.execute(f"UPDATE events SET {updates_str} WHERE id = %s", (event_id,))
            mydb.commit()
            print(f"Event ID {event_id} updated successfully!")
        except Error as e:
            print(f"The error '{e}' occurred")

def search_events(search_term):
    try:
        cursor.execute("""SELECT * FROM events WHERE event_name LIKE %s OR event_location LIKE %s""", 
                       (f"%{search_term}%", f"%{search_term}%"))
        events = cursor.fetchall()
        for event in events:
            print(f"ID: {event[0]}, Name: {event[1]}, Date: {event[2]}, Location: {event[3]}, Description: {event[4]}")
    except Error as e:
        print(f"The error '{e}' occurred")

def get_event_by_id(event_id):
    try:
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
        if event:
            return {
                'event_id': event[0],
                'event_name': event[1],
                'event_date': event[2],
                'event_location': event[3],
                'description': event[4],
            }
        return None
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def generate_event_pdf(event):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"Event ID: {event['event_id']}", ln=True)
    pdf.cell(200, 10, txt=f"Event Name: {event['event_name']}", ln=True)
    pdf.cell(200, 10, txt=f"Event Date: {event['event_date']}", ln=True)
    pdf.cell(200, 10, txt=f"Location: {event['event_location']}", ln=True)
    pdf.multi_cell(0, 10, txt=f"Description: {event['description']}")
    
    pdf_file_name = f"event_{event['event_id']}.pdf"
    pdf.output(pdf_file_name)
    
    return pdf_file_name

def generate_pdf_for_event(event_id):
    event_data = get_event_by_id(event_id)
    if event_data:
        pdf_file = generate_event_pdf(event_data)
        print(f"PDF generated: {pdf_file}")
    else:
        print("Event not found.")

def login(username, password):
    try:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result is None:
            print("Username not found.")
            return

        stored_hash = result[0]

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            print("Login successful!")
        else:
            print("Invalid password.")

    except Error as e:
        print(f"The error '{e}' occurred")

def main():
    action = input("Do you want to (1) Sign Up, (2) Log In, or (3) Manage Events? Enter 1, 2, or 3: ")
    
    if action == '1':
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        sign_up(username, password)
    elif action == '2':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        login(username, password)
    elif action == '3':
        event_action = input("Do you want to (1) Create, (2) View, (3) Update, (4) Delete, or (5) Search Events? Enter 1, 2, 3, 4, or 5: ")
        
        if event_action == '1':
            event_name = input("Enter event name: ")
            event_date = input("Enter event date (YYYY-MM-DD): ")
            event_location = input("Enter event location: ")
            description = input("Enter event description: ")
            create_event(event_name, event_date, event_location, description)
        elif event_action == '2':
            view_events()
        elif event_action == '3':
            event_id = int(input("Enter event ID to update: "))
            event_name = input("Enter new event name (leave blank to keep unchanged): ")
            event_date = input("Enter new event date (leave blank to keep unchanged): ")
            event_location = input("Enter new event location (leave blank to keep unchanged): ")
            description = input("Enter new event description (leave blank to keep unchanged): ")
            update_event(event_id, event_name, event_date, event_location, description)
        elif event_action == '4':
            event_id = int(input("Enter event ID to delete: "))
            delete_event(event_id)
        elif event_action == '5':
            search_term = input("Enter search term: ")
            search_events(search_term)
        else:
            print("Invalid option.")
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()

# Close the database connection after all operations
mydb.close()
