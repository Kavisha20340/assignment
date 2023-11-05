# Django REST API with custom token based authentication with Firebase

This is a Django project that implements custom token-based authentication with Firebase for registering a user, logging in and authorizing a user to access protected views.
## Features

- MongoDB to store user data 
- Firebase for token based authentication
- Django REST for web API
- User registration with mandatory fields (email, password) and optional fields (username, first name, last name)
- User login with custom token generation by Firebase
- View user profile as a protected view
- Edit user data only when authorized

## Prerequisites

Before you start using this project, make sure you have the following necessary setup in your system:

- Python
- Django and Django REST framework
- [Firebase Admin Python SDK](https://firebase.google.com/docs/reference/admin/python)
- Instance of MongoDB server running locally

## Getting Started

1. Clone this repository:

   ```bash
   clone https://github.com/Kavisha20340/assignment

2. Install the required packages in the Pipfile.

3. Configure Firebase Admin SDK: Start a Firebase project and generate a service account key. Dowload it and add it to your project.
  
4. Run the MongoDB server and Django development server.
   

## Usage

This API has four endpoints that we are going to consume using Postman.

### Register

This endpoint creates and stores new user in MongoDB database which requires two mandatory fields (email, password). On registering, a unique username for the user is generated which is saved in the DB and returned in response.

**Endpoint**: /accounts/register/

**Methods**: POST

**Payload**: username,email, password, first_name, last_name

![1](https://github.com/Kavisha20340/assignment/assets/56486195/159ca28e-536b-4e04-90ed-2b620a5223af)

### Login

This endpoint uses Firebase auth to create a custom_token if credentials are valid and logs them in. It also returns the token in response.

**Endpoint**: /accounts/login/

**Methods**: POST

**Payload**: username, password

![2](https://github.com/Kavisha20340/assignment/assets/56486195/c7794913-13f0-4806-9b62-7c9b88249c92)

When the login is successful, a custom token is returned in reponse that will be used for further authentication as shown below:  

![3](https://github.com/Kavisha20340/assignment/assets/56486195/213de196-c820-40db-aa0a-518e252a6110)

Here, we are signing in with the custom token by passing it to the request headers and using Identity Platform API since our application has no frontend.
    
#### View Profile

This endpoint implements a protected view that is only accessible with a valid token. This returns user information in response.

**Endpoint**: /accounts/profile/view/

**Methods**: GET

**Payload**: username

**Authorization**: custom_token

![4](https://github.com/Kavisha20340/assignment/assets/56486195/af638fa6-2db7-4999-8a80-2f7c4f70410a)

##### Edit Profile

This endpoint also implements a protected view that is only accessible with a valid token. This enables to update user information and returns updated user information in reponse

**Endpoint**: /accounts/profile/edit/

**Methods**: POST

**Payload**: username, password

**Authorization**: custom_token

![5](https://github.com/Kavisha20340/assignment/assets/56486195/0f82cc32-14f3-48b3-9755-a29ef81618ca)
