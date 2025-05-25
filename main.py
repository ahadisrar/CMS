import streamlit as st
import mysql.connector
import datetime
import pandas as pd


st.set_page_config(page_title="CUSTOMER MANAGEMENT SYSTEM", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrxLaA404LP8zdl8_ms3qQ3z38xmKcvtgj-g&s")
st.title("CUSTOMER MANAGEMENT SYSTEM")
st.markdown("<center><h1>Welcome to the Customer Portal</h1></center>", unsafe_allow_html=True)

menu = st.sidebar.selectbox('Menu', ('Home', 'Register','Customer', 'Admin','Feedback','Contact Us','Thank You'))

if menu == "Home":
    st.image("https://cdn.dribbble.com/userupload/23215602/file/original-daaa4ad42c79ab0bba7653599b42d6c8.gif")
    st.write("Welcome! This project is a comprehensive Customer Management System designed to help businesses manage their interactions with customers efficiently. Whether you're handling registrations, placing orders, resolving support requests, or collecting feedback ")
    st.image("https://elearn.daffodilvarsity.edu.bd/pluginfile.php/2646677/course/section/575306/MIS.gif")
elif menu=="Register":
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    dob = st.date_input("Date of Birth")
    address = st.text_area("Address")
    city = st.text_input("City")
    country = st.text_input("Country")
    btn2 = st.button("Customer Registration")
    if btn2:
        mydb = mysql.connector.connect(host="localhost", user="root", password="Mys@@2454##", database="customer_db")
        c = mydb.cursor()
        query = "INSERT INTO customers (name, email, phone, gender, dob, address, city, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, email, phone, gender, dob, address, city, country)
        c.execute(query, values)
        mydb.commit()
        st.success("Customer Added Successfully!")

elif menu == "Admin":
    if 'admin_login' not in st.session_state:
        st.session_state['admin_login'] = False
    admin_user = st.text_input("Enter Admin Username")
    admin_pwd = st.text_input("Enter Admin Password", type="password")
    btn = st.button("Login")
    #st.image("https://simplify360.com/wp-content/uploads/2022/03/empathy-in-customer-service.gif")
    if btn:
        mydb = mysql.connector.connect(host="localhost", user="root", password="Mys@@2454##", database="customer_db")
        c = mydb.cursor()
        c.execute("SELECT * FROM admins")
        for r in c:
            if r[2] == admin_user and r[3] == admin_pwd:
                st.session_state['admin_login'] = True
                break
        if not st.session_state['admin_login']:
            st.error("Incorrect Username or Password")

    if st.session_state['admin_login']:
        st.success("Login successful")
        admin_option = st.selectbox("Admin Features", ["None", "View Customers", "Add Customer", "Delete Customer", "View Feedback", "View Orders"])

        if admin_option == "View Customers":
            mydb = mysql.connector.connect(host="localhost", user="root", password="Mys@@2454##", database="customer_db")
            df = pd.read_sql("SELECT * FROM customers", mydb)
            st.dataframe(df)

        elif admin_option == "Add Customer":
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            dob = st.date_input("Date of Birth")
            address = st.text_area("Address")
            city = st.text_input("City")
            country = st.text_input("Country")
            btn2 = st.button("Add Customer")
            if btn2:
                mydb = mysql.connector.connect(host="localhost", user="root", password="Mys@@2454##", database="customer_db")
                c = mydb.cursor()
                query = "INSERT INTO customers (name, email, phone, gender, dob, address, city, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                values = (name, email, phone, gender, dob, address, city, country)
                c.execute(query, values)
                mydb.commit()
                st.success("Customer Added Successfully!")

        elif admin_option == "Delete Customer":
            customer_id = st.text_input("Enter Customer ID to Delete")
            btn3 = st.button("Delete")
            if btn3:
                mydb = mysql.connector.connect(host="localhost", user="root", password="Mys@@2454##", database="customer_db")
                c = mydb.cursor()
                c.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
                mydb.commit()
                st.success("Customer Deleted Successfully!")

        elif admin_option == "View Feedback":
            mydb = mysql.connector.connect(host="localhost", user="root", password="Mys@@2454##", database="customer_db")
            df = pd.read_sql("SELECT * FROM feedback", mydb)
            st.dataframe(df)

        elif admin_option == "View Orders":
            mydb = mysql.connector.connect(host="localhost", user="root", password="Mys@@2454##", database="customer_db")
            df = pd.read_sql("SELECT * FROM orders", mydb)
            st.dataframe(df)
elif menu == "Customer":
    if 'customer_logged_in' not in st.session_state:
        st.session_state.customer_logged_in = False
        st.session_state.customer_id = ""
        st.session_state.name=""

    if not st.session_state.customer_logged_in:
        customer_id = st.text_input("Enter Customer ID")
        name=st.text_input("Enter customer name")
        btn_login = st.button("Login")
        #st.image("https://images.squarespace-cdn.com/content/v1/59fd07670abd04055e1e0a6f/79bb7512-1adf-417c-bb85-61a2520d28f7/PM.gif")

        if btn_login:
            mydb = mysql.connector.connect(host="localhost",user="root",password="Mys@@2454##",database="customer_db")
            c = mydb.cursor()
            c.execute("SELECT * FROM customers WHERE customer_id = %s AND name = %s", (customer_id,name))
            result = c.fetchone()

            if result:
                st.session_state.customer_logged_in = True
                st.session_state.customer_id = customer_id
                st.session_state.name=name
                st.success("Customer Login Successful")
            else:
                st.error("Invalid Customer ID")

    if st.session_state.customer_logged_in:
        customer_id = st.session_state.customer_id
        customer_option = st.selectbox("Features", ["None", "Place Order","View Order History", "Raise Ticket"])

        mydb = mysql.connector.connect(host="localhost",user="root",password="Mys@@2454##",database="customer_db")
        c = mydb.cursor()

        if customer_option == "Place Order":
            product_name = st.text_input("Product Name")
            amount = st.number_input("Amount", min_value=0.0)
            payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "UPI", "Cash on Delivery", "Net Banking"])

            if st.button("Place Order"):
                order_date = datetime.datetime.now()
                c.execute("""
                    INSERT INTO orders (customer_id, product_name, amount, order_date, delivery_status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (customer_id, product_name, amount, order_date, delivery_status))
                mydb.commit()
                st.success("Order Placed Successfully!")

        
        elif customer_option == "View Order History":
            c.execute("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))
            orders = c.fetchall()
            if orders:
                for order in orders:
                    st.write(f"🧾 **Product:** {order[2]}")
                    st.write(f"💰 Amount: ₹{order[3]}")
                    st.write(f"📅 Order Date: {order[4]}")
                    st.write(f"🚚 Delivery Status: {order[5]}")
                    st.markdown("---")
                else:st.info("No orders found.")


        elif customer_option == "Raise Ticket":
            issue_type = st.text_input("Issue Type")
            description = st.text_area("Description")
            if st.button("Raise Ticket"):
                raised_on = datetime.datetime.now()
                status = "Open"
                c.execute("""
                    INSERT INTO support_tickets (customer_id, issue_type, description, status, raised_on)
                    VALUES (%s, %s, %s, %s, %s)
                """, (customer_id, issue_type, description, status, raised_on))
                mydb.commit()
                st.success("Support Ticket Raised Successfully!")

elif menu=='Feedback': # Session to track login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'customer_id' not in st.session_state:
        st.session_state.customer_id = ''
    if 'customer_name' not in st.session_state:
        st.session_state.customer_name = ''

    if not st.session_state.logged_in:
        customer_id = st.text_input("Customer ID")
        customer_name = st.text_input("Customer Name")

         
        if st.button("Login"):
            db = mysql.connector.connect(host="localhost",user="root",password="Mys@@2454##",database="customer_db")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s AND name = %s", (customer_id, customer_name))
            user = cursor.fetchone()
            if user:
                st.session_state.logged_in = True
                st.session_state.customer_id = customer_id
                st.session_state.customer_name = customer_name
                st.success("Login Successful!")
        else:
            st.error("Invalid ID or Name")
    if st.session_state.logged_in:
        st.subheader(f"Welcome, {st.session_state.customer_name}")
        rating = st.slider("Rating", 1, 5)
        comment = st.text_area("Comment")
        if st.button("Submit Feedback"):
            db = mysql.connector.connect(host="localhost",user="root",password="Mys@@2454##",database="customer_db")
            cursor = db.cursor()
            feedback_date = datetime.datetime.now()
            cursor.execute("INSERT INTO feedback (customer_id, rating, comment, feedback_date) VALUES (%s, %s, %s, %s)",
                           (st.session_state.customer_id, rating, comment, feedback_date))
            db.commit()
            st.success("Feedback submitted!")

elif menu=='Contact Us':
    st.markdown("---")
    st.subheader("📞 Contact Us")
    st.markdown("""
    **Customer Support:**  
    ✉️ Email: support@cmsdemo.com  
    📞 Phone: +91-9876543210  
    💬 Live Chat: Available 9 AM – 6 PM (Mon–Sat)

   **Corporate Office:**  
    CMS Pvt. Ltd.  
    123 Demo Street,  
    Tech City, India - 560001

    **Follow Us:**  
   🌐 Website: [www.cmsdemo.com](http://www.cmsdemo.com)  
   📷 Instagram: [@cmsdemo](https://instagram.com/cmsdemo)  
   🐦 Twitter: [@cmsdemo](https://twitter.com/cmsdemo)

   We're here to help you 24x7.  
   Feel free to reach out with your concerns or feedback.
   """)


elif menu=='Thank You':
    st.markdown("---")
    st.subheader("🙏 Thank You for Visiting")
    st.markdown("""
    We appreciate your time and trust in our service.  
    If you have any questions or need help, don't hesitate to raise a support ticket or connect with us.

    Stay connected and happy shopping!  
    **- Team CMS**
    """)
    st.image("https://i.pinimg.com/originals/14/74/8a/14748aff4122c454a2e20ea97a04203d.gif")
   

