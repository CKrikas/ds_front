**Frontend Installation Guide for ds_front**

**1)Prerequisites:**

--Python 3.10.12


--pip (Python package installer)

**2)Installation Steps:**

```
git clone https://github.com/CKrikas/ds_front.git
cd ds_front
```

**3)Install Required Packages:**

Using the command ```pip install -r requirements.txt```, install the necessary packages.


**4)Generate a Secret Key**

The application uses a secret key for session management. You can generate a secret key using the provided keygen.py script.
```python3 keygen.py``` to run the script.

This will print a secret key. Copy this key.

**5)Set the Secret Key**

Create a .env file in the root directory of the project and set the secret key using the following command:
```echo "SECRET_KEY=your_generated_secret_key" > .env```


**6)Run the Application**

Now, you can run the application using the following command: ```python3 app.py```

The application will start and by default will run on http://localhost:4000/.
